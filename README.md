# PoisonProof AI - Dataset Integrity Verification System

A modern Flask web application that simulates a proof-of-concept for AI integrity verification. The system detects potential data poisoning attacks in machine learning datasets through advanced anomaly detection and cryptographic verification.

## 🚀 Features

- **Modern Web Interface**: Clean, responsive design using Bootstrap 5
- **File Upload System**: Support for CSV and image datasets (PNG, JPG, JPEG, GIF, BMP)
- **Anomaly Detection**: Simulated scanning for suspicious patterns and outliers
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

The current implementation includes simulated anomaly detection for demonstration purposes:

### CSV Files
- Random outlier detection
- Data pattern analysis simulation
- Column-wise anomaly flagging

### Image Files
- Visual manipulation detection
- Pixel-level anomaly simulation
- Adversarial pattern identification

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

