import os
import subprocess

from dotenv import load_dotenv
load_dotenv()

def commit_and_push_changes(abs_path_repo):
    print(" -- Committing and pushing changes to GitHub... --")
    path_distance_plot = os.path.join(abs_path_repo, 'data/nordic_ski_bar_chart_distance.png')
    path_elevation_plot = os.path.join(abs_path_repo, 'data/nordic_ski_bar_chart_elevation.png')
    path_to_readme = os.path.join(abs_path_repo, 'README.md')
    path_to_last_updated = os.path.join(abs_path_repo, 'data/last_updated.txt')

    try:
        # Change the working directory to the repository path
        os.chdir(abs_path_repo)

        # Add changes to git
        subprocess.run(["git", "add", path_distance_plot, path_elevation_plot, path_to_readme, path_to_last_updated], check=True)

        # Commit changes
        subprocess.run(["git", "commit", "-m", "Update bar charts"], check=True)

        # Push changes
        subprocess.run(["git", "push"], check=True)

        print("Changes pushed to GitHub successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
