from flask import Flask, render_template, jsonify, request, redirect
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import os
import tempfile
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Start with no data
df = None

# Remove REQUIRED_COLUMNS and has_required_columns checks
# Only check for empty DataFrame

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def get_active_df():
    global df
    return df

# Sample traffic safety data
def generate_sample_data():
    """Generate realistic traffic safety data for demonstration"""
    np.random.seed(42)
    
    # Generate dates for the last 2 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Generate accident data
    n_records = len(dates)
    
    data = {
        'date': dates,
        'accident_type': np.random.choice(['Collision', 'Pedestrian', 'Motorcycle', 'Bicycle', 'Rollover'], n_records, p=[0.4, 0.2, 0.15, 0.15, 0.1]),
        'severity': np.random.choice(['Minor', 'Moderate', 'Severe', 'Fatal'], n_records, p=[0.5, 0.3, 0.15, 0.05]),
        'weather_condition': np.random.choice(['Clear', 'Rainy', 'Foggy', 'Snowy', 'Windy'], n_records, p=[0.6, 0.2, 0.1, 0.05, 0.05]),
        'road_condition': np.random.choice(['Good', 'Fair', 'Poor', 'Wet', 'Icy'], n_records, p=[0.7, 0.15, 0.05, 0.07, 0.03]),
        'time_of_day': np.random.choice(['Morning', 'Afternoon', 'Evening', 'Night'], n_records, p=[0.25, 0.3, 0.25, 0.2]),
        'day_of_week': [d.strftime('%A') for d in dates],
        'month': [d.strftime('%B') for d in dates],
        'year': [d.year for d in dates],
        'location_district': np.random.choice(['Downtown', 'Suburbs', 'Highway', 'Rural', 'Industrial'], n_records, p=[0.3, 0.25, 0.2, 0.15, 0.1]),
        'speed_limit': np.random.choice([25, 30, 35, 40, 45, 50, 55, 60, 65, 70], n_records, p=[0.1, 0.15, 0.2, 0.15, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05]),
        'vehicles_involved': np.random.randint(1, 5, n_records),
        'injuries': np.random.randint(0, 10, n_records),
        'fatalities': np.random.randint(0, 3, n_records),
        'property_damage': np.random.uniform(1000, 50000, n_records),
        'alcohol_involved': np.random.choice([True, False], n_records, p=[0.15, 0.85]),
        'distracted_driving': np.random.choice([True, False], n_records, p=[0.25, 0.75])
    }
    
    # Add some seasonal patterns
    for i, date in enumerate(dates):
        # More accidents in winter months
        if date.month in [12, 1, 2]:
            if np.random.random() < 0.3:
                data['accident_type'][i] = np.random.choice(['Collision', 'Rollover'])
                data['weather_condition'][i] = np.random.choice(['Snowy', 'Icy'])
        
        # More accidents on weekends
        if date.weekday() >= 5:  # Weekend
            if np.random.random() < 0.4:
                data['severity'][i] = np.random.choice(['Moderate', 'Severe', 'Fatal'])
    
    return pd.DataFrame(data)

# Load data
# df = generate_sample_data() # This line is removed as per the new_code

def empty_plotly_figure(message='No data available'):
    import plotly.graph_objects as go
    fig = go.Figure()
    fig.add_annotation(text=message, x=0.5, y=0.5, showarrow=False, font=dict(size=20), xref="paper", yref="paper")
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
    return fig

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard with overview"""
    return render_template('dashboard.html')

@app.route('/analytics')
def analytics():
    """Detailed analytics page"""
    return render_template('analytics.html')

@app.route('/reports')
def reports():
    """Reports and insights page"""
    return render_template('reports.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload (CSV, JSON, Excel) and validate/parse it. Update global df."""
    global df
    if 'datafile' not in request.files:
        return jsonify({'success': False, 'message': 'No file part in the request.'})
    file = request.files['datafile']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected.'})
    # File size check
    file.seek(0, 2)  # Seek to end
    file_length = file.tell()
    file.seek(0)
    if file_length > MAX_FILE_SIZE:
        return jsonify({'success': False, 'message': 'File too large. Max 10MB allowed.'})
    filename = file.filename.lower()
    try:
        # Save to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name
        # Try to parse with pandas
        if filename.endswith('.csv'):
            df_uploaded = pd.read_csv(tmp_path, low_memory=False)
        elif filename.endswith('.json'):
            df_uploaded = pd.read_json(tmp_path)
        elif filename.endswith('.xls') or filename.endswith('.xlsx'):
            df_uploaded = pd.read_excel(tmp_path)
        else:
            os.remove(tmp_path)
            return jsonify({'success': False, 'message': 'Unsupported file type.'})
        os.remove(tmp_path)
        # Check if DataFrame is not empty
        if df_uploaded.empty:
            df = None
            return jsonify({'success': False, 'message': 'Uploaded file is empty or invalid.'})
        df = df_uploaded  # Update global df
        return jsonify({'success': True, 'message': f'File parsed successfully! Rows: {len(df_uploaded)}, Columns: {len(df_uploaded.columns)}'})
    except Exception as e:
        df = None
        return jsonify({'success': False, 'message': f'Error parsing file: {str(e)}'})

@app.route('/api/summary_stats')
def summary_stats():
    """API endpoint for summary statistics"""
    active_df = get_active_df()
    if active_df is None or active_df.empty:
        stats = {
            'total_accidents': 0,
            'total_fatalities': 0,
            'total_injuries': 0,
            'total_property_damage': 0.0,
            'avg_accidents_per_day': 0.0,
            'fatal_accident_rate': 0.0,
            'alcohol_related_rate': 0.0,
            'distracted_driving_rate': 0.0
        }
        return jsonify(stats)
    df = active_df
    # Try to use columns if present, else zeros
    def safe_sum(col):
        return int(df[col].sum()) if col in df.columns else 0
    def safe_float_sum(col):
        return float(df[col].sum()) if col in df.columns else 0.0
    def safe_count(col, val):
        return int((df[col] == val).sum()) if col in df.columns else 0
    def safe_rate(col):
        return float(df[col].sum()) / len(df) * 100 if col in df.columns and len(df) > 0 else 0.0
    stats = {
        'total_accidents': len(df),
        'total_fatalities': safe_sum('fatalities'),
        'total_injuries': safe_sum('injuries'),
        'total_property_damage': round(safe_float_sum('property_damage'), 2),
        'avg_accidents_per_day': round(len(df) / 730, 2) if len(df) > 0 else 0.0,
        'fatal_accident_rate': round(safe_count('severity', 'Fatal') / len(df) * 100, 2) if 'severity' in df.columns and len(df) > 0 else 0.0,
        'alcohol_related_rate': round(safe_rate('alcohol_involved'), 2),
        'distracted_driving_rate': round(safe_rate('distracted_driving'), 2)
    }
    return jsonify(stats)

@app.route('/api/accident_trends')
def accident_trends():
    """API endpoint for accident trends over time"""
    active_df = get_active_df()
    if active_df is None or active_df.empty or not all(col in active_df.columns for col in ['year', 'month']):
        import plotly
        fig = empty_plotly_figure('No data for trends')
        return plotly.io.to_json(fig)
    df = active_df
    monthly_data = df.groupby(['year', 'month']).size().reset_index(name='accidents')
    monthly_data['date'] = pd.to_datetime(monthly_data['year'].astype(str) + '-' + monthly_data['month'] + '-01')
    monthly_data = monthly_data.sort_values('date')
    import plotly.express as px
    fig = px.line(monthly_data, x='date', y='accidents', 
                  title='Monthly Accident Trends',
                  labels={'accidents': 'Number of Accidents', 'date': 'Month'})
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
    import plotly
    return plotly.io.to_json(fig)

@app.route('/api/accident_types')
def accident_types():
    """API endpoint for accident type distribution"""
    active_df = get_active_df()
    if active_df is None or active_df.empty or 'accident_type' not in active_df.columns:
        import plotly
        fig = empty_plotly_figure('No data for accident types')
        return plotly.io.to_json(fig)
    df = active_df
    type_counts = df['accident_type'].value_counts()
    
    fig = px.pie(values=type_counts.values, names=type_counts.index,
                 title='Accident Types Distribution',
                 color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
    import plotly
    return plotly.io.to_json(fig)

@app.route('/api/severity_analysis')
def severity_analysis():
    """API endpoint for severity analysis"""
    active_df = get_active_df()
    if active_df is None or active_df.empty or 'severity' not in active_df.columns:
        import plotly
        fig = empty_plotly_figure('No data for severity')
        return plotly.io.to_json(fig)
    df = active_df
    severity_counts = df['severity'].value_counts()
    
    fig = px.bar(x=severity_counts.index, y=severity_counts.values,
                 title='Accident Severity Distribution',
                 labels={'x': 'Severity', 'y': 'Number of Accidents'},
                 color=severity_counts.values,
                 color_continuous_scale='Reds')
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
    import plotly
    return plotly.io.to_json(fig)

@app.route('/api/weather_impact')
def weather_impact():
    """API endpoint for weather impact analysis"""
    active_df = get_active_df()
    if active_df is None or active_df.empty or 'weather_condition' not in active_df.columns or 'severity' not in active_df.columns:
        import plotly
        fig = empty_plotly_figure('No data for weather impact')
        return plotly.io.to_json(fig)
    df = active_df
    weather_severity = df.groupby('weather_condition')['severity'].apply(
        lambda x: (x == 'Fatal').sum() / len(x) * 100
    ).reset_index()
    weather_severity.columns = ['weather', 'fatal_rate']
    weather_severity['fatal_rate'] = weather_severity['fatal_rate'].astype(float)
    
    fig = px.bar(weather_severity, x='weather', y='fatal_rate',
                 title='Fatal Accident Rate by Weather Condition',
                 labels={'weather': 'Weather Condition', 'fatal_rate': 'Fatal Rate (%)'},
                 color='fatal_rate',
                 color_continuous_scale='Reds')
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
    import plotly
    return plotly.io.to_json(fig)

@app.route('/api/time_analysis')
def time_analysis():
    """API endpoint for time-based analysis"""
    active_df = get_active_df()
    if active_df is None or active_df.empty or 'day_of_week' not in active_df.columns or 'time_of_day' not in active_df.columns:
        import plotly
        fig = empty_plotly_figure('No data for time analysis')
        return plotly.io.to_json(fig)
    df = active_df
    # Day of week analysis
    day_counts = df['day_of_week'].value_counts()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_counts = day_counts.reindex(day_order)
    
    # Time of day analysis
    time_counts = df['time_of_day'].value_counts()
    time_order = ['Morning', 'Afternoon', 'Evening', 'Night']
    time_counts = time_counts.reindex(time_order)
    
    # Create subplot
    fig = make_subplots(rows=1, cols=2, 
                        subplot_titles=('Accidents by Day of Week', 'Accidents by Time of Day'))
    
    fig.add_trace(go.Bar(x=day_counts.index, y=day_counts.values, name='Day of Week'), row=1, col=1)
    fig.add_trace(go.Bar(x=time_counts.index, y=time_counts.values, name='Time of Day'), row=1, col=2)
    
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20), showlegend=False)
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/api/location_analysis')
def location_analysis():
    """API endpoint for location-based analysis"""
    active_df = get_active_df()
    if active_df is None or active_df.empty or 'location_district' not in active_df.columns:
        import plotly
        fig = empty_plotly_figure('No data for location analysis')
        return plotly.io.to_json(fig)
    df = active_df
    location_counts = df['location_district'].value_counts()
    
    fig = px.bar(x=location_counts.index, y=location_counts.values,
                 title='Accidents by Location District',
                 labels={'x': 'District', 'y': 'Number of Accidents'},
                 color=location_counts.values,
                 color_continuous_scale='Blues')
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
    import plotly
    return plotly.io.to_json(fig)

@app.route('/api/speed_analysis')
def speed_analysis():
    """API endpoint for speed limit analysis"""
    active_df = get_active_df()
    if active_df is None or active_df.empty or 'speed_limit' not in active_df.columns or 'severity' not in active_df.columns:
        import plotly
        fig = empty_plotly_figure('No data for speed analysis')
        return plotly.io.to_json(fig)
    df = active_df
    speed_severity = df.groupby('speed_limit')['severity'].apply(
        lambda x: (x == 'Fatal').sum() / len(x) * 100
    ).reset_index()
    speed_severity.columns = ['speed_limit', 'fatal_rate']
    speed_severity['fatal_rate'] = speed_severity['fatal_rate'].astype(float)
    
    fig = px.scatter(speed_severity, x='speed_limit', y='fatal_rate',
                     title='Fatal Accident Rate vs Speed Limit',
                     labels={'speed_limit': 'Speed Limit (mph)', 'fatal_rate': 'Fatal Rate (%)'},
                     size='fatal_rate',
                     color='fatal_rate',
                     color_continuous_scale='Reds')
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
    import plotly
    return plotly.io.to_json(fig)

@app.route('/api/risk_factors')
def risk_factors():
    """API endpoint for risk factor analysis"""
    active_df = get_active_df()
    if active_df is None or active_df.empty or 'severity' not in active_df.columns:
        import plotly
        fig = empty_plotly_figure('No data for risk factors')
        return plotly.io.to_json(fig)
    df = active_df
    # Alcohol involvement
    if 'alcohol_involved' in df.columns:
        alcohol_fatal_rate = float(df[df['alcohol_involved']]['severity'].apply(lambda x: x == 'Fatal').sum() / df['alcohol_involved'].sum() * 100) if df['alcohol_involved'].sum() > 0 else 0.0
    else:
        alcohol_fatal_rate = 0.0
    # Distracted driving
    if 'distracted_driving' in df.columns:
        distracted_fatal_rate = float(df[df['distracted_driving']]['severity'].apply(lambda x: x == 'Fatal').sum() / df['distracted_driving'].sum() * 100) if df['distracted_driving'].sum() > 0 else 0.0
    else:
        distracted_fatal_rate = 0.0
    # Overall fatal rate
    overall_fatal_rate = float((df['severity'] == 'Fatal').sum() / len(df) * 100)
    
    risk_data = {
        'factor': ['Overall', 'Alcohol Involved', 'Distracted Driving'],
        'fatal_rate': [overall_fatal_rate, alcohol_fatal_rate, distracted_fatal_rate]
    }
    
    fig = px.bar(x=risk_data['factor'], y=risk_data['fatal_rate'],
                 title='Fatal Accident Rate by Risk Factor',
                 labels={'x': 'Risk Factor', 'y': 'Fatal Rate (%)'},
                 color=risk_data['fatal_rate'],
                 color_continuous_scale='Reds')
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
    import plotly
    return plotly.io.to_json(fig)

@app.route('/api/monthly_breakdown')
def monthly_breakdown():
    """API endpoint for monthly breakdown by year"""
    active_df = get_active_df()
    if active_df is None or active_df.empty or not all(col in active_df.columns for col in ['year', 'month', 'accident_type', 'fatalities', 'injuries', 'property_damage']):
        import plotly
        fig = empty_plotly_figure('No data for monthly breakdown')
        return plotly.io.to_json(fig)
    df = active_df
    monthly_breakdown = df.groupby(['year', 'month']).agg({
        'accident_type': 'count',
        'fatalities': 'sum',
        'injuries': 'sum',
        'property_damage': 'sum'
    }).reset_index()
    
    monthly_breakdown['date'] = pd.to_datetime(monthly_breakdown['year'].astype(str) + '-' + monthly_breakdown['month'] + '-01')
    monthly_breakdown = monthly_breakdown.sort_values('date')
    
    fig = make_subplots(rows=2, cols=2, 
                        subplot_titles=('Accidents', 'Fatalities', 'Injuries', 'Property Damage ($)'))
    
    fig.add_trace(go.Scatter(x=monthly_breakdown['date'], y=monthly_breakdown['accident_type'], name='Accidents'), row=1, col=1)
    fig.add_trace(go.Scatter(x=monthly_breakdown['date'], y=monthly_breakdown['fatalities'], name='Fatalities'), row=1, col=2)
    fig.add_trace(go.Scatter(x=monthly_breakdown['date'], y=monthly_breakdown['injuries'], name='Injuries'), row=2, col=1)
    fig.add_trace(go.Scatter(x=monthly_breakdown['date'], y=monthly_breakdown['property_damage'], name='Property Damage'), row=2, col=2)
    
    fig.update_layout(height=600, margin=dict(l=20, r=20, t=40, b=20), showlegend=False)
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
#A