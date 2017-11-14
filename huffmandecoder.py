from huffmannode import Node
import settings

class HuffmanDecoder:

    def __init__(self ,root):
        self.root_node = root



    # String String -> void
    # Read encoded message in given path encoded_huffman form and then decode it
    # Write the decoded message to file at given path
    def decode_and_write_to_path(self ,path_to_decode ,path_to_write):

        file_to_decode = open(path_to_decode ,"rb")
        file_to_write  = open(path_to_write ,"w")
        key_to_decode = open(path_to_decode + settings.KEY_FILE_SUFFIX, "r")


        encoded_mes_in_bits = ""

        key = key_to_decode.read()
        self.generate_node_tree(key[1:] ,key[0:1])

        byte_list= list(file_to_decode.read())

        padded_var = byte_list[-1] == 1

        if padded_var:
            full_byte_upperbound = len( byte_list) - 2
        else:
            full_byte_upperbound = len( byte_list) - 1 # If all bytes are perfectly fit, only the padded_var is discarded

        for index in range(0,full_byte_upperbound):
            bitstring = HuffmanDecoder.int_to_8bitstring(byte_list[index])
            encoded_mes_in_bits += bitstring


        if padded_var:
            encoded_mes_in_bits += bin(byte_list[-2])[3:]
        # The first padded 1 bit is ignored, otherwise it disrupts the information being encrypted
        # print(encoded_mes_in_bits)

        print("decoding...")
        decoded_message = self.decode(encoded_mes_in_bits)

        file_to_write.write(decoded_message)

        file_to_write.close()
        file_to_decode.close()
        key_to_decode.close()


    @staticmethod
    # Int -> String
    # Convert the given integer to an 8-bit string
    # Adds 0's on the left of the string
    # until it has 8 bits
    # Given:  31
    # Wanted: "00011111"
    def int_to_8bitstring(n):

        if not (0 <= n <= 255):
            raise Exception("Input int out of bounds : ", n)

        eight_bitstring = ""

        for bit_index in range(0,8) :
            bit_value = 2** (7 - bit_index)
            if n >= bit_value:
                eight_bitstring += "1"
                n -= bit_value
            else:
                eight_bitstring += "0"

        return eight_bitstring



    # String Node -> String
    # Uses given root-node and the huffman code tree it contains
    # to decode given message (ex: "001100111010110......")
    def decode(self, encoded_message):

        lobits = encoded_message

        # Node N -> Tuple(String,N)
        # Traversing through the Node based on the given bit_index
        # Return a tuple of current node's character and current bit_index
        # TERMINATION: When Node's char field is a Character
        def decode_one_char(node, bit_index):

            if node.char:
                return (node.char, bit_index)

            else:
                current_bit = lobits[bit_index]
                if current_bit == "0":
                    return decode_one_char(node.left, bit_index + 1)
                else:
                    return decode_one_char(node.right, bit_index + 1)

        index = 0
        decoded_message = ""
        index_boundary = len(encoded_message)

        while (index < index_boundary - 1):
            print("decoding ", index, " out of ", index_boundary)

            tuple_of_sn = decode_one_char(self.root_node, index)
            decoded_message += tuple_of_sn[0]
            index = tuple_of_sn[1]

        return decoded_message

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

            current_node_char= lochar.pop(0)

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


        root_node = generate_node_tree_accu(list(string))


        self.root_node = root_node
