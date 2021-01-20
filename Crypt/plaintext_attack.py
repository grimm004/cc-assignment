import itertools
import subprocess
import os
import tqdm
import threading


def encrypt_hex_string(hex_string: str) -> str:
    return subprocess \
        .run(f"{os.path.dirname(os.path.realpath(__file__))}\\encrypt.exe {hex_string}",
             stdout=subprocess.PIPE) \
        .stdout.strip().decode("utf-8")


def encrypt_string(string: str) -> str:
    return encrypt_hex_string("".join("{:02x}".format(ord(c)) for c in string))


if __name__ == "__main__":
    with open("words.txt", "rt") as words_file:
        words = [word.replace("\n", "") for word in words_file.readlines() if 4 <= len(word) - 1 <= 6]

    assert "tile" in words
    assert "bills" in words
    assert "print" in words

    print(f"Running on {len(words)} words.")

    target_ciphertext = "903408ec4d951acfaeb47ca88390c475"

    def clear_buffer(buffer_copy):
        encrypted_buffer = encrypt_string("".join(buffer_copy))
        if target_ciphertext in encrypted_buffer:
            i = encrypted_buffer.index(target_ciphertext)
            print(f"Found {target_ciphertext} at index {i} corresponding to plaintext \"{buffer_copy[i // 32]}\"")
            exit(0)

    buffer = []

    threads = []

    for permutation in tqdm.tqdm(itertools.product(words, repeat=3), total=len(words)**3):
        plaintext = ".".join(permutation)
        if len(plaintext) == 16:
            buffer.append(plaintext)

        if len(buffer) == 1020:
            thread = threading.Thread(target=clear_buffer, args=[buffer.copy()])
            threads.append(thread)
            thread.start()

    thread = threading.Thread(target=clear_buffer, args=[buffer.copy()])
    threads.append(thread)
    thread.start()

    for thread in threads:
        thread.join()
