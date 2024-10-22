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

    # Match found for Bilbo: welcome
    # User: Bilbo, Password: welcome, Time taken: 2344.64 seconds
    # Match found for Gandalf: wizard
    # User: Gandalf, Password: wizard, Time taken: 7495.38 seconds
    # Match found for Thorin: diamond
    # User: Thorin, Password: diamond, Time taken: 2344.04 seconds
    # Match found for Fili: desire
    # User: Fili, Password: desire, Time taken: 1880.71 seconds
    # Match found for Kili: ossify
    # User: Kili, Password: ossify, Time taken: 2725.14 seconds
    # Match found for Balin: hangout
    # User: Balin, Password: hangout, Time taken: 13274.77 seconds
    # Match found for Dwalin: drossy
    # User: Dwalin, Password: drossy, Time taken: 2730.43 seconds
    # Match found for Oin: ispaghul
    # User: Oin, Password: ispaghul, Time taken: 6315.32 seconds
    # Match found for Gloin: oversave
    # User: Gloin, Password: oversave, Time taken: 12465.40 seconds
    # Match found for Dori: indoxylic
    # User: Dori, Password: indoxylic, Time taken: 10288.76 seconds
    # Match found for Nori: swagsman
    # User: Nori, Password: swagsman, Time taken: 63603.55 seconds
    # Match found for Ori: airway
    # User: Ori, Password: airway, Time taken: 9261.85 seconds
    # Match found for Bifur: corrosible
    # User: Bifur, Password: corrosible, Time taken: 8044.68 seconds
    # Match found for Bofur: libellate
    # User: Bofur, Password: libellate, Time taken: 6359.91 seconds
    # Match found for Durin: purrone
    # User: Durin, Password: purrone, Time taken: 51000 seconds


    for i, password in enumerate(word_list[60000:], start=60000):
        if i % 10000 == 0:
            print(f"Attempt {i}: Trying password '{password}'")
            print(f"Encoded Password: {password.encode()}")
            print(f"Stored Hash: {stored_hash.encode()}")

        if bcrypt.checkpw(password.encode(), stored_hash.encode()):
            print(f"Match found for {user}: {password}")
            return password

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
