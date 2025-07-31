# Traffic Safety Analytics Dashboard

A comprehensive web-based analytics platform for analyzing traffic safety data with interactive dashboards, advanced analytics, and detailed reporting capabilities.

## 🚗 Features

### 📊 Interactive Dashboards
- **Overview Dashboard**: Real-time traffic safety metrics and key performance indicators
- **Advanced Analytics**: Deep dive into patterns, risk factors, and correlations
- **Reports & Insights**: Comprehensive reporting with actionable recommendations

### 📈 Data Visualization
- Interactive charts using Plotly.js
- Multiple chart types: line charts, bar charts, pie charts, scatter plots
- Responsive design for all device sizes
- Real-time data updates

### 🔍 Analytics Capabilities
- **Trend Analysis**: Monthly and yearly accident trends
- **Geographic Analysis**: Accident distribution by location districts
- **Weather Impact**: Correlation between weather conditions and accident severity
- **Time-based Analysis**: Day of week and time of day patterns
- **Risk Factor Analysis**: Alcohol involvement, distracted driving, speed limits
- **Severity Analysis**: Accident severity distribution and fatal rates

### 📋 Sample Data
The application includes realistic sample data with:
- 2 years of daily accident records
- Multiple accident types (Collision, Pedestrian, Motorcycle, Bicycle, Rollover)
- Severity levels (Minor, Moderate, Severe, Fatal)
- Weather conditions (Clear, Rainy, Foggy, Snowy, Windy)
- Location districts (Downtown, Suburbs, Highway, Rural, Industrial)
- Time-based patterns with seasonal variations

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Modern CSS with gradients and animations
- **Icons**: Font Awesome
- **Fonts**: Inter (Google Fonts)

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ML_project
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

## 🚀 Usage

### Main Dashboard (`/`)
- Landing page with overview statistics
- Quick access to all dashboard sections
- Real-time summary metrics

### Overview Dashboard (`/dashboard`)
- Comprehensive traffic safety metrics
- Interactive charts for trends and patterns
- Key performance indicators
- Geographic and time-based analysis

### Advanced Analytics (`/analytics`)
- Weather impact analysis
- Speed limit correlation studies
- Risk factor analysis
- Monthly breakdown charts
- Actionable insights and recommendations

### Reports & Insights (`/reports`)
- Executive summary statistics
- Report generation options
- Annual trends overview
- Strategic recommendations

## 📊 API Endpoints

The application provides RESTful API endpoints for data access:

- `GET /api/summary_stats` - Summary statistics
- `GET /api/accident_trends` - Monthly accident trends
- `GET /api/accident_types` - Accident type distribution
- `GET /api/severity_analysis` - Severity distribution
- `GET /api/weather_impact` - Weather impact analysis
- `GET /api/time_analysis` - Time-based patterns
- `GET /api/location_analysis` - Geographic distribution
- `GET /api/speed_analysis` - Speed limit analysis
- `GET /api/risk_factors` - Risk factor analysis
- `GET /api/monthly_breakdown` - Monthly breakdown charts

## 🎨 Design Features

### Modern UI/UX
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Gradient Backgrounds**: Beautiful color schemes and visual appeal
- **Smooth Animations**: Hover effects and transitions
- **Card-based Layout**: Clean, organized information presentation
- **Interactive Elements**: Engaging user experience

### Color Scheme
- Primary: Purple gradient (#667eea to #764ba2)
- Secondary: Pink gradient (#f093fb to #f5576c)
- Accent: Blue gradient (#4facfe to #00f2fe)
- Success: Green gradient (#43e97b to #38f9d7)

## 📁 Project Structure

```
ML_project/
├── main.py                 # Flask application and API endpoints
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── templates/             # HTML templates
│   ├── index.html         # Landing page
│   ├── dashboard.html     # Main dashboard
│   ├── analytics.html     # Advanced analytics
│   └── reports.html       # Reports and insights
└── static/                # Static assets (CSS, JS, images)
```

## 🔧 Customization

### Adding Real Data
Replace the sample data generation in `main.py` with your actual data source:

```python
# Replace generate_sample_data() with your data loading function
def load_real_data():
    # Load your CSV, database, or API data
    df = pd.read_csv('your_traffic_data.csv')
    return df

df = load_real_data()
```

### Customizing Charts
Modify the chart configurations in the API endpoints to match your data structure and visualization preferences.

### Styling
Update the CSS in the HTML templates to match your brand colors and design preferences.

## 📈 Key Insights

The application provides valuable insights such as:

1. **Weather Impact**: Adverse weather conditions significantly increase fatal accident rates
2. **Speed Correlation**: Higher speed limits correlate with increased fatal accidents
3. **Risk Factors**: Alcohol involvement and distracted driving are major contributors
4. **Seasonal Patterns**: Winter months show increased accident frequency
5. **Geographic Distribution**: Downtown areas have highest frequency, highways have highest severity
6. **Time Patterns**: Afternoon/evening hours show highest accident rates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔮 Future Enhancements

- **Machine Learning Integration**: Predictive modeling for accident forecasting
- **Real-time Data**: Live data feeds from traffic monitoring systems
- **Mobile App**: Native mobile application
- **Export Features**: PDF and Excel report generation
- **User Authentication**: Multi-user support with role-based access
- **Database Integration**: PostgreSQL or MongoDB for data persistence
- **API Documentation**: Swagger/OpenAPI documentation
- **Unit Tests**: Comprehensive test coverage

---

**Built with ❤️ using Python, Flask, and modern web technologies**

