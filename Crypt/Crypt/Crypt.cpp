// Crypt.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "./des.h"

int main()
{
	const unsigned long long key = 0x98a1bef23455dc03ull;
	
	unsigned long long block = 0x0123456789abcdefull;
	
	printf("%llx -> %llx", key, DES::encrypt(block, key));

	return 0;
}
