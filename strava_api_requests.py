import os
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def store_activities(activities):
    try:
        with open('data/activities.json', 'w') as f:
            json.dump(activities, f, indent=4)
        print("Activities stored successfully.")
    except Exception as e:
        print(f"Error storing activities: {e}")


class StravaAPI:
    def __init__(self):
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.club_id = os.getenv('CLUB_ID')
        
        self.token_url = os.getenv('TOKEN_URL')
        self.auth_url = os.getenv('AUTH_URL')
        self.refresh_token = os.getenv('REFRESH_TOKEN')
        self.access_token = None

    def get_refresh_token(self):
        try:
            payload = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'code': self.authorization_code,
                'grant_type': 'authorization_code'
            }
            response = requests.post(self.token_url, data=payload)
            response.raise_for_status()
            self.refresh_token = response.json().get('refresh_token')
            print("Refresh Token obtained successfully.")
            return self.refresh_token
        except requests.exceptions.RequestException as e:
            print(f"Error obtaining refresh token: {e}")

    def get_access_token(self):
        if not self.refresh_token:
            print("Refresh token is not set. Cannot obtain access token.")
            return

        try:
            payload = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token
            }
            response = requests.post(self.token_url, data=payload)
            response.raise_for_status()
            self.access_token = response.json().get('access_token')
            print("Access Token obtained successfully.")
            return self.access_token
        except requests.exceptions.RequestException as e:
            print(f"Error obtaining access token: {e}")

    def fetch_all_club_activities(self, after, per_page=200):
        if not self.access_token:
            print("Access token is not set. Cannot fetch club activities.")
            return []

        all_activities = []
        page = 1

        while True:
            try:
                url = f'https://www.strava.com/api/v3/clubs/{self.club_id}/activities'
                params = {
                    'page': page,
                    'per_page': per_page,
                    'access_token': self.access_token,
                    'after': after
                }
                response = requests.get(url, params=params)
                response.raise_for_status()
                activities = response.json()

                if not activities:
                    print("No more activities available.")
                    break

                for activity in activities:
                    if activity not in all_activities:
                        all_activities.append(activity)

                page += 1

            except requests.exceptions.RequestException as e:
                print(f"Error fetching club activities: {e}")
                break

        return all_activities

    def save_activities_to_json(self, activities, filename):
        with open(filename, 'w') as file:
            json.dump(activities, file, indent=4)
        print(f"Activities saved to {filename}")

    def plot_activity_distances(self, activities, activity_type):
        filtered_activities = [
            activity for activity in activities if activity['type'] == activity_type
        ]
        if not filtered_activities:
            print(f"No activities found for type: {activity_type}")
            return

        # Prepare data for plotting
        distances = [activity['distance']/1000  for activity in filtered_activities]
        athletes = [activity['athlete']['firstname'] for activity in filtered_activities]

        df = pd.DataFrame({
            'Athlete': athletes,
            'Distance': distances
        })

        df = df.groupby('Athlete').sum().reset_index()

        # Plot
        plt.figure(figsize=(10, 6))
        plt.bar(df['Athlete'], df['Distance'])
        plt.title(f'{activity_type} Distances by Athlete')
        plt.xlabel('Athletes 👑')
        plt.ylabel('Distance in km')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        plt.savefig('data/nordic_ski_bar_chart.jpg')

def main():
    strava_api = StravaAPI()
    strava_api.get_access_token()

    # Fetch activities from 1st November 2024
    first_of_november = int(datetime(2024, 11, 1).timestamp())
    activities_after_october = strava_api.fetch_all_club_activities(after=first_of_november)
    strava_api.plot_activity_distances(activities_after_october, 'NordicSki')




if __name__ == '__main__':
    main()