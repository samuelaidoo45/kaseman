import os
import subprocess

# Replace the path with your virtual environment activation script path
virtualenv_activation_script = "/home/tivateo2/app.tivateonline.com/loanreport/myenv/bin/activate"

# Replace the path with your desired directory
target_directory = "/home/tivateo2/app.tivateonline.com/loanreport"

def activate_virtualenv_and_change_directory(virtualenv_activation_script, target_directory):
    # Activate the virtual environment
    activate_command = f"source {virtualenv_activation_script} && cd {target_directory}"
    
    # Run the activation commands using subprocess
    subprocess.run(activate_command, shell=True)

if __name__ == "__main__":
    activate_virtualenv_and_change_directory(virtualenv_activation_script, target_directory)
