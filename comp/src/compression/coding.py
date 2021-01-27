from compression.codings.huffmancoding import HuffmanCoding, HuffmanCoder, PpmEncoder, PpmDecoder
from compression.codings.dictcoding import DictCoding


def encode(data: bytearray) -> bytearray:
    with open("./data/latex_dict.txt", "rt") as dict_file:
        dict_coding = DictCoding.from_strings(s.replace("\n", "") for s in dict_file.readlines())
        dict_encoded = dict_coding.encode(data)

    huffman_encoded = PpmEncoder().encode(dict_encoded)

    return huffman_encoded


def decode(data: bytearray) -> bytearray:
    huffman_decoded = PpmDecoder().decode(data)

    with open("./data/latex_dict.txt", "rt") as dict_file:
        dict_coding = DictCoding.from_strings(s.replace("\n", "") for s in dict_file.readlines())
        dict_decoded = dict_coding.decode(huffman_decoded)

    return dict_decoded
