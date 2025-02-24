import requests
import json
import time

# Define the range of User IDs to scan
START_USER_ID = 4211364971
END_USER_ID = 8065019393
BATCH_SIZE = 100  # Number of users per request

# Updated list of flagged words
bad_words = [
    "predator", "adult", "grooming", "inappropriate", "danger", "meet me", "private", 
    "cum", "sl0t", "fun", "rp", "studio rp", "geooan", "goon", "g00n", "go0n", "g0on", 
    "age", "13", "13yr", "furry", "fur", "inch", "tip", "slave", "master", "slut", 
    "mommy", "mummy", "mum", "dad", "daddy", "1yr", "2yr", "3yr", "4yr", "5yr", "bull", 
    "15yr", "yr"
]

# Output file for suspicious users
OUTPUT_FILE = "suspicious_users.json"

# Function to get user info from Roblox API with error handling
def get_user_info(user_ids):
    url = "https://users.roblox.com/v1/users"
    params = {"userIds": user_ids}

    while True:  # Retry if rate-limited
        response = requests.post(url, json=params)

        if response.status_code == 200:
            return response.json().get("data", [])
        elif response.status_code == 429:  # Rate limit error
            print("⚠️ Rate limited! Waiting 30 seconds before retrying...")
            time.sleep(30)  # Wait longer to avoid getting blocked
        else:
            print(f"❌ Error fetching user info: {response.status_code}")
            return []

# Load previous results if they exist
try:
    with open(OUTPUT_FILE, "r") as file:
        suspicious_users = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    suspicious_users = []

# Start scanning users in batches (NO DELAY)
for user_id in range(START_USER_ID, END_USER_ID, BATCH_SIZE):
    batch_ids = list(range(user_id, min(user_id + BATCH_SIZE, END_USER_ID)))
    print(f"🔍 Scanning User IDs: {batch_ids[0]} to {batch_ids[-1]}")

    user_data = get_user_info(batch_ids)

    for user in user_data:
        user_id = user.get("id", "Unknown")
        username = user.get("name", "Unknown")
        description = user.get("description", "").lower()

        # Check for flagged words in user descriptions
        red_flags = [word for word in bad_words if word in description]

        if red_flags:
            print(f"⚠️ Flagged User: {username} (ID: {user_id}) - Flags: {', '.join(red_flags)}")
            suspicious_users.append({
                "user_id": user_id,
                "username": username,
                "red_flags": red_flags
            })

    # Save results after each batch (FORCE SAVE)
    try:
        with open(OUTPUT_FILE, "w") as file:
            json.dump(suspicious_users, file, indent=2)
        print(f"✅ {len(suspicious_users)} suspicious users saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")

print(f"✅ Scanning complete! Total flagged users: {len(suspicious_users)}")
print(f"📂 Open {OUTPUT_FILE} to see the results.")
