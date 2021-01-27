from typing import Dict, Iterable, Optional, Union, List

FILE_BUFFER = 4 * 1024


class FrequencyTable:
    def __init__(self, frequencies: Optional[List[int]] = None):
        self.__symbol_freqs: List[int] = [] if not frequencies else frequencies
        self.__cum_freqs: Optional[List[int]] = None

    def __init_cumulative(self):
        cumulative: List[int] = [0]
        total: int = 0
        for freq in self.__symbol_freqs:
            total += freq
            cumulative.append(total)
        assert total == self.get_total()
        self.__cum_freqs = cumulative

    def get_total(self) -> Union[int]:
        return sum(self.__symbol_freqs)

    def get_symbol_count(self) -> int:
        return len(self.__symbol_freqs)

    def get(self, symbol: int):
        return self.__symbol_freqs[symbol]

    # def set(self, symbol: int, freq: int):
    #     if freq < 0:
    #         raise ValueError("Negative frequency")
    #     self.__symbol_freqs[symbol] = freq
    #     self.__cum_freqs = None
    
    def get_low(self, symbol):
        if self.__cum_freqs is None:
            self.__init_cumulative()
        return self.__cum_freqs[symbol]

    def get_high(self, symbol):
        if self.__cum_freqs is None:
            self.__init_cumulative()
        return self.__cum_freqs[symbol + 1]

    def to_dict(self) -> Dict[int, int]:
        return {sym: freq for sym, freq in enumerate(self.__symbol_freqs)}

    def to_list(self) -> List[int]:
        return self.__symbol_freqs.copy()

    def __getitem__(self, symbol: int) -> int:
        return self.__symbol_freqs[symbol]

    def __setitem__(self, symbol: int, value: int):
        self.__symbol_freqs[symbol] = value

    def accumulate(self, symbols: Iterable[int]) -> "FrequencyTable":
        for symbol in symbols:
            if not (0 <= symbol < len(self.__symbol_freqs)):
                raise ValueError("Symbol not in range")
            self.__symbol_freqs[symbol] += 1

        self.__cum_freqs = None
        return self

    @staticmethod
    def from_symbols(symbols: Iterable[int]) -> "FrequencyTable":
        return FrequencyTable.create_flat(max(symbols) + 1).accumulate(symbols)

    @staticmethod
    def from_source_file(filename) -> "FrequencyTable":
        freq_table: FrequencyTable = FrequencyTable()
        with open(filename, "rb") as file:
            data = file.read(FILE_BUFFER)
            while data:
                freq_table.accumulate(data)
                data = file.read(FILE_BUFFER)
        return freq_table

    @staticmethod
    def create_flat(symbol_count: int):
        return FrequencyTable([1] * symbol_count)
