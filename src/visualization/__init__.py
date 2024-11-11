import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Define the tasks and their durations (in days)
tasks = [
    {"Task": "Data Collection", "Start": "2024-09-01", "End": "2024-09-05"},
    {"Task": "Feature Engineering", "Start": "2024-09-06", "End": "2024-09-10"},
    {"Task": "Clustering", "Start": "2024-09-11", "End": "2024-09-15"},
    {"Task": "Model Training", "Start": "2024-09-16", "End": "2024-09-20"},
    {"Task": "Model Evaluation", "Start": "2024-09-21", "End": "2024-09-25"},
    {"Task": "Repetition Counting", "Start": "2024-10-01", "End": "2024-10-25"}
]

# Convert the date strings to datetime objects
for task in tasks:
    task["Start"] = datetime.strptime(task["Start"], "%Y-%m-%d")
    task["End"] = datetime.strptime(task["End"], "%Y-%m-%d")

# Create a figure and axis with a larger size and customized background
fig, ax = plt.subplots(figsize=(12, 6), facecolor='#f7f7f7')  # Set the background of the figure to light gray

# Set gridlines for better visibility
ax.grid(True, axis='x', linestyle='--', color='gray', alpha=0.5)

# Plot the Gantt chart with better color and style
for i, task in enumerate(tasks):
    ax.barh(i, (task["End"] - task["Start"]).days, left=task["Start"], height=0.6, 
            color='#3B9E9F', edgecolor='black', linewidth=1.2, zorder=10)  # Stylish bar color
    ax.text(task["Start"] + timedelta(days=(task["End"] - task["Start"]).days / 2), i, task["Task"],
            ha='center', va='center', color='white', fontweight='bold', fontsize=10, zorder=20)

# Set labels and title with improved fonts
ax.set_xlabel('Timeline', fontsize=12, fontweight='bold', color='#333333')  # Darker text color
ax.set_ylabel('Tasks', fontsize=12, fontweight='bold', color='#333333')
ax.set_title('Project Gantt Chart: Strength Training Context-Aware System', fontsize=14, fontweight='bold', color='#333333')

# Format the x-axis with dates and improve appearance
ax.xaxis.set_major_locator(mdates.WeekdayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %Y'))
plt.xticks(rotation=45, fontsize=10, ha='right', color='#333333')  # Dark text color for x-axis
plt.yticks(fontsize=10, color='#333333')

# Add a background color for the plot area
ax.set_facecolor('#ffffff')  # White background for the plot area

# Improve layout and make sure everything fits
plt.tight_layout()

# Show the Gantt chart
plt.show()