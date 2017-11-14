from huffmanencoder import HuffmanEncoder
from huffmandecoder import HuffmanDecoder


text = open("files/textfile","r")
huffmanbinaryfile = open("files/readable_binary_huffman","w")

message = text.read()


huffmanencode = HuffmanEncoder(message)
huffmanencode.write_encoded_message_to_path("files/encoded_huffman")
print("encoding finished")

huffmanbinaryfile.write(huffmanencode.encoded_binary_message)

huffmandecode = HuffmanDecoder(None)

huffmandecode.decode_and_write_to_path("files/encoded_huffman","files/decoded")
print("decoding finished")

text.close()
huffmanbinaryfile.close()