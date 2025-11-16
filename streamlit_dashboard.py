"""
Financial Trading Data Warehouse - Streamlit Dashboard
Interactive analytics dashboard for trading data warehouse
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sqlalchemy import create_engine, text
import os
from datetime import datetime, timedelta
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Financial Trading Data Warehouse",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Theme - Navy Blue & Gold Accents
# Dark background with white text throughout
st.markdown("""
    <style>
    /* ===== DARK THEME - NAVY BLUE & GOLD ===== */
    
    /* Main app background - Dark */
    .stApp {
        background-color: #0f172a;
    }
    
    /* Main content area - Dark */
    .main .block-container {
        background-color: #0f172a;
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Main header - White text */
    .main-header {
        font-size: 2.5rem;
        font-weight: 600;
        color: #ffffff;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 1.5rem;
    }
    
    /* All headings - White text */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 600;
    }
    
    h1 {
        border-bottom: 2px solid #f59e0b;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    
    h2 {
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* All text - White */
    p, div, span, label, li {
        color: #ffffff !important;
    }
    
    /* Metric cards - Dark with gold accent */
    div[data-testid="stMetricContainer"] {
        background-color: #1e293b;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #334155;
        border-left: 3px solid #f59e0b;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 600;
    }
    
    [data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
        font-weight: 500;
    }
    
    [data-testid="stMetricDelta"] {
        color: #f59e0b !important;
    }
    
    /* Sidebar - Dark background */
    [data-testid="stSidebar"] {
        background-color: #1e293b !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] h1 {
        border-bottom: 2px solid #f59e0b;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] span {
        color: #ffffff !important;
    }
    
    /* Radio buttons in sidebar - White text */
    [data-testid="stSidebar"] .stRadio label {
        color: #ffffff !important;
    }
    
    /* Buttons - Gold accent */
    .stButton > button {
        background-color: #f59e0b;
        color: #0f172a;
        border-radius: 6px;
        font-weight: 600;
        border: none;
    }
    
    .stButton > button:hover {
        background-color: #fbbf24;
        color: #0f172a;
    }
    
    /* All labels - White text */
    label {
        color: #ffffff !important;
        font-weight: 500;
    }
    
    /* Selectbox - Dark with white text */
    .stSelectbox > div > div > select {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #475569;
        border-radius: 6px;
    }
    
    .stSelectbox > div > div > select option {
        background-color: #1e293b !important;
        color: #ffffff !important;
    }
    
    .stSelectbox > div > div > select:focus {
        border-color: #f59e0b;
        box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.3);
    }
    
    /* Text input - Dark with white text */
    .stTextInput > div > div > input {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #475569;
        border-radius: 6px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #f59e0b;
        box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.3);
    }
    
    /* Date input - Dark with white text */
    .stDateInput > div > div > input {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #475569;
        border-radius: 6px;
    }
    
    .stDateInput > div > div > input:focus {
        border-color: #f59e0b;
        box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.3);
    }
    
    /* Multiselect - Dark with white text */
    .stMultiSelect > div > div {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #475569;
        border-radius: 6px;
    }
    
    .stMultiSelect > div > div > div {
        color: #ffffff !important;
    }
    
    /* Info boxes - Dark theme */
    .stInfo {
        background-color: #1e3a8a;
        border-left: 3px solid #3b82f6;
        color: #ffffff !important;
    }
    
    .stWarning {
        background-color: #78350f;
        border-left: 3px solid #f59e0b;
        color: #ffffff !important;
    }
    
    .stError {
        background-color: #7f1d1d;
        border-left: 3px solid #ef4444;
        color: #ffffff !important;
    }
    
    .stSuccess {
        background-color: #064e3b;
        border-left: 3px solid #10b981;
        color: #ffffff !important;
    }
    
    /* Chart containers - Dark background */
    .js-plotly-plot {
        background-color: #1e293b;
    }
    
    /* Dataframe - Dark theme */
    .dataframe {
        background-color: #1e293b;
        color: #ffffff;
    }
    
    .dataframe th {
        background-color: #334155;
        color: #ffffff !important;
    }
    
    .dataframe td {
        color: #ffffff !important;
    }
    
    /* Divider - Light gray on dark */
    hr {
        border: none;
        border-top: 1px solid #475569;
        margin: 1.5rem 0;
    }
    
    /* Scrollbar - Gold accent */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #f59e0b;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #fbbf24;
    }
    
    /* Markdown text - White */
    .stMarkdown {
        color: #ffffff !important;
    }
    
    /* Code blocks - Dark */
    code {
        background-color: #1e293b;
        color: #f59e0b;
    }
    
    /* Tables - Dark theme */
    table {
        color: #ffffff !important;
    }
    
    /* Streamlit default text elements */
    .element-container {
        color: #ffffff !important;
    }
    
    /* Ensure all Streamlit text is white */
    .stText, .stMarkdown, .stWrite {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# Database connection function using SQLAlchemy
@st.cache_resource
def init_connection():
    """Initialize database connection using SQLAlchemy"""
    try:
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            st.error("❌ DATABASE_URL not found in environment variables. Please create a .env file.")
            st.stop()
        
        # Parse and fix connection string if needed
        if 'pooler.supabase.com' in database_url and ':5432' in database_url:
            database_url = database_url.replace(':5432', ':6543')
        
        # Convert psycopg2 URI to SQLAlchemy format if needed
        if database_url.startswith('postgresql://'):
            # SQLAlchemy uses postgresql:// (not postgres://)
            if database_url.startswith('postgresql://'):
                pass  # Already correct
            elif database_url.startswith('postgres://'):
                database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        # Create SQLAlchemy engine
        engine = create_engine(database_url, pool_pre_ping=True, pool_recycle=300)
        return engine
    except Exception as e:
        st.error(f"❌ Database connection failed: {str(e)}")
        st.info("💡 Make sure your .env file contains DATABASE_URL with your Supabase connection string.")
        st.stop()

# Initialize connection
engine = init_connection()

# Query execution function with caching
@st.cache_data(ttl=300)  # Cache for 5 minutes
def run_query(query, params=None):
    """Execute SQL query and return DataFrame using SQLAlchemy"""
    try:
        # Use pandas read_sql with SQLAlchemy engine
        # For parameterized queries, params should be a dict with :param_name format
        if params and isinstance(params, dict):
            query_obj = text(query)
            df = pd.read_sql(query_obj, engine, params=params)
        else:
            # For non-parameterized queries
            query_obj = text(query) if not isinstance(query, str) or ':' in query else query
            df = pd.read_sql(query_obj, engine)
        return df
    except Exception as e:
        st.error(f"Query error: {str(e)}")
        return pd.DataFrame()

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Select Dashboard",
    ["🏠 Overview", "💼 Portfolio Analytics", "👥 Trader Performance", 
     "⚠️ Risk Analysis", "📈 Time Series", "🔍 Data Explorer", "🏗️ Data Warehouse Architecture"]
)

# ============================================================================
# OVERVIEW PAGE
# ============================================================================

if page == "🏠 Overview":
    st.markdown('<div class="main-header">Financial Trading Data Warehouse</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Key Metrics
    st.subheader("📊 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_trades = run_query("SELECT COUNT(*) as count FROM fact_trades;")
        st.metric("Total Trades", f"{total_trades['count'].iloc[0]:,}")
    
    with col2:
        total_value = run_query("""
            SELECT SUM(trade_value) as total 
            FROM fact_trades;
        """)
        value = total_value['total'].iloc[0] if not total_value.empty else 0
        st.metric("Total Trade Value", f"${value:,.0f}")
    
    with col3:
        unique_securities = run_query("SELECT COUNT(DISTINCT security_key) as count FROM fact_trades;")
        st.metric("Unique Securities", f"{unique_securities['count'].iloc[0]:,}")
    
    with col4:
        total_pnl = run_query("""
            SELECT SUM(realized_pnl) as total 
            FROM fact_trades 
            WHERE realized_pnl IS NOT NULL;
        """)
        pnl = total_pnl['total'].iloc[0] if not total_pnl.empty else 0
        st.metric("Total Realized P&L", f"${pnl:,.0f}", 
                 delta=f"{pnl/1000000:.1f}M" if pnl != 0 else "0")
    
    st.markdown("---")
    
    # Recent Activity Chart
    st.subheader("📈 Daily Trading Activity (Last 30 Days)")
    
    daily_activity = run_query("""
        SELECT 
            d.date,
            COUNT(*) as trade_count,
            SUM(ft.trade_value) as daily_volume,
            SUM(ft.realized_pnl) as daily_pnl
        FROM fact_trades ft
        JOIN dim_date d ON ft.date_key = d.date_key
        WHERE d.date >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY d.date
        ORDER BY d.date;
    """)
    
    if not daily_activity.empty:
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Daily Trade Volume', 'Daily Realized P&L'),
            vertical_spacing=0.1
        )
        
        fig.add_trace(
            go.Scatter(
                x=daily_activity['date'],
                y=daily_activity['daily_volume'],
                mode='lines+markers',
                name='Volume',
                line=dict(color='#1e3a8a', width=3),
                fill='tonexty',
                fillcolor='rgba(30, 58, 138, 0.1)',
                marker=dict(color='#1e3a8a', size=6)
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=daily_activity['date'],
                y=daily_activity['daily_pnl'],
                mode='lines+markers',
                name='P&L',
                line=dict(color='#f59e0b', width=3),
                fill='tozeroy',
                fillcolor='rgba(245, 158, 11, 0.1)',
                marker=dict(color='#f59e0b', size=6)
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            height=600,
            showlegend=False,
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1e293b', size=12)
        )
        
        fig.update_xaxes(title_text="Date", row=2, col=1, gridcolor='rgba(226, 232, 240, 0.5)')
        fig.update_yaxes(title_text="Volume ($)", row=1, col=1, gridcolor='rgba(226, 232, 240, 0.5)')
        fig.update_yaxes(title_text="P&L ($)", row=2, col=1, gridcolor='rgba(226, 232, 240, 0.5)')
        
        st.plotly_chart(fig, width='stretch')
    
    # Top Securities
    st.subheader("🏆 Top 10 Securities by Volume")
    
    top_securities = run_query("""
        SELECT 
            s.ticker_symbol,
            s.security_name,
            COUNT(*) as trade_count,
            SUM(ft.trade_value) as total_volume,
            AVG(ft.price) as avg_price
        FROM fact_trades ft
        JOIN dim_security s ON ft.security_key = s.security_key
        WHERE s.is_current = TRUE
        GROUP BY s.ticker_symbol, s.security_name
        ORDER BY total_volume DESC
        LIMIT 10;
    """)
    
    if not top_securities.empty:
        fig = px.bar(
            top_securities,
            x='ticker_symbol',
            y='total_volume',
            hover_data=['security_name', 'trade_count', 'avg_price'],
            labels={'ticker_symbol': 'Ticker', 'total_volume': 'Total Volume ($)'},
            color='total_volume',
            color_continuous_scale=[[0, '#1e3a8a'], [0.5, '#3b82f6'], [1, '#f59e0b']]
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, width='stretch')

# ============================================================================
# PORTFOLIO ANALYTICS PAGE
# ============================================================================

elif page == "💼 Portfolio Analytics":
    st.title("💼 Portfolio Analytics")
    st.markdown("---")
    
    # Account Selection
    accounts_df = run_query("""
        SELECT account_key, account_name, account_type
        FROM dim_account
        ORDER BY account_name;
    """)
    
    if not accounts_df.empty:
        selected_accounts = st.multiselect(
            "Select Accounts",
            options=accounts_df['account_key'].tolist(),
            format_func=lambda x: accounts_df[accounts_df['account_key'] == x]['account_name'].iloc[0]
        )
        
        if selected_accounts:
            account_list = tuple(selected_accounts)
            
            # Portfolio Metrics
            st.subheader("📊 Portfolio Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            portfolio_metrics = run_query(f"""
                SELECT 
                    COUNT(DISTINCT ft.security_key) as positions,
                    SUM(ft.trade_value) as total_volume,
                    SUM(ft.realized_pnl) as total_pnl,
                    AVG(ft.realized_pnl) as avg_pnl
                FROM fact_trades ft
                WHERE ft.account_key IN {account_list if len(account_list) > 1 else f"({account_list[0]})"};
            """)
            
            if not portfolio_metrics.empty:
                with col1:
                    st.metric("Positions", f"{portfolio_metrics['positions'].iloc[0]:,}")
                with col2:
                    st.metric("Total Volume", f"${portfolio_metrics['total_volume'].iloc[0]:,.0f}")
                with col3:
                    st.metric("Total P&L", f"${portfolio_metrics['total_pnl'].iloc[0]:,.0f}")
                with col4:
                    st.metric("Avg P&L per Trade", f"${portfolio_metrics['avg_pnl'].iloc[0]:,.2f}")
            
            # Portfolio Composition
            st.subheader("📊 Portfolio Composition by Security")
            
            portfolio_composition = run_query(f"""
                SELECT 
                    s.ticker_symbol,
                    s.security_name,
                    SUM(ft.trade_value) as total_value,
                    SUM(ft.realized_pnl) as total_pnl,
                    COUNT(*) as trade_count
                FROM fact_trades ft
                JOIN dim_security s ON ft.security_key = s.security_key
                WHERE ft.account_key IN {account_list if len(account_list) > 1 else f"({account_list[0]})"}
                    AND s.is_current = TRUE
                GROUP BY s.ticker_symbol, s.security_name
                ORDER BY total_value DESC;
            """)
            
            if not portfolio_composition.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Pie chart
                    fig_pie = px.pie(
                        portfolio_composition.head(10),
                        values='total_value',
                        names='ticker_symbol',
                        title="Top 10 Holdings by Value"
                    )
                    st.plotly_chart(fig_pie, width='stretch')
                
                with col2:
                    # Bar chart
                    fig_bar = px.bar(
                        portfolio_composition.head(10),
                        x='ticker_symbol',
                        y='total_pnl',
                        color='total_pnl',
                        color_continuous_scale=[[0, '#1e3a8a'], [0.5, '#3b82f6'], [1, '#f59e0b']],
                        title="P&L by Security (Top 10)"
                    )
                    st.plotly_chart(fig_bar, width='stretch')
            
            # Portfolio Performance Over Time
            st.subheader("📈 Portfolio Performance Over Time")
            
            date_range = st.date_input(
                "Select Date Range",
                value=(datetime.now().date() - timedelta(days=90), datetime.now().date()),
                max_value=datetime.now().date()
            )
            
            if len(date_range) == 2:
                # Build account filter
                if len(account_list) > 1:
                    account_filter = f"({','.join(map(str, account_list))})"
                else:
                    account_filter = f"({account_list[0]})"
                
                portfolio_timeline = run_query(f"""
                    SELECT 
                        d.date,
                        SUM(ft.trade_value) as daily_volume,
                        SUM(ft.realized_pnl) as daily_pnl,
                        COUNT(*) as trade_count
                    FROM fact_trades ft
                    JOIN dim_date d ON ft.date_key = d.date_key
                    WHERE ft.account_key IN {account_filter}
                        AND d.date BETWEEN :start_date AND :end_date
                    GROUP BY d.date
                    ORDER BY d.date;
                """, params={'start_date': date_range[0], 'end_date': date_range[1]})
                
                if not portfolio_timeline.empty:
                    fig = make_subplots(
                        rows=2, cols=1,
                        subplot_titles=('Daily Volume', 'Cumulative P&L'),
                        vertical_spacing=0.1
                    )
                    
                    fig.add_trace(
                        go.Scatter(
                            x=portfolio_timeline['date'],
                            y=portfolio_timeline['daily_volume'],
                            mode='lines+markers',
                            name='Volume',
                            line=dict(color='#1e3a8a', width=3),
                            marker=dict(color='#1e3a8a', size=6)
                        ),
                        row=1, col=1
                    )
                    
                    portfolio_timeline['cumulative_pnl'] = portfolio_timeline['daily_pnl'].cumsum()
                    fig.add_trace(
                        go.Scatter(
                            x=portfolio_timeline['date'],
                            y=portfolio_timeline['cumulative_pnl'],
                            mode='lines',
                            name='Cumulative P&L',
                            line=dict(color='#f59e0b', width=3),
                            fill='tozeroy',
                            fillcolor='rgba(245, 158, 11, 0.15)'
                        ),
                        row=2, col=1
                    )
                    
                    fig.update_layout(
                        height=600, 
                        showlegend=False,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#1e293b', size=12)
                    )
                    fig.update_xaxes(title_text="Date", row=2, col=1, gridcolor='rgba(226, 232, 240, 0.5)')
                    fig.update_yaxes(title_text="Volume ($)", row=1, col=1, gridcolor='rgba(226, 232, 240, 0.5)')
                    fig.update_yaxes(title_text="Cumulative P&L ($)", row=2, col=1, gridcolor='rgba(226, 232, 240, 0.5)')
                    
                    st.plotly_chart(fig, width='stretch')

# ============================================================================
# TRADER PERFORMANCE PAGE
# ============================================================================

elif page == "👥 Trader Performance":
    st.title("👥 Trader Performance Metrics")
    st.markdown("---")
    
    # Use materialized view for performance
    trader_performance = run_query("""
        SELECT 
            trader_key,
            full_name,
            desk_name,
            trading_days,
            total_trades,
            total_volume,
            total_pnl,
            avg_pnl,
            pnl_stddev,
            sharpe_ratio
        FROM mv_trader_performance_mtd
        ORDER BY total_pnl DESC;
    """)
    
    if not trader_performance.empty:
        # Top Performers
        st.subheader("🏆 Top Performers")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            top_pnl = trader_performance.nlargest(1, 'total_pnl')
            st.metric(
                "Highest P&L",
                f"${top_pnl['total_pnl'].iloc[0]:,.0f}",
                delta=top_pnl['full_name'].iloc[0]
            )
        
        with col2:
            top_sharpe = trader_performance.nlargest(1, 'sharpe_ratio')
            st.metric(
                "Best Sharpe Ratio",
                f"{top_sharpe['sharpe_ratio'].iloc[0]:.2f}",
                delta=top_sharpe['full_name'].iloc[0]
            )
        
        with col3:
            top_volume = trader_performance.nlargest(1, 'total_volume')
            st.metric(
                "Highest Volume",
                f"${top_volume['total_volume'].iloc[0]:,.0f}",
                delta=top_volume['full_name'].iloc[0]
            )
        
        st.markdown("---")
        
        # Trader Comparison Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("P&L by Trader")
            fig_pnl = px.bar(
                trader_performance.head(20),
                x='full_name',
                y='total_pnl',
                color='total_pnl',
                color_continuous_scale=[[0, '#1e3a8a'], [0.5, '#3b82f6'], [1, '#f59e0b']],
                labels={'full_name': 'Trader', 'total_pnl': 'Total P&L ($)'}
            )
            fig_pnl.update_layout(
                height=500, 
                xaxis_tickangle=-45,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1e293b', size=12),
                xaxis=dict(gridcolor='rgba(226, 232, 240, 0.5)'),
                yaxis=dict(gridcolor='rgba(226, 232, 240, 0.5)')
            )
            st.plotly_chart(fig_pnl, width='stretch')
        
        with col2:
            st.subheader("Sharpe Ratio by Trader")
            fig_sharpe = px.bar(
                trader_performance.head(20),
                x='full_name',
                y='sharpe_ratio',
                color='sharpe_ratio',
                color_continuous_scale=[[0, '#1e3a8a'], [0.5, '#3b82f6'], [1, '#fbbf24']],
                labels={'full_name': 'Trader', 'sharpe_ratio': 'Sharpe Ratio'}
            )
            fig_sharpe.update_layout(
                height=500, 
                xaxis_tickangle=-45,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1e293b', size=12),
                xaxis=dict(gridcolor='rgba(226, 232, 240, 0.5)'),
                yaxis=dict(gridcolor='rgba(226, 232, 240, 0.5)')
            )
            st.plotly_chart(fig_sharpe, width='stretch')
        
        # Risk-Return Scatter
        st.subheader("Risk-Return Analysis")
        fig_scatter = px.scatter(
            trader_performance,
            x='pnl_stddev',
            y='total_pnl',
            size='total_trades',
            color='sharpe_ratio',
            hover_data=['full_name', 'desk_name'],
            labels={
                'pnl_stddev': 'Risk (Std Dev of P&L)',
                'total_pnl': 'Total P&L ($)',
                'sharpe_ratio': 'Sharpe Ratio'
            },
            color_continuous_scale=[[0, '#1e3a8a'], [0.5, '#3b82f6'], [1, '#f59e0b']],
            title="Risk vs Return by Trader"
        )
        fig_scatter.update_layout(
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1e293b', size=12)
        )
        st.plotly_chart(fig_scatter, width='stretch')
        
        # Detailed Table
        st.subheader("📋 Detailed Performance Table")
        st.dataframe(
            trader_performance.style.format({
                'total_volume': '${:,.0f}',
                'total_pnl': '${:,.2f}',
                'avg_pnl': '${:,.2f}',
                'pnl_stddev': '${:,.2f}',
                'sharpe_ratio': '{:.2f}'
            }),
            width='stretch',
            height=400
        )

# ============================================================================
# RISK ANALYSIS PAGE
# ============================================================================

elif page == "⚠️ Risk Analysis":
    st.title("⚠️ Risk Analysis")
    st.markdown("---")
    
    # VaR Calculation
    st.subheader("📊 Value at Risk (VaR) Analysis")
    
    confidence_level = st.select_slider(
        "Confidence Level",
        options=[90, 95, 99],
        value=95
    )
    
    # Get daily P&L data
    daily_pnl = run_query("""
        SELECT 
            d.date,
            SUM(ft.realized_pnl) as daily_pnl
        FROM fact_trades ft
        JOIN dim_date d ON ft.date_key = d.date_key
        WHERE ft.realized_pnl IS NOT NULL
        GROUP BY d.date
        ORDER BY d.date;
    """)
    
    if not daily_pnl.empty:
        # Calculate VaR
        pnl_values = daily_pnl['daily_pnl'].dropna()
        var_percentile = (100 - confidence_level) / 100
        var_value = np.percentile(pnl_values, var_percentile * 100)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("VaR (95%)", f"${var_value:,.0f}")
        with col2:
            st.metric("Mean Daily P&L", f"${pnl_values.mean():,.0f}")
        with col3:
            st.metric("Std Dev", f"${pnl_values.std():,.0f}")
        with col4:
            st.metric("Min Daily P&L", f"${pnl_values.min():,.0f}")
        
        # P&L Distribution
        st.subheader("📈 Daily P&L Distribution")
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=pnl_values,
            nbinsx=50,
            name='Daily P&L',
            marker_color='#1e3a8a'
        ))
        
        # Add VaR line
        fig.add_vline(
            x=var_value,
            line_dash="dash",
            line_color="#f59e0b",
            annotation_text=f"VaR ({confidence_level}%)"
        )
        
        fig.update_layout(
            title="Distribution of Daily P&L",
            xaxis_title="Daily P&L ($)",
            yaxis_title="Frequency",
            height=400
        )
        
        st.plotly_chart(fig, width='stretch')
        
        # Time Series with VaR
        st.subheader("📊 Daily P&L Time Series")
        
        fig_ts = go.Figure()
        fig_ts.add_trace(go.Scatter(
            x=daily_pnl['date'],
            y=daily_pnl['daily_pnl'],
            mode='lines+markers',
            name='Daily P&L',
            line=dict(color='#1e3a8a', width=3),
            marker=dict(color='#1e3a8a', size=6),
            fill='tozeroy',
            fillcolor='rgba(30, 58, 138, 0.1)'
        ))
        
        # Add VaR threshold line
        fig_ts.add_hline(
            y=var_value,
            line_dash="dash",
            line_color="#f59e0b",
            annotation_text=f"VaR ({confidence_level}%)"
        )
        
        fig_ts.update_layout(
            title="Daily P&L Over Time with VaR Threshold",
            xaxis_title="Date",
            yaxis_title="Daily P&L ($)",
            height=400
        )
        
        st.plotly_chart(fig_ts, width='stretch')
    
    # Portfolio Risk Metrics
    st.subheader("📊 Portfolio Risk Metrics by Account")
    
    account_risk = run_query("""
        SELECT 
            a.account_name,
            COUNT(*) as trade_count,
            SUM(ft.trade_value) as total_volume,
            SUM(ft.realized_pnl) as total_pnl,
            STDDEV(ft.realized_pnl) as pnl_stddev,
            AVG(ft.realized_pnl) as avg_pnl,
            CASE 
                WHEN STDDEV(ft.realized_pnl) > 0 
                THEN (AVG(ft.realized_pnl) - 0.03) / STDDEV(ft.realized_pnl)
                ELSE 0 
            END as sharpe_ratio
        FROM fact_trades ft
        JOIN dim_account a ON ft.account_key = a.account_key
        WHERE ft.realized_pnl IS NOT NULL
        GROUP BY a.account_key, a.account_name
        HAVING COUNT(*) > 10
        ORDER BY total_pnl DESC;
    """)
    
    if not account_risk.empty:
        fig_risk = px.scatter(
            account_risk.head(20),
            x='pnl_stddev',
            y='total_pnl',
            size='total_volume',
            color='sharpe_ratio',
            hover_data=['account_name', 'trade_count'],
            labels={
                'pnl_stddev': 'Risk (Std Dev)',
                'total_pnl': 'Total P&L ($)',
                'sharpe_ratio': 'Sharpe Ratio'
            },
            color_continuous_scale=[[0, '#1e3a8a'], [0.5, '#3b82f6'], [1, '#f59e0b']],
            title="Risk-Return Profile by Account"
        )
        fig_risk.update_layout(
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1e293b', size=12)
        )
        st.plotly_chart(fig_risk, width='stretch')

# ============================================================================
# TIME SERIES PAGE
# ============================================================================

elif page == "📈 Time Series":
    st.title("📈 Time Series Analysis")
    st.markdown("---")
    
    # Security Selection
    securities_df = run_query("""
        SELECT DISTINCT s.security_key, s.ticker_symbol, s.security_name
        FROM dim_security s
        JOIN fact_trades ft ON s.security_key = ft.security_key
        WHERE s.is_current = TRUE
        ORDER BY s.ticker_symbol;
    """)
    
    if not securities_df.empty:
        selected_security = st.selectbox(
            "Select Security",
            options=securities_df['security_key'].tolist(),
            format_func=lambda x: f"{securities_df[securities_df['security_key'] == x]['ticker_symbol'].iloc[0]} - {securities_df[securities_df['security_key'] == x]['security_name'].iloc[0]}"
        )
        
        # Date Range
        date_range = st.date_input(
            "Select Date Range",
            value=(datetime.now().date() - timedelta(days=180), datetime.now().date()),
            max_value=datetime.now().date()
        )
        
        if len(date_range) == 2 and selected_security:
            # Get time series data
            time_series = run_query("""
                SELECT 
                    d.date,
                    ft.trade_timestamp,
                    ft.price,
                    ft.trade_value,
                    ft.quantity,
                    ft.realized_pnl
                FROM fact_trades ft
                JOIN dim_date d ON ft.date_key = d.date_key
                WHERE ft.security_key = :security_key
                    AND d.date BETWEEN :start_date AND :end_date
                ORDER BY ft.trade_timestamp;
            """, params={'security_key': selected_security, 'start_date': date_range[0], 'end_date': date_range[1]})
            
            if not time_series.empty:
                # Price Chart
                st.subheader("💰 Price Over Time")
                fig_price = px.line(
                    time_series,
                    x='trade_timestamp',
                    y='price',
                    labels={'trade_timestamp': 'Time', 'price': 'Price ($)'},
                    title=f"Price Movement: {securities_df[securities_df['security_key'] == selected_security]['ticker_symbol'].iloc[0]}"
                )
                fig_price.update_traces(line_color='#1e3a8a', line_width=2)
                st.plotly_chart(fig_price, width='stretch')
                
                # Volume Chart
                st.subheader("📊 Trading Volume Over Time")
                
                # Aggregate by day
                daily_agg = time_series.groupby('date').agg({
                    'trade_value': 'sum',
                    'quantity': 'sum',
                    'realized_pnl': 'sum'
                }).reset_index()
                
                fig_volume = make_subplots(
                    rows=2, cols=1,
                    subplot_titles=('Daily Volume', 'Daily P&L'),
                    vertical_spacing=0.1
                )
                
                fig_volume.add_trace(
                    go.Bar(
                        x=daily_agg['date'],
                        y=daily_agg['trade_value'],
                        name='Volume',
                        marker_color='#1e3a8a'
                    ),
                    row=1, col=1
                )
                
                fig_volume.add_trace(
                    go.Bar(
                        x=daily_agg['date'],
                        y=daily_agg['realized_pnl'],
                        name='P&L',
                        marker_color='#f59e0b'
                    ),
                    row=2, col=1
                )
                
                fig_volume.update_layout(
                    height=600, 
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#1e293b', size=12)
                )
                fig_volume.update_xaxes(title_text="Date", row=2, col=1)
                fig_volume.update_yaxes(title_text="Volume ($)", row=1, col=1)
                fig_volume.update_yaxes(title_text="P&L ($)", row=2, col=1)
                
                st.plotly_chart(fig_volume, width='stretch')
                
                # Statistics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Avg Price", f"${time_series['price'].mean():.2f}")
                with col2:
                    st.metric("Total Volume", f"${time_series['trade_value'].sum():,.0f}")
                with col3:
                    st.metric("Total P&L", f"${time_series['realized_pnl'].sum():,.0f}")
                with col4:
                    st.metric("Trade Count", f"{len(time_series):,}")

# ============================================================================
# DATA EXPLORER PAGE
# ============================================================================

elif page == "🔍 Data Explorer":
    st.title("🔍 Data Explorer")
    st.markdown("---")
    
    # Query Builder
    st.subheader("📝 Custom Query Builder")
    
    query_type = st.selectbox(
        "Select Query Type",
        ["Recent Trades", "Top Securities", "Account Summary", "Trader Activity", "Custom SQL"]
    )
    
    if query_type == "Recent Trades":
        limit = st.slider("Number of rows", 10, 1000, 100)
        query = f"""
            SELECT 
                ft.trade_timestamp,
                s.ticker_symbol,
                s.security_name,
                t.full_name as trader,
                a.account_name,
                ft.trade_type,
                ft.quantity,
                ft.price,
                ft.trade_value,
                ft.realized_pnl
            FROM fact_trades ft
            JOIN dim_security s ON ft.security_key = s.security_key
            JOIN dim_trader t ON ft.trader_key = t.trader_key
            JOIN dim_account a ON ft.account_key = a.account_key
            WHERE s.is_current = TRUE AND t.is_current = TRUE
            ORDER BY ft.trade_timestamp DESC
            LIMIT {limit};
        """
        df = run_query(query)
        st.dataframe(df, width='stretch', height=400)
    
    elif query_type == "Top Securities":
        limit = st.slider("Number of securities", 10, 100, 20)
        query = f"""
            SELECT 
                s.ticker_symbol,
                s.security_name,
                COUNT(*) as trade_count,
                SUM(ft.trade_value) as total_volume,
                AVG(ft.price) as avg_price,
                SUM(ft.realized_pnl) as total_pnl
            FROM fact_trades ft
            JOIN dim_security s ON ft.security_key = s.security_key
            WHERE s.is_current = TRUE
            GROUP BY s.ticker_symbol, s.security_name
            ORDER BY total_volume DESC
            LIMIT {limit};
        """
        df = run_query(query)
        st.dataframe(df.style.format({
            'total_volume': '${:,.0f}',
            'avg_price': '${:,.2f}',
            'total_pnl': '${:,.2f}'
        }), width='stretch', height=400)
    
    elif query_type == "Account Summary":
        query = """
            SELECT 
                a.account_name,
                a.account_type,
                COUNT(*) as trade_count,
                SUM(ft.trade_value) as total_volume,
                SUM(ft.realized_pnl) as total_pnl,
                AVG(ft.realized_pnl) as avg_pnl
            FROM fact_trades ft
            JOIN dim_account a ON ft.account_key = a.account_key
            GROUP BY a.account_key, a.account_name, a.account_type
            ORDER BY total_volume DESC;
        """
        df = run_query(query)
        st.dataframe(df.style.format({
            'total_volume': '${:,.0f}',
            'total_pnl': '${:,.2f}',
            'avg_pnl': '${:,.2f}'
        }), width='stretch', height=400)
    
    elif query_type == "Trader Activity":
        query = """
            SELECT 
                t.full_name,
                t.desk_name,
                COUNT(*) as trade_count,
                COUNT(DISTINCT ft.date_key) as trading_days,
                SUM(ft.trade_value) as total_volume,
                SUM(ft.realized_pnl) as total_pnl
            FROM fact_trades ft
            JOIN dim_trader t ON ft.trader_key = t.trader_key
            WHERE t.is_current = TRUE
            GROUP BY t.trader_key, t.full_name, t.desk_name
            ORDER BY total_pnl DESC;
        """
        df = run_query(query)
        st.dataframe(df.style.format({
            'total_volume': '${:,.0f}',
            'total_pnl': '${:,.2f}'
        }), width='stretch', height=400)
    
    elif query_type == "Custom SQL":
        st.warning("⚠️ Be careful with custom SQL queries. Only SELECT statements are recommended.")
        custom_query = st.text_area("Enter SQL Query", height=200)
        
        if st.button("Execute Query"):
            if custom_query.strip().upper().startswith('SELECT'):
                df = run_query(custom_query)
                st.dataframe(df, width='stretch', height=400)
            else:
                st.error("Only SELECT queries are allowed for security reasons.")

# ============================================================================
# DATA WAREHOUSE ARCHITECTURE PAGE
# ============================================================================

elif page == "🏗️ Data Warehouse Architecture":
    st.title("🏗️ Data Warehouse Architecture")
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📐 Star Schema", "📊 Dimension Tables", "📈 Fact Tables", 
        "🔗 Relationships", "📋 Table Explorer"
    ])
    
    # ========================================================================
    # STAR SCHEMA TAB
    # ========================================================================
    with tab1:
        st.subheader("📐 Star Schema Overview")
        st.markdown("""
        The Financial Trading Data Warehouse uses a **Star Schema** design pattern, which consists of:
        - **1 Central Fact Table**: `fact_trades` (transactional grain)
        - **Multiple Dimension Tables**: Providing descriptive context for analysis
        """)
        
        # Star Schema Visualization
        st.markdown("### Schema Diagram")
        
        # Create a visual representation using Plotly
        fig_schema = go.Figure()
        
        # Fact table in center
        fact_x, fact_y = 0, 0
        fig_schema.add_trace(go.Scatter(
            x=[fact_x], y=[fact_y],
            mode='markers+text',
            marker=dict(size=100, color='#f59e0b', symbol='square'),
            text=['fact_trades'],
            textposition='middle center',
            textfont=dict(size=14, color='white', weight='bold'),
            name='Fact Table',
            hovertemplate='<b>fact_trades</b><br>Central Fact Table<br><extra></extra>'
        ))
        
        # Dimension tables around the fact table
        dim_tables = [
            ('dim_date', -2, 1.5),
            ('dim_time', 2, 1.5),
            ('dim_security', -2, -1.5),
            ('dim_trader', 2, -1.5),
            ('dim_account', 0, 2),
            ('dim_exchange', 0, -2),
            ('dim_counterparty', -2.5, 0),
            ('dim_strategy', 2.5, 0)
        ]
        
        for dim_name, x, y in dim_tables:
            fig_schema.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='markers+text',
                marker=dict(size=80, color='#1e3a8a', symbol='circle'),
                text=[dim_name.replace('dim_', '')],
                textposition='middle center',
                textfont=dict(size=11, color='white'),
                name='Dimension',
                hovertemplate=f'<b>{dim_name}</b><br>Dimension Table<br><extra></extra>',
                showlegend=False
            ))
            
            # Draw line from dimension to fact
            fig_schema.add_trace(go.Scatter(
                x=[x, fact_x], y=[y, fact_y],
                mode='lines',
                line=dict(color='#475569', width=2, dash='dot'),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        fig_schema.update_layout(
            title="Star Schema Visualization",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-4, 4]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-3, 3]),
            height=600,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            legend=dict(x=0.02, y=0.98, bgcolor='rgba(30, 41, 59, 0.8)')
        )
        
        st.plotly_chart(fig_schema, use_container_width=True)
        
        # Schema Description
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Fact Table
            - **fact_trades**: Central transactional table
              - Grain: One row per executed trade
              - Measures: quantity, price, trade_value, commission, realized_pnl
              - Partitioned: Monthly RANGE partitioning on trade_timestamp
            """)
        
        with col2:
            st.markdown("""
            #### Dimension Tables
            - **Time Dimensions**: dim_date, dim_time
            - **Entity Dimensions**: dim_security, dim_trader, dim_account
            - **Reference Dimensions**: dim_exchange, dim_counterparty, dim_strategy
            - **SCD Type 2**: dim_security, dim_trader (temporal tracking)
            """)
    
    # ========================================================================
    # DIMENSION TABLES TAB
    # ========================================================================
    with tab2:
        st.subheader("📊 Dimension Tables")
        
        # Get list of dimension tables
        dim_tables_query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE 'dim_%'
            ORDER BY table_name;
        """
        dim_tables = run_query(dim_tables_query)
        
        if not dim_tables.empty:
            selected_dim = st.selectbox(
                "Select Dimension Table to Explore",
                options=dim_tables['table_name'].tolist()
            )
            
            if selected_dim:
                # Get table metadata
                col_metadata = run_query(f"""
                    SELECT 
                        column_name,
                        data_type,
                        character_maximum_length,
                        is_nullable,
                        column_default
                    FROM information_schema.columns
                    WHERE table_name = '{selected_dim}'
                    ORDER BY ordinal_position;
                """)
                
                # Get row count
                row_count = run_query(f"SELECT COUNT(*) as count FROM {selected_dim};")
                count = row_count['count'].iloc[0] if not row_count.empty else 0
                
                # Display metadata
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Table Name", selected_dim)
                with col2:
                    st.metric("Row Count", f"{count:,}")
                with col3:
                    st.metric("Columns", len(col_metadata))
                
                st.markdown("---")
                
                # Column information
                st.markdown("### Column Information")
                st.dataframe(
                    col_metadata,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Sample data
                st.markdown("### Sample Data (First 10 Rows)")
                sample_data = run_query(f"SELECT * FROM {selected_dim} LIMIT 10;")
                if not sample_data.empty:
                    st.dataframe(sample_data, use_container_width=True, height=300)
                else:
                    st.info("No data available in this table.")
                
                # Special information for SCD Type 2 tables
                if selected_dim in ['dim_security', 'dim_trader']:
                    st.markdown("---")
                    st.info(f"""
                    **SCD Type 2 (Slowly Changing Dimension)**
                    
                    This table uses Type 2 tracking to maintain historical versions:
                    - `is_current`: Boolean flag indicating current version
                    - `effective_date`: When this version became active
                    - `expiry_date`: When this version was superseded (NULL for current)
                    - `version_number`: Sequential version identifier
                    """)
    
    # ========================================================================
    # FACT TABLES TAB
    # ========================================================================
    with tab3:
        st.subheader("📈 Fact Tables")
        
        # Get list of fact tables
        fact_tables_query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE 'fact_%'
            ORDER BY table_name;
        """
        fact_tables = run_query(fact_tables_query)
        
        if not fact_tables.empty:
            selected_fact = st.selectbox(
                "Select Fact Table to Explore",
                options=fact_tables['table_name'].tolist()
            )
            
            if selected_fact:
                # Get table metadata
                col_metadata = run_query(f"""
                    SELECT 
                        column_name,
                        data_type,
                        character_maximum_length,
                        is_nullable,
                        column_default
                    FROM information_schema.columns
                    WHERE table_name = '{selected_fact}'
                    ORDER BY ordinal_position;
                """)
                
                # Get row count
                row_count = run_query(f"SELECT COUNT(*) as count FROM {selected_fact};")
                count = row_count['count'].iloc[0] if not row_count.empty else 0
                
                # Get statistics for numeric columns
                numeric_cols = col_metadata[col_metadata['data_type'].isin(['numeric', 'integer', 'bigint', 'double precision', 'real', 'decimal'])]
                
                # Display metadata
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Table Name", selected_fact)
                with col2:
                    st.metric("Row Count", f"{count:,}")
                with col3:
                    st.metric("Columns", len(col_metadata))
                
                st.markdown("---")
                
                # Column information
                st.markdown("### Column Information")
                st.dataframe(
                    col_metadata,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Key metrics for fact_trades
                if selected_fact == 'fact_trades':
                    st.markdown("---")
                    st.markdown("### Key Metrics")
                    
                    metrics = run_query("""
                        SELECT 
                            COUNT(*) as total_trades,
                            SUM(trade_value) as total_volume,
                            SUM(realized_pnl) as total_pnl,
                            AVG(trade_value) as avg_trade_value,
                            MIN(trade_timestamp) as earliest_trade,
                            MAX(trade_timestamp) as latest_trade
                        FROM fact_trades;
                    """)
                    
                    if not metrics.empty:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Trades", f"{metrics['total_trades'].iloc[0]:,}")
                            st.metric("Total Volume", f"${metrics['total_volume'].iloc[0]:,.0f}")
                        with col2:
                            st.metric("Total P&L", f"${metrics['total_pnl'].iloc[0]:,.0f}")
                            st.metric("Avg Trade Value", f"${metrics['avg_trade_value'].iloc[0]:,.2f}")
                        with col3:
                            st.metric("Earliest Trade", str(metrics['earliest_trade'].iloc[0])[:10])
                            st.metric("Latest Trade", str(metrics['latest_trade'].iloc[0])[:10])
                
                # Sample data
                st.markdown("---")
                st.markdown("### Sample Data (First 10 Rows)")
                sample_data = run_query(f"SELECT * FROM {selected_fact} LIMIT 10;")
                if not sample_data.empty:
                    st.dataframe(sample_data, use_container_width=True, height=300)
                else:
                    st.info("No data available in this table.")
                
                # Partitioning information for fact_trades
                if selected_fact == 'fact_trades':
                    st.markdown("---")
                    st.info("""
                    **Table Partitioning**
                    
                    This table is partitioned by month using RANGE partitioning on `trade_timestamp`:
                    - Improves query performance through partition pruning
                    - Enables efficient data archival and maintenance
                    - Each partition contains one month of trading data
                    """)
    
    # ========================================================================
    # RELATIONSHIPS TAB
    # ========================================================================
    with tab4:
        st.subheader("🔗 Table Relationships")
        
        # Get foreign key relationships
        relationships = run_query("""
            SELECT
                tc.table_name AS fact_table,
                kcu.column_name AS fact_column,
                ccu.table_name AS dimension_table,
                ccu.column_name AS dimension_key,
                tc.constraint_name
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
                AND (tc.table_name LIKE 'fact_%' OR tc.table_name LIKE 'dim_%')
            ORDER BY tc.table_name, kcu.column_name;
        """)
        
        if not relationships.empty:
            st.markdown("### Foreign Key Relationships")
            st.dataframe(
                relationships,
                use_container_width=True,
                hide_index=True
            )
            
            # Create relationship diagram
            st.markdown("---")
            st.markdown("### Relationship Diagram")
            
            # Group relationships by fact table
            fact_rels = {}
            for _, row in relationships.iterrows():
                fact = row['fact_table']
                if fact not in fact_rels:
                    fact_rels[fact] = []
                fact_rels[fact].append({
                    'dimension': row['dimension_table'],
                    'fact_col': row['fact_column'],
                    'dim_col': row['dimension_key']
                })
            
            # Display relationships
            for fact_table, dims in fact_rels.items():
                st.markdown(f"#### {fact_table}")
                for rel in dims:
                    st.markdown(f"  - **{rel['fact_col']}** → `{rel['dimension']}.{rel['dim_col']}`")
        else:
            st.info("No foreign key relationships found in the schema.")
        
        # Show materialized views
        st.markdown("---")
        st.markdown("### Materialized Views")
        
        mv_query = """
            SELECT 
                schemaname,
                matviewname,
                pg_size_pretty(pg_total_relation_size(schemaname||'.'||matviewname)) as size
            FROM pg_matviews
            WHERE schemaname = 'public'
            ORDER BY matviewname;
        """
        materialized_views = run_query(mv_query)
        
        if not materialized_views.empty:
            st.dataframe(
                materialized_views,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No materialized views found.")
    
    # ========================================================================
    # TABLE EXPLORER TAB
    # ========================================================================
    with tab5:
        st.subheader("📋 Interactive Table Explorer")
        
        # Get all tables
        all_tables = run_query("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        
        if not all_tables.empty:
            selected_table = st.selectbox(
                "Select Table",
                options=all_tables['table_name'].tolist()
            )
            
            if selected_table:
                # Table statistics
                stats = run_query(f"""
                    SELECT 
                        COUNT(*) as row_count,
                        pg_size_pretty(pg_total_relation_size('{selected_table}')) as table_size
                    FROM {selected_table};
                """)
                
                col1, col2 = st.columns(2)
                with col1:
                    if not stats.empty:
                        st.metric("Row Count", f"{stats['row_count'].iloc[0]:,}")
                with col2:
                    if not stats.empty:
                        st.metric("Table Size", stats['table_size'].iloc[0])
                
                # Column details with data types
                st.markdown("### Column Details")
                columns_info = run_query(f"""
                    SELECT 
                        c.column_name,
                        c.data_type,
                        c.character_maximum_length,
                        c.is_nullable,
                        CASE 
                            WHEN pk.column_name IS NOT NULL THEN 'PRIMARY KEY'
                            WHEN fk.column_name IS NOT NULL THEN 'FOREIGN KEY'
                            ELSE ''
                        END as key_type
                    FROM information_schema.columns c
                    LEFT JOIN (
                        SELECT ku.column_name
                        FROM information_schema.table_constraints tc
                        JOIN information_schema.key_column_usage ku
                            ON tc.constraint_name = ku.constraint_name
                        WHERE tc.table_name = '{selected_table}'
                            AND tc.constraint_type = 'PRIMARY KEY'
                    ) pk ON c.column_name = pk.column_name
                    LEFT JOIN (
                        SELECT ku.column_name
                        FROM information_schema.table_constraints tc
                        JOIN information_schema.key_column_usage ku
                            ON tc.constraint_name = ku.constraint_name
                        WHERE tc.table_name = '{selected_table}'
                            AND tc.constraint_type = 'FOREIGN KEY'
                    ) fk ON c.column_name = fk.column_name
                    WHERE c.table_name = '{selected_table}'
                    ORDER BY c.ordinal_position;
                """)
                
                st.dataframe(columns_info, use_container_width=True, hide_index=True)
                
                # Data preview
                st.markdown("### Data Preview")
                preview_rows = st.slider("Number of rows to display", 5, 100, 20)
                preview_data = run_query(f"SELECT * FROM {selected_table} LIMIT {preview_rows};")
                
                if not preview_data.empty:
                    st.dataframe(preview_data, use_container_width=True, height=400)
                else:
                    st.info("No data available in this table.")
                
                # Export option
                st.markdown("---")
                if st.button(f"📥 Export {selected_table} Data (CSV)"):
                    export_data = run_query(f"SELECT * FROM {selected_table};")
                    if not export_data.empty:
                        csv = export_data.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name=f"{selected_table}.csv",
                            mime="text/csv"
                        )

# ============================================================================
# FOOTER
# ============================================================================

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Data Warehouse Status")
st.sidebar.info("""
**Last Updated:** Real-time data from Supabase

**Database:** PostgreSQL 15.x (Supabase)

**Total Trades:** 961,100+

**Data Range:** 2023-2024
""")

# Note: SQLAlchemy engine handles connection pooling automatically
# No need to manually close connections

