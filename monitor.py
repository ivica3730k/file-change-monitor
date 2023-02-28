import os
import hashlib
import json
import time

# Set the folder path to monitor, it is path to this file with the folder name appended
folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'watched_folder')

# Create a dictionary to store the file hashes
file_hashes = {}

# Load the file hashes from a JSON file if it exists
if os.path.exists('file_hashes.json'):
    with open('file_hashes.json', 'r') as f:
        file_hashes = json.load(f)

# Main loop to monitor the folder for changes
while True:
    # Traverse the directory tree and get a list of all the files
    seen_files = set()
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            # Check if the file is new or already seen before
            if file_path not in file_hashes:
                # Calculate the hash of the file
                file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()

                # Update the file hash dictionary
                file_hashes[file_path] = file_hash

                # Print a message indicating that the file is new
                print(f'New file detected: {file_path}')

            else:
                # Calculate the hash of the file
                file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()

                # Check if the file hash has changed
                if file_hashes[file_path] != file_hash:
                    # Update the file hash dictionary
                    file_hashes[file_path] = file_hash

                    # Print a message indicating that the file hash has changed
                    print(f'File {file_path} has changed. New hash: {file_hash}')

            # Add the file to the set of seen files
            seen_files.add(file_path)

    # Check for files that have been removed
    removed_files = set(file_hashes.keys()) - seen_files
    for file in removed_files:
        print(f'File {file} has been removed.')
        del file_hashes[file]

    # Save the file hash dictionary to a JSON file
    with open('file_hashes.json', 'w') as f:
        json.dump(file_hashes, f)

    # Wait for 1 second before checking again
    time.sleep(1)
