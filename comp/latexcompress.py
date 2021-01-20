from abc import ABC, abstractmethod
from typing import Dict, Union, List
from array import array


def encode(uncompressed_latex: str) -> bytes:
    return LaTeXCompression().encode(uncompressed_latex)


def decode(compressed_latex: bytes) -> str:
    return LaTeXCompression().decode(compressed_latex)


class Compression(ABC):
    @abstractmethod
    def encode(self, uncompressed: Union[bytes, str]) -> Union[bytes, str]: pass

    @abstractmethod
    def decode(self, compressed: Union[bytes, str]) -> Union[bytes, str]: pass


class TextCompression(Compression):
    @abstractmethod
    def encode(self, uncompressed: str) -> Union[bytes, str]: pass

    @abstractmethod
    def decode(self, compressed: Union[bytes, str]) -> Union[bytes, str]: pass


class BinaryCompression(Compression):
    @abstractmethod
    def encode(self, uncompressed: bytes) -> bytes: pass

    @abstractmethod
    def decode(self, compressed: bytes) -> Union[bytes, str]: pass


class LaTeXCompression(TextCompression):
    def __init__(self):
        super().__init__()

        self.dictionary: Dict[str, str] = {
            "\\documentclass" : "\\/d/",
            "\\usepackage": "\\/u/",
            "\\title": "\\/t/",
            "\\author": "\\/a/",
            "\\date": "\\/D/",
            "\\maketitle": "\\/m/",
            "\\begin": "\\/b/",
            "\\end": "\\/e/",
            "\\section": "\\/s/",
            "\\LaTeX": "\\/l/"
        }

    def encode(self, uncompressed: str) -> Union[bytes, str]:

        for key, codeword in self.dictionary.items():
            uncompressed = uncompressed.replace(key, codeword)

        return uncompressed.encode("ascii")

    def decode(self, compressed: bytes) -> Union[bytes, str]:
        input_str: str = compressed.decode("ascii")

        for key, codeword in reversed(list(self.dictionary.items())):
            input_str = input_str.replace(codeword, key)

        return input_str


class LZWCompression(BinaryCompression):
    def __init__(self):
        pass

    def encode(self, uncompressed: bytes) -> bytes:
        # if (iBuf == null) throw new Exception("Input buffer is null.");
        assert uncompressed is not None
        # if (iBuf.Length == 0) throw new Exception("Input buffer is empty.");
        assert len(uncompressed) != 0

        # DeCompressedSize = iBuf.Length;
        uncompressed_size: int = len(uncompressed)

        # var dictionary = new Dictionary<List<byte>, int>(new ArrayComparer());
        # for (var i = 0; i < 256; i++)
        # {
        #     var e = new List<byte> {(byte) i};
        #     dictionary.Add(e, i);
        # }
        dictionary: Dict[bytes, int] = {bytes([i]): i for i in range(256)}

        # var window = new List<byte>();
        window: array = array("B")

        # var oBuf   = new List<int>();
        compressed_buffer: array = array("I")

        # foreach (var b in iBuf)
        for byte in uncompressed:
            # var windowChain = new List<byte>(window) {b};
            window_chain: bytes = bytes([byte])

            # if (dictionary.ContainsKey(windowChain))
            if window_chain in dictionary:
                # window.Clear();
                del window[:]
                # window.AddRange(windowChain);
                window.extend(window_chain)
            # else
            else:
                # if (dictionary.ContainsKey(window))
                if window in dictionary:
                    # oBuf.Add(dictionary[window]);
                    compressed_buffer.append(dictionary[window.tobytes()])
                # else
                else:
                    # throw new Exception("Error Encoding.");
                    raise Exception("Error Encoding.")

                # dictionary.Add(windowChain, dictionary.Count);
                dictionary[window_chain] = len(dictionary)

                # window.Clear();
                del window[:]

                # window.Add(b);
                window.append(byte)

        # if (window.Count != 0)
        if len(window) != 0:
            # oBuf.Add(dictionary[window]);
            compressed_buffer.append(dictionary[window.tobytes()])

        compressed_size: int = len(compressed_buffer.tobytes())

        print(f"Uncompressed: {uncompressed_size}\n"
              f"Compressed: {compressed_size}\n"
              f"Compression Ratio: {uncompressed_size / compressed_size}")

        # return GetBytes(oBuf.ToArray());
        print(compressed_buffer)
        return compressed_buffer.tobytes()

    def decode(self, compressed: bytes) -> bytes:
        # https://gist.github.com/mjs3339/9b2cfe7f872c58c41435d6adfe1a9913
        return bytes()


# import io
#
# class BitReader:
#     def __init__(self):
#         io.BytesIO
#
#     def read_bit(self):
#
#
# class BitWriter:
#     def __init__(self):
#         pass



if __name__ == "__main__":
    print(LZWCompression().encode(bytes(list(range(10)))))
