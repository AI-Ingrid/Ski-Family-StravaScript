from datetime import datetime
from strava_api_requests import StravaAPI
from utils import plot_activity_distances
from sync_to_github import commit_and_push_changes

def connect_to_strava_api():
    strava_api = StravaAPI()
    strava_api.get_access_token()
    return strava_api

def fetch_activities_after_date(strava_api, date):
    activities_after_date = strava_api.fetch_all_club_activities(after=date)
    return activities_after_date


def main():
    strava_api = connect_to_strava_api()

    #first_of_november = int(datetime(2024, 11, 1).timestamp())
    #activities = fetch_activities_after_date(strava_api, first_of_november)

    #plot_activity_distances(activities, 'NordicSki')

    # Commit and push changes
    commit_and_push_changes()

if __name__ == '__main__':
    main()
