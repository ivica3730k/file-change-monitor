import os
import hashlib
import redis
import time

# Set the folder path to monitor, it is path to this file with the folder name appended
folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'watched_folder')

# Create a Redis client
redis_client = redis.Redis(host='192.168.106.2', port=30000)

# Main loop to monitor the folder for changes
while True:
    # Traverse the directory tree and get a list of all the files
    seen_files = set()
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Calculate the hash of the file
            file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
            
            # Check if the file hash has changed or if the file is new
            key = f"file_hashes:{file_path}"
            if not redis_client.exists(key):
                # The file is new
                redis_client.set(key, file_hash)
                print(f'New file {file_path} added. Hash: {file_hash}')
            elif redis_client.get(key).decode() != file_hash:
                # The file has changed
                redis_client.set(key, file_hash)
                print(f'File {file_path} has changed. New hash: {file_hash}')
                
            # Add the file to the set of seen files
            seen_files.add(file_path)
    
    # Check for files that have been removed
    for key in redis_client.scan_iter('file_hashes:*'):
        file_path = key.decode().replace('file_hashes:', '', 1)
        if file_path not in seen_files:
            print(f'File {file_path} has been removed.')
            redis_client.delete(key)
    
    # Wait for 1 second before checking again
    time.sleep(1)
