import requests
import json

# Set your GitHub username here
username = 'rizitis'

# Read the token from a file
with open('.token.txt', 'r') as token_file:
    token = token_file.read().strip()  # Reads token and removes any extra spaces/newlines

# GitHub API endpoint to get all repos (with pagination)
repos_url = f'https://api.github.com/users/{username}/repos?per_page=100&page=1'
headers = {'Authorization': f'token {token}'}

# GitHub API endpoint to get user info
user_url = f'https://api.github.com/users/{username}'

# Prepare a list to store clone stats
clone_data = []

# Function to handle paginated results
def get_all_repos(url):
    repos = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            repos.extend(response.json())
            # Get the next page URL from the 'Link' header if exists
            if 'next' in response.links:
                url = response.links['next']['url']
            else:
                break
        else:
            print(f"Error fetching data: {response.status_code}")
            break
    return repos

# Fetch user info (like avatar, username)
def get_user_info():
    response = requests.get(user_url, headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        return {
            'username': user_info['login'],
            'avatar_url': user_info['avatar_url'],
            'html_url': user_info['html_url']
        }
    else:
        print(f"Error fetching user info: {response.status_code}")
        return None

# Get the user information
user_info = get_user_info()

# Get the list of all repositories
repos = get_all_repos(repos_url)

# Loop through each repository to get clone stats
for repo in repos:
    repo_name = repo['name']
    clones_url = f'https://api.github.com/repos/{username}/{repo_name}/traffic/clones'
    clones_response = requests.get(clones_url, headers=headers).json()

    # Check if the 'count' and 'uniques' keys are in the response
    if 'count' in clones_response and 'uniques' in clones_response:
        clone_count = clones_response['count']
        unique_cloners = clones_response['uniques']
        clone_data.append({
            'repo': repo_name,
            'clones': clone_count,
            'unique_cloners': unique_cloners,
            'user': user_info  # Adding user info to the repo data
        })

# Sort the repositories by the number of clones in descending order
sorted_clone_data = sorted(clone_data, key=lambda x: x['clones'], reverse=True)

# Write the results to a file (clone_stats.json)
with open('clone_stats.json', 'w') as outfile:
    json.dump(sorted_clone_data, outfile, indent=4)

# Print the sorted data to the console
print(f"Found {len(sorted_clone_data)} repositories with clone stats:")
for data in sorted_clone_data:
    print(f"Repository: {data['repo']} | Clones: {data['clones']} | Unique Cloners: {data['unique_cloners']}")

# Confirm that the JSON file has been created
print("The clone statistics have been saved to 'clone_stats.json'.")
