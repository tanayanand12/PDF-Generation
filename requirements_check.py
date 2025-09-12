# requirements_check.py
"""Utility to verify all required packages are available."""

def check_requirements():
    """Check if all required packages are installed."""
    required_packages = [
        'fastapi', 'uvicorn', 'pydantic', 'openai', 'reportlab',
        'python-dotenv', 'requests', 'typing-extensions'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False
    
    print("All required packages are installed!")
    return True

if __name__ == "__main__":
    check_requirements()


