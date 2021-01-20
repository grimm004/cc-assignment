# Test your encoder and decoder with input file specified by the user

# Usage: python testEncoderDecoder.py testFile
# where testFile.tex is the name of the input tex file

import os
import sys
import zipfile

testFile = sys.argv[1]
inputFile = testFile + ".tex"
encodedFile = testFile + ".lz"
zipEncodedFile = testFile + ".zip"
decodedFile = testFile + "-decoded.tex"

# Size of input file
inputSize = os.path.getsize(inputFile)
print("Input file: \t{0}".format(inputFile))
print("Input size: \t{0}\n".format(str(inputSize)))

# Create zip file as benchmark
with zipfile.ZipFile(zipEncodedFile, "w", zipfile.ZIP_DEFLATED) as zipFile:
    zipFile.write(inputFile)
zipEncodedSize = os.path.getsize(zipEncodedFile)
print("Encoded zip file: \t{0}".format(zipEncodedFile))
print("Encoded zip size: \t{0}\n".format(str(zipEncodedSize)))

# Runs your encoder and prints out size of encoded file
os.system("python encoder.py " + inputFile)
encodedSize = os.path.getsize(encodedFile)
print("Encoded file: \t{0}".format(encodedFile))
print("Encoded size: \t{0}\n".format(str(encodedSize)))

# Runs your decoder and prints out size of decoded file
os.system("python decoder.py " + encodedFile)
decodedSize = os.path.getsize(decodedFile)
print("Decoded file: \t{0}".format(decodedFile))
print("Decoded size: \t{0}\n".format(str(decodedSize)))

# Checks whether input and decoded files have the same size
if decodedSize != inputSize:
    print("ERROR: Incorrect decoded file size")
else:
    # Checks that input and decoded files are the same
    if open(inputFile, 'r').read() != open(decodedFile, 'r').read():
        print("\n ERROR: Incorrect decoded file contents")
    else:
        # Files are the same.
        print("\nSUCCESS: Lossless compression")
        print("COMPRESSION RATIO: \t{0}\t [zip {1}]".format(str(inputSize / encodedSize),
                                                            str(inputSize / zipEncodedSize)))
