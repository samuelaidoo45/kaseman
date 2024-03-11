import subprocess

def run_passenger(app_script, port=3000):
    try:
        # Use subprocess to run the app.py script with the built-in Python HTTP server
        subprocess.run(["python", "-m", "http.server", str(port)], check=True, cwd=app_script)
    except subprocess.CalledProcessError as e:
        print(f"Error running app.py: {e}")

if __name__ == "__main__":
    # Replace with the actual path to your app.py script
    app_script_path = "./run.py"

    # Specify the port (optional, defaults to 3000)
    run_passenger(app_script_path, port=8000)
