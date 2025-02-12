import os
import subprocess
from datetime import datetime
from strava_api_requests import StravaAPI
from utils import plot_activity_charts, get_page_and_last_activity_number, get_all_stored_activities
from push_to_github import commit_and_push_changes

def connect_to_strava_api():
    print(" -- Connecting to Strava API... --")
    strava_api = StravaAPI()
    strava_api.get_access_token()
    return strava_api

def fetch_activities_after_date(strava_api, path_to_activity_data):
    print(" -- Fetching activities... --")
    strava_api.get_club_activities_and_store_them(filename=path_to_activity_data)

    all_activities = get_all_stored_activities(filename=path_to_activity_data)
    return all_activities

def get_emoji_images(abs_path):
    emoji_files = ['emojis/1st-place.png', 'emojis/2nd-place.png', 'emojis/3rd-place.png',
                   'emojis/troll.png', 'emojis/troll.png', 'emojis/troll.png', 'emojis/troll.png']

    # Prepend abs_path to each file name
    return [f"{abs_path}/{emoji}" for emoji in emoji_files]


def update_last_updated_time(last_updated_path, current_time=None):
    with open(last_updated_path, 'w') as file:
        file.write(current_time)


def update_readme_with_last_updated_time(abs_path_repo, path_to_last_updated_time):
    print(" -- Updating README.md with last updated time... --")
    readme_path = os.path.join(abs_path_repo, 'README.md')
    last_updated_time = datetime.now().strftime('Updated on %B %d, %Y at %I:%M %p')
    update_last_updated_time(path_to_last_updated_time, last_updated_time)

    with open(readme_path, 'r') as file:
        lines = file.readlines()

    # Update the last line with the current date and time
    lines[-1] = f"_{last_updated_time}_\n"

    with open(readme_path, 'w') as file:
        file.writelines(lines)


def start_ssh_agent(abs_repo_path):
    print(" -- Starting SSH agent... --")
    script_path = abs_repo_path + '/start_ssh_agent.sh'
    env_path = abs_repo_path + '/.env'
    subprocess.run([script_path, env_path], check=True)


def main():
    strava_api = connect_to_strava_api()

    abs_path = os.getenv('ABS_PATH_REPO')
    path_to_activity_data = abs_path + '/data/activities.csv'
    path_to_last_updated_time = abs_path + '/data/last_updated.txt'

    activities = fetch_activities_after_date(strava_api, path_to_activity_data)

    if activities:
        emoji_images = get_emoji_images(abs_path)
        plot_activity_charts(activities, 'NordicSki', emoji_images, abs_path)
        update_readme_with_last_updated_time(abs_path, path_to_last_updated_time)
        start_ssh_agent(abs_path)
        commit_and_push_changes(abs_path)

    print(" -- Process finished --")

if __name__ == '__main__':
    main()
