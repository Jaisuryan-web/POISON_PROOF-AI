#!/usr/bin/env python3
"""
PoisonProof AI - Feature Demo Script
Demonstrates all new features programmatically
"""

import requests
import json
import time
from pathlib import Path

BASE_URL = "http://127.0.0.1:5000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def demo_api_endpoints():
    """Demonstrate API endpoints"""
    print_section("📡 API ENDPOINTS DEMO")
    
    # 1. Get audit logs
    print("1️⃣ Fetching audit logs...")
    try:
        response = requests.get(f"{BASE_URL}/api/audit-log")
        data = response.json()
        print(f"   ✓ Found {data.get('count', 0)} audit log entries")
        if data.get('logs'):
            latest = data['logs'][-1]
            print(f"   Latest: {latest.get('event')} at {latest.get('timestamp', 'N/A')[:19]}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    time.sleep(1)
    
    # 2. Get models
    print("\n2️⃣ Fetching trained models...")
    try:
        response = requests.get(f"{BASE_URL}/api/models")
        data = response.json()
        print(f"   ✓ Found {data.get('count', 0)} trained models")
        if data.get('models'):
            best = max(data['models'], key=lambda m: m.get('accuracy', 0))
            print(f"   Best: {best.get('model_name', 'Unknown')} - {best.get('accuracy', 0)*100:.2f}% accuracy")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    time.sleep(1)
    
    # 3. Export audit log
    print("\n3️⃣ Exporting audit log as CSV...")
    try:
        response = requests.get(f"{BASE_URL}/api/audit-log/export")
        if response.status_code == 200:
            output_path = Path("audit_export.csv")
            output_path.write_bytes(response.content)
            print(f"   ✓ Exported to {output_path}")
            print(f"   Size: {len(response.content)} bytes")
        else:
            print(f"   ✗ Export failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

def demo_detection_coverage():
    """Show detection pattern coverage"""
    print_section("🔍 DETECTION COVERAGE")
    
    patterns = {
        "XSS": ["<script>", "onerror=", "alert()", "javascript:"],
        "SQL Injection": ["DROP TABLE", "UNION SELECT", "'OR'1'='1", "--"],
        "Command Injection": [";rm -rf", "|nc", "$()", "whoami"],
        "Path Traversal": ["../", "/etc/passwd"],
        "LDAP Injection": ["*)(", "(|"],
        "NoSQL Injection": ["$ne:", "$where:"]
    }
    
    print("Supported attack patterns:\n")
    total = 0
    for category, examples in patterns.items():
        print(f"   {category}: {len(examples)} patterns")
        for ex in examples[:2]:  # Show first 2
            print(f"      • {ex}")
        total += len(examples)
    
    print(f"\n   Total: 40+ unique patterns across {len(patterns)} categories")

def demo_image_forensics():
    """Show image forensics capabilities"""
    print_section("🖼️ IMAGE FORENSICS")
    
    techniques = [
        ("Error Level Analysis (ELA)", "Detects recompression artifacts"),
        ("EXIF Metadata", "Identifies editing software traces"),
        ("Entropy Analysis", "Detects steganography"),
        ("Blur Detection", "Measures image sharpness"),
        ("Dynamic Range", "Checks compression quality")
    ]
    
    print("Image forensics techniques:\n")
    for i, (name, desc) in enumerate(techniques, 1):
        print(f"   {i}. {name}")
        print(f"      → {desc}")

def demo_cyber_effects():
    """Show cyber theme features"""
    print_section("🎨 CYBER THEME FEATURES")
    
    effects = [
        "Matrix Rain Animation - Binary rain background",
        "Neon Glow Effects - Glowing text and borders",
        "Cyber Scan Lines - Animated scanning effect",
        "Threat Meter - Color-coded risk visualization",
        "Terminal Console - Live training output",
        "Glitch Effects - Cyberpunk-style text distortion",
        "Pulse Animations - Breathing status badges"
    ]
    
    print("Visual enhancements:\n")
    for effect in effects:
        name, desc = effect.split(" - ")
        print(f"   ✨ {name}")
        print(f"      {desc}")

def demo_model_comparison():
    """Show model comparison features"""
    print_section("📊 MODEL COMPARISON DASHBOARD")
    
    features = [
        "Accuracy Comparison Chart - Grouped bar chart (Plotly)",
        "Hash Verification - SHA-256 integrity checks",
        "Model Metrics - Accuracy, Precision, Recall",
        "Download Models - Direct .pkl file downloads",
        "Delete Models - With confirmation prompt",
        "Best Model Highlight - Automatic identification"
    ]
    
    print("Dashboard capabilities:\n")
    for feature in features:
        name, desc = feature.split(" - ")
        print(f"   📈 {name}")
        print(f"      {desc}")

def demo_live_training():
    """Show live training features"""
    print_section("🔴 LIVE TRAINING CONSOLE")
    
    print("Server-Sent Events (SSE) streaming:\n")
    print("   1. Upload cleaned dataset")
    print("   2. Real-time console output appears:")
    print("      [INFO] Loading cleaned dataset...")
    print("      [INFO] Training DecisionTreeClassifier...")
    print("      [OK] Accuracy: 0.8521")
    print("      [SECURE] Model hash: a41e9f0bcd...")
    print("      [DONE] Training complete ✅")
    print("\n   3. Metrics update live:")
    print("      • Progress bar: 0% → 100%")
    print("      • Accuracy badge updates in real-time")
    print("      • Model hash appears when ready")

def main():
    """Run all demos"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║           🛡️  POISONPROOF AI - FEATURE DEMO  🛡️          ║
    ║                                                           ║
    ║         Advanced AI Security & Integrity Platform        ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    print("\n⚠️  Note: Make sure the Flask server is running at http://127.0.0.1:5000\n")
    input("Press Enter to start demo...")
    
    # Run demos
    demo_detection_coverage()
    time.sleep(2)
    
    demo_image_forensics()
    time.sleep(2)
    
    demo_cyber_effects()
    time.sleep(2)
    
    demo_live_training()
    time.sleep(2)
    
    demo_model_comparison()
    time.sleep(2)
    
    demo_api_endpoints()
    
    # Summary
    print_section("✅ DEMO COMPLETE")
    print("""
    🎉 All features demonstrated!
    
    Next steps:
    1. Visit http://127.0.0.1:5000 to see the UI
    2. Upload a dataset to test detection
    3. Train a model to see live console
    4. Check /models dashboard for comparisons
    5. Use API endpoints in your CI/CD pipeline
    
    Documentation:
    • README.md - Setup and usage guide
    • FEATURES.md - Detailed feature descriptions
    • API docs at /api/* endpoints
    
    Happy hacking! 🚀
    """)

if __name__ == "__main__":
    main()
