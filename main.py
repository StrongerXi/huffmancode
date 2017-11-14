from huffmancode import HuffmanEncoder, HuffmanDecoder



text = open("textfile","r")
huffmanbinaryfile = open("huffmancode","w")

message = text.read()
#print(message)
#print("quit")



huffmanencode = HuffmanEncoder(message)
huffmanencode.write_encoded_message_to_path("binary")

huffmandecode = HuffmanDecoder(huffmanencode.root_node)
huffmandecode.decode_and_write_to_path("binary","decoded")

huffmanbinaryfile.write(huffmanencode.encoded_binary_message)

#print(huffman.get_encoded_message())
#print(huffman.get_encoded_message().__len__())


#print(huffman.char_to_code_dict)

#codefile.write(huffman.get_encoded_message())


text.close()
huffmanbinaryfile.close()
