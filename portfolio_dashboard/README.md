# 📊 Investor Portfolio Analytics Dashboard

A professional, dynamic portfolio analytics dashboard built with Streamlit. This application provides comprehensive investment analysis with beautiful visualizations and easy data management.

## ✨ Features

- **📊 Client Overview**: Portfolio summaries, KPIs, asset allocation, and ROI trends
- **⚖️ Risk & Performance**: Risk-return analysis, investment size comparisons, ROI distributions
- **📤 Data Management**: Upload Excel/CSV files, download data, replace or append functionality
- **🎨 Professional UI**: Gradient designs, custom metric cards, interactive charts
- **🔄 Dynamic**: Handles changing data and column names automatically

## 🚀 Quick Start

### Local Development

1. **Clone/Download this project**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser:** http://localhost:8501

### Sample Data

The app comes with sample data in `data/portfolio_data.csv`. You can:
- View and analyze this sample data immediately
- Upload your own Excel/CSV files in the "Data Management" tab
- Replace or append to existing data

## 📁 Project Structure

```
portfolio_dashboard/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── utils/
│   ├── data_loader.py         # Data loading/saving functions
│   └── analytics.py           # ROI, risk, growth calculations
└── data/
    └── portfolio_data.csv     # Portfolio data (file-based storage)
```

## 📊 Data Format

Your Excel/CSV file should have these columns (minimum):

| Column | Description | Example |
|--------|-------------|---------|
| client_id | Unique client identifier | C001, C002 |
| asset_type | Type of investment | Stocks, Bonds, Real Estate |
| investment_amount | Initial investment (₹) | 100000 |
| current_value | Current value (₹) | 125000 |
| investment_start_date | Investment date | 2023-01-15 |

**Flexible Column Names:** The app automatically handles variations like:
- `investment_amount_inr`, `invested_amount` → `investment_amount`
- `annual_return_inr`, `return_inr`, `current_val` → `current_value`

## 🌐 Deploy to Streamlit Cloud

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your GitHub repository
   - Main file: `app.py`
   - Click "Deploy"

3. **Your app will be live at:** `https://YOUR_APP.streamlit.app`

## 🎯 Key Analytics

### ROI Calculation
```
ROI % = ((Current Value - Investment Amount) / Investment Amount) × 100
```

### Risk Assessment
Based on:
- Asset type volatility (Stocks: 7/10, Bonds: 3/10, etc.)
- ROI variance across similar assets
- Categorized as Low, Medium, or High

### Growth Metrics
- **CAGR**: Compound Annual Growth Rate
- **Time-weighted returns**: Based on investment duration
- **Profit/Loss**: Total gains or losses

## 🔧 Customization

### Modify Risk Scores
Edit `utils/analytics.py`, function `calculate_risk()`:
```python
asset_risk_scores = {
    'stocks': 7,      # Change these values
    'bonds': 3,
    'crypto': 9,
    # Add more asset types
}
```

### Change UI Colors
Edit gradient colors in `app.py`:
```python
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

## 📝 Usage Tips

1. **Upload Data**: Use the "Data Management" tab to upload Excel/CSV files
2. **Filter Views**: Select clients and asset types from the sidebar
3. **Download Reports**: Export current data as CSV from the Data Management tab
4. **Dynamic Updates**: The app recalculates all metrics automatically when data changes

## 🛠️ Technologies

- **Streamlit**: Web framework
- **Pandas**: Data manipulation
- **Plotly**: Interactive visualizations
- **NumPy**: Numerical calculations

## 📄 License

This project is open source and available for personal and commercial use.

## 🤝 Support

For issues or questions:
1. Check the sample data format
2. Ensure column names match expected format
3. Use the Debug info in the sidebar to see available columns

---

**Built with ❤️ using Streamlit and Python**
