import bcrypt
import time
import nltk
import ssl
from datetime import datetime

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


# Function to attempt cracking a password
def crack_password(user, stored_hash):
    print(f"Cracking password for {user} with hash {stored_hash}")
    word_list = [word.lower() for word in words.words() if 6 <= len(word) <= 10]
    print(f"Loaded {len(word_list)} possible words.")

    for i, password in enumerate(word_list):
        if i % 1000 == 0:
            print(f"Attempt {i}: Trying password '{password.encode()}' with hash {stored_hash}")

        hashed = bcrypt.hashpw(password.encode(), stored_hash.encode())
        # # Check if the hash matches
        # if hashed.decode().split('$')[-1] == stored_hash:
        #     print(f"Match found for {user}: {password}")
        #     return password

        if i % 1000 == 0:
            print(f"Attempt {i}: Trying password '{password}'")
            print(f"Encoded Password: {password.encode()}")
            print(f"Stored Hash: {stored_hash.encode()}")

        if bcrypt.checkpw(password.encode(), stored_hash.encode()):
            print(f"Match found for {user}: {password}")
            return password

        # # Use bcrypt.checkpw to check if the password matches the stored hash
        # if bcrypt.checkpw(password.encode(), stored_hash.encode()):
        #     print(f"Match found for {user}: {password}")
        #     return password

        # if hashed == stored_hash:
        #     print(f"Match found for {user}: {password}")
        #     return password

    print(f"No match found for {user}.")
    return None


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
