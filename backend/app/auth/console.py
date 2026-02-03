"""Authentication module for the Todo App console interface."""

import os
from app.agents.main import agent_handler


class AuthConsole:
    """Handles authentication flows in the console application."""

    def __init__(self):
        self.current_user = None
        self.current_token = None

    def signup_flow(self):
        """Handle the signup flow in console."""
        print("\n--- Sign Up ---")

        email = input("Enter email: ").strip()
        if not email:
            print("Email is required!")
            return False

        password = input("Enter password (at least 6 characters): ").strip()
        if not password:
            print("Password is required!")
            return False

        result = agent_handler.signup(email, password)

        if result["success"]:
            print(f"\n{result['message']}")
            self.current_user = result["user"]
            self.current_token = result["token"]
            print(f"Welcome, {email}! You are now logged in.")
            return True
        else:
            print(f"\nError: {result['message']}")
            return False

    def login_flow(self):
        """Handle the login flow in console."""
        print("\n--- Log In ---")

        email = input("Enter email: ").strip()
        if not email:
            print("Email is required!")
            return False

        password = input("Enter password: ").strip()
        if not password:
            print("Password is required!")
            return False

        result = agent_handler.login(email, password)

        if result["success"]:
            print(f"\n{result['message']}")
            self.current_user = result["user"]
            self.current_token = result["token"]
            print(f"Welcome back, {email}!")
            return True
        else:
            print(f"\nError: {result['message']}")
            return False

    def logout(self):
        """Log out the current user."""
        self.current_user = None
        self.current_token = None
        print("\nLogged out successfully.")

    def is_authenticated(self):
        """Check if user is authenticated."""
        if not self.current_token:
            return False

        # Verify the token is still valid
        auth_result = agent_handler.authenticate_request(self.current_token)
        return auth_result.get("authenticated", False)

    def ensure_authentication(self):
        """Ensure user is authenticated before proceeding."""
        if not self.is_authenticated():
            print("\n⚠️  Authentication required!")
            choice = input("Would you like to (l)ogin or (s)ignup? [l/s]: ").strip().lower()

            if choice == 's':
                if self.signup_flow():
                    return True
                else:
                    return False
            elif choice == 'l':
                if self.login_flow():
                    return True
                else:
                    return False
            else:
                print("Authentication required to continue.")
                return False
        return True

    def get_current_user_info(self):
        """Get current user information."""
        if self.is_authenticated():
            return self.current_user
        return None