from backend.main import app

print("Registered Routes:")
for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        print(f"{route.methods} {route.path}")
    elif hasattr(route, 'path'):
        print(f"GET/POST/PUT/DELETE/PATCH {route.path}")