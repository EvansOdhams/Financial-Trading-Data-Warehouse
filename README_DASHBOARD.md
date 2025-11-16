# Financial Trading Data Warehouse - Streamlit Dashboard

**Academic Project**  
MSc AI, Data Mining and Big Data  
Unit: CSA 806 - Data Mining & Big Data  
Module 2: Data Warehousing

---

Interactive analytics dashboard for the Financial Trading Data Warehouse project. This dashboard was developed as part of a comprehensive data warehousing module focusing on dimensional modeling, ETL processes, and business intelligence visualization.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database Connection

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Supabase connection string:
   ```
   DATABASE_URL=postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
   ```

   **Important:** Use the **Connection Pooler** URI (port 6543), not the direct connection (port 5432).

   To get your connection string:
   - Go to Supabase Dashboard
   - Settings → Database
   - Copy the "URI" connection string under "Connection string"

### 3. Run the Dashboard

```bash
streamlit run streamlit_dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📚 Project Overview

This project demonstrates the implementation of a complete data warehousing solution for financial trading data, including:

- **Dimensional Modeling**: Star schema design with fact and dimension tables
- **ETL Processes**: Data extraction, transformation, and loading from multiple sources
- **Data Warehouse Architecture**: PostgreSQL-based data warehouse hosted on Supabase
- **Business Intelligence**: Interactive Streamlit dashboard for analytics and reporting
- **Performance Optimization**: Materialized views, indexing, and query optimization

The dashboard provides real-time analytics capabilities for trading operations, portfolio management, risk analysis, and trader performance evaluation.

## 📊 Dashboard Features

### 🏠 Overview
- Key metrics (total trades, volume, P&L)
- Daily trading activity charts
- Top securities by volume

### 💼 Portfolio Analytics
- Account selection and filtering
- Portfolio composition charts
- Performance over time
- Position analysis

### 👥 Trader Performance
- Trader rankings by P&L
- Sharpe ratio analysis
- Risk-return scatter plots
- Detailed performance tables

### ⚠️ Risk Analysis
- Value at Risk (VaR) calculations
- P&L distribution analysis
- Portfolio risk metrics
- Risk-return profiles by account

### 📈 Time Series
- Security price movements
- Trading volume over time
- Interactive date range selection
- Statistical summaries

### 🔍 Data Explorer
- Pre-built query templates
- Custom SQL query interface
- Data export capabilities

## 🛠️ Technical Details

### Database Connection
- Uses connection pooling for better performance
- Caches query results for 5 minutes
- Automatic connection management

### Performance Optimizations
- Materialized views for fast aggregations
- Query result caching
- Efficient partition pruning

### Visualization
- Interactive Plotly charts
- Responsive design
- Real-time data updates

## 📝 Notes

- The dashboard connects to your Supabase database in real-time
- Query results are cached for 5 minutes to improve performance
- Only SELECT queries are allowed in the custom SQL interface for security
- Make sure your materialized views are refreshed for accurate analytics

## 🚀 Deployment to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add your `DATABASE_URL` as a secret in Streamlit Cloud settings
5. Deploy!

**Note:** In Streamlit Cloud, add `DATABASE_URL` under "Secrets" instead of using a `.env` file.

## 🔒 Security

- Never commit your `.env` file to version control
- Use environment variables or Streamlit secrets for production
- The dashboard only allows SELECT queries in custom SQL

## 🎓 Academic Context

This project was completed as part of the **MSc AI, Data Mining and Big Data** program, specifically for **Module 2: Data Warehousing**. The project demonstrates:

- Understanding of dimensional modeling concepts (star schema, fact tables, dimension tables)
- Implementation of ETL processes for data integration
- Design and deployment of a cloud-based data warehouse
- Development of business intelligence dashboards
- Application of data warehousing best practices in a real-world financial domain

### Key Learning Outcomes

- **Data Modeling**: Designed and implemented a star schema for financial trading data
- **ETL Development**: Created robust ETL pipelines for data extraction and transformation
- **Cloud Infrastructure**: Deployed data warehouse on Supabase (PostgreSQL)
- **Visualization**: Built interactive dashboards using Streamlit and Plotly
- **Performance Tuning**: Optimized queries using materialized views and indexing strategies

## 📞 Troubleshooting

### Connection Issues
- Verify your connection string uses port 6543 (pooler)
- Check that your Supabase project is active
- Ensure your IP is not blocked by Supabase firewall

### Performance Issues
- Refresh materialized views: `REFRESH MATERIALIZED VIEW mv_daily_portfolio_var;`
- Check database query performance in Supabase dashboard
- Reduce date ranges in time series queries

### Missing Data
- Ensure all ETL processes have completed
- Check that materialized views are populated
- Verify data date ranges match your queries

