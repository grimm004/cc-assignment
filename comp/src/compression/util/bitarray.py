from typing import Union, Iterable, List, Generator, Optional


class BitArray:
    def __init__(self, byte_data: Optional[Union[bytearray, bytes]] = None):
        if type(byte_data) is bytes:
            byte_data = bytearray(byte_data)
        self.__bytes: bytearray = byte_data if byte_data else bytearray()
        self.__length_bits: int = 8 * len(self.__bytes)

    @staticmethod
    def __check_bit(bit: Union[int, bool]) -> int:
        if type(bit) is bool:
            return 1 if bit else 0
        elif type(bit) is int:
            if bit in (0, 1):
                return bit
            else:
                raise ValueError("bit must be 0, 1, True or False")
        else:
            raise TypeError("bit must of be type bool or int")

    @staticmethod
    def __check_byte(byte: int):
        if type(byte) is not int:
            raise TypeError("byte must be an integer")
        if not (0 <= byte < 256):
            raise ValueError("byte must be in range(0, 256)")

    def __check_bit_index(self, bit_index: int):
        if type(bit_index) != int:
            raise TypeError(f"bit_index must be of type int")
        if not (0 <= bit_index < self.__length_bits):
            raise IndexError("bit_index out of bounds")

    def __pos_in_byte(self) -> int:
        return self.__length_bits % 8

    def append_bit(self, bit: Union[int, bool]) -> "BitArray":
        bit = self.__check_bit(bit)

        if self.__pos_in_byte() == 0:
            self.__bytes.append(0)

        if bit == 1:
            self.__bytes[-1] |= (bit << (7 - self.__pos_in_byte()))
        else:
            self.__bytes[-1] &= ~(bit << (7 - self.__pos_in_byte()))

        self.__length_bits += 1

        return self

    def append_bits(self, bits: Iterable[Union[int, bool]]) -> "BitArray":
        for bit in bits:
            self.append_bit(bit)

        return self

    def append_byte(self, byte: int) -> "BitArray":
        self.__check_byte(byte)

        for i in range(8):
            self.append_bit((byte >> (7 - i)) & 1)

        return self

    def append_bytes(self, byte_list: Union[Iterable[int], bytearray]) -> "BitArray":
        for byte in byte_list:
            self.append_byte(byte)

        return self

    def pad_to_byte(self) -> "BitArray":
        if self.__length_bits < 8 * len(self.__bytes):
            self.__length_bits = 8 * len(self.__bytes)

        return self

    def get_bit(self, bit_index: int) -> int:
        self.__check_bit_index(bit_index)

        return (self.__bytes[bit_index // 8] >> (7 - (bit_index % 8))) & 1

    def get_bits(self, bit_index: int, n_bits: int) -> List[int]:
        if type(n_bits) is not int:
            raise ValueError("n_bits must be of type int")
        return [self.get_bit(bit_index + i) for i in range(n_bits)]

    def get_all_bits(self) -> List[int]:
        return list(self.get_bit_generator())

    def set_bit(self, bit_index: int, bit: Union[int, bool]) -> "BitArray":
        self.__check_bit_index(bit_index)
        bit = self.__check_bit(bit)

        if bit == 1:
            self.__bytes[bit_index // 8] |= (1 << (7 - (bit_index % 8)))
        else:
            self.__bytes[bit_index // 8] &= ~(1 << (7 - (bit_index % 8)))

        return self

    def set_bits(self, bit_index: int, bits: List[Union[int, bool]]) -> "BitArray":
        for i, bit in enumerate(bits):
            self.set_bit(bit_index + i, bit)

        return self

    def get_byte(self, bit_index: int) -> int:
        self.__check_bit_index(bit_index)

        return sum([self.get_bit(bit_index + 7 - i) * (2 ** i) for i in range(8)])

    def get_bytes(self, bit_index: int, n_bytes: int) -> bytearray:
        if type(n_bytes) is not int or n_bytes < 0:
            raise ValueError("n_bytes must be a non-negative integer")

        return bytearray(self.get_byte(bit_index + (8 * i)) for i in range(n_bytes))

    def get_all_bytes(self) -> bytearray:
        return self.__bytes.copy()

    def set_byte(self, bit_index: int, byte: int) -> "BitArray":
        self.__check_bit_index(bit_index)
        self.__check_byte(byte)

        for i in range(8):
            self.set_bit(bit_index + i, (byte >> (7 - i)) & 1)

        return self

    def set_bytes(self, bit_index: int, byte_list: Union[List[int], bytearray]) -> "BitArray":
        for i, byte in enumerate(byte_list):
            self.set_byte(bit_index + (8 * i), byte)

        return self

    def get_len_bytes(self) -> int:
        return len(self.__bytes)

    def get_len_bits(self) -> int:
        return self.__length_bits

    def get_bit_generator(self) -> Generator[int, None, None]:
        for i in range(self.__length_bits):
            yield self.get_bit(i)

    def get_byte_generator(self) -> Generator[int, None, None]:
        for i in range(self.get_len_bytes()):
            yield self.get_byte(8 * i)

    def clear(self):
        self.__bytes.clear()
        self.__length_bits = 0

    def copy(self) -> "BitArray":
        copy = BitArray()
        copy.__length_bits = self.__length_bits
        copy.__bytes = self.__bytes.copy()
        return copy

    def encode_to_bytearray(self) -> bytearray:
        data: bytearray = bytearray()
        for i in range(4):
            data.insert(i, (self.__length_bits >> (8 * i)) & 0xFF)
        data.extend(self.__bytes)
        return data

    @staticmethod
    def encode_from_bytes(byte_data: Iterable[int]) -> "BitArray":
        byte_iterator = iter(byte_data)
        size_bits = 0
        for i in range(4):
            try:
                size_bits |= next(byte_iterator) << (8 * i)
            except StopIteration:
                raise ValueError("Invalid byte_data.")

        byte_array: bytearray = bytearray()

        try:
            for _ in range((size_bits // 8) + (1 if size_bits % 8 else 0)):
                byte_array.append(next(byte_iterator))
        except StopIteration:
            pass

        bitarray = BitArray()
        bitarray.__length_bits = size_bits
        bitarray.__bytes = byte_array

        return bitarray

    def __len__(self) -> int:
        return self.get_len_bits()

    def __getitem__(self, bit_index: Union[int, slice]) -> Union[int, List[int]]:
        if type(bit_index) is int:
            return self.get_bit(bit_index)
        elif type(bit_index) is slice:
            return [self.get_bit(i) for i in range(bit_index.start, bit_index.stop,
                                                   bit_index.step if bit_index.step is not None else 1)]
        else:
            raise ValueError("Key must be an int or slice")

    def __setitem__(self, bit_index: int, bit: Union[int, bool]):
        self.set_bit(bit_index, bit)

    def __iter__(self):
        return self.get_bit_generator()
