import latexcompress
from os import path
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encode a LaTeX file.")
    parser.add_argument("input_path", type=str, help="path of the file to encode")
    parser.add_argument("-o", "--output", dest="output_path", type=str, default=None,
                        help="path to output the encoded file to")

    args = parser.parse_args()

    input_path = args.input_path
    output_path = f"{path.splitext(input_path)[0]}.lz" if args.output_path is None else args.output_path

    try:
        with open(input_path, "rb") as input_file, open(output_path, "wb") as output_file:
            input_text_data: bytes = input_file.read()
            input_text: str = input_text_data.decode("ascii")
            encoded_file_data: bytes = latexcompress.encode(input_text)
            output_file.write(encoded_file_data)
    except FileNotFoundError:
        print(f"Could not find input file '{input_path}'.")
