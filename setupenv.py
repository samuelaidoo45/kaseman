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
    activate_script = "venv\\Scripts\\activate" if sys.platform == "win32" else "venv/bin/activate"
    activate_command = f"{activate_script}"
    subprocess.run(activate_command, shell=True, check=True)

    # Step 5: Install Flask
    subprocess.run(["pip", "install", "Flask"], check=True)

