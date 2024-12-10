import subprocess

from dotenv import load_dotenv
load_dotenv()

def commit_and_push_changes(abs_path_repo):
    path_distance_plot = abs_path_repo + '/data/nordic_ski_bar_chart_distance.png'
    path_elevation_plot = abs_path_repo + '/data/nordic_ski_bar_chart_elevation.png'
    
    try:
        # Add changes to git
        subprocess.run(["git", "add", path_distance_plot], check=True)
        subprocess.run(["git", "add", path_elevation_plot], check=True)

        # Commit changes
        subprocess.run(["git", "commit", "-m", "Update bar charts"], check=True)

        # Push changes
        subprocess.run(["git", "push"], check=True)  # Adjust branch name if necessary

        print("Changes pushed to GitHub successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
