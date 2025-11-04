import os
import hashlib
import pandas as pd
import numpy as np
import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from PIL import Image, ImageChops
from io import BytesIO
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

def _robust_z_score(series: pd.Series):
    """Compute robust z-scores using Median Absolute Deviation (MAD)."""
    s = pd.to_numeric(series, errors='coerce')
    med = np.nanmedian(s)
    mad = np.nanmedian(np.abs(s - med))
    if mad == 0 or np.isnan(mad):
        # Fallback to standard deviation if MAD is zero
        std = np.nanstd(s)
        if std == 0 or np.isnan(std):
            return pd.Series(np.zeros(len(s)), index=series.index)
        return (s - np.nanmean(s)) / std
    return 0.6745 * (s - med) / mad


def _iqr_bounds(series: pd.Series):
    """Return lower and upper bounds using IQR method."""
    s = pd.to_numeric(series, errors='coerce')
    q1 = np.nanpercentile(s, 25)
    q3 = np.nanpercentile(s, 75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return lower, upper


def _detect_csv_anomalies(df: pd.DataFrame, max_findings: int = 50):
    """Detect real anomalies in a CSV using robust statistics on numeric columns.

    - Uses robust z-score (MAD) and IQR fences per numeric column.
    - Aggregates per-row anomalies into severity and confidence.
    """
    anomalies = []
    if df.empty:
        return anomalies

    # Keep only numeric columns for detection
    num_df = df.select_dtypes(include=[np.number]).copy()
    if num_df.empty:
        return anomalies

    row_scores = np.zeros(len(num_df))
    detail_records = []

    for col in num_df.columns:
        rz = _robust_z_score(num_df[col])
        lower, upper = _iqr_bounds(num_df[col])

        # Flags
        z_flags = np.abs(rz) > 3.5
        iqr_flags = (num_df[col] < lower) | (num_df[col] > upper)
        flags = z_flags | iqr_flags

        # Accumulate row scores by magnitude
        row_scores += np.where(flags, np.minimum(np.abs(rz.fillna(0)), 10), 0)

        # Record detailed column anomalies
        flagged_idx = np.where(flags)[0]
        for idx in flagged_idx:
            value = num_df.iloc[idx][col]
            rz_val = float(rz.iloc[idx]) if not np.isnan(rz.iloc[idx]) else 0.0
            magnitude = min(abs(rz_val) / 4.0, 1.0)  # normalize
            severity = 'High' if abs(rz_val) > 5 else 'Medium' if abs(rz_val) > 4 else 'Low'
            detail_records.append({
                'row': int(idx) + 1,
                'column': col,
                'value': None if pd.isna(value) else (float(value) if isinstance(value, (int, float, np.floating, np.integer)) else value),
                'rz': rz_val,
                'severity': severity,
                'confidence': round(0.6 + 0.4 * magnitude, 2)
            })

    # Rank rows by total anomaly score
    top_indices = np.argsort(-row_scores)[:max_findings]
    for idx in top_indices:
        if row_scores[idx] <= 0:
            continue
        # Collect columns for this row
        cols = [d for d in detail_records if d['row'] == int(idx) + 1]
        if not cols:
            continue
        # Determine overall severity
        high = any(c['severity'] == 'High' for c in cols)
        med = any(c['severity'] == 'Medium' for c in cols)
        severity = 'High' if high else 'Medium' if med else 'Low'
        confidence = round(min(0.95, 0.5 + 0.05 * len(cols) + 0.02 * float(row_scores[idx])) , 2)
        columns_str = ', '.join(sorted({c['column'] for c in cols}))
        anomalies.append({
            'type': 'Data Outlier',
            'location': f'Row {int(idx) + 1} (Columns: {columns_str})',
            'severity': severity,
            'description': 'Robust statistical detection flagged outlier values (MAD/IQR).',
            'confidence': confidence
        })

    # If too few anomalies found, surface a few strongest individual column hits
    if len(anomalies) < 5 and detail_records:
        detail_records.sort(key=lambda d: abs(d['rz']), reverse=True)
        for d in detail_records[: (5 - len(anomalies))]:
            anomalies.append({
                'type': 'Column Outlier',
                'location': f"Row {d['row']}, Column '{d['column']}'",
                'severity': d['severity'],
                'description': 'Value deviates significantly from distribution (robust z-score).',
                'confidence': d['confidence']
            })

    return anomalies


def _analyze_image(filepath: str):
    """Detect basic image anomalies: potential manipulation (ELA) and blur (gradient variance)."""
    findings = []
    with Image.open(filepath) as img:
        img = img.convert('RGB')

        # Error Level Analysis (ELA) - approximate manipulation signal
        buf = BytesIO()
        img.save(buf, format='JPEG', quality=90)
        buf.seek(0)
        comp = Image.open(buf).convert('RGB')

        diff = ImageChops.difference(img, comp)
        diff_np = np.asarray(diff, dtype=np.uint8)
        ela_score = float(diff_np.mean())  # average difference

        # Heuristic thresholds (tunable)
        if ela_score > 12.0:
            findings.append({
                'type': 'Visual Manipulation',
                'location': 'Global',
                'severity': 'High' if ela_score > 20 else 'Medium',
                'description': 'Error Level Analysis suggests possible local recompression or edits.',
                'confidence': round(min(0.95, 0.5 + (ela_score / 40.0)), 2)
            })

        # Blur/Sharpness via simple gradient variance (no OpenCV dependency)
        gray = np.asarray(img.convert('L'), dtype=np.float32)
        # Simple finite differences
        gx = gray[:, 1:] - gray[:, :-1]
        gy = gray[1:, :] - gray[:-1, :]
        grad_mag = np.sqrt(gx[:, :-1] ** 2 + gy[:-1, :] ** 2)
        grad_var = float(np.var(grad_mag))

        if grad_var < 25.0:  # low gradient variance => possibly blurry
            findings.append({
                'type': 'Image Quality',
                'location': 'Global',
                'severity': 'Medium' if grad_var < 15 else 'Low',
                'description': 'Low edge/texture energy indicates blur or low-detail image.',
                'confidence': round(0.6 if grad_var < 20 else 0.55, 2)
            })

        # Dynamic range check (very narrow intensity spread)
        rng = float(gray.max() - gray.min())
        if rng < 30.0:
            findings.append({
                'type': 'Image Quality',
                'location': 'Global',
                'severity': 'Low',
                'description': 'Very low dynamic range; image may be washed out or overly compressed.',
                'confidence': 0.55
            })

    return findings


def simulate_anomaly_detection(filepath, file_type):
    """
    Perform anomaly detection on uploaded dataset using lightweight, real methods:
    - CSV: robust statistics (MAD-based z-scores and IQR fences) on numeric columns
    - Images: ELA (error level analysis) + blur/dynamic range checks
    """
    anomalies = []

    if file_type == 'csv':
        try:
            df = pd.read_csv(filepath)
            anomalies = _detect_csv_anomalies(df, max_findings=50)
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
            anomalies = _analyze_image(filepath)
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