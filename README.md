# PoisonProof AI — Dataset Integrity Verification System

PoisonProof AI is a modern Flask web app that helps you assess dataset integrity for AI/ML workflows. It provides:
- A clean Bootstrap 5 UI for uploading CSV or image datasets
- Real anomaly identification for tabular CSVs (robust statistics) and images (digital forensics heuristics)
- SHA‑256 hashing for dataset fingerprinting
- Visual summaries via Plotly charts

This README walks you from installing uv (fast Python package manager) to running and using the app, and then dives deep into how anomalies are detected with examples.

## 🔐 Secure Lab Flow (Enhanced)

- Entry: Home with Matrix rain background → "Scan Your Dataset" → `/secure-upload`
- Upload: CSV or image is validated, hashed (SHA-256), stored under `uploads/`, and tagged with a session ID
- Scan: 
  - CSV: MAD + IQR + 40+ injection signatures (XSS, SQLi, command injection, path traversal, LDAP, NoSQL)
  - Images: ELA + blur + EXIF metadata + entropy analysis (steganography detection)
- Results: Color-coded table + Plotly chart + copyable hash + threat meter
- Clean:
  - Auto: drops High severity rows with animated completion
  - Manual: interactive checkbox review for precise control
- Train: **LIVE** real-time streaming console with Server-Sent Events showing training progress
- Models Dashboard: Compare all trained models with accuracy charts and hash verification
- API: RESTful endpoints for programmatic access + audit log export (JSON/CSV)
- Logs: Complete audit trail in `logs/audit.json`; model registry in `trained_models/model_hashes.json`

## 🚀 Quick Start (Windows PowerShell with uv)

Install dependencies and run:
```powershell
uv sync
uv run python .\run.py
```

Access at: `http://127.0.0.1:5000`

## 🎨 New Cyber Features

### Matrix Rain Background
- Animated binary rain on landing page
- Neon glow effects on headings
- Futuristic cyber-lab aesthetic

### Live Training Console
- Real-time Server-Sent Events streaming
- Epoch-by-epoch progress updates
- Animated metrics display
- Model hash generation with verification

### Advanced Detection
- **40+ Payload Signatures**: XSS, SQLi, command injection, path traversal, LDAP, NoSQL
- **Image Forensics**: EXIF metadata analysis, entropy-based steganography detection
- **Enhanced ELA**: Improved Error Level Analysis with confidence scores

### Model Comparison Dashboard
- View all trained models in one place
- Accuracy/precision/recall comparison charts
- Hash verification status for each model
- Download or delete models
- Best model highlighting

## 📡 API Endpoints

All API endpoints return JSON responses:

### Get Audit Log
```bash
GET /api/audit-log
```
Returns all audit log entries with session IDs, timestamps, and actions.

### Export Audit Log (CSV)
```bash
GET /api/audit-log/export
```
Downloads audit log as CSV file.

### Get Models
```bash
GET /api/models
```
Returns all trained models with metrics and hashes.

### Verify File Hash
```bash
POST /api/verify/<expected_hash>
Content-Type: multipart/form-data
file: <file_to_verify>
```
Verifies file integrity by comparing against expected hash.

Example with curl:
```bash
curl -X POST -F "file=@dataset.csv" http://localhost:5000/api/verify/abc123...
```

## �🚀 Features

- Modern, responsive UI (Bootstrap 5, icons, toasts, progress indicators)
- CSV and image upload (CSV, PNG, JPG, JPEG, GIF, BMP)
- Real anomaly detection:
  - CSV: robust z-scores (MAD) + IQR outlier fences with per-row aggregation
  - Images: Error Level Analysis (ELA), blur/texture (gradient variance), and dynamic range checks
- SHA‑256 hashing of uploaded file for integrity
- Results page with severity-coded table, copyable hash, and a Plotly pie chart

## 🛠️ Technology Stack

- Backend: Flask
- Frontend: HTML5, Bootstrap 5, JavaScript
- Data: Pandas, NumPy, Pillow (PIL)
- Charts: Plotly.js

## 📋 Prerequisites

- Python 3.10+ (Python 3.12 supported)
- pip (Python package installer)
- uv (recommended for super-fast installs)

## 🔧 Installation with uv (Windows PowerShell)

1) Install/upgrade pip and uv
```powershell
python -m pip install --upgrade pip
python -m pip install uv
uv --version
```

2) Create and activate a virtual environment
```powershell
uv venv .venv
.\.venv\Scripts\Activate.ps1
```

3) Install dependencies from requirements.txt (Python 3.12-friendly)
```powershell
# If you are on Python 3.12, ensure requirements have:
#   numpy>=1.26,<3.0 and pandas>=2.2,<3.0
uv pip install -r requirements.txt
```

Alternative: pyproject workflow (optional)
```powershell
uv init --app
uv add flask==2.3.3 werkzeug==2.3.7 pillow==10.0.1 plotly==5.17.0
uv add "numpy>=1.26,<3.0" "pandas>=2.2,<3.0"
uv sync
uv run python run.py
```

## ▶️ Quick start

1) Start the app
```powershell
uv run -r requirements.txt python run.py
```

2) Access the app
Open your browser to: `http://127.0.0.1:5000`

3) Generate a big dataset (optional, for a rich demo)
```powershell
uv run -r requirements.txt python generate_large_dataset.py
```
This creates `large_employee_dataset.csv` (1000 rows, ~75 anomalies) in the project root.

4) Upload a file
- Go to “Scan Dataset” in the navbar.
- Drag-and-drop `large_employee_dataset.csv` (or your own CSV) or upload an image (PNG/JPG/etc.).
- A modal spinner appears while scanning; the file is hashed and analyzed, then deleted from disk.

5) View results
- Anomalies appear in a color-coded table (severity and confidence).
- The SHA‑256 hash can be copied to clipboard.
- A Plotly pie chart shows the severity distribution.

## 📁 Project structure

```
PoisonProof-AI/
├── app.py                  # Flask app + detection logic
├── config.py               # Settings (upload size, extensions, envs)
├── run.py                  # Entry point (uv/pip/python friendly)
├── generate_large_dataset.py# Create a 1000-row CSV with injected anomalies
├── requirements.txt        # Dependencies
├── templates/              # Jinja templates (Bootstrap UI)
│   ├── base.html
│   ├── index.html          # Landing page
│   ├── upload.html         # Upload form + loading modal
│   └── results.html        # Results (table + chart + hash)
├── static/
│   ├── css/style.css       # Custom styles
│   └── js/main.js          # UI helpers, toasts, animations
├── uploads/                # Temp storage (auto-cleaned)
├── large_employee_dataset.csv (generated)
└── README.md
```

## 🧠 How anomaly detection works

The app performs lightweight, real anomaly identification without heavy ML dependencies.

### A) CSV datasets (tabular)

We analyze only numeric columns using two robust statistical methods and then aggregate anomalies per row:

1) Robust z-score via MAD (Median Absolute Deviation)
   - For a numeric series x:
     - Median: m = median(x)
     - MAD: mad = median(|x - m|)
     - Robust z: rz = 0.6745 * (x - m) / mad  (0.6745 scales MAD to ~std)
   - We flag values with |rz| > 3.5 as strong outliers.

2) IQR fences (Interquartile Range)
   - q1 = 25th percentile, q3 = 75th percentile, iqr = q3 - q1
   - Lower fence = q1 - 1.5*iqr, Upper fence = q3 + 1.5*iqr
   - Values outside these fences are flagged.

3) Row aggregation and scoring
   - For each numeric column: if a cell is flagged by either method, its magnitude contributes to that row’s score.
   - Rows are sorted by total anomaly score; up to 50 highest rows are reported.
   - Severity is High if any column is very extreme (e.g., |rz| > 5), Medium for moderate extremes, else Low.
   - Confidence grows with magnitude and the number of flagged columns in the row.

Example (CSV)

Suppose a salary column has mostly values around 60,000–120,000, but one entry is 900,000. The median and MAD will be stable despite outliers, so the robust z-score for 900,000 is very large (|rz| >> 3.5), making it a High severity anomaly with high confidence. If that same row also has an impossible performance score (e.g., 11.5 on a 0–10 scale), the row score increases and the row becomes a top finding.

Tuning knobs (in `app.py`)
- Threshold for |rz| (default 3.5)
- IQR factor (default 1.5)
- Max reported findings (default 50)

Where to look: functions `_robust_z_score`, `_iqr_bounds`, `_detect_csv_anomalies`.

### B) Image datasets

We use three simple, effective heuristics:

1) Error Level Analysis (ELA)
   - Convert original to JPEG (quality≈90), then compute the pixel-wise difference between original and recompressed images.
   - Edited regions often recompress differently, yielding higher local differences.
   - We use the mean difference (ELA score) as a global signal; a high mean suggests edits or heavy recompression.

2) Blur/Texture via gradient variance
   - Convert to grayscale, compute finite differences in x/y, take gradient magnitude, then compute its variance.
   - Low variance indicates little edge/texture energy → possibly blurred or low-detail images.

3) Dynamic range
   - If max(gray) - min(gray) is very small, the image might be washed out or overly compressed.

Example (Image)

If you upload an image that has been locally airbrushed to remove text, the ELA score often increases because the touched-up region recompresses differently. The system will flag a “Visual Manipulation” with Medium or High severity depending on the score. If the image is also very blurry, you may see an additional “Image Quality” finding.

Tuning knobs (in `app.py`)
- ELA mean threshold (default 12.0; >20 is High)
- Blur threshold on gradient variance (default <25.0)
- Dynamic range threshold (default <30.0)

Where to look: function `_analyze_image`.

## 🧪 Using the application step-by-step

1) Generate a large CSV (optional)
```powershell
uv run -r requirements.txt python generate_large_dataset.py
```
This creates `large_employee_dataset.csv` with realistic distributions and ~75 injected anomalies (e.g., negative salaries, impossible scores, extreme overtime, age/experience mismatches).

2) Start the server
```powershell
uv run -r requirements.txt python run.py
```

3) Upload and scan
- Visit `http://127.0.0.1:5000` → “Scan Dataset”
- Drop `large_employee_dataset.csv` or any image file
- Wait for the modal spinner to finish (files are deleted after processing)

4) Read the results
- Severity badges (High/Medium/Low) indicate urgency
- Confidence indicates strength of evidence
- Copy the SHA‑256 hash and store it for later integrity verification
- The Plotly chart displays the severity distribution of findings

## 🛠️ Troubleshooting (Windows, Python 3.12)

Symptom: `uv add -r requirements.txt` fails building numpy 1.24.x with `ModuleNotFoundError: distutils`.

Cause: Python 3.12 removed distutils; old numpy/pandas rely on it. Fix by using 3.12‑compatible versions:
- `numpy >= 1.26`
- `pandas >= 2.2`

Solutions:
```powershell
# If using requirements.txt, ensure the ranges are updated, then:
uv pip install -r requirements.txt

# Or explicitly add compatible versions in a pyproject workflow:
uv add "numpy>=1.26,<3.0" "pandas>=2.2,<3.0"
uv sync
```

Other tips:
- If Plotly imports warn in your editor, ensure Plotly is installed in the active venv.
- If a CSV has no numeric columns, the CSV detector will return no anomalies.
- Very small images may bypass blur/ELA thresholds; try higher resolution for better signals.

## 🔒 Security

- Filenames are sanitized (`secure_filename`), types are validated, and max upload size is enforced
- Files are deleted after processing to minimize exposure
- Use a strong `SECRET_KEY` in production (via environment variable)

On Windows PowerShell, set environment variables like:
```powershell
$env:FLASK_ENV = "production"
$env:SECRET_KEY = "your-secure-secret-key"
python run.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Commit changes: `git commit -m "feat: add YourFeature"`
4. Push branch: `git push origin feature/YourFeature`
5. Open a Pull Request

## 📄 License

MIT — see [LICENSE](LICENSE)

## 📬 Support

Open an issue in the repository or contact the maintainer.

---

This is a proof‑of‑concept with practical, explainable detection. For higher assurance, integrate domain‑specific rules, model‑based detectors, and provenance tracking.
# PoisonProof AI - Dataset Integrity Verification System

A modern Flask web application that simulates a proof-of-concept for AI integrity verification. The system detects potential data poisoning attacks in machine learning datasets through advanced anomaly detection and cryptographic verification.

## 🚀 Features

- **Modern Web Interface**: Clean, responsive design using Bootstrap 5
- **File Upload System**: Support for CSV and image datasets (PNG, JPG, JPEG, GIF, BMP)
- **Anomaly Detection**: Real detection for CSVs using robust statistics (MAD-based z-scores and IQR) and image checks via Error Level Analysis (ELA) and blur metrics
- **Cryptographic Verification**: SHA-256 hashing for dataset integrity verification
- **Visual Analytics**: Interactive charts showing anomaly distribution
- **Real-time Processing**: Loading indicators and progress tracking
- **Security Features**: File validation, secure upload handling, and data cleanup

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Data Processing**: Pandas, NumPy, Pillow
- **Visualization**: Plotly.js
- **Security**: Werkzeug, SHA-256 hashing

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/joedanields/PoisonProof-AI.git
   cd PoisonProof-AI
   ```

2. **Create a virtual environment** (recommended)
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

## 🚀 Quick Start

1. **Run the application**
   ```bash
   python run.py
   ```
   Or use Flask's built-in command:
   ```bash
   python app.py
   ```

2. **Access the application**
   Open your web browser and navigate to: `http://127.0.0.1:5000`

## 📁 Project Structure

```
PoisonProof-AI/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── run.py                # Application runner script
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── base.html        # Base template with navbar/footer
│   ├── index.html       # Landing page
│   ├── upload.html      # File upload page
│   └── results.html     # Scan results page
├── static/              # Static assets
│   ├── css/
│   │   └── style.css    # Custom styles
│   └── js/
│       └── main.js      # JavaScript functionality
├── uploads/             # Temporary file storage (auto-created)
└── README.md           # This file
```

## 🎯 Usage

### 1. Landing Page
- Overview of AI integrity challenges
- Feature descriptions and benefits
- Call-to-action to start scanning

### 2. Upload Dataset
- Drag-and-drop or click to upload files
- File validation (type and size checking)
- Supported formats: CSV, PNG, JPG, JPEG, GIF, BMP
- Maximum file size: 16MB

### 3. Scan Results
- List of detected anomalies with severity levels
- Interactive pie chart showing anomaly distribution
- SHA-256 hash for dataset verification
- Copy hash functionality for future reference

## 🔒 Security Features

- **File Validation**: Strict file type and size checking
- **Secure Filenames**: Werkzeug's secure_filename for safe file handling
- **Temporary Storage**: Files are automatically deleted after processing
- **Hash Verification**: SHA-256 cryptographic hashing for integrity
- **CSRF Protection**: Built-in Flask security features

## 🎨 UI Components

### Color Coding
- **High Severity**: Red (Immediate attention required)
- **Medium Severity**: Yellow (Review recommended)
- **Low Severity**: Green (Minor concern)

### Interactive Elements
- Loading spinners during processing
- Progress indicators
- Hover effects on cards and buttons
- Responsive design for mobile devices

## ⚙️ Configuration

The application supports multiple environments through `config.py`:

- **Development**: Debug mode enabled, detailed error messages
- **Production**: Security hardened, optimized for deployment
- **Testing**: Configured for automated testing

## 🧪 Simulated Anomaly Detection
The application uses lightweight, real anomaly identification methods without heavy ML dependencies:

### CSV Files (tabular)
- Robust z-score using Median Absolute Deviation (MAD)
- IQR (interquartile range) fences per numeric column
- Per-row aggregation into severity + confidence
   - Tunables in `app.py`: z-score threshold (3.5), IQR factor (1.5), max results (50)

### Image Files
- Error Level Analysis (ELA) to flag potential edits/recompression
- Blur/texture check via gradient variance
- Dynamic range check for over-compression/washed-out images

These can be tuned in `app.py` inside `_detect_csv_anomalies` and `_analyze_image`.

## 🚀 Deployment

### Local Development
```bash
export FLASK_ENV=development
python run.py
```

### Production Deployment
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secure-secret-key
python run.py
```

## 🔄 Future Enhancements

- Real anomaly detection algorithms
- Machine learning model integration
- Database storage for scan history
- User authentication and authorization
- API endpoints for programmatic access
- Advanced visualization options
- Batch processing capabilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Bootstrap team for the excellent CSS framework
- Plotly.js for interactive visualizations
- Flask community for the robust web framework
- Open source community for inspiration and tools

## 📞 Support

For support, email [joedanielajd@gmail.com] or create an issue in the GitHub repository.

---

