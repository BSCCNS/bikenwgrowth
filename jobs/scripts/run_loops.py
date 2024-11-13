import subprocess

def run_script(script_name):
    try:
        # Execute the script
        subprocess.run(['python', script_name], check=True)
        print(f"{script_name} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing {script_name}: {e}")

if __name__ == "__main__":
    # List of scripts to run
    scripts = ['downloadloop.py','analysisloop.py']
    
    for script in scripts:
        run_script(script)
