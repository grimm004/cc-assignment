from compression import coding
from os import path
from argparse import ArgumentParser, Namespace
import sys


def encode_file(input_path: str, output_path: str):
    with open(input_path, "rb") as input_file, open(output_path, "wb") as output_file:
        input_data: bytearray = bytearray(input_file.read())
        if not input_data.isascii():
            raise ValueError("Input file is not encoded using ASCII.")
        encoded_data: bytearray = coding.encode(input_data)
        output_file.write(encoded_data)


def main() -> int:
    parser: ArgumentParser = ArgumentParser(description="Encode a LaTeX file.")
    parser.add_argument("input_path", type=str, help="path of the file to encode")
    parser.add_argument("-o", "--output", dest="output_path", type=str, default=None,
                        help="path to output the encoded file to")

    args: Namespace = parser.parse_args()

    input_path: str = args.input_path
    output_path: str = f"{path.splitext(input_path)[0]}.lz" if args.output_path is None else args.output_path
    try:
        encode_file(input_path, output_path)
    except FileNotFoundError as e:
        print(f"Could not find file '{e.filename}'.")
    except ValueError as e:
        print(str(e))

    return 0


if __name__ == "__main__":
    sys.exit(main())
