import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Investor Analytics Dashboard", layout="wide", page_icon="📊")

# --- PROFESSIONAL UI STYLING ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    /* Main Content Container */
    .block-container {
        padding: 2rem 3rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin: 2rem auto;
    }
    
    /* Metrics Cards */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 700;
        color: #2d3748;
    }
    [data-testid="stMetricLabel"] {
        font-size: 14px;
        font-weight: 600;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Custom Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    .metric-card h3 {
        margin: 0;
        font-size: 32px;
        font-weight: 700;
    }
    .metric-card p {
        margin: 5px 0 0 0;
        font-size: 13px;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 10px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.2);
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: white;
        color: #667eea;
    }
    
    /* Headers */
    h1 {
        color: #2d3748;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    h2, h3 {
        color: #2d3748;
        font-weight: 700;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 12px 30px;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 20px;
        border: 2px dashed #667eea;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    </style>
""", unsafe_allow_html=True)

# --- IMPORT ANALYTICS MODULES ---
from utils.data_loader import load_portfolio_data, save_portfolio_data
from utils.analytics import calculate_roi, calculate_risk, calculate_growth

# --- HEADER ---
st.markdown("<h1 style='text-align: center; font-size: 3rem; margin-bottom: 0;'>📊 Investor Portfolio Analytics</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #718096; font-size: 1.1rem; margin-bottom: 2rem;'>Advanced Investment Portfolio Management & Analysis Platform</p>", unsafe_allow_html=True)
st.markdown("---")

# --- DATA LOADING ---
@st.cache_data
def load_and_process_data():
    """Load data from CSV and process it with analytics"""
    try:
        df = load_portfolio_data()
        
        if df.empty:
            return pd.DataFrame()
        
        # Normalize column names
        df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
        
        # Handle different column name variations
        column_mappings = {
            'annual_return': 'current_value',
            'return_amount': 'current_value',
            'annual_return_inr': 'current_value',
            'return_inr': 'current_value',
            'current_val': 'current_value',
            'invested_amount': 'investment_amount',
            'investment_amount_inr': 'investment_amount',
            'amount_invested': 'investment_amount'
        }
        
        for old_name, new_name in column_mappings.items():
            if old_name in df.columns and new_name not in df.columns:
                df = df.rename(columns={old_name: new_name})
        
        # Calculate current_value if missing
        if 'current_value' not in df.columns:
            if 'roi_percent' in df.columns and 'investment_amount' in df.columns:
                df['current_value'] = df['investment_amount'] * (1 + df['roi_percent'] / 100)
            elif 'investment_amount' in df.columns:
                df['current_value'] = df['investment_amount']
        
        # Run Analytics
        df = calculate_roi(df)
        df = calculate_risk(df)
        df = calculate_growth(df)
        
        return df
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return pd.DataFrame()

# Load data
df = load_and_process_data()

if df.empty:
    st.warning("⚠️ No data available. Please upload data in the 'Data Management' tab.")
    st.info("💡 You can upload an Excel or CSV file with your portfolio data.")
    
    # Show sample data format
    with st.expander("📋 Required Data Format"):
        st.write("Your file should have these columns (at minimum):")
        sample_df = pd.DataFrame({
            'client_id': ['C001', 'C001', 'C002'],
            'asset_type': ['Stocks', 'Bonds', 'Real Estate'],
            'investment_amount': [100000, 50000, 200000],
            'current_value': [120000, 52000, 250000],
            'investment_start_date': ['2023-01-01', '2023-02-01', '2023-03-01']
        })
        st.dataframe(sample_df)

# Only show dashboard if data exists
if not df.empty:
    # --- DEBUG INFO ---
    with st.sidebar.expander("🔍 Debug: Data Info", expanded=False):
        st.write("**Available columns:**")
        st.code(", ".join(df.columns))
        st.write(f"**Total rows:** {len(df)}")
        st.write(f"**Unique clients:** {df['client_id'].nunique()}")

    # --- SIDEBAR FILTERS ---
    st.sidebar.markdown("<h2 style='color: white; text-align: center;'>🔍 Filters</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("---")

    clients = sorted(df['client_id'].unique())
    selected_client = st.sidebar.selectbox("📌 Select Client ID", clients, help="Choose a client to view their portfolio")

    # Additional filters
    st.sidebar.markdown("---")
    asset_types = ['All'] + sorted(df['asset_type'].unique().tolist())
    selected_asset = st.sidebar.selectbox("🏦 Filter by Asset Type", asset_types)

    # Filter data
    client_df = df[df['client_id'] == selected_client].copy()
    if selected_asset != 'All':
        client_df = client_df[client_df['asset_type'] == selected_asset]

    # --- TABBED INTERFACE ---
    tab1, tab2, tab3 = st.tabs(["📊 Client Overview", "⚖️ Risk & Performance", "📤 Data Management"])

    with tab1:
        st.markdown(f"<h2>Portfolio Summary: {selected_client}</h2>", unsafe_allow_html=True)
        
        # KPIs with Professional Cards
        col1, col2, col3, col4 = st.columns(4)
        
        # Safe column access with fallbacks
        total_invested = client_df['investment_amount'].sum() if 'investment_amount' in client_df.columns else 0
        total_current = client_df['current_value'].sum() if 'current_value' in client_df.columns else total_invested
        avg_roi = client_df['roi_percent'].mean() if 'roi_percent' in client_df.columns else 0
        total_profit = total_current - total_invested
        
        with col1:
            st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                    <h3>₹{total_invested:,.0f}</h3>
                    <p>💰 Total Invested</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                    <h3>₹{total_current:,.0f}</h3>
                    <p>📈 Current Value</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            roi_color = "#4ade80" if avg_roi >= 0 else "#f87171"
            st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                    <h3 style="color: {roi_color};">{avg_roi:.1f}%</h3>
                    <p>📊 Avg ROI</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            risk_mode = client_df['risk_level'].mode()[0] if not client_df.empty and 'risk_level' in client_df.columns else "N/A"
            risk_colors = {"Low": "#10b981", "Medium": "#f59e0b", "High": "#ef4444"}
            risk_color = risk_colors.get(risk_mode, "#6b7280")
            st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
                    <h3 style="color: {risk_color};">{risk_mode}</h3>
                    <p>⚠️ Risk Level</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Additional Metrics Row
        col5, col6, col7 = st.columns(3)
        col5.metric("📂 Total Assets", len(client_df))
        col6.metric("💵 Total Profit/Loss", f"₹{total_profit:,.0f}", 
                   delta=f"{(total_profit/total_invested)*100:.1f}%" if total_invested > 0 else "0%")
        
        # Safe access for best performing asset
        if 'roi_percent' in client_df.columns and not client_df.empty:
            best_asset = client_df.loc[client_df['roi_percent'].idxmax(), 'asset_type']
        else:
            best_asset = "N/A"
        col7.metric("🎯 Best Performing", best_asset)

        st.markdown("<br>", unsafe_allow_html=True)

        # Charts Row
        c1, c2 = st.columns(2)
        with c1:
            asset_pie = px.pie(
                client_df, 
                names='asset_type', 
                values='investment_amount',
                title="<b>Asset Allocation Distribution</b>",
                hole=0.5,
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            asset_pie.update_layout(
                font=dict(size=14),
                title_font=dict(size=18, color="#2d3748"),
                legend=dict(orientation="v", yanchor="middle", y=0.5)
            )
            st.plotly_chart(asset_pie, use_container_width=True)
            
        with c2:
            if 'investment_start_date' in client_df.columns:
                perf_line = px.line(
                    client_df.sort_values('investment_start_date'), 
                    x='investment_start_date', 
                    y='roi_percent',
                    title="<b>ROI Trend Over Time</b>", 
                    markers=True,
                    color_discrete_sequence=['#667eea']
                )
                perf_line.update_layout(
                    font=dict(size=14),
                    title_font=dict(size=18, color="#2d3748"),
                    xaxis_title="Investment Date",
                    yaxis_title="ROI (%)",
                    hovermode='x unified'
                )
                st.plotly_chart(perf_line, use_container_width=True)

        # Data Table
        st.markdown("<h3>📋 Portfolio Holdings Details</h3>", unsafe_allow_html=True)
        
        # Select available columns for display
        display_cols = []
        col_mapping = {}
        if 'asset_type' in client_df.columns:
            display_cols.append('asset_type')
            col_mapping['asset_type'] = 'Asset Type'
        if 'investment_amount' in client_df.columns:
            display_cols.append('investment_amount')
            col_mapping['investment_amount'] = 'Investment (₹)'
        if 'current_value' in client_df.columns:
            display_cols.append('current_value')
            col_mapping['current_value'] = 'Current Value (₹)'
        if 'roi_percent' in client_df.columns:
            display_cols.append('roi_percent')
            col_mapping['roi_percent'] = 'ROI (%)'
        if 'risk_level' in client_df.columns:
            display_cols.append('risk_level')
            col_mapping['risk_level'] = 'Risk Level'
        
        if display_cols:
            display_df = client_df[display_cols].copy()
            display_df = display_df.rename(columns=col_mapping)
            st.dataframe(display_df, use_container_width=True, height=400)

    with tab2:
        st.markdown("<h2>⚖️ Risk vs. Return Analysis</h2>", unsafe_allow_html=True)
        
        if 'risk_score' in client_df.columns and 'roi_percent' in client_df.columns:
            # Risk Scatter
            scatter_fig = px.scatter(
                client_df, 
                x='risk_score', 
                y='roi_percent',
                size='investment_amount', 
                color='risk_level',
                hover_name='asset_type', 
                title="<b>Risk-Return Profile Matrix</b>",
                labels={'risk_score': 'Risk Score', 'roi_percent': 'ROI (%)'},
                color_discrete_map={'Low': '#10b981', 'Medium': '#f59e0b', 'High': '#ef4444'}
            )
            scatter_fig.update_layout(
                template="plotly_white",
                font=dict(size=14),
                title_font=dict(size=20, color="#2d3748"),
                height=500
            )
            st.plotly_chart(scatter_fig, use_container_width=True)

        # Two column layout for additional charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Assets by Value
            asset_bar = px.bar(
                client_df.sort_values('investment_amount', ascending=True), 
                y='asset_type', 
                x='investment_amount',
                color='risk_level' if 'risk_level' in client_df.columns else None,
                title="<b>Investment Size by Asset</b>",
                orientation='h',
                color_discrete_map={'Low': '#10b981', 'Medium': '#f59e0b', 'High': '#ef4444'}
            )
            asset_bar.update_layout(
                font=dict(size=12),
                title_font=dict(size=16, color="#2d3748"),
                showlegend=False
            )
            st.plotly_chart(asset_bar, use_container_width=True)
        
        with col2:
            if 'roi_percent' in client_df.columns:
                # ROI Distribution
                roi_hist = px.histogram(
                    client_df, 
                    x='roi_percent',
                    nbins=15,
                    title="<b>ROI Distribution</b>",
                    color_discrete_sequence=['#667eea']
                )
                roi_hist.update_layout(
                    font=dict(size=12),
                    title_font=dict(size=16, color="#2d3748"),
                    xaxis_title="ROI (%)",
                    yaxis_title="Count"
                )
                st.plotly_chart(roi_hist, use_container_width=True)

    with tab3:
        st.markdown("<h2>📤 Data Management</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📁 Upload New Data")
            st.info("💡 Upload Excel (.xlsx) or CSV (.csv) file with portfolio data")
            
            uploaded_file = st.file_uploader("Choose File", type=["xlsx", "csv"])

            if uploaded_file is not None:
                try:
                    # Read file
                    if uploaded_file.name.endswith('.xlsx'):
                        new_df = pd.read_excel(uploaded_file)
                    else:
                        new_df = pd.read_csv(uploaded_file)
                    
                    # Normalize column names
                    new_df.columns = new_df.columns.str.lower().str.strip().str.replace(" ", "_")
                    
                    st.success(f"✅ File loaded! {len(new_df)} rows, {len(new_df.columns)} columns")
                    
                    # Preview
                    st.markdown("#### 📋 Data Preview")
                    st.dataframe(new_df.head(10), use_container_width=True)
                    
                    # Statistics
                    st1, st2, st3 = st.columns(3)
                    st1.metric("Total Rows", len(new_df))
                    st2.metric("Unique Clients", new_df['client_id'].nunique() if 'client_id' in new_df.columns else "N/A")
                    st3.metric("Total Columns", len(new_df.columns))
                    
                    # Save options
                    save_option = st.radio("Save Option:", ["Replace All Data", "Append to Existing Data"])
                    
                    if st.button("💾 Save Data", type="primary"):
                        try:
                            if save_option == "Replace All Data":
                                save_portfolio_data(new_df)
                                st.success("🎉 Data replaced successfully!")
                            else:
                                # Append to existing
                                existing_df = load_portfolio_data()
                                combined_df = pd.concat([existing_df, new_df], ignore_index=True)
                                save_portfolio_data(combined_df)
                                st.success("🎉 Data appended successfully!")
                            
                            st.balloons()
                            st.cache_data.clear()
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Save failed: {e}")
                            
                except Exception as e:
                    st.error(f"❌ Error reading file: {e}")
        
        with col2:
            st.markdown("### 📊 Current Data Info")
            if not df.empty:
                st.metric("Total Records", len(df))
                st.metric("Unique Clients", df['client_id'].nunique())
                st.metric("Total Investment", f"₹{df['investment_amount'].sum():,.0f}" if 'investment_amount' in df.columns else "N/A")
                
                st.markdown("#### 📋 Column List")
                st.code("\n".join(df.columns.tolist()))
                
                # Download current data
                st.markdown("#### 💾 Download Current Data")
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name="portfolio_data.csv",
                    mime="text/csv"
                )

# --- FOOTER ---
st.markdown("---")
st.markdown(f"""
    <div style='text-align: center; color: #718096; padding: 20px;'>
        <p><b>Investor Portfolio Analytics Dashboard</b> | Built with Streamlit & Python</p>
        <p>Last Updated: {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
""", unsafe_allow_html=True)