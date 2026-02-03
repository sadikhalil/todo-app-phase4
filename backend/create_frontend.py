"""Next.js Application for the Multi-User Todo Web Application."""

import os
from app.agents.frontend_agent import frontend_agent


def create_nextjs_application():
    """Create the complete Next.js application structure."""
    print("Creating Next.js application for multi-user Todo web application...")

    # Generate the project structure
    project_structure = frontend_agent.generate_nextjs_project()

    # Create the actual files
    frontend_agent.create_project_files("./frontend")

    print("Next.js application created successfully!")
    print("Files created:")
    for dir_name, files in project_structure.items():
        for file_name in files.keys():
            print(f"  - {dir_name}/{file_name}")

    print("\nAdditional files created:")
    print("  - package.json")
    print("  - tailwind.config.js")
    print("  - postcss.config.js")

    print("\nTo run the application:")
    print("  1. cd frontend")
    print("  2. npm install")
    print("  3. npm run dev")

    return project_structure


if __name__ == "__main__":
    create_nextjs_application()