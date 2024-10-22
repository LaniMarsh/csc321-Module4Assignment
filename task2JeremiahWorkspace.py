import random

import bcrypt
import time
import nltk
import ssl
from datetime import datetime
import numpy as np
import multiprocessing

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('words')
from nltk.corpus import words


# Function to parse a single line from the shadow file
def parse(entry):
    parts = entry.split('$')
    user = parts[0].split(':')[0]
    full_hash = '$'.join(parts[1:])  # Reconstruct the full bcrypt hash
    print(f"Parsed -> User: {user}, Full Hash: {full_hash}")
    return user, f"${full_hash}"


def crack_sublist(sublist, user, stored_hash, result, found_flag):
    print(f"Process {multiprocessing.current_process().name}: Cracking with {sublist}.")

    for i, password in enumerate(sublist):
        if i % 10 == 0:
            print(f"Attempt {i}: Trying password '{password}' with hash {stored_hash}")
            print(f"Encoded Password: {password.encode()}")
            print(f"Stored Hash: {stored_hash.encode()}")

        if bcrypt.checkpw(password.encode(), stored_hash.encode()):
            print(f"Match found for {user}: {password}")
            result.value = password
            found_flag.set()
            return
    if not found_flag.is_set():
        print(f"Process {multiprocessing.current_process().name}: Password not found in chunk {sublist}.")


# Function to attempt cracking a password
def crack_password(user, stored_hash):
    word_list = [word.lower() for word in words.words() if 6 <= len(word) <= 10]
    print(f"Loaded {len(word_list)} possible words.")

    # split list into equal chunks
    np_arr = np.array(word_list)
    sublists = np.array_split(np_arr, 26)

    manager = multiprocessing.Manager()
    result = manager.Value('s', '')  # To store the found word
    found_flag = manager.Event()

    with multiprocessing.Pool(processes=26) as pool:
        jobs = []
        for sublist in sublists:
            job = pool.apply_async(crack_sublist, (sublist, user, stored_hash, result, found_flag))
            jobs.append(job)

        # wait for all jobs
        for job in jobs:
            job.wait()

            if found_flag.is_set():
                pool.terminate()  # Stop all workers
                break

        if result.value:
            print(f"Search complete. Password '{result.value}' cracked.")
        else:
            print(f"Search complete. Password not found.")
        return result.value


if __name__ == '__main__':
    shadow_file = open('lessPasswords.txt', 'r')
    users = shadow_file.readlines()
    shadow_file.close()

    print(f"Total users to process: {len(users)}")

    for user_entry in users:
        user_entry = user_entry.strip()
        print(f"\nProcessing user entry: {user_entry}")
        print(f"\nTime started - {datetime.now()}")
        user, full_hash = parse(user_entry)

        start_time = time.time()
        password = crack_password(user, full_hash)
        end_time = time.time()

        if password:
            print(f"User: {user}, Password: {password}, Time taken: {end_time - start_time:.2f} seconds")
        else:
            print(f"User: {user}, Password not found after {end_time - start_time:.2f} seconds")
