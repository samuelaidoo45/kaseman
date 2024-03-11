import os
import sys
import subprocess

def create_flask_app(app_name):
    # Step 1: Create a new directory for the Flask app
    try:
        os.mkdir(app_name)
    except FileExistsError:
        print(f"Directory '{app_name}' already exists. Please choose a different name.")
        sys.exit(1)

    # Step 2: Change to the app directory
    os.chdir(app_name)

    # Step 3: Create a virtual environment
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)

    # Step 4: Activate the virtual environment
    activate_script = "myenv\\Scripts\\activate" if sys.platform == "win32" else "myenv/bin/activate"
    activate_command = f"{activate_script}"
    subprocess.run(activate_command, shell=True, check=True)

    # Step 5: Install Flask
    subprocess.run(["pip", "install", "Flask"], check=True)

    # Step 6: Create a minimal Flask app file
    app_code = f"""
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
"""
    with open("app.py", "w") as app_file:
        app_file.write(app_code)

    print(f"Flask app '{app_name}' has been set up successfully!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python setup_flask_app.py <app_name>")
        sys.exit(1)

    app_name = sys.argv[1]
    create_flask_app(app_name)
