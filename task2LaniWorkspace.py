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

def parse(entry):
    parts = entry.split('$')
    user = parts[0].split(':')[0]
    full_hash = '$'.join(parts[1:])
    print(f"Parsed -> User: {user}, Full Hash: {full_hash}")
    return user, f"${full_hash}"

def crack_password(user, stored_hash):
    print(f"Cracking password for {user} with hash {stored_hash}")
    word_list = [word.lower() for word in words.words() if 6 <= len(word) <= 10]
    print(f"Loaded {len(word_list)} possible words.")

    for i, password in enumerate(word_list):
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

        # User: Bilbo, Password: welcome, Time taken: 2344.64 seconds
        # User: Gandalf, Password: wizard, Time taken: 7495.38 seconds
        # User: Thorin, Password: diamond, Time taken: 2344.04 seconds
        # User: Fili, Password: desire, Time taken: 1880.71 seconds
        # User: Kili, Password: ossify, Time taken: 2725.14 seconds
        # User: Balin, Password: hangout, Time taken: 13274.77 seconds
        # User: Dwalin, Password: drossy, Time taken: 2730.43 seconds
        # User: Oin, Password: ispaghul, Time taken: 6315.32 seconds
        # User: Gloin, Password: oversave, Time taken: 12465.40 seconds
        # User: Dori, Password: indoxylic, Time taken: 10288.76 seconds
        # User: Nori, Password: swagsman, Time taken: 63603.55 seconds
        # User: Ori, Password: airway, Time taken: 9261.85 seconds
        # User: Bifur, Password: corrosible, Time taken: 8044.68 seconds
        # User: Bofur, Password: libellate, Time taken: 6359.91 seconds
        # User: Durin, Password: purrone, Time taken: 51000 seconds
