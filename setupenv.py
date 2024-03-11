import os
import subprocess

def run_passenger(port=3000):
    try:
        # Get the current script directory
        script_directory = os.path.dirname(os.path.realpath(__file__))

        # Activate the existing virtual environment named 'myenv'
        venv_path = os.path.join(script_directory, 'myenv')
        activate_script = os.path.join(venv_path, 'bin', 'activate') if os.name == 'posix' else os.path.join(venv_path, 'Scripts', 'activate.bat')
        activate_command = f'source {activate_script}' if os.name == 'posix' else f'. {activate_script}'
        subprocess.run(activate_command, shell=True, check=True)

        # Install Flask (if needed, you can skip this step if Flask is already installed in your 'myenv')
        # subprocess.run(['pip', 'install', 'flask'], check=True)

        # Run the run.py script with "python run.py"
        subprocess.run(['python', 'run.py', str(port)], check=True, cwd=script_directory)

    except subprocess.CalledProcessError as e:
        print(f"Error running run.py: {e}")

if __name__ == "__main__":
    # Specify the port (optional, defaults to 3000)
    run_passenger(port=8000)
