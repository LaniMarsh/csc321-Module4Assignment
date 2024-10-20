import time
import random
import string
import pandas as pd
from Crypto.Hash import SHA256


def generateRandomString(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def hash_input(unhashed_input: str) -> str:
    hash_obj = SHA256.new()
    hash_obj.update(unhashed_input.encode('utf-8'))
    return hash_obj.hexdigest()


# trancate hash of length 64 characters to x number of bits
def truncate_hash(hashed_input: str, n: int) -> str:
    hash_int = int(hashed_input, 16)
    truncated_hash_int = hash_int >> (256 - n)
    return hex(truncated_hash_int)


entries = []

for i in range(8, 52, 2):
    print(f"Finding collision for hash truncated to {i} bits")
    hash_dict = {}
    start_time = time.time()
    while 1:
        mx = generateRandomString(10)
        hashed_mx = hash_input(mx)
        truncated_hash = truncate_hash(hashed_mx, i)

        if hash_dict.get(truncated_hash):
            end_time = time.time()
            print("Collision found!")

            cur_out = [i, mx, hash_dict[truncated_hash], truncated_hash, (end_time - start_time)]
            print("n: ", i)
            print("m1: ", hash_dict[truncated_hash])
            print("m2: ", mx)
            print("hash: ", truncated_hash)
            print("time (s): ", (end_time - start_time))

            entries.append(cur_out)

            print()

            break
        else:
            hash_dict[truncated_hash] = mx

output = pd.DataFrame(entries, columns=['n', 'm1', 'm2', 'hash', 'time (s)'])
print(output)
