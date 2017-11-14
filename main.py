from huffmancode import HuffmanCode



text = open("textfile","r")
huffmanbinaryfile = open("huffmancode","w")

message = text.read()
#print(message)
#print("quit")



huffman = HuffmanCode(message)
huffman.write_encoded_message_to_path("binary")
huffman.decode_and_write_to_path("binary","decoded")

huffmanbinaryfile.write(huffman.encoded_binary_message)

#print(huffman.get_encoded_message())
#print(huffman.get_encoded_message().__len__())


#print(huffman.char_to_code_dict)

#codefile.write(huffman.get_encoded_message())


text.close()
huffmanbinaryfile.close()
