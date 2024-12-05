import json
import pandas as pd
import matplotlib.pyplot as plt

def plot_activity_distances(activities, activity_type):
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
    plt.savefig('data/nordic_ski_bar_chart.png')
    plt.show()


def store_activities(activities):
    try:
        with open('data/activities.json', 'w') as f:
            json.dump(activities, f, indent=4)
        print("Activities stored successfully.")
    except Exception as e:
        print(f"Error storing activities: {e}")

