import unittest
from .bitarray import BitArray
import random


class TestBitArray(unittest.TestCase):
    def test_bits(self):
        bit_array = BitArray()

        bit_array.append_bit(0)

        self.assertEqual(len(bit_array), 1)
        self.assertEqual(bit_array.get_bit(0), 0)

        bit_array.append_bit(1)

        self.assertEqual(len(bit_array), 2)
        self.assertEqual(bit_array.get_len_bytes(), 1)
        self.assertEqual(bit_array.get_bit(0), 0)
        self.assertEqual(bit_array.get_bit(1), 1)

        with self.assertRaises(ValueError):
            bit_array.append_bit(-1)
        with self.assertRaises(ValueError):
            bit_array.append_bit(2)

        bit_array.append_bit(0)
        bit_array.append_bit(0)
        bit_array.append_bit(0)
        bit_array.append_bit(0)
        bit_array.append_bit(0)
        bit_array.append_bit(1)

        self.assertEqual(len(bit_array), 8)
        self.assertEqual(bit_array.get_len_bytes(), 1)
        self.assertEqual(bit_array.get_bit(7), 1)

        bit_array.append_bit(1)

        self.assertEqual(len(bit_array), 9)
        self.assertEqual(bit_array.get_len_bytes(), 2)
        self.assertEqual(bit_array.get_bit(8), 1)

        bit_array.append_bit(True)
        bit_array.append_bit(False)
        bit_array.append_bit(True)
        bit_array.append_bit(False)
        bit_array.append_bit(True)
        bit_array.append_bit(False)
        bit_array.append_bit(True)

        self.assertEqual(len(bit_array), 16)
        self.assertEqual(bit_array.get_len_bytes(), 2)

        self.assertEqual(bit_array.get_bit(0), 0)
        self.assertEqual(bit_array.get_bit(1), 1)
        self.assertEqual(bit_array.get_bit(2), 0)
        self.assertEqual(bit_array.get_bit(3), 0)
        self.assertEqual(bit_array.get_bit(4), 0)
        self.assertEqual(bit_array.get_bit(5), 0)
        self.assertEqual(bit_array.get_bit(6), 0)
        self.assertEqual(bit_array.get_bit(7), 1)

        self.assertEqual(bit_array.get_bit(8), 1)
        self.assertEqual(bit_array.get_bit(9), 1)
        self.assertEqual(bit_array.get_bit(10), 0)
        self.assertEqual(bit_array.get_bit(11), 1)
        self.assertEqual(bit_array.get_bit(12), 0)
        self.assertEqual(bit_array.get_bit(13), 1)
        self.assertEqual(bit_array.get_bit(14), 0)
        self.assertEqual(bit_array.get_bit(15), 1)

        with self.assertRaises(IndexError):
            bit_array.get_bit(100)
        with self.assertRaises(IndexError):
            bit_array.get_bit(-1)
        with self.assertRaises(IndexError):
            bit_array.get_bit(16)

        bit_array.set_bit(5, 1)

        self.assertEqual(len(bit_array), 16)
        self.assertEqual(bit_array.get_len_bytes(), 2)
        self.assertEqual(bit_array.get_bit(5), 1)

        bit_array.set_bit(5, 0)

        self.assertEqual(len(bit_array), 16)
        self.assertEqual(bit_array.get_len_bytes(), 2)
        self.assertEqual(bit_array.get_bit(5), 0)

    def test_padding(self):
        bit_array = BitArray()

        bit_array.append_bit(1)
        bit_array.pad_to_byte()

        self.assertEqual(len(bit_array), 8)
        self.assertEqual(bit_array.get_len_bytes(), 1)

        bit_array.append_bit(0)

        self.assertEqual(len(bit_array), 9)
        self.assertEqual(bit_array.get_len_bytes(), 2)

        bit_array.append_byte(0xCC)

        self.assertEqual(len(bit_array), 17)
        self.assertEqual(bit_array.get_len_bytes(), 3)

        bit_array.pad_to_byte()

        self.assertEqual(len(bit_array), 24)
        self.assertEqual(bit_array.get_len_bytes(), 3)

        bit_array.pad_to_byte()

        self.assertEqual(len(bit_array), 24)
        self.assertEqual(bit_array.get_len_bytes(), 3)

    def test_bytes(self):
        bit_array = BitArray()

        bit_array.append_byte(0x00)
        self.assertEqual(len(bit_array), 8)
        self.assertEqual(bit_array.get_len_bytes(), 1)
        self.assertEqual(bit_array.get_byte(0), 0x00)

        bit_array.append_bit(1)

        bit_array.append_byte(0xFF)
        self.assertEqual(len(bit_array), 17)
        self.assertEqual(bit_array.get_len_bytes(), 3)
        for i in range(9, 17):
            self.assertEqual(bit_array[i], 1)
        self.assertEqual(bit_array.get_bit(8), 1)
        self.assertEqual(bit_array.get_byte(9), 0xFF)

        with self.assertRaises(IndexError):
            bit_array.get_bit(17)

        bit_array.append_bit(1)
        bit_array.append_byte(0x12)
        bit_array.append_byte(0xAB)

        self.assertEqual(len(bit_array), 8 + 1 + 8 + 1 + 8 + 8)
        self.assertEqual(bit_array.get_len_bytes(), 5)
        self.assertEqual(bit_array.get_byte(18), 0x12)
        self.assertEqual(bit_array.get_byte(26), 0xAB)

        bit_array.append_byte(0x6A)
        bit_array.append_byte(0x01)

        self.assertEqual(bit_array.get_byte(34), 0x6A)
        self.assertEqual(bit_array.get_byte(42), 0x01)

        bit_array.append_bit(1)
        bit_array.append_bit(0)
        bit_array.append_bit(1)
        bit_array.append_bit(0)
        bit_array.append_bit(1)
        bit_array.append_bit(0)
        bit_array.append_bit(1)
        bit_array.append_bit(0)

        self.assertEqual(bit_array.get_byte(50), 0b10101010)

        bit_array.set_byte(18, 0b11001100)

        self.assertEqual(bit_array.get_byte(18), 0b11001100)

    def test_clear(self):
        bit_array = BitArray()

        bit_array.append_byte(0xCC)
        bit_array.append_byte(0xFF)
        bit_array.append_byte(0x00)
        bit_array.append_byte(0x12)
        bit_array.append_byte(0xAB)

        bit_array.clear()

        self.assertEqual(len(bit_array), 0)
        self.assertEqual(len(bit_array.get_all_bytes()), 0)

    def test_copy(self):
        bit_array = BitArray()

        bit_array.append_byte(0xCC)
        bit_array.append_bit(0)
        bit_array.append_byte(0xFF)
        bit_array.append_bit(1)

        bit_array2 = bit_array.copy()

        self.assertEqual(len(bit_array), len(bit_array2))
        self.assertEqual(bit_array.get_len_bytes(), bit_array2.get_len_bytes())
        self.assertEqual(len(bit_array.get_all_bytes()), len(bit_array2.get_all_bytes()))

        bit_array.append_byte(0xCC)
        bit_array.append_bit(0)
        bit_array.append_byte(0xFF)
        bit_array.append_bit(1)

        self.assertNotEqual(len(bit_array.get_all_bytes()), len(bit_array2.get_all_bytes()))

    def test_coding(self):
        for i in range(20):
            bit_array = BitArray()
            for _ in range(2 ** i):
                bit_array.append_byte(random.randint(0, 255))

            for _ in range(i):
                bit_array.append_bit(random.randint(0, 1))

            byte_data = bit_array.encode_to_bytearray()

            bit_array2 = BitArray.encode_from_bytes(byte_data)

            self.assertEqual(len(bit_array), len(bit_array2))
            self.assertEqual(bit_array.get_len_bytes(), bit_array2.get_len_bytes())
            self.assertEqual(bit_array.get_all_bytes(), bit_array2.get_all_bytes())

    def test_iterator(self):
        bit_array = BitArray()

        bits = [0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1]

        for bit in bits:
            bit_array.append_bit(bit)

        for i, bit in enumerate(bit_array):
            self.assertEqual(bit, bits[i])

        bit_array.clear()

        byte_set = [0x00, 0x01, 0x02, 0x10, 0x11, 0x12, 0xAF, 0xAA, 0xCC, 0xFF, 0x00, 0x11]

        for bit in byte_set:
            bit_array.append_byte(bit)

        i = 0
        for byte in bit_array.get_byte_generator():
            self.assertEqual(byte, byte_set[i])
            i += 1


if __name__ == "__main__":
    unittest.main()
