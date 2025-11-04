"""
Machine Learning Model 1: Customer Segmentation using K-Means Clustering
Analyzes customer behavior and segments them into distinct groups for targeted marketing
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

class CustomerSegmentation:
    """Customer Segmentation Model using K-Means Clustering"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = None
        self.n_clusters = None
        self.feature_columns = None
        
    def load_and_prepare_data(self):
        """Load and prepare customer transaction data"""
        print("📊 Loading data...")
        
        # Load data
        transactions = pd.read_csv("raw_data/pos_transactions.csv", parse_dates=['date'])
        customers = pd.read_csv("raw_data/customers.csv", parse_dates=['signup_date'])
        
        print(f"✓ Loaded {len(transactions):,} transactions")
        print(f"✓ Loaded {len(customers):,} customers\n")
        
        # Assign random customer IDs to transactions (simulating real data)
        np.random.seed(42)
        transactions['customer_id'] = np.random.randint(1, 5001, len(transactions))
        
        # Calculate customer features
        print("🔧 Engineering features...")
        customer_features = transactions.groupby('customer_id').agg({
            'transaction_id': 'count',      # Frequency
            'total_amount': ['sum', 'mean', 'std'],  # Monetary
            'quantity': ['sum', 'mean'],
            'date': ['min', 'max']
        })
        
        # Flatten column names
        customer_features.columns = ['_'.join(col).strip() for col in customer_features.columns.values]
        customer_features.columns = [
            'transaction_count', 'total_spent', 'avg_transaction', 'std_transaction',
            'total_items', 'avg_items', 'first_purchase', 'last_purchase'
        ]
        
        # Calculate recency (days since last purchase)
        customer_features['recency_days'] = (
            pd.Timestamp('2025-11-04') - pd.to_datetime(customer_features['last_purchase'])
        ).dt.days
        
        # Calculate customer lifetime (days between first and last purchase)
        customer_features['customer_lifetime_days'] = (
            pd.to_datetime(customer_features['last_purchase']) - 
            pd.to_datetime(customer_features['first_purchase'])
        ).dt.days
        
        # Merge with customer demographics
        customer_features = customer_features.merge(
            customers[['customer_id', 'age', 'gender', 'city', 'loyalty_tier']], 
            left_index=True, 
            right_on='customer_id',
            how='left'
        )
        
        # Fill missing std with 0 (customers with single transaction)
        customer_features['std_transaction'] = customer_features['std_transaction'].fillna(0)
        
        print(f"✓ Created {len(customer_features.columns)} features for {len(customer_features):,} customers\n")
        
        return customer_features
    
    def find_optimal_clusters(self, X, max_clusters=10):
        """Use elbow method and silhouette score to find optimal number of clusters"""
        print("🔍 Finding optimal number of clusters...")
        
        inertias = []
        silhouette_scores = []
        K_range = range(2, max_clusters + 1)
        
        for k in K_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(X)
            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(X, kmeans.labels_))
        
        # Plot elbow curve and silhouette scores
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Elbow method
        ax1.plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
        ax1.set_xlabel('Number of Clusters (k)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Inertia (Within-Cluster Sum of Squares)', fontsize=12, fontweight='bold')
        ax1.set_title('Elbow Method for Optimal k', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Silhouette scores
        ax2.plot(K_range, silhouette_scores, 'go-', linewidth=2, markersize=8)
        ax2.set_xlabel('Number of Clusters (k)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Silhouette Score', fontsize=12, fontweight='bold')
        ax2.set_title('Silhouette Score for Optimal k', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save plot
        output_dir = Path("ml_models/outputs")
        output_dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_dir / 'customer_segmentation_elbow.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Find optimal k (highest silhouette score)
        optimal_k = K_range[np.argmax(silhouette_scores)]
        print(f"✓ Optimal number of clusters: {optimal_k}")
        print(f"✓ Silhouette score: {max(silhouette_scores):.3f}\n")
        
        return optimal_k
    
    def train_model(self, customer_features):
        """Train K-Means clustering model"""
        print("🤖 Training K-Means clustering model...")
        
        # Select features for clustering (RFM + behavior)
        self.feature_columns = [
            'recency_days',
            'transaction_count',
            'total_spent',
            'avg_transaction',
            'total_items',
            'customer_lifetime_days'
        ]
        
        X = customer_features[self.feature_columns].copy()
        
        # Handle any missing values
        X = X.fillna(0)
        
        # Standardize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Find optimal clusters
        self.n_clusters = self.find_optimal_clusters(X_scaled, max_clusters=8)
        
        # Train final model
        self.model = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=20)
        customer_features['cluster'] = self.model.fit_predict(X_scaled)
        
        print(f"✓ Model trained successfully with {self.n_clusters} clusters\n")
        
        return customer_features
    
    def analyze_segments(self, customer_features):
        """Analyze and interpret customer segments"""
        print("📊 Analyzing customer segments...\n")
        
        segment_analysis = customer_features.groupby('cluster').agg({
            'customer_id': 'count',
            'total_spent': ['mean', 'sum'],
            'transaction_count': 'mean',
            'avg_transaction': 'mean',
            'recency_days': 'mean',
            'customer_lifetime_days': 'mean',
            'age': 'mean'
        }).round(2)
        
        # Flatten column names
        segment_analysis.columns = [
            'customer_count', 'avg_total_spent', 'total_revenue', 
            'avg_frequency', 'avg_transaction_value', 'avg_recency_days',
            'avg_lifetime_days', 'avg_age'
        ]
        
        # Sort by total revenue
        segment_analysis = segment_analysis.sort_values('total_revenue', ascending=False)
        
        # Assign segment names based on characteristics
        segment_names = []
        for idx in segment_analysis.index:
            data = segment_analysis.loc[idx]
            
            if data['avg_total_spent'] > segment_analysis['avg_total_spent'].median() * 1.5:
                if data['avg_recency_days'] < 30:
                    segment_names.append('🌟 VIP Champions')
                else:
                    segment_names.append('💎 High-Value At-Risk')
            elif data['avg_frequency'] > segment_analysis['avg_frequency'].median():
                if data['avg_recency_days'] < 60:
                    segment_names.append('🔄 Loyal Regulars')
                else:
                    segment_names.append('⚠️ Slipping Regulars')
            elif data['avg_recency_days'] > 120:
                segment_names.append('😴 Dormant Customers')
            else:
                segment_names.append('🆕 Occasional Shoppers')
        
        segment_analysis['segment_name'] = segment_names
        
        print("=" * 100)
        print("CUSTOMER SEGMENT ANALYSIS")
        print("=" * 100)
        print(segment_analysis.to_string())
        print("\n")
        
        return segment_analysis
    
    def visualize_segments(self, customer_features, segment_analysis):
        """Create comprehensive visualizations of customer segments"""
        print("📈 Creating visualizations...")
        
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Segment distribution (pie chart)
        ax1 = fig.add_subplot(gs[0, 0])
        segment_counts = customer_features['cluster'].value_counts().sort_index()
        colors = sns.color_palette("husl", self.n_clusters)
        ax1.pie(segment_counts.values, labels=[f'Segment {i}' for i in segment_counts.index],
                autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.set_title('Customer Distribution by Segment', fontsize=12, fontweight='bold')
        
        # 2. Revenue by segment (bar chart)
        ax2 = fig.add_subplot(gs[0, 1])
        segment_revenue = segment_analysis['total_revenue'].sort_values(ascending=True)
        bars = ax2.barh(range(len(segment_revenue)), segment_revenue.values, color=colors)
        ax2.set_yticks(range(len(segment_revenue)))
        ax2.set_yticklabels([f'Seg {i}' for i in segment_revenue.index])
        ax2.set_xlabel('Total Revenue ($)', fontsize=10, fontweight='bold')
        ax2.set_title('Revenue by Segment', fontsize=12, fontweight='bold')
        ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
        
        # 3. Average spending per customer
        ax3 = fig.add_subplot(gs[0, 2])
        avg_spending = segment_analysis['avg_total_spent'].sort_values(ascending=True)
        ax3.barh(range(len(avg_spending)), avg_spending.values, color=colors)
        ax3.set_yticks(range(len(avg_spending)))
        ax3.set_yticklabels([f'Seg {i}' for i in avg_spending.index])
        ax3.set_xlabel('Avg Spending per Customer ($)', fontsize=10, fontweight='bold')
        ax3.set_title('Average Customer Value by Segment', fontsize=12, fontweight='bold')
        
        # 4. Recency vs Frequency scatter
        ax4 = fig.add_subplot(gs[1, :2])
        for cluster in customer_features['cluster'].unique():
            cluster_data = customer_features[customer_features['cluster'] == cluster]
            ax4.scatter(cluster_data['recency_days'], cluster_data['transaction_count'],
                       label=f'Segment {cluster}', alpha=0.6, s=50)
        ax4.set_xlabel('Recency (Days Since Last Purchase)', fontsize=10, fontweight='bold')
        ax4.set_ylabel('Frequency (Transaction Count)', fontsize=10, fontweight='bold')
        ax4.set_title('Customer Segments: Recency vs Frequency', fontsize=12, fontweight='bold')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # 5. Total spent vs Transaction count
        ax5 = fig.add_subplot(gs[1, 2])
        for cluster in customer_features['cluster'].unique():
            cluster_data = customer_features[customer_features['cluster'] == cluster]
            ax5.scatter(cluster_data['transaction_count'], cluster_data['total_spent'],
                       label=f'Segment {cluster}', alpha=0.6, s=50)
        ax5.set_xlabel('Transaction Count', fontsize=10, fontweight='bold')
        ax5.set_ylabel('Total Spent ($)', fontsize=10, fontweight='bold')
        ax5.set_title('Frequency vs Monetary Value', fontsize=12, fontweight='bold')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        
        # 6. Feature importance heatmap
        ax6 = fig.add_subplot(gs[2, :])
        segment_features = customer_features.groupby('cluster')[self.feature_columns].mean()
        segment_features_scaled = (segment_features - segment_features.min()) / (segment_features.max() - segment_features.min())
        sns.heatmap(segment_features_scaled.T, annot=True, fmt='.2f', cmap='YlOrRd', 
                   ax=ax6, cbar_kws={'label': 'Normalized Value'})
        ax6.set_xlabel('Cluster', fontsize=10, fontweight='bold')
        ax6.set_ylabel('Features', fontsize=10, fontweight='bold')
        ax6.set_title('Segment Characteristics Heatmap (Normalized)', fontsize=12, fontweight='bold')
        
        plt.suptitle('Customer Segmentation Analysis Dashboard', fontsize=16, fontweight='bold', y=0.995)
        
        # Save visualization
        output_dir = Path("ml_models/outputs")
        plt.savefig(output_dir / 'customer_segmentation_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ Saved: customer_segmentation_analysis.png")
        print("✓ Saved: customer_segmentation_elbow.png\n")
    
    def generate_recommendations(self, segment_analysis):
        """Generate marketing recommendations for each segment"""
        print("=" * 100)
        print("MARKETING RECOMMENDATIONS BY SEGMENT")
        print("=" * 100)
        
        for idx in segment_analysis.index:
            segment = segment_analysis.loc[idx]
            print(f"\n🎯 {segment['segment_name']} (Segment {idx})")
            print(f"   Size: {int(segment['customer_count']):,} customers")
            print(f"   Revenue: ${segment['total_revenue']:,.2f}")
            print(f"   Avg Spending: ${segment['avg_total_spent']:.2f}")
            print(f"   Avg Recency: {segment['avg_recency_days']:.0f} days")
            
            # Recommendations based on segment characteristics
            if 'VIP Champions' in segment['segment_name']:
                print("   💡 Strategy: VIP retention program, exclusive offers, personalized service")
            elif 'High-Value At-Risk' in segment['segment_name']:
                print("   💡 Strategy: Re-engagement campaigns, win-back offers, satisfaction surveys")
            elif 'Loyal Regulars' in segment['segment_name']:
                print("   💡 Strategy: Loyalty rewards, upsell opportunities, referral programs")
            elif 'Slipping Regulars' in segment['segment_name']:
                print("   💡 Strategy: Reminder campaigns, special discounts, feedback collection")
            elif 'Dormant' in segment['segment_name']:
                print("   💡 Strategy: Aggressive re-activation, deep discounts, new product alerts")
            else:
                print("   💡 Strategy: Welcome campaigns, onboarding, frequency building offers")
        
        print("\n" + "=" * 100 + "\n")

def main():
    """Main execution"""
    print("\n" + "=" * 100)
    print("  🤖 MACHINE LEARNING MODEL 1: CUSTOMER SEGMENTATION")
    print("=" * 100 + "\n")
    
    # Initialize model
    segmentation = CustomerSegmentation()
    
    # Load and prepare data
    customer_features = segmentation.load_and_prepare_data()
    
    # Train model
    customer_features = segmentation.train_model(customer_features)
    
    # Analyze segments
    segment_analysis = segmentation.analyze_segments(customer_features)
    
    # Create visualizations
    segmentation.visualize_segments(customer_features, segment_analysis)
    
    # Generate recommendations
    segmentation.generate_recommendations(segment_analysis)
    
    # Save results
    output_dir = Path("ml_models/outputs")
    customer_features.to_csv(output_dir / 'customer_segments.csv', index=False)
    segment_analysis.to_csv(output_dir / 'segment_analysis.csv')
    print("✓ Saved customer segments to: ml_models/outputs/customer_segments.csv")
    print("✓ Saved segment analysis to: ml_models/outputs/segment_analysis.csv")
    
    print("\n" + "=" * 100)
    print("  ✅ CUSTOMER SEGMENTATION COMPLETE!")
    print("=" * 100)
    print("\nNext Steps:")
    print("  1. Review visualizations in: ml_models/outputs/")
    print("  2. Use segment insights for targeted marketing campaigns")
    print("  3. Monitor segment migration over time")
    print("  4. Customize offers based on segment characteristics\n")

if __name__ == "__main__":
    main()
