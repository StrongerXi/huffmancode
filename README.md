# huffmancode

This program enables compression/decompression through huffman code.

Text to be compressed should be written into "textfile"

Compressed file consists of two unit files:

1. A file that contains key information for decompresser to reconstruct a huffman tree. ("encoded_huffmansuffix")
2. A file that contains the compressed content encoded in bytes. 
    ("encoded_huffman") (not easily readable) 

Decompressed file is named "decoded"

Another file has been made available for those who are curious to the process of compressing/decompressing:

"readable_binary_huffman": A readable huffman code file of textfile, with 1's and 0's'

