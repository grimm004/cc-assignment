import sys
import glob
from compression.codings.dictcoding import DictCoding
from compression.codings.huffmancoding import HuffmanCoding
from compression.util.tables import FrequencyTable


def main() -> int:
    frequency_table = FrequencyTable.create_flat(256)

    with open("./data/latex_dict.txt", "rt") as file:
        dict_strings = file.readlines()
    dict_encoder = DictCoding.from_strings(dict_strings)
    for filepath in glob.glob("./data/*.tex"):
        print(f"Updating frequencies with '{filepath}'.")
        with open(filepath, "rb") as file:
            file_data = file.read()
            if not file_data.isascii():
                continue
            encoded_data = dict_encoder.encode(file_data)
            frequency_table.accumulate(encoded_data)
    h_tree = HuffmanCoding().load_from_frequencies(frequency_table)
    with open("./data/huffman_coding.json", "wt") as file:
        file.write(h_tree.to_json())

    return 0


if __name__ == "__main__":
    sys.exit(main())
