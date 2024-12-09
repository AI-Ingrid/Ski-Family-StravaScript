import os
import subprocess

from dotenv import load_dotenv
load_dotenv()

def commit_and_push_changes():
    abs_path_repo = os.getenv('ABS_PATH_REPO')
    
    try:
        os.chdir(abs_path_repo) 

        # Add changes to git
        subprocess.run(["git", "add", "data/nordic_ski_bar_chart_distance.png"], check=True)
        subprocess.run(["git", "add", "data/nordic_ski_bar_chart_elevation.png"], check=True)

        # Commit changes
        subprocess.run(["git", "commit", "-m", "Update bar charts"], check=True)

        # Push changes
        subprocess.run(["git", "push"], check=True)  # Adjust branch name if necessary

        print("Changes pushed to GitHub successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
