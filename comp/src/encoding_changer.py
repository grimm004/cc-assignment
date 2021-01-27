
input_file_name = "./data/dynamics_and_relativity.tex"
output_file_name = "./data/dynamics_and_relativity-ascii.tex"

chunk_size = 4 * 1024

with open(input_file_name, "rb") as input_file,\
        open(output_file_name, "wb") as output_file:

    chunk = input_file.read(chunk_size)
    while chunk:
        output_file.write(bytes(byte for byte in chunk if byte < 128))
        chunk = input_file.read(chunk_size)

with open(output_file_name, "rt") as output_file:
    assert all(ord(c) < 128 for c in output_file.read())
