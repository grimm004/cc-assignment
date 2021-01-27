"""
Huffman coder by wcrr51

#
# (PPM Wrapper and Model) Copyright (c) Project Nayuki
#
# https://www.nayuki.io/page/reference-arithmetic-coding
# https://github.com/nayuki/Reference-arithmetic-coding
#
"""

from typing import Any, Optional, Union, Tuple, Iterable, Dict, List, Generator
import heapq
import json
from compression.util.bitarray import BitArray
from compression.util.tables import FrequencyTable


class HuffmanCoder:
    def __init__(self, huffman_tree: "HuffmanCoding"):
        self.tree: HuffmanCoding = huffman_tree

    def encode(self, input_bytes: bytes) -> bytearray:
        bits = BitArray()
        self.tree.get_code(0)
        bits.append_bits(self.tree.get_code_iterable(input_bytes))
        return bits.encode_to_bytearray()

    def decode(self, input_bytes: bytes) -> bytearray:
        input_bits = BitArray.encode_from_bytes(input_bytes)

        return bytearray(self.tree.get_symbol_generator(input_bits))


class HuffmanCoding:
    def __init__(self, tree: Optional[Union[int, list]] = None, codes: Optional[Dict[int, List[int]]] = None):
        self.__tree: Union[int, list] = tree if tree is not None else []
        self.__codes: Dict[int, List[int]] = codes if codes is not None else {}

    def load_from_frequencies(self, freq_table: FrequencyTable) -> "HuffmanCoding":
        # Using a heap queue for efficiency
        element_queue = []
        for symbol, frequency in enumerate(freq_table.to_list()):
            heapq.heappush(element_queue, (frequency, 1, symbol))

        # Handle edge cases
        if not element_queue:
            self.__tree = []
            self.__generate_codes()
            return self
        elif len(element_queue) == 1:
            self.__tree = [element_queue[0][2]]
            self.__generate_codes()
            return self

        # While there are two or more elements
        while len(element_queue) > 1:
            # Dequeue two items of smallest frequency (secondarily sorted by number of sub-elements)
            f0, n0, item0 = heapq.heappop(element_queue)
            f1, n1, item1 = heapq.heappop(element_queue)
            # Push subgraph formed from the items with the summed frequency
            heapq.heappush(element_queue, (f1 + f0, n0 + n1, [item1, item0]))

        # The final element left in the queue is the full graph
        _, _, self.__tree = heapq.heappop(element_queue)

        self.__generate_codes()

        return self

    def __generate_codes(self):
        stack: List[Tuple[Union[int, list], List[int]]] = []
        # Initialise the current node to the root of the tree
        current_node: Union[int, list, None] = self.__tree
        # Store the route for the current node
        current_route = []
        # Re-set the codes dictionary
        self.__codes = {}
        # While there are nodes to visit
        while current_node is not None or stack:
            # While there is a left node to visit
            while current_node is not None:
                # Add the node and its route to the stack
                stack.append((current_node, current_route.copy()))
                # If there is another left node
                if type(current_node) is list and current_node:
                    # Update the current node and route
                    current_node = current_node[0]
                    current_route.append(0)
                else:
                    current_node = None

            # Pop the node at the top of the stack
            (current_node, current_route) = stack.pop()

            # If the it is a leaf
            if type(current_node) is int:
                # Save its route in the code dictionary
                self.__codes[current_node] = current_route

            # If the current node has children
            if type(current_node) is list and len(current_node) == 2:
                # Select the right node
                current_node = current_node[1]
                # Update the current route
                current_route.append(1)
            else:
                current_node = None

    def get_tree(self) -> List[Any]:
        return self.__tree

    def get_code_dict(self) -> Dict[int, List[int]]:
        return self.__codes

    def get_code(self, symbol: int) -> List[int]:
        if type(symbol) is not int:
            raise TypeError("symbol must be of type int")
        if symbol not in self.__codes:
            raise ValueError(f"Symbol {symbol} not in code dictionary.")
        return self.__codes[symbol]

    def get_code_iterable(self, symbols: Iterable[int]) -> Iterable[int]:
        for symbol in symbols:
            for bit in self.get_code(symbol):
                yield bit

    def get_first_symbol(self, bit_data: Union[List[int], BitArray], bit_start_position: int = 0) -> Tuple[int, int]:
        # Start at the root node of the tree
        current_node: Union[int, list] = self.__tree
        offset = 0
        # Repeat while current_node is not a leaf node
        while type(current_node) is list:
            if not (bit_start_position + offset < len(bit_data)):
                raise ValueError("Invalid codeword")
            # Go to the child node corresponding to the next code element
            bit = bit_data[bit_start_position + offset]
            current_node = current_node[bit]
            offset += 1
        # Return the resultant symbol and the length consumed
        return current_node, offset

    def get_symbol_generator(self, code: Iterable[int]) -> Generator[int, None, None]:
        # Function assumes constant frequency table
        # Start at the root node of the tree
        current_node: Union[int, list] = self.__tree
        # Repeat while current_node is not a leaf node
        for bit in code:
            # If the current node is a symbol
            if type(current_node) is int:
                # Return it
                yield current_node
                # Re-set the current node to the root of the tree
                current_node = self.__tree

            if type(current_node) is list:
                if 0 <= bit < len(current_node):
                    # Go to the child node corresponding to the current bit
                    current_node = current_node[bit]
                else:
                    raise ValueError("Invalid codeword")

        # If the ending node is a symbol
        if type(current_node) is int:
            # Return it
            yield current_node
        else:
            raise ValueError("Invalid codeword")

    @staticmethod
    def from_json(json_string: str) -> "HuffmanCoding":
        tree_data = json.loads(json_string)
        return HuffmanCoding(tree_data["tree"], {int(k): v for k, v in tree_data["codes"].items()})

    def to_json(self) -> str:
        return json.dumps({"tree": self.__tree, "codes": self.__codes})

    def __getitem__(self, item: Union[int, List[int]]) -> List[int]:
        if type(item) is int:
            return self.get_code(item)
        elif type(item) is list:
            return list(bit for symbol in item for bit in self.get_code(symbol))
        else:
            raise TypeError("item must be an int or list of ints")

    def __setitem__(self):
        raise Exception("Symbol code may not be set.")


class PpmEncoder:
    def __init__(self):
        self.__encoder: HuffmanCoding = HuffmanCoding()

    def encode(self, data: bytearray) -> bytearray:
        # Set up encoder and model. In this PPM model, symbol 256 represents EOF;
        # its frequency is 1 in the order -1 context but its frequency
        # is 0 in all other contexts (which have non-negative order).
        model = PpmModel(3, 257, 256)
        history = []

        output_data: BitArray = BitArray()

        for symbol in data:
            # Encode one byte
            # print("ENCODING:", chr(symbol))
            self.__encode_symbol(model, history, symbol, output_data)
            # print(chr(symbol), output_data.get_all_bits())
            model.increment_contexts(history, symbol)

            if model.model_order >= 1:
                # Prepend current symbol, dropping oldest symbol if necessary
                if len(history) == model.model_order:
                    history.pop()
                history.insert(0, symbol)

        # print("ENCODING: EOF")
        self.__encode_symbol(model, history, 256, output_data)  # EOF

        # print("".join(str(b) for b in output_data.get_all_bits()))

        return output_data.get_all_bytes()

    def __encode_symbol(self, model: "PpmModel", history: List[int], symbol: int, output_data: BitArray):
        # Try to use highest order context that exists based on the history suffix, such
        # that the next symbol has non-zero frequency. When symbol 256 is produced at a context
        # at any non-negative order, it means "escape to the next lower order with non-empty
        # context". When symbol 256 is produced at the order -1 context, it means "EOF".
        for order in reversed(range(len(history) + 1)):
            # print("Processing order", order)
            ctx: PpmModel.Context = model.root_context
            for sym in history[: order]:
                assert ctx.child_contexts is not None
                ctx = ctx.child_contexts[sym]
                if ctx is None:
                    break
            else:  # ctx is not None
                self.__encoder.load_from_frequencies(ctx.frequencies)
                # print("256 freq:", ctx.frequencies.get(256))
                if symbol != 256 and ctx.frequencies.get(symbol) > 0:
                    code = self.__encoder.get_code(symbol)
                    output_data.append_bits(code)
                    return
                # Else write context escape symbol and continue decrementing the order
                self.__encoder.load_from_frequencies(ctx.frequencies)
                code = self.__encoder.get_code(256)  # EOF
                # print("Context escape:")
                # print("".join(str(b) for b in code))
                output_data.append_bits(code)
        # Logic for order = -1
        # print("Processing order -1")
        self.__encoder.load_from_frequencies(model.order_minus1_freqs)
        # self.__encoder.write(model.order_minus1_freqs, symbol)
        code = self.__encoder.get_code(symbol)
        # print("".join(str(b) for b in code))
        output_data.append_bits(code)


class PpmDecoder:
    def __init__(self):
        self.__decoder: HuffmanCoding = HuffmanCoding()

    def decode(self, data: bytearray) -> bytearray:
        input_data: BitArray = BitArray(data)

        # Set up decoder and model. In this PPM model, symbol 256 represents EOF;
        # its frequency is 1 in the order -1 context but its frequency
        # is 0 in all other contexts (which have non-negative order).
        model: PpmModel = PpmModel(3, 257, 256)
        history: List[int] = []

        output_data: bytearray = bytearray()

        pos_bits = 0
        while True:
            # Decode and write one byte
            p = pos_bits
            symbol, pos_bits = self.__decode_symbol(model, history, input_data, pos_bits)
            if symbol == 256:  # EOF symbol
                break
            # print("OUTPUT SYMBOL", chr(symbol), "matched from", p, "to", pos_bits)
            output_data.append(symbol)
            model.increment_contexts(history, symbol)

            if model.model_order >= 1:
                # Prepend current symbol, dropping oldest symbol if necessary
                if len(history) == model.model_order:
                    history.pop()
                history.insert(0, symbol)

        return output_data

    def __decode_symbol(self, model: "PpmModel", history: List[int],
                        input_data: BitArray, pos_bits: int) -> Tuple[int, int]:
        # Try to use highest order context that exists based on the history suffix. When symbol 256
        # is consumed at a context at any non-negative order, it means "escape to the next lower order
        # with non-empty context". When symbol 256 is consumed at the order -1 context, it means "EOF".
        for order in reversed(range(len(history) + 1)):
            # print("Processing order", order)
            ctx = model.root_context
            for sym in history[: order]:
                assert ctx.child_contexts is not None
                ctx = ctx.child_contexts[sym]
                if ctx is None:
                    break
            else:  # ctx is not None
                self.__decoder.load_from_frequencies(ctx.frequencies)
                # print("256 freq:", ctx.frequencies.get(256))
                symbol, bit_count = self.__decoder.get_first_symbol(input_data, pos_bits)
                pos_bits += bit_count
                # print("Match", symbol, "at", pos_bits, "in", bit_count, "bits")
                # symbol = self.__decoder.read(ctx.frequencies)
                if symbol < 256:
                    return symbol, pos_bits
                # print("Context escape:")
                # print("".join(str(b) for b in input_data[pos_bits-bit_count:pos_bits]))
            # Else we read the context escape symbol, so continue decrementing the order
        # Logic for order = -1
        # print("Processing order -1")
        self.__decoder.load_from_frequencies(model.order_minus1_freqs)
        symbol, bit_count = self.__decoder.get_first_symbol(input_data, pos_bits)
        # print("Match", symbol, "at", pos_bits, "in", bit_count, "bits")
        pos_bits += bit_count
        # print("".join(str(b) for b in input_data[pos_bits-bit_count:pos_bits]))
        return symbol, pos_bits


class PpmModel:
    def __init__(self, order: int, symbol_count: int, escape_symbol: int):
        if order < -1 or symbol_count <= 0 or not (0 <= escape_symbol < symbol_count):
            raise ValueError()
        self.model_order: int = order
        self.symbol_limit: int = symbol_count
        self.escape_symbol: int = escape_symbol

        if order >= 0:
            self.root_context = PpmModel.Context(symbol_count, order >= 1)
            self.root_context.frequencies.accumulate([escape_symbol])
        else:
            self.root_context = None
        self.order_minus1_freqs = FrequencyTable.create_flat(symbol_count)

    def increment_contexts(self, history, symbol):
        if self.model_order == -1:
            return
        if len(history) > self.model_order or not (0 <= symbol < self.symbol_limit):
            raise ValueError()

        ctx = self.root_context
        ctx.frequencies.accumulate([symbol])
        for (i, sym) in enumerate(history):
            child_ctxs = ctx.child_contexts
            assert child_ctxs is not None

            if child_ctxs[sym] is None:
                child_ctxs[sym] = PpmModel.Context(self.symbol_limit, i + 1 < self.model_order)
                child_ctxs[sym].frequencies.accumulate([self.escape_symbol])
            ctx = child_ctxs[sym]
            ctx.frequencies.accumulate([symbol])

    class Context:
        def __init__(self, symbol_count: int, has_child_ctxs: bool):
            self.frequencies: FrequencyTable = FrequencyTable([0] * symbol_count)
            self.child_contexts: Optional[List[PpmModel.Context]] = ([None] * symbol_count) if has_child_ctxs else None


if __name__ == "__main__":
    string = "Hello, world!"

    # h_tree = HuffmanCoding().load_from_frequencies(FrequencyTable.from_symbols(string.encode("ascii")))

    # print(h_tree.get_tree())
    # print(h_tree.get_code_dict())

    # encoded = [c for char in string for c in h_tree[ord(char)]]
    # encoded_length = len(encoded)
    #
    # decoded = "".join(chr(char) for char in h_tree.get_symbol_generator(encoded))
    # print(f"Success: {8 * len(string) / encoded_length}" if string == decoded else "Failure")
    # print(f"Original: {string}\nDecoded: {decoded}\n")

    original_data = bytearray(string, "ascii")

    encoder: PpmEncoder = PpmEncoder()
    encoded_data = encoder.encode(original_data)
    print(len(encoded_data), encoded_data)

    decoder: PpmDecoder = PpmDecoder()
    decoded_data = decoder.decode(encoded_data)
    print(len(decoded_data), decoded_data)

    print(original_data == decoded_data)
