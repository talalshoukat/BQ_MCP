#!/usr/bin/env python3
"""
Setup script for BigQuery MCP Agent
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_config_file():
    """Check if config file exists and is valid"""
    print("📋 Checking configuration...")
    config_path = Path("config.yaml")
    
    if not config_path.exists():
        print("❌ config.yaml not found")
        return False
    
    # Basic YAML validation
    try:
        import yaml
        with open(config_path, 'r') as f:
            yaml.safe_load(f)
        print("✅ config.yaml is valid")
        return True
    except Exception as e:
        print(f"❌ config.yaml is invalid: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return False
    return True

def check_google_credentials():
    """Check if Google Cloud credentials are configured"""
    print("🔐 Checking Google Cloud credentials...")
    
    # Check if gcloud is installed
    if not run_command("gcloud --version", "Checking gcloud CLI"):
        print("⚠️  gcloud CLI not found - you may need to install it")
        print("   Visit: https://cloud.google.com/sdk/docs/install")
        return False
    
    # Check if authenticated
    try:
        result = subprocess.run("gcloud auth list --filter=status:ACTIVE --format=value(account)", 
                              shell=True, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            print(f"✅ Authenticated as: {result.stdout.strip()}")
            return True
        else:
            print("⚠️  Not authenticated with gcloud")
            print("   Run: gcloud auth application-default login")
            return False
    except Exception as e:
        print(f"⚠️  Could not check authentication: {e}")
        return False

def run_tests():
    """Run basic tests"""
    print("🧪 Running basic tests...")
    return run_command("python test_agent.py", "Running agent tests")

def main():
    """Main setup function"""
    print("🚀 BigQuery MCP Agent Setup")
    print("=" * 40)
    
    checks = [
        ("Python Version", check_python_version),
        ("Configuration", check_config_file),
        ("Dependencies", install_dependencies),
        ("Google Credentials", check_google_credentials),
        ("Basic Tests", run_tests)
    ]
    
    failed_checks = []
    
    for check_name, check_func in checks:
        if not check_func():
            failed_checks.append(check_name)
        print()
    
    print("=" * 40)
    
    if failed_checks:
        print(f"❌ Setup completed with {len(failed_checks)} issue(s):")
        for check in failed_checks:
            print(f"   - {check}")
        print("\n💡 Please resolve the issues above before using the agent")
    else:
        print("🎉 Setup completed successfully!")
        print("\n💡 You can now run the agent:")
        print("   python main.py")
    
    return len(failed_checks) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
