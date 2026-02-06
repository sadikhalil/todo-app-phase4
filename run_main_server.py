#!/usr/bin/env python3.11
"""
Script to start the consolidated Todo application server (main + MCP functionality)
"""

import subprocess
import sys
import os

def main():
    print("Starting Consolidated Todo Application Server...")
    print("Server will be available at http://localhost:8000")
    print("Includes both main API and MCP endpoints at /mcp/*")

    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    os.chdir(backend_dir)

    # Start the main server (now includes MCP functionality)
    cmd = [
        "python3.11",
        "-m", "uvicorn",
        "main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting consolidated server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nConsolidated server stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()