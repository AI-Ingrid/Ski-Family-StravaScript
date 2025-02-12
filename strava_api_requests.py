import os
import time
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
        self.token_expires_at = 0

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
            data = response.json()

            self.refresh_token = data.get('refresh_token')
            self.token_expires_at = data.get('expires_at', 0)

            print("Refresh Token obtained successfully.")
            return self.refresh_token

        except requests.exceptions.RequestException as e:
            print(f"Error obtaining refresh token: {e}")

    def get_access_token(self):
        if not self.refresh_token:
            print("Refresh token is not set. Cannot obtain access token.")
            return

        if time.time() >= self.token_expires_at:
            try:
                payload = {
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'grant_type': 'refresh_token',
                    'refresh_token': self.refresh_token
                }
                response = requests.post(self.token_url, data=payload)
                response.raise_for_status()
                data = response.json()

                self.access_token = data.get('access_token')
                self.token_expires_at = data.get('expires_at', 0)

                print("Access Token obtained successfully.")
                return self.access_token
            except requests.exceptions.RequestException as e:
                print(f"Error obtaining access token: {e}")
        else:
            print("Access token is still valid.")
            return self.access_token

    def get_club_activities_and_store_them(self, filename='data/activities.csv'):
        self.get_access_token()

        if not self.access_token:
            print("Access token is not set. Cannot fetch club activities.")
            return []

        page = 1
        all_activities = []

        while True:
            try:
                url = f'https://www.strava.com/api/v3/clubs/{self.club_id}/activities'
                params = {
                    'page': page,
                    'per_page': 100,
                    'access_token': self.access_token,
                }
                response = requests.get(url, params=params)
                response.raise_for_status()
                activities = response.json()

                if not activities:
                    print("No more activities available.")
                    break

                all_activities.extend(activities)

                page += 1

            except requests.exceptions.RequestException as e:
                print(f"Error fetching club activities: {e}")
                break

        store_activities_with_metadata(all_activities, filename=filename)
