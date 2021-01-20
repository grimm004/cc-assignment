#include <bitset>
#include <iostream>
#include <thread>
#include "./des.h"

uint64_t to64BitKey(uint64_t input)
{
	const std::bitset<56> keyBits(input);
	std::bitset<64> outputBits(0);
	for (int8_t i = 0; i < 56; i++)
		outputBits[i / 7uI64 + i + 1uI64] = keyBits[i];
	return outputBits.to_ullong();
}

uint64_t to56BitKey(uint64_t input)
{
	const std::bitset<64> keyBits(input);
	std::bitset<56> outputBits(0);
	for (int8_t i = 0; i < 56; i++)
		outputBits[i] = keyBits[i / 7uI64 + i + 1uI64];
	return outputBits.to_ullong();
}

void attack(DES oracle, const uint64_t startKey = 0uI64, const uint64_t endKey = 0x100000000000000I64)
{
	const uint64_t block = 0x0uI64;
	const uint64_t targetCiphertext = oracle.encrypt(block);

	std::cout << std::hex;
	std::cout << "Searching for target chiphertext 0x" << targetCiphertext << " for block 0x" << block << " between 0x" << startKey << " and 0x" << endKey << " on thread ID 0x" << std::this_thread::get_id() << ".\n";
	
	for (uint64_t i = startKey; i < endKey; i++)
	{
		if (i % 0x1000000 == 0) std::cout << "Searched " << i - startKey << " keys out of " << endKey - startKey << " on thread " << std::this_thread::get_id() << ".\n";
		const uint64_t key = to64BitKey(i);
		const uint64_t ciphertext = DES::encrypt(block, key);
		if (ciphertext == targetCiphertext)
		{
			std::cout << "Found key: 0x" << std::hex << key << " (0x" << i << ") on thread 0x" << std::this_thread::get_id() << "\n";
			exit(0);
		}
	}
}

int main()
{
	// const uint64_t block0 = 0x903408ec4d951acfull;
	// const uint64_t block1 = 0xaeb47ca88390c475ull;
	//
	// const uint64_t outBlock0 = DES::decrypt(block0, key);
	// const uint64_t outBlock1 = DES::decrypt(block1, key);

	// char out0[9] = { 0, 0, 0, 0, 0, 0, 0, 0, 0 };
	// for (int i = 0; i < 8; ++i)
	// 	out0[7 - i] = static_cast<char>(outBlock0 >> 8 * i & 0xff);
	// out0[8] = 0;
	//
	// char out1[9] = { 0, 0, 0, 0, 0, 0, 0, 0, 0 };
	// for (int i = 0; i < 8; ++i)
	// 	out1[7 - i] = static_cast<char>(outBlock1 >> 8 * i & 0xff);
	// out1[8] = 0;
	//
	// printf("%llx [%llx]-> %llx [%s]\n", block0, key, outBlock0, out0);
	// printf("%llx [%llx]-> %llx [%s]\n", block1, key, outBlock1, out1);
	//
	// cout << out0 << out1 << "\n";

	const uint64_t key = to56BitKey(0x98a1bef23455dc03uI64);
	std::cout << std::hex << key << "\n"; // 0x9942ff934ab701uI64
	
	const DES oracle(0x98a1bef23455dc03uI64);
	// attack(oracle);

	const uint64_t start = 0uI64, end = 0x100000000000000i64, range = end - start, perWorker = range / 8I64;

	std::thread workers[8];
	for (int i = 0; i < 8; i++)
	{
		uint64_t workerStart = start + i * perWorker, workerEnd = workerStart + perWorker;
		workers[i] = std::thread(attack, oracle, workerStart, workerEnd);
	}

	// std::thread th(attack, oracle, 0x9942ff934ab701uI64, 0x9942ff934ab702uI64);
	//
	// th.join();
	
	for (int i = 0; i < 8; i++)
		workers[i].join();

	return 0;
}
