"""
Retail Data Lakehouse - Interactive Streamlit Web Application
Shows business analytics, ML models, and interactive dashboards
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Retail Data Lakehouse",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Data loading functions
@st.cache_data
def load_transactions():
    """Load POS transactions data"""
    file_path = Path("raw_data/pos_transactions.csv")
    if file_path.exists():
        return pd.read_csv(file_path)
    return None

@st.cache_data
def load_customers():
    """Load customers data"""
    file_path = Path("raw_data/customers.csv")
    if file_path.exists():
        return pd.read_csv(file_path)
    return None

@st.cache_data
def load_products():
    """Load products data"""
    file_path = Path("raw_data/products_inventory.csv")
    if file_path.exists():
        return pd.read_csv(file_path)
    return None

@st.cache_data
def load_campaigns():
    """Load marketing campaigns data"""
    file_path = Path("raw_data/marketing_campaigns.csv")
    if file_path.exists():
        return pd.read_csv(file_path)
    return None

@st.cache_data
def load_customer_segments():
    """Load customer segmentation results"""
    file_path = Path("ml_models/outputs/customer_segments.csv")
    if file_path.exists():
        return pd.read_csv(file_path)
    return None

@st.cache_data
def load_segment_analysis():
    """Load segment analysis"""
    file_path = Path("ml_models/outputs/segment_analysis.csv")
    if file_path.exists():
        return pd.read_csv(file_path, index_col=0)
    return None

@st.cache_data
def load_demand_forecast():
    """Load demand forecasting results"""
    file_path = Path("ml_models/outputs/demand_forecast.csv")
    if file_path.exists():
        return pd.read_csv(file_path)
    return None


# Load all data
transactions = load_transactions()
customers = load_customers()
products = load_products()
campaigns = load_campaigns()
customer_segments = load_customer_segments()
segment_analysis = load_segment_analysis()
demand_forecast = load_demand_forecast()

# Header
st.markdown('<h1 class="main-header">🏪 Retail Data Lakehouse</h1>', unsafe_allow_html=True)
st.markdown("**Interactive Analytics Dashboard | Machine Learning Insights | Business Intelligence**")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/000000/shop.png", width=150)
    st.markdown("## 📊 Navigation")
    
    page = st.radio(
        "Select a page:",
        ["🏠 Overview", "📈 Business Analytics", "🤖 ML Models", "📊 Data Explorer", "ℹ️ About"]
    )
    
    st.markdown("---")
    st.markdown("### 📌 Project Info")
    st.info("""
    **Retail Data Lakehouse**
    
    - 16,050 records
    - 2 ML models
    - $2.37M opportunity
    - Interactive dashboards
    """)
    
    st.markdown("---")
    st.markdown("### 🔗 Links")
    st.markdown("[GitHub Repository](https://github.com/Pragna987/Retail_Lakehouse)")
    st.markdown("[Documentation](https://github.com/Pragna987/Retail_Lakehouse/blob/main/README.md)")

# Main content area
if page == "🏠 Overview":
    # KPI Metrics
    st.markdown("## 📊 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    if transactions is not None:
        total_revenue = transactions['total_amount'].sum()
        total_transactions = len(transactions)
        avg_transaction = transactions['total_amount'].mean()
        
        with col1:
            st.metric("💰 Total Revenue", f"${total_revenue/1e6:.2f}M")
        with col2:
            st.metric("🛒 Transactions", f"{total_transactions:,}")
        with col3:
            st.metric("👥 Customers", f"{len(customers):,}" if customers is not None else "N/A")
        with col4:
            st.metric("📦 Products", f"{len(products):,}" if products is not None else "N/A")
        with col5:
            st.metric("💵 Avg Transaction", f"${avg_transaction:.2f}")
    
    st.markdown("---")
    
    # Quick insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Customer Segmentation Insights")
        if segment_analysis is not None:
            for idx, row in segment_analysis.iterrows():
                with st.expander(f"📍 {row['segment_name']}", expanded=True):
                    st.metric("Customers", f"{int(row['customer_count']):,}")
                    st.metric("Revenue", f"${row['total_revenue']:,.2f}")
                    st.metric("Avg Spending", f"${row['avg_total_spent']:,.2f}")
                    st.metric("Avg Recency", f"{row['avg_recency_days']:.0f} days")
        else:
            st.info("Run ML models to see customer segmentation results")
    
    with col2:
        st.markdown("### 📈 Demand Forecast Summary")
        if demand_forecast is not None:
            urgency_counts = demand_forecast['urgency'].value_counts()
            
            st.metric("🔴 High Priority", urgency_counts.get('HIGH', 0))
            st.metric("🟡 Medium Priority", urgency_counts.get('MEDIUM', 0))
            st.metric("🟢 Low Priority", urgency_counts.get('LOW', 0))
            st.metric("📦 Total Units to Order", f"{int(demand_forecast['recommended_order_qty'].sum()):,}")
        else:
            st.info("Run ML models to see demand forecasting results")

elif page == "📈 Business Analytics":
    st.markdown("## 📈 Business Analytics Dashboard")
    
    tab1, tab2, tab3, tab4 = st.tabs(["💰 Revenue", "👥 Customers", "📦 Inventory", "📢 Marketing"])
    
    with tab1:
        st.markdown("### Revenue Analysis")
        
        if transactions is not None:
            # Revenue by store
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Revenue by Store")
                store_revenue = transactions.groupby('store_id')['total_amount'].sum().sort_values(ascending=False)
                
                fig = px.bar(
                    x=store_revenue.index.astype(str),
                    y=store_revenue.values,
                    labels={'x': 'Store ID', 'y': 'Revenue ($)'},
                    title="Revenue by Store",
                    color=store_revenue.values,
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### Monthly Revenue Trend")
                transactions['date'] = pd.to_datetime(transactions['date'])
                monthly_revenue = transactions.groupby(transactions['date'].dt.to_period('M'))['total_amount'].sum()
                
                fig = px.line(
                    x=monthly_revenue.index.astype(str),
                    y=monthly_revenue.values,
                    labels={'x': 'Month', 'y': 'Revenue ($)'},
                    title="Monthly Revenue Trend",
                    markers=True
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Revenue statistics
            st.markdown("#### Revenue Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Revenue", f"${store_revenue.sum():,.2f}")
            with col2:
                st.metric("Avg per Store", f"${store_revenue.mean():,.2f}")
            with col3:
                st.metric("Top Store Revenue", f"${store_revenue.max():,.2f}")
            with col4:
                st.metric("Min Store Revenue", f"${store_revenue.min():,.2f}")
    
    with tab2:
        st.markdown("### Customer Analysis")
        
        if customers is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Customer Distribution by City")
                city_dist = customers['city'].value_counts()
                
                fig = px.pie(
                    values=city_dist.values,
                    names=city_dist.index,
                    title="Customers by City",
                    hole=0.3
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### Loyalty Tier Distribution")
                loyalty_dist = customers['loyalty_tier'].value_counts()
                
                fig = px.bar(
                    x=loyalty_dist.index,
                    y=loyalty_dist.values,
                    labels={'x': 'Loyalty Tier', 'y': 'Number of Customers'},
                    title="Customers by Loyalty Tier",
                    color=loyalty_dist.values,
                    color_continuous_scale='Greens'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Age distribution
            st.markdown("#### Age Distribution")
            fig = px.histogram(
                customers,
                x='age',
                nbins=20,
                labels={'age': 'Age', 'count': 'Number of Customers'},
                title="Customer Age Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### Inventory Analysis")
        
        if products is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Products by Category")
                category_dist = products['category'].value_counts()
                
                fig = px.pie(
                    values=category_dist.values,
                    names=category_dist.index,
                    title="Product Distribution by Category"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### Stock Level Distribution")
                fig = px.histogram(
                    products,
                    x='stock_level',
                    nbins=30,
                    labels={'stock_level': 'Stock Level', 'count': 'Number of Products'},
                    title="Stock Level Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Products needing reorder
            st.markdown("#### Products Needing Reorder")
            needs_reorder = products[products['stock_level'] < products['reorder_point']]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Products Below Reorder Point", len(needs_reorder))
            with col2:
                st.metric("% of Total Products", f"{len(needs_reorder)/len(products)*100:.1f}%")
            with col3:
                st.metric("Total Products", len(products))
            
            if len(needs_reorder) > 0:
                st.dataframe(
                    needs_reorder[['product_id', 'product_name', 'category', 'stock_level', 'reorder_point']].head(10),
                    use_container_width=True
                )
    
    with tab4:
        st.markdown("### Marketing Campaign Performance")
        
        if campaigns is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Campaign ROI by Type")
                campaign_roi = campaigns.groupby('campaign_type').agg({
                    'conversions': 'sum',
                    'budget': 'sum'
                }).reset_index()
                campaign_roi['roi'] = (campaign_roi['conversions'] / campaign_roi['budget']) * 100
                
                fig = px.bar(
                    campaign_roi,
                    x='campaign_type',
                    y='roi',
                    labels={'campaign_type': 'Campaign Type', 'roi': 'ROI (%)'},
                    title="ROI by Campaign Type",
                    color='roi',
                    color_continuous_scale='RdYlGn'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### Conversion Rate by Type")
                avg_conversion = campaigns.groupby('campaign_type')['conversion_rate'].mean()
                
                fig = px.bar(
                    x=avg_conversion.index,
                    y=avg_conversion.values,
                    labels={'x': 'Campaign Type', 'y': 'Conversion Rate (%)'},
                    title="Average Conversion Rate by Type",
                    color=avg_conversion.values,
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Campaign statistics
            st.markdown("#### Campaign Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Campaigns", len(campaigns))
            with col2:
                st.metric("Total Budget", f"${campaigns['budget'].sum():,.2f}")
            with col3:
                st.metric("Total Conversions", f"{int(campaigns['conversions'].sum()):,}")
            with col4:
                st.metric("Avg Click Rate", f"{campaigns['click_rate'].mean():.2f}%")

elif page == "🤖 ML Models":
    st.markdown("## 🤖 Machine Learning Models")
    
    tab1, tab2 = st.tabs(["🎯 Customer Segmentation", "📈 Demand Forecasting"])
    
    with tab1:
        st.markdown("### Customer Segmentation (K-Means Clustering)")
        
        if segment_analysis is not None and customer_segments is not None:
            # Segment overview
            st.markdown("#### Segment Overview")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Segment sizes
                fig = px.pie(
                    segment_analysis,
                    values='customer_count',
                    names='segment_name',
                    title="Customer Distribution by Segment",
                    hole=0.4
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Revenue by segment
                fig = px.bar(
                    segment_analysis,
                    x='segment_name',
                    y='total_revenue',
                    labels={'segment_name': 'Segment', 'total_revenue': 'Revenue ($)'},
                    title="Revenue by Segment",
                    color='total_revenue',
                    color_continuous_scale='Greens'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Segment details
            st.markdown("#### Segment Details")
            
            for idx, row in segment_analysis.iterrows():
                with st.expander(f"📍 {row['segment_name']}", expanded=True):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Customers", f"{int(row['customer_count']):,}")
                        st.metric("Total Revenue", f"${row['total_revenue']:,.2f}")
                    
                    with col2:
                        st.metric("Avg Spending", f"${row['avg_total_spent']:,.2f}")
                        st.metric("Avg Frequency", f"{row['avg_frequency']:.2f}")
                    
                    with col3:
                        st.metric("Avg Trans Value", f"${row['avg_transaction_value']:,.2f}")
                        st.metric("Avg Recency", f"{row['avg_recency_days']:.0f} days")
                    
                    with col4:
                        st.metric("Avg Lifetime", f"{row['avg_lifetime_days']:.0f} days")
                        st.metric("Avg Age", f"{row['avg_age']:.0f} years")
            
            # Segment comparison
            st.markdown("#### Segment Comparison")
            
            comparison_metrics = ['avg_total_spent', 'avg_frequency', 'avg_recency_days', 'avg_age']
            selected_metric = st.selectbox("Select metric to compare:", comparison_metrics)
            
            fig = px.bar(
                segment_analysis,
                x='segment_name',
                y=selected_metric,
                labels={'segment_name': 'Segment', selected_metric: selected_metric.replace('_', ' ').title()},
                title=f"Comparison: {selected_metric.replace('_', ' ').title()}",
                color=selected_metric,
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Business impact
            st.markdown("#### 💰 Business Impact")
            
            col1, col2, col3 = st.columns(3)
            
            total_revenue = segment_analysis['total_revenue'].sum()
            slipping_revenue = segment_analysis.iloc[0]['total_revenue']
            dormant_revenue = segment_analysis.iloc[1]['total_revenue']
            
            with col1:
                st.metric(
                    "Win-Back Opportunity",
                    f"${slipping_revenue * 0.2:,.2f}",
                    help="20% improvement in Slipping Regulars"
                )
            
            with col2:
                st.metric(
                    "Reactivation Potential",
                    f"${dormant_revenue * 0.15:,.2f}",
                    help="15% reactivation of Dormant Customers"
                )
            
            with col3:
                st.metric(
                    "Total Opportunity",
                    f"${(slipping_revenue * 0.2 + dormant_revenue * 0.15):,.2f}",
                    help="Combined revenue opportunity"
                )
        
        else:
            st.warning("⚠️ Customer segmentation results not found. Please run the ML model first.")
            st.code("python ml_customer_segmentation.py", language="bash")
    
    with tab2:
        st.markdown("### Demand Forecasting (Gradient Boosting)")
        
        if demand_forecast is not None:
            # Urgency overview
            st.markdown("#### Forecast Summary")
            
            urgency_counts = demand_forecast['urgency'].value_counts()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "🔴 High Priority",
                    urgency_counts.get('HIGH', 0),
                    help="Products below reorder point"
                )
            
            with col2:
                st.metric(
                    "🟡 Medium Priority",
                    urgency_counts.get('MEDIUM', 0),
                    help="Products approaching reorder point"
                )
            
            with col3:
                st.metric(
                    "🟢 Low Priority",
                    urgency_counts.get('LOW', 0),
                    help="Products with sufficient stock"
                )
            
            with col4:
                st.metric(
                    "📦 Total Units",
                    f"{int(demand_forecast['recommended_order_qty'].sum()):,}",
                    help="Total units to order (30 days)"
                )
            
            # Urgency distribution
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.pie(
                    values=urgency_counts.values,
                    names=urgency_counts.index,
                    title="Forecast Distribution by Urgency",
                    color_discrete_map={'HIGH': '#f5576c', 'MEDIUM': '#ff8008', 'LOW': '#6dd5ed'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Orders by category
                category_orders = demand_forecast.groupby('category')['recommended_order_qty'].sum().sort_values(ascending=False)
                
                fig = px.bar(
                    x=category_orders.index,
                    y=category_orders.values,
                    labels={'x': 'Category', 'y': 'Units to Order'},
                    title="Recommended Orders by Category",
                    color=category_orders.values,
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Top priority products
            st.markdown("#### 🔴 Top 20 Priority Products")
            
            top_priority = demand_forecast.nlargest(20, 'recommended_order_qty')[
                ['product_id', 'category', 'current_stock', '30day_forecast', 'recommended_order_qty', 'urgency']
            ]
            
            # Add color coding
            def highlight_urgency(row):
                if row['urgency'] == 'HIGH':
                    return ['background-color: #ffe5e5'] * len(row)
                elif row['urgency'] == 'MEDIUM':
                    return ['background-color: #fff4e5'] * len(row)
                else:
                    return ['background-color: #e5f5ff'] * len(row)
            
            st.dataframe(
                top_priority.style.apply(highlight_urgency, axis=1),
                use_container_width=True
            )
            
            # Forecast vs Current Stock
            st.markdown("#### Forecast vs Current Stock Analysis")
            
            # Filter by urgency
            urgency_filter = st.multiselect(
                "Filter by urgency:",
                options=['HIGH', 'MEDIUM', 'LOW'],
                default=['HIGH']
            )
            
            filtered_forecast = demand_forecast[demand_forecast['urgency'].isin(urgency_filter)]
            
            fig = px.scatter(
                filtered_forecast,
                x='current_stock',
                y='30day_forecast',
                color='urgency',
                size='recommended_order_qty',
                hover_data=['product_id', 'category'],
                labels={'current_stock': 'Current Stock', '30day_forecast': '30-Day Forecast'},
                title="Current Stock vs 30-Day Forecast",
                color_discrete_map={'HIGH': '#f5576c', 'MEDIUM': '#ff8008', 'LOW': '#6dd5ed'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Business impact
            st.markdown("#### 💰 Business Impact")
            
            col1, col2, col3 = st.columns(3)
            
            avg_unit_cost = 50  # Assumed average unit cost
            inventory_investment = demand_forecast['recommended_order_qty'].sum() * avg_unit_cost
            
            with col1:
                st.metric(
                    "Stockouts Prevented",
                    urgency_counts.get('HIGH', 0),
                    help="High-priority products that would stock out"
                )
            
            with col2:
                st.metric(
                    "Inventory Investment",
                    f"${inventory_investment:,.2f}",
                    help="Estimated investment needed (30 days)"
                )
            
            with col3:
                st.metric(
                    "Products Forecasted",
                    f"{len(demand_forecast):,}",
                    help="Total products with forecasts"
                )
        
        else:
            st.warning("⚠️ Demand forecasting results not found. Please run the ML model first.")
            st.code("python ml_demand_forecasting.py", language="bash")


elif page == "📊 Data Explorer":
    st.markdown("## 📊 Data Explorer")
    
    dataset = st.selectbox(
        "Select dataset to explore:",
        ["Transactions", "Customers", "Products", "Marketing Campaigns", "Customer Segments", "Demand Forecast"]
    )
    
    if dataset == "Transactions" and transactions is not None:
        st.markdown("### 🛒 POS Transactions")
        st.dataframe(transactions.head(100), use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", f"{len(transactions):,}")
        with col2:
            st.metric("Date Range", f"{transactions['date'].min()} to {transactions['date'].max()}")
        with col3:
            st.metric("Columns", len(transactions.columns))
    
    elif dataset == "Customers" and customers is not None:
        st.markdown("### 👥 Customers")
        st.dataframe(customers.head(100), use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Customers", f"{len(customers):,}")
        with col2:
            st.metric("Cities", customers['city'].nunique())
        with col3:
            st.metric("Columns", len(customers.columns))
    
    elif dataset == "Products" and products is not None:
        st.markdown("### 📦 Products & Inventory")
        st.dataframe(products.head(100), use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Products", f"{len(products):,}")
        with col2:
            st.metric("Categories", products['category'].nunique())
        with col3:
            st.metric("Columns", len(products.columns))
    
    elif dataset == "Marketing Campaigns" and campaigns is not None:
        st.markdown("### 📢 Marketing Campaigns")
        st.dataframe(campaigns, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Campaigns", len(campaigns))
        with col2:
            st.metric("Total Budget", f"${campaigns['budget'].sum():,.2f}")
        with col3:
            st.metric("Columns", len(campaigns.columns))
    
    elif dataset == "Customer Segments" and customer_segments is not None:
        st.markdown("### 🎯 Customer Segments")
        st.dataframe(customer_segments.head(100), use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Customers", f"{len(customer_segments):,}")
        with col2:
            st.metric("Segments", customer_segments['cluster'].nunique())
        with col3:
            st.metric("Columns", len(customer_segments.columns))
    
    elif dataset == "Demand Forecast" and demand_forecast is not None:
        st.markdown("### 📈 Demand Forecast")
        st.dataframe(demand_forecast.head(100), use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Products Forecasted", f"{len(demand_forecast):,}")
        with col2:
            st.metric("High Priority", demand_forecast[demand_forecast['urgency']=='HIGH'].shape[0])
        with col3:
            st.metric("Columns", len(demand_forecast.columns))
    
    else:
        st.info("Dataset not available. Please run the project scripts to generate data.")

elif page == "ℹ️ About":
    st.markdown("## ℹ️ About This Project")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🏪 Retail Data Lakehouse
        
        A comprehensive data engineering and machine learning project demonstrating:
        
        **🏗️ Architecture:**
        - Medallion Architecture (Bronze/Silver/Gold layers)
        - Delta Lake for ACID transactions
        - Apache Spark for big data processing
        
        **🤖 Machine Learning:**
        - **Customer Segmentation** using K-Means Clustering
        - **Demand Forecasting** using Gradient Boosting Regressor
        - Feature engineering with lag features and rolling statistics
        
        **📊 Analytics:**
        - Interactive dashboards with Streamlit
        - Business intelligence visualizations
        - Real-time data exploration
        
        **💼 Business Value:**
        - $2.37M revenue opportunity identified
        - 206 stockouts prevented
        - 2 customer segments for targeted marketing
        
        ### 📈 Project Statistics
        
        - **16,050** total records generated
        - **2** machine learning models trained
        - **15** visualizations created
        - **3** interactive dashboards
        - **$12.9M** total revenue analyzed
        
        ### 🛠️ Technologies Used
        
        **Programming:**
        - Python 3.11
        - Streamlit
        
        **Data Processing:**
        - pandas, numpy
        - PySpark, Delta Lake
        
        **Machine Learning:**
        - scikit-learn
        - K-Means Clustering
        - Gradient Boosting
        
        **Visualization:**
        - matplotlib, seaborn
        - Plotly
        - Streamlit
        
        ### 🔗 Resources
        
        - [GitHub Repository](https://github.com/Pragna987/Retail_Lakehouse)
        - [Documentation](https://github.com/Pragna987/Retail_Lakehouse/blob/main/README.md)
        - [Project Guide](https://github.com/Pragna987/Retail_Lakehouse/blob/main/retail-lakehouse-project/COMPLETE_PROJECT_GUIDE.md)
        """)
    
    with col2:
        st.markdown("### 🎯 Quick Actions")
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.success("Data refreshed!")
            st.rerun()
        
        if st.button("📥 Download Sample Data", use_container_width=True):
            if transactions is not None:
                csv = transactions.head(100).to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="sample_transactions.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        st.markdown("---")
        
        st.markdown("### 📞 Contact")
        st.info("""
        **Project Author**
        
        Pragna987
        
        GitHub: [@Pragna987](https://github.com/Pragna987)
        """)
        
        st.markdown("---")
        
        st.markdown("### 📅 Project Timeline")
        st.success("""
        **November 2025**
        
        ✅ Environment Setup
        ✅ Data Generation
        ✅ ML Models Trained
        ✅ Dashboards Created
        ✅ GitHub Published
        ✅ Streamlit App Built
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p><strong>Retail Data Lakehouse</strong> | Built with ❤️ using Streamlit</p>
    <p>© 2025 Pragna987 | Data Engineering + Machine Learning + Business Intelligence</p>
</div>
""", unsafe_allow_html=True)
