import csv
import pandas as pd

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def plot_activity_charts(activities, activity_type, medal_images, abs_path):
    print(f"-- Plotting charts for activity type: {activity_type} --")
    filtered_activities = [
        activity for activity in activities if activity['type'] == activity_type
    ]
    if not filtered_activities:
        print(f"No activities found for type: {activity_type}")
        return

    # Prepare data for plotting
    distances = [float(activity['distance']) / 1000 for activity in filtered_activities]
    elevations = [float(activity['elevation_gain']) for activity in filtered_activities]
    athletes = [(activity['athlete_name'] + " " + activity['athlete_lastname']) for activity in filtered_activities]

    df_distance = pd.DataFrame({
        'Athlete': athletes,
        'Distance': distances
    })

    df_elevation = pd.DataFrame({
        'Athlete': athletes,
        'Elevation': elevations
    })

    df_distance = df_distance.groupby('Athlete').sum().reset_index()
    df_elevation = df_elevation.groupby('Athlete').sum().reset_index()

    # Sort the DataFrame by Distance/Elevation in descending order
    df_distance = df_distance.sort_values(by='Distance', ascending=False).reset_index(drop=True)
    df_elevation = df_elevation.sort_values(by='Elevation', ascending=False).reset_index(drop=True)

    color_distance = '#4682B4'
    color_elevation = '#5F9EA0'

    # -- Plot distance --
    plt.figure(figsize=(12, 8))
    bars = plt.bar(df_distance['Athlete'], df_distance['Distance'], color=color_distance)

    # Add images above each bar according to rank
    for i, (bar, medal_image) in enumerate(zip(bars, medal_images)):
        yval = bar.get_height()
        img = plt.imread(medal_image)
        imagebox = OffsetImage(img, zoom=0.2)  # Adjust zoom to scale the image appropriately
        ab = AnnotationBbox(imagebox, (bar.get_x() + bar.get_width() / 2, yval + 1.0), frameon=False)  # Adjusted y-position
        plt.gca().add_artist(ab)

    plt.title('Oversikt over km tilbakelagt per familiemedlem', fontsize=16)
    plt.xlabel('Familiemedlemmer', fontsize=12)
    plt.ylabel('km', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(abs_path + '/data/nordic_ski_bar_chart_distance.png')
    plt.close()

    # -- Plot elevation --
    plt.figure(figsize=(12, 8))
    bars = plt.bar(df_elevation['Athlete'], df_elevation['Elevation'], color=color_elevation)

    # Add images above each bar according to rank
    for i, (bar, medal_image) in enumerate(zip(bars, medal_images)):
        yval = bar.get_height()
        img = plt.imread(medal_image)
        imagebox = OffsetImage(img, zoom=0.2)  # Adjust zoom to scale the image appropriately
        ab = AnnotationBbox(imagebox, (bar.get_x() + bar.get_width() / 2, yval + 1.0), frameon=False)  # Adjusted y-position
        plt.gca().add_artist(ab)

    plt.title('Oversikt over høydemetere', fontsize=16)
    plt.xlabel('Familiemedlemmer', fontsize=12)
    plt.ylabel('meter', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(abs_path + '/data/nordic_ski_bar_chart_elevation.png')
    plt.close()


def store_activities_with_metadata(new_activities, page, last_activity_number, filename='data/activities.csv'):
    try:
        # Define the CSV column headers including page and activity number
        headers = ['page', 'activity_number', 'athlete_name', 'athlete_lastname' ,'distance', 'type', 'elevation_gain']

        # Open the file in append mode to add new data without overwriting
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)

            # Write the headers if the file is empty
            if file.tell() == 0:
                writer.writeheader()

            # Write each activity with additional metadata
            for activity in new_activities:
                last_activity_number += 1
                athlete_name = activity.get('athlete', {}).get('firstname', 'Unknown')
                athlete_lastname = activity.get('athlete', {}).get('lastname', 'Unknown')
                distance = activity.get('distance', 0.0)
                type = activity.get('type', 'Unknown')
                elevation_gain = activity.get('total_elevation_gain', 0.0)

                writer.writerow({
                    'page': page,
                    'activity_number': last_activity_number,
                    'athlete_name': athlete_name,
                    'athlete_lastname': athlete_lastname,
                    'distance': distance,
                    'type': type,
                    'elevation_gain': elevation_gain,
                })

        print(f"Activities from page {page} successfully stored in {filename}.")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")


def get_page_and_last_activity_number(filename='data/activities.csv'):
    # Open the CSV file in read mode
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            last_row = None

            # Iterate over the rows to find the last one
            for row in reader:
                last_row = row

            if last_row:
                # Extract the page and activity number from the last row
                last_page = int(last_row['page'])
                last_activity_number = int(last_row['activity_number'])
                return last_page, last_activity_number
            else:
                # If the file is empty, return starting defaults
                return 1, -1
    except FileNotFoundError:
        print(f"File {filename} not found. Starting from the beginning.")
        return 1, -1
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")
        return 1, -1


def get_all_stored_activities(filename='data/activities.csv'):
    activities = []
    try:
        # Open the CSV file in read mode
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Iterate over each row and add it to the activities list
            for row in reader:
                activities.append(row)

    except FileNotFoundError:
        print(f"File {filename} not found. No activities to return.")
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")

    return activities