"""
Dictionary coder by wcrr51
"""

from typing import Union, Dict, Iterable
from compression.util.bitarray import BitArray


class DictCoding:
    def __init__(self, dictionary: Dict[str, int]):
        self.__encode_dictionary: Dict[str, int] = dictionary

    def encode(self, input_data: Union[bytearray, bytes]) -> bytearray:
        output_data: BitArray = BitArray()

        pos = 0
        # Loop through input
        while pos < len(input_data):
            next_split = 0
            # Find next splitting character (space, tab, or newline or open curly bracket)
            while pos + next_split < len(input_data) and \
                    input_data[pos + next_split] not in (ord(" "), ord("\t"), ord("\n"), ord("{")):
                next_split += 1

            # Ignore
            if next_split == 0 or pos + next_split == len(input_data):
                output_data.append_byte(input_data[pos])
                pos += 1
                continue

            word = input_data[pos:pos+next_split].decode("ascii")

            if word in self.__encode_dictionary:
                codeword = self.__encode_dictionary[word]
                output_data.append_bit(1)
                for i in range(15):
                    output_data.append_bit((codeword >> i) & 0b1)
                pos += len(word)
            else:
                output_data.append_byte(input_data[pos])
                pos += 1

        return output_data.get_all_bytes()

    def decode(self, input_data: Union[bytearray, bytes]) -> bytearray:
        input_data: BitArray = BitArray(input_data)
        output_data: bytearray = bytearray()

        decode_dictionary: Dict[int, str] = {v: k for k, v in self.__encode_dictionary.items()}

        pos = 0
        while pos < input_data.get_len_bytes():
            if input_data.get_bit(8 * pos):
                code_num = 0
                for i in range(15):
                    code_num |= input_data.get_bit((8 * pos) + 1 + i) << i

                output_data.extend(decode_dictionary[code_num].encode("utf-8"))
                pos += 2
            else:
                output_data.append(input_data.get_byte(8 * pos))
                pos += 1

        return output_data

    @staticmethod
    def from_strings(strings: Iterable[str]) -> "DictCoding":
        dictionary: Dict[str, int] = {}
        pos = 0
        for string in strings:
            if len(string) > 2 and string.isascii():
                dictionary[string] = pos
                pos += 1
        return DictCoding(dictionary)


if __name__ == "__main__":
    d_coding = DictCoding.from_strings(["hello", "why", "not", "test", "word", "a", "another", "\\usepackage"])

    text = "\\usepackage{test}\nhello there test\n word why not add another\t to a words hello word another"
    data = bytearray(text, "ascii")
    encoded_data = d_coding.encode(data)
    decoded_data = d_coding.decode(encoded_data)

    print(data)
    print(encoded_data)
    print(decoded_data)

    print("Success" if decoded_data == data else "Failure")
