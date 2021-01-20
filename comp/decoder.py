import latexcompress
from os import path
from argparse import ArgumentParser, Namespace

if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser(description="Decode an encoded LaTeX file.")
    parser.add_argument("input_path", type=str, help="path of the file to decode")
    parser.add_argument("-o", "--output", dest="output_path", type=str, default=None, help="path to output the decoded file to")

    args: Namespace = parser.parse_args()

    input_path: str = args.input_path
    output_path: str = f"{path.splitext(input_path)[0]}-decoded.tex" if args.output_path is None else args.output_path

    try:
        with open(input_path, "rb") as input_file:
            input_data: bytearray = bytearray(input_file.read())
            decoded_file_text: str = latexcompress.decode(input_data)

            with open(output_path, "wt") as output_file:
                output_file.write(decoded_file_text)
    except FileNotFoundError:
        print(f"Could not find input file '{input_path}'.")
