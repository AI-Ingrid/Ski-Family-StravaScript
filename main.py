import os
from datetime import datetime
from strava_api_requests import StravaAPI
from utils import plot_activity_charts, get_page_and_last_activity_number, get_all_stored_activities
from push_to_github import commit_and_push_changes

def connect_to_strava_api():
    strava_api = StravaAPI()
    strava_api.get_access_token()
    return strava_api

def fetch_activities_after_date(date, strava_api, path_to_activity_data):
    last_page, last_activity_number = get_page_and_last_activity_number(filename=path_to_activity_data)
    strava_api.get_new_club_activities_and_store_them(after=date,
                                                      page=last_page,
                                                      last_activity_number=last_activity_number,
                                                      filename=path_to_activity_data)

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
    readme_path = os.path.join(abs_path_repo, 'README.md')
    last_updated_time = datetime.now().strftime('Updated on %B %d, %Y at %I:%M %p')
    update_last_updated_time(path_to_last_updated_time, last_updated_time)

    with open(readme_path, 'r') as file:
        lines = file.readlines()

    # Update the last line with the current date and time
    lines[-1] = f"_{last_updated_time}_\n"

    with open(readme_path, 'w') as file:
        file.writelines(lines)


def main():
    strava_api = connect_to_strava_api()

    first_of_november = int(datetime(2024, 11, 1).timestamp())

    abs_path = os.getenv('ABS_PATH_REPO')
    path_to_activity_data = abs_path + '/data/activities.csv'
    path_to_last_updated_time = abs_path + '/data/last_updated.txt'

    activities = fetch_activities_after_date(first_of_november, strava_api, path_to_activity_data)

    if activities:
        emoji_images = get_emoji_images(abs_path)
        plot_activity_charts(activities, 'NordicSki', emoji_images, abs_path)
        update_readme_with_last_updated_time(abs_path, path_to_last_updated_time)
        commit_and_push_changes(abs_path)

if __name__ == '__main__':
    main()
