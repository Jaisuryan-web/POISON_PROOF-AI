import os
import hashlib
import pandas as pd
import numpy as np
import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import plotly.graph_objs as go
import plotly.utils
from config import config

def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Create uploads directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register routes
    register_routes(app)
    
    return app

def register_routes(app):
    """Register all routes with the app"""
    
    @app.route('/')
    def index():
        """Landing page describing the AI integrity problem"""
        return render_template('index.html')

    @app.route('/upload')
    def upload_page():
        """File upload page"""
        return render_template('upload.html')

    @app.route('/scan', methods=['POST'])
    def scan_file():
        """Handle file upload and scanning"""
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('upload_page'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('upload_page'))
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Get file extension to determine type
            file_type = filename.rsplit('.', 1)[1].lower()
            
            # Calculate file hash
            file_hash = calculate_file_hash(filepath)
            
            # Simulate anomaly detection
            anomalies = simulate_anomaly_detection(filepath, file_type)
            
            # Generate chart
            chart_json = generate_anomaly_chart(anomalies)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return render_template('results.html', 
                                 anomalies=anomalies, 
                                 file_hash=file_hash,
                                 filename=filename,
                                 chart_json=chart_json)
        else:
            flash('Invalid file type. Please upload CSV or image files only.', 'error')
            return redirect(url_for('upload_page'))

    @app.route('/api/scan-status')
    def scan_status():
        """API endpoint for checking scan status (for future real-time updates)"""
        return jsonify({'status': 'completed'})

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'csv', 'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def calculate_file_hash(filepath):
    """Calculate SHA-256 hash of uploaded file"""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        # Read file in chunks to handle large files
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def simulate_anomaly_detection(filepath, file_type):
    """
    Simulate anomaly detection on uploaded dataset
    Returns dummy flagged data for demonstration
    """
    anomalies = []
    
    if file_type == 'csv':
        try:
            # Read CSV file
            df = pd.read_csv(filepath)
            num_rows, num_cols = df.shape
            
            # Simulate anomaly detection with dummy data
            # Generate random anomalies for demonstration
            num_anomalies = min(5, max(1, num_rows // 20))  # 5% of rows or max 5
            
            for i in range(num_anomalies):
                row_idx = np.random.randint(0, num_rows)
                col_idx = np.random.randint(0, num_cols)
                col_name = df.columns[col_idx] if col_idx < len(df.columns) else f'Column_{col_idx}'
                
                anomalies.append({
                    'type': 'Data Outlier',
                    'location': f'Row {row_idx + 1}, Column "{col_name}"',
                    'severity': np.random.choice(['High', 'Medium', 'Low']),
                    'description': f'Suspicious value detected: potential data poisoning',
                    'confidence': round(np.random.uniform(0.7, 0.95), 2)
                })
                
        except Exception as e:
            anomalies.append({
                'type': 'File Error',
                'location': 'File processing',
                'severity': 'High',
                'description': f'Error reading CSV file: {str(e)}',
                'confidence': 1.0
            })
    
    elif file_type in ['png', 'jpg', 'jpeg', 'gif', 'bmp']:
        try:
            # Simulate image anomaly detection
            img = Image.open(filepath)
            width, height = img.size
            
            # Generate dummy image anomalies
            num_anomalies = np.random.randint(1, 4)
            
            for i in range(num_anomalies):
                x = np.random.randint(0, width)
                y = np.random.randint(0, height)
                
                anomalies.append({
                    'type': 'Visual Manipulation',
                    'location': f'Pixel region ({x}, {y})',
                    'severity': np.random.choice(['High', 'Medium', 'Low']),
                    'description': 'Potential adversarial pattern or manipulation detected',
                    'confidence': round(np.random.uniform(0.6, 0.9), 2)
                })
                
        except Exception as e:
            anomalies.append({
                'type': 'File Error',
                'location': 'Image processing',
                'severity': 'High',
                'description': f'Error processing image: {str(e)}',
                'confidence': 1.0
            })
    
    return anomalies

def generate_anomaly_chart(anomalies):
    """Generate a chart visualization of anomalies using Plotly"""
    if not anomalies:
        return None
    
    # Count anomalies by severity
    severity_counts = {'High': 0, 'Medium': 0, 'Low': 0}
    for anomaly in anomalies:
        severity = anomaly.get('severity', 'Low')
        severity_counts[severity] += 1
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=list(severity_counts.keys()),
        values=list(severity_counts.values()),
        marker_colors=['#dc3545', '#ffc107', '#28a745']  # Bootstrap colors
    )])
    
    fig.update_layout(
        title="Anomaly Distribution by Severity",
        font=dict(size=14),
        showlegend=True,
        height=400
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# Create the app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)