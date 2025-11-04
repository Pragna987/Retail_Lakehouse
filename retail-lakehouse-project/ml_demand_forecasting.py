"""
Machine Learning Model 2: Demand Forecasting for Inventory Optimization
Predicts future product demand using time series analysis and XGBoost
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

class DemandForecasting:
    """Demand Forecasting Model for Inventory Optimization"""
    
    def __init__(self):
        self.model = None
        self.feature_columns = None
        
    def load_and_prepare_data(self):
        """Load and prepare transaction and product data"""
        print("📊 Loading data...")
        
        # Load data
        transactions = pd.read_csv("raw_data/pos_transactions.csv", parse_dates=['date'])
        products = pd.read_csv("raw_data/products_inventory.csv")
        
        print(f"✓ Loaded {len(transactions):,} transactions")
        print(f"✓ Loaded {len(products):,} products\n")
        
        return transactions, products
    
    def engineer_features(self, transactions, products):
        """Create features for demand forecasting"""
        print("🔧 Engineering features for demand forecasting...")
        
        # Create daily product sales data
        daily_sales = transactions.groupby(['date', 'product_id']).agg({
            'quantity': 'sum',
            'total_amount': 'sum',
            'transaction_id': 'count'
        }).reset_index()
        daily_sales.columns = ['date', 'product_id', 'quantity_sold', 'revenue', 'num_transactions']
        
        # Add time-based features
        daily_sales['year'] = daily_sales['date'].dt.year
        daily_sales['month'] = daily_sales['date'].dt.month
        daily_sales['day'] = daily_sales['date'].dt.day
        daily_sales['day_of_week'] = daily_sales['date'].dt.dayofweek
        daily_sales['day_of_year'] = daily_sales['date'].dt.dayofyear
        daily_sales['week_of_year'] = daily_sales['date'].dt.isocalendar().week
        daily_sales['is_weekend'] = (daily_sales['day_of_week'] >= 5).astype(int)
        daily_sales['is_month_start'] = daily_sales['date'].dt.is_month_start.astype(int)
        daily_sales['is_month_end'] = daily_sales['date'].dt.is_month_end.astype(int)
        
        # Merge with product information
        daily_sales = daily_sales.merge(
            products[['product_id', 'category', 'unit_cost', 'stock_level', 'reorder_point']], 
            on='product_id',
            how='left'
        )
        
        # Calculate unit_price from revenue and quantity
        daily_sales['unit_price'] = daily_sales['revenue'] / daily_sales['quantity_sold'].replace(0, 1)
        
        # Sort by date
        daily_sales = daily_sales.sort_values(['product_id', 'date'])
        
        # Create lag features (past sales)
        print("   Creating lag features...")
        for lag in [1, 3, 7, 14, 30]:
            daily_sales[f'quantity_lag_{lag}'] = daily_sales.groupby('product_id')['quantity_sold'].shift(lag)
        
        # Create rolling statistics
        print("   Creating rolling statistics...")
        for window in [7, 14, 30]:
            daily_sales[f'quantity_rolling_mean_{window}'] = (
                daily_sales.groupby('product_id')['quantity_sold']
                .transform(lambda x: x.rolling(window, min_periods=1).mean())
            )
            daily_sales[f'quantity_rolling_std_{window}'] = (
                daily_sales.groupby('product_id')['quantity_sold']
                .transform(lambda x: x.rolling(window, min_periods=1).std())
            )
        
        # Fill NaN values
        daily_sales = daily_sales.fillna(0)
        
        print(f"✓ Created {len(daily_sales.columns)} features for {len(daily_sales):,} records\n")
        
        return daily_sales
    
    def prepare_training_data(self, daily_sales):
        """Prepare data for model training"""
        print("📚 Preparing training data...")
        
        # Select features for modeling
        self.feature_columns = [
            'month', 'day', 'day_of_week', 'day_of_year', 'week_of_year',
            'is_weekend', 'is_month_start', 'is_month_end',
            'unit_price', 'unit_cost', 'stock_level', 'reorder_point',
            'quantity_lag_1', 'quantity_lag_3', 'quantity_lag_7', 'quantity_lag_14', 'quantity_lag_30',
            'quantity_rolling_mean_7', 'quantity_rolling_mean_14', 'quantity_rolling_mean_30',
            'quantity_rolling_std_7', 'quantity_rolling_std_14', 'quantity_rolling_std_30'
        ]
        
        # Target variable
        target = 'quantity_sold'
        
        # Remove rows with missing lag data (but allow zeros)
        df_train = daily_sales[daily_sales['quantity_lag_30'].notna()].copy()
        
        # If still empty, use less strict criteria
        if len(df_train) == 0:
            df_train = daily_sales[daily_sales['quantity_lag_7'].notna()].copy()
        
        X = df_train[self.feature_columns]
        y = df_train[target]
        
        # Split into train and test sets (80/20)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, shuffle=False
        )
        
        print(f"✓ Training set: {len(X_train):,} samples")
        print(f"✓ Test set: {len(X_test):,} samples\n")
        
        return X_train, X_test, y_train, y_test, df_train
    
    def train_model(self, X_train, y_train):
        """Train Gradient Boosting model for demand forecasting"""
        print("🤖 Training Gradient Boosting Regressor...")
        
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42,
            verbose=0
        )
        
        self.model.fit(X_train, y_train)
        
        print("✓ Model trained successfully\n")
        
        return self.model
    
    def evaluate_model(self, X_train, X_test, y_train, y_test):
        """Evaluate model performance"""
        print("📊 Evaluating model performance...\n")
        
        # Predictions
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
        
        # Calculate metrics
        train_metrics = {
            'MAE': mean_absolute_error(y_train, y_train_pred),
            'RMSE': np.sqrt(mean_squared_error(y_train, y_train_pred)),
            'R2': r2_score(y_train, y_train_pred)
        }
        
        test_metrics = {
            'MAE': mean_absolute_error(y_test, y_test_pred),
            'RMSE': np.sqrt(mean_squared_error(y_test, y_test_pred)),
            'R2': r2_score(y_test, y_test_pred)
        }
        
        print("=" * 80)
        print("MODEL PERFORMANCE METRICS")
        print("=" * 80)
        print(f"\nTraining Set:")
        print(f"  Mean Absolute Error (MAE):  {train_metrics['MAE']:.3f} units")
        print(f"  Root Mean Squared Error:    {train_metrics['RMSE']:.3f} units")
        print(f"  R² Score:                   {train_metrics['R2']:.3f}")
        
        print(f"\nTest Set:")
        print(f"  Mean Absolute Error (MAE):  {test_metrics['MAE']:.3f} units")
        print(f"  Root Mean Squared Error:    {test_metrics['RMSE']:.3f} units")
        print(f"  R² Score:                   {test_metrics['R2']:.3f}")
        print("\n" + "=" * 80 + "\n")
        
        return y_train_pred, y_test_pred, train_metrics, test_metrics
    
    def visualize_results(self, y_train, y_test, y_train_pred, y_test_pred, df_train):
        """Create comprehensive visualizations"""
        print("📈 Creating visualizations...")
        
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # 1. Actual vs Predicted (Training)
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.scatter(y_train, y_train_pred, alpha=0.5, s=20, label='Predictions')
        ax1.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 
                'r--', lw=2, label='Perfect Prediction')
        ax1.set_xlabel('Actual Demand (units)', fontsize=10, fontweight='bold')
        ax1.set_ylabel('Predicted Demand (units)', fontsize=10, fontweight='bold')
        ax1.set_title('Training Set: Actual vs Predicted', fontsize=12, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Actual vs Predicted (Test)
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.scatter(y_test, y_test_pred, alpha=0.5, s=20, color='green', label='Predictions')
        ax2.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 
                'r--', lw=2, label='Perfect Prediction')
        ax2.set_xlabel('Actual Demand (units)', fontsize=10, fontweight='bold')
        ax2.set_ylabel('Predicted Demand (units)', fontsize=10, fontweight='bold')
        ax2.set_title('Test Set: Actual vs Predicted', fontsize=12, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Feature Importance
        ax3 = fig.add_subplot(gs[1, :])
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=True).tail(15)
        
        ax3.barh(range(len(feature_importance)), feature_importance['importance'].values, color='steelblue')
        ax3.set_yticks(range(len(feature_importance)))
        ax3.set_yticklabels(feature_importance['feature'].values, fontsize=9)
        ax3.set_xlabel('Importance Score', fontsize=10, fontweight='bold')
        ax3.set_title('Top 15 Feature Importance', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='x')
        
        # 4. Residuals (Test Set)
        ax4 = fig.add_subplot(gs[2, 0])
        residuals = y_test - y_test_pred
        ax4.scatter(y_test_pred, residuals, alpha=0.5, s=20, color='purple')
        ax4.axhline(y=0, color='r', linestyle='--', linewidth=2)
        ax4.set_xlabel('Predicted Demand (units)', fontsize=10, fontweight='bold')
        ax4.set_ylabel('Residuals', fontsize=10, fontweight='bold')
        ax4.set_title('Residual Plot (Test Set)', fontsize=12, fontweight='bold')
        ax4.grid(True, alpha=0.3)
        
        # 5. Residuals Distribution
        ax5 = fig.add_subplot(gs[2, 1])
        ax5.hist(residuals, bins=50, color='orange', edgecolor='black', alpha=0.7)
        ax5.axvline(x=0, color='r', linestyle='--', linewidth=2)
        ax5.set_xlabel('Residual Value', fontsize=10, fontweight='bold')
        ax5.set_ylabel('Frequency', fontsize=10, fontweight='bold')
        ax5.set_title('Residual Distribution', fontsize=12, fontweight='bold')
        ax5.grid(True, alpha=0.3)
        
        plt.suptitle('Demand Forecasting Model Performance', fontsize=16, fontweight='bold', y=0.995)
        
        # Save visualization
        output_dir = Path("ml_models/outputs")
        output_dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_dir / 'demand_forecasting_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ Saved: demand_forecasting_analysis.png\n")
    
    def generate_forecast(self, products, daily_sales, forecast_days=30):
        """Generate demand forecast for next N days"""
        print(f"🔮 Generating {forecast_days}-day demand forecast...")
        
        # Get latest data for each product
        latest_data = daily_sales.groupby('product_id').last().reset_index()
        
        forecasts = []
        
        for product_id in products['product_id'].unique():
            product_data = latest_data[latest_data['product_id'] == product_id]
            
            if len(product_data) == 0:
                continue
            
            # Prepare features for forecasting
            forecast_features = product_data[self.feature_columns].copy()
            
            # Make prediction
            predicted_demand = self.model.predict(forecast_features)[0]
            
            # Get product info
            product_info = products[products['product_id'] == product_id].iloc[0]
            
            # Calculate recommended order quantity
            safety_stock = predicted_demand * forecast_days * 0.2  # 20% safety buffer
            total_forecast = predicted_demand * forecast_days + safety_stock
            current_stock = product_info['stock_level']
            recommended_order = max(0, total_forecast - current_stock)
            
            forecasts.append({
                'product_id': product_id,
                'category': product_info['category'],
                'current_stock': current_stock,
                'reorder_point': product_info['reorder_point'],
                'daily_demand_forecast': predicted_demand,
                f'{forecast_days}day_forecast': predicted_demand * forecast_days,
                'safety_stock': safety_stock,
                'recommended_order_qty': recommended_order,
                'days_until_stockout': current_stock / max(predicted_demand, 0.1),
                'urgency': 'HIGH' if current_stock < product_info['reorder_point'] else 
                          ('MEDIUM' if recommended_order > 0 else 'LOW')
            })
        
        forecast_df = pd.DataFrame(forecasts)
        forecast_df = forecast_df.sort_values('urgency', ascending=False)
        
        print(f"✓ Generated forecasts for {len(forecast_df)} products\n")
        
        return forecast_df
    
    def visualize_forecast(self, forecast_df):
        """Visualize demand forecast results"""
        print("📊 Creating forecast visualizations...")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. Urgency distribution
        urgency_counts = forecast_df['urgency'].value_counts()
        colors = {'HIGH': '#E74C3C', 'MEDIUM': '#F39C12', 'LOW': '#2ECC71'}
        ax1.pie(urgency_counts.values, labels=urgency_counts.index, autopct='%1.1f%%',
                colors=[colors[x] for x in urgency_counts.index], startangle=90, explode=[0.1, 0, 0])
        ax1.set_title('Stock Replenishment Urgency', fontsize=12, fontweight='bold')
        
        # 2. Top 10 products by recommended order quantity
        top_orders = forecast_df.nlargest(10, 'recommended_order_qty')
        ax2.barh(range(10), top_orders['recommended_order_qty'].values, color='darkblue', edgecolor='black')
        ax2.set_yticks(range(10))
        ax2.set_yticklabels([f'Product {pid}' for pid in top_orders['product_id'].values], fontsize=9)
        ax2.set_xlabel('Recommended Order Quantity', fontsize=10, fontweight='bold')
        ax2.set_title('Top 10 Products: Order Recommendations', fontsize=12, fontweight='bold')
        ax2.invert_yaxis()
        ax2.grid(True, alpha=0.3, axis='x')
        
        # 3. Forecast by category
        category_forecast = forecast_df.groupby('category')['30day_forecast'].sum().sort_values()
        ax3.barh(range(len(category_forecast)), category_forecast.values, color='teal', edgecolor='black')
        ax3.set_yticks(range(len(category_forecast)))
        ax3.set_yticklabels(category_forecast.index, fontsize=9)
        ax3.set_xlabel('30-Day Forecast (units)', fontsize=10, fontweight='bold')
        ax3.set_title('Demand Forecast by Category', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='x')
        
        # 4. Days until stockout distribution
        ax4.hist(forecast_df['days_until_stockout'].clip(0, 100), bins=30, 
                color='coral', edgecolor='black', alpha=0.7)
        ax4.axvline(x=30, color='red', linestyle='--', linewidth=2, label='30-day threshold')
        ax4.set_xlabel('Days Until Stockout', fontsize=10, fontweight='bold')
        ax4.set_ylabel('Number of Products', fontsize=10, fontweight='bold')
        ax4.set_title('Stockout Risk Analysis', fontsize=12, fontweight='bold')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save visualization
        output_dir = Path("ml_models/outputs")
        plt.savefig(output_dir / 'demand_forecast_results.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✓ Saved: demand_forecast_results.png\n")
    
    def print_forecast_summary(self, forecast_df):
        """Print forecast summary and recommendations"""
        print("=" * 100)
        print("DEMAND FORECAST SUMMARY (Next 30 Days)")
        print("=" * 100)
        
        print(f"\n📊 Overall Statistics:")
        print(f"   Total Products Analyzed: {len(forecast_df):,}")
        print(f"   High Urgency (Below Reorder Point): {len(forecast_df[forecast_df['urgency'] == 'HIGH']):,}")
        print(f"   Medium Urgency (Order Recommended): {len(forecast_df[forecast_df['urgency'] == 'MEDIUM']):,}")
        print(f"   Low Urgency (Stock Sufficient): {len(forecast_df[forecast_df['urgency'] == 'LOW']):,}")
        
        print(f"\n🎯 Top 10 Priority Orders:")
        print("=" * 100)
        top_10 = forecast_df.nlargest(10, 'recommended_order_qty')
        for idx, row in top_10.iterrows():
            print(f"   Product {row['product_id']:4d} | {row['category']:15s} | "
                  f"Current: {int(row['current_stock']):4d} | "
                  f"Forecast: {int(row['30day_forecast']):4d} | "
                  f"Order: {int(row['recommended_order_qty']):4d} units | "
                  f"Urgency: {row['urgency']}")
        
        print("\n" + "=" * 100 + "\n")

def main():
    """Main execution"""
    print("\n" + "=" * 100)
    print("  🤖 MACHINE LEARNING MODEL 2: DEMAND FORECASTING")
    print("=" * 100 + "\n")
    
    # Initialize model
    forecaster = DemandForecasting()
    
    # Load data
    transactions, products = forecaster.load_and_prepare_data()
    
    # Engineer features
    daily_sales = forecaster.engineer_features(transactions, products)
    
    # Prepare training data
    X_train, X_test, y_train, y_test, df_train = forecaster.prepare_training_data(daily_sales)
    
    # Train model
    forecaster.train_model(X_train, y_train)
    
    # Evaluate model
    y_train_pred, y_test_pred, train_metrics, test_metrics = forecaster.evaluate_model(
        X_train, X_test, y_train, y_test
    )
    
    # Visualize results
    forecaster.visualize_results(y_train, y_test, y_train_pred, y_test_pred, df_train)
    
    # Generate forecast
    forecast_df = forecaster.generate_forecast(products, daily_sales, forecast_days=30)
    
    # Visualize forecast
    forecaster.visualize_forecast(forecast_df)
    
    # Print summary
    forecaster.print_forecast_summary(forecast_df)
    
    # Save results
    output_dir = Path("ml_models/outputs")
    forecast_df.to_csv(output_dir / 'demand_forecast.csv', index=False)
    print("✓ Saved demand forecast to: ml_models/outputs/demand_forecast.csv")
    
    print("\n" + "=" * 100)
    print("  ✅ DEMAND FORECASTING COMPLETE!")
    print("=" * 100)
    print("\nNext Steps:")
    print("  1. Review forecast visualizations in: ml_models/outputs/")
    print("  2. Use forecasts for inventory planning and purchasing")
    print("  3. Monitor forecast accuracy and retrain model monthly")
    print("  4. Integrate with automated ordering systems\n")

if __name__ == "__main__":
    main()
