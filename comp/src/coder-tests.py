import unittest
from typing import Tuple
from parameterized import parameterized
import os
import glob

import encoder
import decoder

FILES = glob.glob(".\\data\\*.tex")


class EncodingTestCase(unittest.TestCase):
    @parameterized.expand(FILES)
    def test_files(self, input_path):
        input_size: int = os.path.getsize(input_path)

        path_parts: Tuple[str, str] = os.path.split(input_path)
        base_name: str = os.path.splitext(path_parts[-1])[0]

        output_path: str = os.path.join(*path_parts[:-1], "output", base_name)
        output_file_path: str = os.path.join(output_path, base_name)

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        with open(input_path, "rb") as input_file:
            input_data = input_file.read()

        encoded_path: str = f"{output_file_path}.lz"
        if input_data.isascii():
            encoder.encode_file(input_path, encoded_path)
            encoded_size: int = os.path.getsize(encoded_path)

            decoded_path: str = f"{output_file_path}-decoded.tex"
            decoder.decode_file(encoded_path, decoded_path)
            decoded_size: int = os.path.getsize(decoded_path)

            self.assertEqual(input_size, decoded_size, "Input size does not match decoded size.")
            with open(decoded_path, "rb") as decoded_file:
                self.assertEqual(input_data, decoded_file.read(), "Input data does not match output data.")

            self.assertTrue(input_size == 0 or encoded_size > 0, "Encoded file size is zero for non-zero input size.")

            print(f"File '{input_path}' coded successfully "
                  f"with compression ratio {input_size / encoded_size:.2f}")
        else:
            with self.assertRaises(ValueError):
                encoder.encode_file(input_path, encoded_path)
            print(f"Error raised for non-ascii file '{input_path}'")


if __name__ == "__main__":
    unittest.main()
