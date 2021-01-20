// Crypt.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "./des.h"

int main()
{
	const unsigned long long key = 0x98a1bef23455dc03ull;

	const unsigned long long testBlock = 0x0123456789abcdefull;
	const unsigned long long block0 = 0x903408ec4d951acfull;
	const unsigned long long block1 = 0xaeb47ca88390c475ull;

	const unsigned long long outBlock0 = DES::decrypt(block0, key);
	const unsigned long long outBlock1 = DES::decrypt(block1, key);

	char out0[9] = { 0, 0, 0, 0, 0, 0, 0, 0, 0 };
	for (int i = 0; i < 8; ++i)
		out0[7 - i] = static_cast<char>(outBlock0 >> 8 * i & 0xff);
	out0[8] = 0;

	char out1[9] = { 0, 0, 0, 0, 0, 0, 0, 0, 0 };
	for (int i = 0; i < 8; ++i)
		out1[7 - i] = static_cast<char>(outBlock1 >> 8 * i & 0xff);
	out1[8] = 0;

	printf("%llx [%llx]-> %llx [%s]\n", block0, key, outBlock0, out0);
	printf("%llx [%llx]-> %llx [%s]\n", block1, key, outBlock1, out1);
	
	cout << out0 << out1 << "\n";

	return 0;
}
