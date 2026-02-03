#!/usr/bin/env python3
"""
Script to start the main Todo application server
"""

import subprocess
import sys
import os

def main():
    print("Starting Main Todo Application Server...")
    print("Server will be available at http://localhost:8000")

    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    os.chdir(backend_dir)

    # Start the main server
    cmd = [
        sys.executable,
        "-m", "uvicorn",
        "src.api.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting main server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nMain server stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()