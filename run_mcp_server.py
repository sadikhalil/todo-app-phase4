#!/usr/bin/env python3
"""
Script to start the MCP server for Todo Chat
"""

import subprocess
import sys
import os

def main():
    print("Starting MCP Server for Todo Chat...")
    print("Server will be available at http://localhost:8001")

    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    os.chdir(backend_dir)

    # Start the MCP server
    cmd = [
        sys.executable,
        "-m", "uvicorn",
        "mcp.server:app",
        "--host", "0.0.0.0",
        "--port", "8001",
        "--reload"
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting MCP server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nMCP server stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()