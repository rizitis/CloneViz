import matplotlib.pyplot as plt
import json

# Load the clone statistics from the 'clone_stats.json' file
with open('clone_stats.json', 'r') as f:
    clone_data = json.load(f)

# Extract repository names, clone counts, and unique cloners for visualization
repo_names = [data['repo'] for data in clone_data]
clones = [data['clones'] for data in clone_data]
unique_cloners = [data['unique_cloners'] for data in clone_data]

# Limit the length of repository names if they are too long (optional)
max_name_length = 40
repo_names = [name if len(name) <= max_name_length else name[:max_name_length] + "..." for name in repo_names]

# Limit the number of repositories shown (optional)
top_n = 20  # Adjust this number based on how many repos you want to display
clone_data_sorted = sorted(clone_data, key=lambda x: x['clones'], reverse=True)[:top_n]

repo_names = [data['repo'] for data in clone_data_sorted]
clones = [data['clones'] for data in clone_data_sorted]
unique_cloners = [data['unique_cloners'] for data in clone_data_sorted]

# Create a figure and axis for the plot
plt.figure(figsize=(14, 10))  # Increase the figure size for better readability

# Create a horizontal bar chart for clones
plt.barh(repo_names, clones, color='skyblue', label='Clones')

# Add labels and title
plt.xlabel('Number of Clones')
plt.title('Top Repositories by Clone Count')

# Add another horizontal bar for unique cloners
plt.barh(repo_names, unique_cloners, color='salmon', alpha=0.6, label='Unique Cloners')

# Add legend
plt.legend()

# Adjust layout for better spacing
plt.tight_layout()

# Display the plot with proper space
plt.show()
