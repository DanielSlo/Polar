
import os
import time


CACHE_DIR = "caches"
def remove_duplicates():
    # Get all cache files
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    
    cache_files = os.listdir(CACHE_DIR)

    # Create a set to store unique user IDs
    unique_users = set()

    # Iterate over cache files
    for filename in cache_files:
        filepath = os.path.join(CACHE_DIR, filename)
        with open(filepath, 'r') as file:
            # Read the user ID from the cache file
            user_id = file.readline().strip()

            # Check if the user ID is already in the set
            if user_id in unique_users:
                # Remove the duplicate cache file
                os.remove(filepath)
            else:
                # Add the user ID to the set
                unique_users.add(user_id)
            
CACHE_LIFETIME_SECONDS = 43200  # 12 hours
MAX_CACHE_SIZE_BYTES = 1073741824  # 1 GB


def cleanup_cache():
    while True:
        try:
            # Get the current time
            current_time = time.time()

            # Iterate over files in the cache directory
            for filename in os.listdir(CACHE_DIR):
                filepath = os.path.join(CACHE_DIR, filename)

                # Get the modification time of the file
                modification_time = os.path.getmtime(filepath)

                # Check if the file is older than the cache lifetime
                if current_time - modification_time > CACHE_LIFETIME_SECONDS:
                    os.remove(filepath)

            # Check the total size of the cache directory
            total_size = sum(os.path.getsize(os.path.join(CACHE_DIR, f)) for f in os.listdir(CACHE_DIR))
            if total_size > MAX_CACHE_SIZE_BYTES:
                # Delete the oldest cache file
                oldest_file = min(os.listdir(CACHE_DIR), key=lambda f: os.path.getmtime(os.path.join(CACHE_DIR, f)))
                os.remove(os.path.join(CACHE_DIR, oldest_file))
        except FileNotFoundError:
            # Cache directory is empty, continue without deleting files
            pass

        # Sleep for some time before checking again
        # time.sleep(3600)  # Check every hour
        time.sleep(1800)  # Check every half hour