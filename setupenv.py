import os
import subprocess

def run_passenger(port=3000):
    try:
        # Get the current script directory
        script_directory = os.path.dirname(os.path.realpath(__file__))

        # Use subprocess to run the run.py script with "python run.py"
        subprocess.run(["python", "run.py", str(port)], check=True, cwd=script_directory)
    except subprocess.CalledProcessError as e:
        print(f"Error running run.py: {e}")

if __name__ == "__main__":
    # Specify the port (optional, defaults to 3000)
    run_passenger(port=8000)
