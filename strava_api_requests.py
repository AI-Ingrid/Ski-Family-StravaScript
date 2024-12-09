import os
import json
import requests

from utils import store_activities_with_metadata
from dotenv import load_dotenv
load_dotenv()


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

    def get_new_club_activities_and_store_them(self, after, per_page=200, page=1, last_activity_number=0, filename='data/activities.csv'):
        if not self.access_token:
            print("Access token is not set. Cannot fetch club activities.")
            return []

        all_activities = []

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

                for activity in activities[last_activity_number:]:
                    if activity not in all_activities:
                        all_activities.append(activity)
                
                store_activities_with_metadata(activities[last_activity_number:], page, last_activity_number, filename=filename)
                last_activity_number += len(activities[last_activity_number:])

                if last_activity_number < (200 * page):
                    break

                page += 1

            except requests.exceptions.RequestException as e:
                print(f"Error fetching club activities: {e}")
                break

