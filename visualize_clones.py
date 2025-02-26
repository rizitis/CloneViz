import matplotlib.pyplot as plt
import seaborn as sns
import json
import requests
from PIL import Image
from io import BytesIO
import matplotlib.offsetbox as offsetbox

# Load the clone statistics from JSON file
with open('clone_stats.json', 'r') as f:
    clone_data = json.load(f)

# Get user avatar URL from the first entry (assuming all users are the same)
user_avatar_url = clone_data[0].get("user", {}).get("avatar_url", "")
user_username = clone_data[0].get("user", {}).get("username", "")

# Load the user avatar from the URL
response = requests.get(user_avatar_url)
user_avatar = Image.open(BytesIO(response.content))

# Limit to top N repositories
top_n = 8 # Chnage this to the repo number you want to appears in plot.
clone_data_sorted = sorted(clone_data, key=lambda x: x['clones'], reverse=True)[:top_n]

# Extract data for the repositories
repo_names = [data['repo'] for data in clone_data_sorted]
clones = [data['clones'] for data in clone_data_sorted]
unique_cloners = [data['unique_cloners'] for data in clone_data_sorted]

# Set seaborn theme for the plot
sns.set_theme(style="whitegrid")

# Create figure
fig, ax = plt.subplots(figsize=(14, 8))

# Plot bars for clones and unique cloners
bar_width = 0.6
ax.barh(repo_names, clones, height=bar_width, color="#1f77b4", label="Clones")
ax.barh(repo_names, unique_cloners, height=bar_width * 0.7, color="#ff7f0e", alpha=0.8, label="Unique Cloners")

# Add GitHub logo (Top-Right Corner)
github_url = "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
response = requests.get(github_url)
github_icon = Image.open(BytesIO(response.content))
github_imagebox = offsetbox.AnnotationBbox(
    offsetbox.OffsetImage(github_icon, zoom=0.06), (0.92, 1.05), xycoords='axes fraction', frameon=False)
ax.add_artist(github_imagebox)

# Add user avatar to the top-left corner
if user_avatar_url:
    user_avatar_box = offsetbox.AnnotationBbox(
        offsetbox.OffsetImage(user_avatar, zoom=0.1), (-0.05, 1.05), xycoords='axes fraction', frameon=False)
    ax.add_artist(user_avatar_box)

# Labels and Title
ax.set_xlabel("Number of Clones", fontsize=14, fontweight="bold")
ax.set_title(f"Top Repositories by Clone Count - {user_username}", fontsize=16, fontweight="bold", pad=15)
ax.set_yticks(range(len(repo_names)))
ax.set_yticklabels(repo_names, fontsize=12)

# Grid, legend, and layout
ax.legend(fontsize=12)
ax.grid(axis="x", linestyle="--", alpha=0.6)
plt.tight_layout()

# Show the plot
plt.show()
