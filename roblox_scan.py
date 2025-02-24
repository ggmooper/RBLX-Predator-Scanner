import requests
import json
import time

# List of words to scan for in user profiles
bad_words = ["predator", "adult", "grooming", "inappropriate", "danger", "meet me", "private", "cum", "sl0t", "fun", "rp", "studio rp", "geooan", "goon", "g00n", "go0n", "g0on", "age", "13", "13yr", "furry", "fur", "inch", "tip", "slave", "master", "slut", "mommy", "mummy", "mum", "dad", "daddy", "1yr", "2yr", "3yr", "4yr", "5yr", "bull", "15yr", "yr"]

# Function to fetch user info from Roblox API
def get_user_info(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()  # Return the user data
    else:
        print(f"Failed to retrieve data for user {user_id}. Status code: {response.status_code}")
        return None

# Function to analyze user data for red flags (including scanning for bad words)
def analyze_user(user_info):
    red_flags = []

    # Get the bio, default to empty string if not available
    bio = user_info.get("description", "")

    # Check the bio for any flagged words
    for word in bad_words:
        if word.lower() in bio.lower():
            red_flags.append(f"Contains flagged word: {word}")

    # Add more analysis checks here as needed...

    return red_flags

# Define the range of user IDs to check
start_user_id = 3409340668
end_user_id = 7966088193

# List to hold suspicious users
suspicious_users = []

print(f"Checking users from {start_user_id} to {end_user_id}...")

# Loop through the range of user IDs
for user_id in range(start_user_id, end_user_id + 1):
    print(f"Processing user {user_id}...")
    
    user_info = get_user_info(user_id)  # Fetch user info

    if user_info:  # If user info is found
        print(f"User found: {user_info['name']}")
        # Call analyze_user() to check for red flags
        red_flags = analyze_user(user_info)

        if red_flags:
            suspicious_users.append({
                'user_id': user_id,
                'username': user_info['name'],
                'red_flags': red_flags
            })

    # Add delay between requests to avoid hitting API limits
    time.sleep(000.00001)  # 1 second delay between requests

# After checking all users, save suspicious users to a file
with open("suspicious_users.json", "w") as file:
    json.dump(suspicious_users, file, indent=2)

print("Finished processing all users.")
