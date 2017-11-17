from huffmannode import Node
from collections import deque

class HuffmanDecoder:

    def __init__(self ,root):
        self.root_node = root



    # String String -> void
    # Read encoded message in given path encoded_huffman form and then decode it
    # Write the decoded message to file at given path
    def decode_and_write_to_path(self ,path_to_decode ,path_to_write):

        file_to_decode = open(path_to_decode ,"rb")
        file_to_write  = open(path_to_write ,"w")



        encoded_mes_in_bits = []

        key_length = file_to_decode.readline().decode()
        key_length = int( key_length[:len(key_length)-1]) # This eliminates the '\n' character at the end which helps identify end of the number to read

        initial_identifier = file_to_decode.read(1).decode()

        key_for_tree_construction = file_to_decode.read(key_length-1).decode() # key_length-1 because initial identifier is already read.

        #print("key message: ", key_for_tree_construction)

        self.generate_node_tree(key_for_tree_construction ,initial_identifier)

        byte_list= list(file_to_decode.read())

        #print("received base 10 code", byte_list)

        padded_var = byte_list[-1] == 1

        if padded_var:
            full_byte_upperbound = len( byte_list) - 2
        else:
            full_byte_upperbound = len( byte_list) - 1 # If all bytes are perfectly fit, only the padded_var is discarded

        for index in range(0,full_byte_upperbound):
            #print("converting ", index, " bytes out of ", full_byte_upperbound)
            bitstring = HuffmanDecoder.int_to_8bitstring(byte_list[index])
            #print(bitstring)
            encoded_mes_in_bits.append(bitstring)

        encoded_mes_in_bits = "".join(encoded_mes_in_bits)


        if padded_var:
            encoded_mes_in_bits += bin(byte_list[-2])[3:]
            #print(bin(byte_list[-2])[3:])
        # The first padded 1 bit is ignored, otherwise it disrupts the information being encrypted

        #print("encoded_bits_read: ", encoded_mes_in_bits)

        print("decoding...")
        decoded_message = self.decode(encoded_mes_in_bits)

        file_to_write.write(decoded_message)

        file_to_write.close()
        file_to_decode.close()

    @staticmethod
    # Int -> String
    # Convert the given integer to an 8-bit string
    # Adds 0's on the left of the string
    # until it has 8 bits
    # Given:  31
    # Wanted: "00011111"
    def int_to_8bitstring(n):

        eight_bitstring = bin(n)[2:]

        pad_size = 8 - len(eight_bitstring)

        eight_bitstring = "0"*pad_size + eight_bitstring

        return eight_bitstring



    # String Node -> String
    # Uses given root-node and the huffman code tree it contains
    # to decode given message (ex: "001100111010110......")
    def decode(self, encoded_message):

        lobits = deque(encoded_message)

        # If root node contains an actual character, this means encrypted message only contains that character since no
        # node that contains character could connect to further nodes
        # In this trivial case, return the same number of the character as there are digits in encoded_message immediately.
        if self.root_node.char:
            return self.root_node.char * len(encoded_message)


        # Node -> Character
        # Traversing through the Node based on the global lobits in the outside function decode
        # Return a tuple of current node's character and current bit_index
        # TERMINATION: When Node's char field is a Character
        def decode_one_char(node):

            while(not node.char):
                if lobits.popleft() == "0":
                    node = node.left
                    continue
                else:
                    node = node.right
                    continue

            return node.char


        index = 0
        decoded_message = []
        index_boundary = len(encoded_message)

        while (lobits):
            #print("decoding ", index, " out of ", index_boundary)

            char = decode_one_char(self.root_node)
            decoded_message.append(char)
            #index = index_boundary - lobits.__len__()

            #print("decoded char: ", decoded_message)

            #print("index: ", index)

        return "".join(decoded_message)







    # String Character-> Node
    # Take in a String sequence that contains the information to
    # generate a node tree which can decode a specific type of
    # Huffman Code. Use the char as identifier for node that contains no character
    #
    def generate_node_tree(self, string, char):

        passed_most_frequent = [False]
        identifier = [char]

        # [List-of Char] Char -> Node
        # Use given identifier for node that contains no character
        # to traverse through the string and build a node-tree for huffman code decoding
        def generate_node_tree_accu(lochar):

            current_node_char= lochar.popleft()

            if passed_most_frequent[0]:

                if current_node_char == identifier[0]:
                    node = Node(char=False)
                else:
                    node = Node(char=current_node_char)
                    return node


            else:
                if current_node_char == identifier[0]:
                    node = Node(char=False)
                else:
                    identifier[0] = current_node_char
                    node = Node(char=current_node_char)
                    passed_most_frequent[0] = True

                    return node

            left_node = generate_node_tree_accu(lochar)
            right_node= generate_node_tree_accu(lochar)



            node.left  = left_node
            node.right = right_node
            return node


        root_node = generate_node_tree_accu(deque(string))


        self.root_node = root_node
