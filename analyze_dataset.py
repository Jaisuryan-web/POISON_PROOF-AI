#!/usr/bin/env python3
"""
Quick Dataset Analyzer
Analyzes training datasets for model readiness
"""

import pandas as pd
import numpy as np
import sys

def analyze_dataset(filepath):
    """Analyze dataset for training readiness"""
    
    print("\n" + "="*70)
    print("🔍 DATASET ANALYSIS REPORT")
    print("="*70)
    
    try:
        df = pd.read_csv(filepath)
        print(f"\n✓ Successfully loaded: {filepath}")
    except Exception as e:
        print(f"\n✗ Error loading dataset: {e}")
        return
    
    # Basic info
    print(f"\n📊 BASIC INFORMATION")
    print("-" * 70)
    print(f"   Total rows: {len(df):,}")
    print(f"   Total columns: {len(df.columns)}")
    
    # Get file size
    import os
    if os.path.exists(filepath):
        file_size = os.path.getsize(filepath)
        if file_size < 1024:
            size_str = f"{file_size} bytes"
        elif file_size < 1024**2:
            size_str = f"{file_size/1024:.1f} KB"
        else:
            size_str = f"{file_size/(1024**2):.1f} MB"
        print(f"   File size: {size_str}")
    
    # Column info
    print(f"\n📋 COLUMNS")
    print("-" * 70)
    for col in df.columns:
        null_count = df[col].isnull().sum()
        null_pct = (null_count / len(df)) * 100
        print(f"   • {col:25s} {str(df[col].dtype):15s} Nulls: {null_count:4d} ({null_pct:5.1f}%)")
    
    # Check for target variable
    print(f"\n🎯 TARGET VARIABLE ANALYSIS")
    print("-" * 70)
    
    potential_targets = ['is_anomaly', 'label', 'target', 'class', 'anomaly']
    target_col = None
    
    for col in potential_targets:
        if col in df.columns:
            target_col = col
            break
    
    if target_col:
        print(f"   ✓ Found target variable: '{target_col}'")
        value_counts = df[target_col].value_counts()
        print(f"\n   Distribution:")
        for val, count in value_counts.items():
            pct = (count / len(df)) * 100
            print(f"      {val}: {count:4d} ({pct:5.1f}%)")
        
        # Class imbalance check
        if len(value_counts) == 2:
            ratio = value_counts.max() / value_counts.min()
            if ratio > 3:
                print(f"\n   ⚠️  Class imbalance detected (ratio: {ratio:.1f}:1)")
                print(f"      Consider rebalancing or using class_weight='balanced'")
            else:
                print(f"\n   ✓ Classes are reasonably balanced (ratio: {ratio:.1f}:1)")
    else:
        print(f"   ⚠️  No target variable found")
        print(f"      Looking for: {', '.join(potential_targets)}")
        print(f"      You may need to add a target column for supervised learning")
    
    # Numerical features
    print(f"\n📈 NUMERICAL FEATURES")
    print("-" * 70)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if target_col and target_col in numeric_cols:
        numeric_cols.remove(target_col)
    
    if numeric_cols:
        print(f"   Found {len(numeric_cols)} numerical features:")
        stats = df[numeric_cols].describe().T
        print(f"\n   {'Feature':<25s} {'Min':>10s} {'Mean':>10s} {'Max':>10s} {'Std':>10s}")
        print(f"   {'-'*25} {'-'*10} {'-'*10} {'-'*10} {'-'*10}")
        for col in numeric_cols[:10]:  # Show first 10
            print(f"   {col:<25s} {df[col].min():>10.2f} {df[col].mean():>10.2f} {df[col].max():>10.2f} {df[col].std():>10.2f}")
        
        if len(numeric_cols) > 10:
            print(f"   ... and {len(numeric_cols) - 10} more")
    else:
        print(f"   No numerical features found")
    
    # Categorical features
    print(f"\n📝 CATEGORICAL FEATURES")
    print("-" * 70)
    
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if cat_cols:
        print(f"   Found {len(cat_cols)} categorical features:")
        for col in cat_cols[:5]:  # Show first 5
            unique_count = df[col].nunique()
            print(f"   • {col:<25s} {unique_count:4d} unique values")
            
            # Show sample values if not too many
            if unique_count <= 10:
                sample_vals = df[col].value_counts().head(5).index.tolist()
                print(f"      Examples: {', '.join([str(v)[:30] for v in sample_vals[:3]])}")
        
        if len(cat_cols) > 5:
            print(f"   ... and {len(cat_cols) - 5} more")
    else:
        print(f"   No categorical features found")
    
    # Data quality
    print(f"\n🔍 DATA QUALITY CHECKS")
    print("-" * 70)
    
    issues = []
    
    # Check for missing values
    total_nulls = df.isnull().sum().sum()
    if total_nulls > 0:
        issues.append(f"Missing values: {total_nulls} cells ({(total_nulls / (len(df) * len(df.columns)) * 100):.1f}%)")
    
    # Check for duplicates
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        issues.append(f"Duplicate rows: {duplicates}")
    
    # Check for constant columns
    constant_cols = [col for col in df.columns if df[col].nunique() == 1]
    if constant_cols:
        issues.append(f"Constant columns: {len(constant_cols)} ({', '.join(constant_cols[:3])})")
    
    # Check for high cardinality
    high_card_cols = [col for col in cat_cols if df[col].nunique() > 100]
    if high_card_cols:
        issues.append(f"High cardinality: {len(high_card_cols)} columns with >100 unique values")
    
    if issues:
        print(f"   Found {len(issues)} potential issues:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    else:
        print(f"   ✓ No major data quality issues detected")
    
    # Training readiness
    print(f"\n✅ TRAINING READINESS")
    print("-" * 70)
    
    readiness_score = 0
    max_score = 5
    
    # Check 1: Has target variable
    if target_col:
        print(f"   ✓ Target variable present")
        readiness_score += 1
    else:
        print(f"   ✗ No target variable found")
    
    # Check 2: Has features
    if len(numeric_cols) > 0:
        print(f"   ✓ Numerical features present ({len(numeric_cols)})")
        readiness_score += 1
    else:
        print(f"   ✗ No numerical features")
    
    # Check 3: Sufficient data
    if len(df) >= 100:
        print(f"   ✓ Sufficient samples ({len(df)} rows)")
        readiness_score += 1
    else:
        print(f"   ⚠️  Small dataset ({len(df)} rows, recommend 100+)")
    
    # Check 4: No excessive missing data
    if (df.isnull().sum().sum() / (len(df) * len(df.columns))) < 0.1:
        print(f"   ✓ Low missing data rate")
        readiness_score += 1
    else:
        print(f"   ⚠️  High missing data rate")
    
    # Check 5: Balanced classes
    if target_col and len(df[target_col].value_counts()) > 1:
        ratio = df[target_col].value_counts().max() / df[target_col].value_counts().min()
        if ratio < 5:
            print(f"   ✓ Reasonably balanced classes")
            readiness_score += 1
        else:
            print(f"   ⚠️  Imbalanced classes (ratio: {ratio:.1f}:1)")
    else:
        readiness_score += 1
    
    print(f"\n   Training readiness: {readiness_score}/{max_score} ({'✓ READY' if readiness_score >= 4 else '⚠️ NEEDS ATTENTION'})")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS")
    print("-" * 70)
    
    recommendations = []
    
    if not target_col:
        recommendations.append("Add a target variable column (e.g., 'is_anomaly', 'label')")
    
    if total_nulls > 0:
        recommendations.append(f"Handle {total_nulls} missing values (imputation or removal)")
    
    if duplicates > 0:
        recommendations.append(f"Remove {duplicates} duplicate rows")
    
    if high_card_cols:
        recommendations.append(f"Consider encoding or hashing high-cardinality features")
    
    if target_col and len(df[target_col].value_counts()) == 2:
        ratio = df[target_col].value_counts().max() / df[target_col].value_counts().min()
        if ratio > 3:
            recommendations.append("Consider SMOTE or class_weight='balanced' for imbalanced classes")
    
    if len(numeric_cols) < 3:
        recommendations.append("Consider feature engineering to create more numerical features")
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
    else:
        print(f"   ✓ Dataset looks good! Ready for training.")
    
    print(f"\n" + "="*70)
    print(f"Analysis complete! 🎉")
    print("="*70 + "\n")

def main():
    """Main execution"""
    
    if len(sys.argv) < 2:
        # Default to training_dataset.csv
        filepath = "training_dataset.csv"
        print(f"No file specified, analyzing default: {filepath}")
    else:
        filepath = sys.argv[1]
    
    analyze_dataset(filepath)

if __name__ == "__main__":
    main()
