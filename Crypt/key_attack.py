import sys
import subprocess
import os
import des
import itertools
import string
from concurrent import futures
from des import DesKey

# def encrypt_hex_string(hex_string: str) -> str:
#     return subprocess \
#         .run(f"{os.path.dirname(os.path.realpath(__file__))}\\encrypt.exe \"{hex_string}\"",
#              stdout=subprocess.PIPE) \
#         .stdout.strip().decode("utf-8")
#
#
# def encrypt_string(string: str) -> str:
#     return encrypt_hex_string("".join("{:02x}".format(ord(c)) for c in string))
#
#
# def split_string(string: str, n: int, gap: str = " ", transform=lambda s: s) -> str:
#     return gap.join([transform(string[i:i+n]) for i in range(0, len(string), n)])
#
#
# def format_encrypted_string(string: str) -> str:
#     return split_string(string, 16, transform=lambda s: split_string(s, 2, "-"))
#
#
# def evaluate(comb, target):
#     encoded = "".join(comb).encode("utf-8")
#     key = des.DesKey(encoded)
#
#     encrypted = key.encrypt(b"aaaaaaaa")
#
#     if encrypted == target:
#         print(f"Found plaintext key: {comb}, {encoded}")
#         exit(0)
#
#     return encrypted


if __name__ == "__main__":
    def main() -> int:
        plaintext = "tile.bills.print"
        m = plaintext.encode("utf-8")
        k = bytes.fromhex('98a1bef23455dc03')
        key = DesKey(k)
        c = key.encrypt(m)
        print(c.hex())

        # print(format_encrypted_string(encrypt_string("\x90\x34\x08\xec\x4d\x95\x1a\xcf\xae\xb4\x7c\xa8\x83\x90\xc4\x75")))

        # key = des.DesKey(bytes.fromhex("98a1bef23455dc03"))
        # target: bytes = key.decrypt(bytes.fromhex("903408ec4d951acfaeb47ca88390c475"))

        # print(target)
        # print(str(bytes.fromhex("98a1bef23455dc03")))
        
        # count = 0

        # with futures.ProcessPoolExecutor() as executor:
        #     results = []
        #     for comb in itertools.product(string.ascii_letters + string.digits, repeat=8):
        #         print(comb)
        #         executor.submit(evaluate, comb, target)

        #     for r in futures.as_completed(results):
        #         print(r.result())

        # for comb in itertools.product(string.ascii_letters + string.digits, repeat=8):
        #     encoded = "".join(comb).encode("utf-8")
        #     key = des.DesKey(encoded)
            
        #     if key.encrypt(b"aaaaaaaa") == target:
        #         print(f"Found plaintext key: {comb}, {encoded}")
        #         break

        #     count += 1

        #     if count % 10000 == 0:
        #         print(count, encoded)

        # Target: 90-34-08-ec-4d-95-1a-cf ae-b4-7c-a8-83-90-c4-75

        return 0

    sys.exit(main())
