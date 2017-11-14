import math
import numpy



class Node:

    def __init__(self,char=False,left=None,right=None,frequency=0):
        self.char      = char
        self.left      = left
        self.right     = right
        self.frequency = frequency



    def __str__(self):

        return "Node with char " + str(self.char) + ", and frequency " + str(self.frequency)


    # Node -> String
    # Returns the string representation of the node tree described by given root node
    # The nodes should be printed in increasing order of their respective frequency
    def get_node_tree_string(root):

        def get_node_tree_string_accu(current_root,prefix):

            str = ""

            if current_root.char:
                str  = prefix + current_root.__str__()

            else:

                str = prefix + get_node_tree_string_accu(current_root.left,prefix + "  ")
                str += "\n"

                str += prefix + get_node_tree_string_accu(current_root.right, prefix + "  ")
                str += "\n"

            return str

        return get_node_tree_string_accu(root,"")



class HuffmanEncoder:

    def __init__(self,message):

        self.__secretMessage = message

        self.frequency_dict = self.get_frequency_dict(message)

        self.ordered_lon = self.get_ordered_lon(self.frequency_dict)

        self.root_node = self.get_root_node(self.ordered_lon)

        self.char_to_code_dict = self.generate_encoding_map(self.root_node)

        self.generate_decoding_key_message()

        self.encode_to_binary()






    # Encode the secretMessage given at construction of HuffmanCode Instance
    # The encoded message is held in the instance variable self.encoded_message
    def encode_to_binary(self):

        message_holder = ""

        chars_tobe_encoded = list(self.__secretMessage)

        while(len(chars_tobe_encoded) > 0):

            message_holder += self.char_to_code_dict[chars_tobe_encoded.pop(0)]

        self.encoded_binary_message = message_holder


    # String -> void
    # Write encoded message in terms of bytes into file
    # at given path in binary form.
    def write_encoded_message_to_path(self,path_to_write):
        encoded_file = open(path_to_write,"wb")

        binary_code = self.encoded_binary_message

        list_of_base10_code = []

        number_of_full_bytes = len(binary_code) // 8

        for index in range(0,number_of_full_bytes):
            list_of_base10_code.append(int(binary_code[0:8],2))
            binary_code = binary_code[8:]

        if binary_code:
            list_of_base10_code.append(int(binary_code,2))

        # The 0 digits at the front of bytes are eliminated here
        # Therefore, they must be padded back when converting byte to 8-bit bitstring

        header_key_message = self.decoding_key_message + "\n"


        encoded_file.write(header_key_message.encode() + bytes(list_of_base10_code))
        encoded_file.close()





    # String -> Dictionary{(char : frequency}
    # Counts and collects the frequency of each character in
    # a given string, then store character as key to its corresponding frequency
    # in a dictionary
    # Given:  f("aabc")
    # Wanted: {"a" : 2, "b" : 1, "c" : 1}

    @staticmethod
    def get_frequency_dict(string):

        frequency_dict = {}

        for index in range(0,len(string)):
            current_char = string[index]

            if current_char in frequency_dict:
                frequency_dict[current_char] += 1
            else:
                frequency_dict[current_char] = 1


        return frequency_dict



    # Dictionary{(char : frequency} -> [List-of Node]
    # Make a list of Node based by mapping each character key and
    # frequency value in given dictionary to a unique Node's char and frequency fields
    # Given:  {"a" : 2, "b" : 1, "c" : 1}
    # Wanted: [Node(char = "a", frequency = 2), Node(char = "b", frequency = 1), Node(char = "c", frequency = 1)
    @staticmethod
    def get_ordered_lon(fdict):

        lon = []

        for key in fdict:
            node = Node(char=key,frequency=fdict[key])
            HuffmanEncoder.insert_node(lon,node)

        return lon


    @staticmethod
    # [List-of Node] Node -> [List-of Node]
    # Insert a node into given list-of node so that
    # the resulting lon is ordered based on Node Frequency, from lowest to highest
    # ASSUME: given lon is already sorted
    def insert_node(given_lon, a_node):

        for index in range(0,len(given_lon)):
            if a_node.frequency <= given_lon[index].frequency:
                given_lon.insert(index,a_node)
                return given_lon

        given_lon.append(a_node) # At this point, given node must have a higher frequency than all nodes in lon

        return given_lon


    @staticmethod
    # [List-of Node] -> Node
    # Applying HuffmanCode to encode the characters in given nodes with their
    # respective frequency.
    # Return the root Node which can be used as a starting point for decoding
    def get_root_node(lon):

        lon = lon.copy()

        while(len(lon) > 1):

            # Left and Right node represents the nodes with
            # lowest and second lowest frequency respectively

            right_node = lon.pop(0)
            left_node  = lon.pop(0)

            # Combine these nodes into a sub-section of one new node,
            # and insert this node back into lon for further processing
            combined_node = Node(left= left_node, right= right_node, frequency= left_node.frequency + right_node.frequency)

            HuffmanEncoder.insert_node(lon, combined_node)

        # Finally return the single root node (it implicitly contains the entire tree of nodes)
        return lon[0]


    @staticmethod
    # Node -> Dictionary{( Character : Code)}
    # Code is a string sequence of 1 and 0's, such as "0011"
    # Convert given root node, and the node tree it carries, into a
    # encoding map that converts character into Code based on huffman code
    def generate_encoding_map(root):

        encoding_dictionary = {}

        # Node Code -> Void
        # The work-horse of generate_encoding_map function
        # it uses Code as an accumulator to code each node
        # TERMINATION : When a node is at the end of a node tree >> It holds a character, instead of connecting to two other nodes
        # ASSUME      : The node tree carried by root is not self referential, meaning there's no circular path that may results in
        #               an infinite loop
        def generate_dict(root, code):

            if root.char:
                encoding_dictionary[root.char] = code
            else:
                generate_dict(root.left, code + "0")
                generate_dict(root.right, code + "1")

        generate_dict(root,"")

        return encoding_dictionary



    # Node -> String
    # Generate a sequence of String that serves as
    # a decoding key so that receiver of the key and encoded message
    # can decode the message based on huffman code
    # Idea: Node that contains a char is represented by the char
    #       Node that contains two other nodes is represented by ???(THIS IS DIFFICULT)
    #TODO: cannot find a good sentinel to represent place-holder nodes, because if that character is contained in original text, it messes up the encryption
    #       Split into two classes: encoder and decoder
    def generate_decoding_key_message(self):

        key = ""
        most_left_node = self.root_node
        while(most_left_node.char == False):

            most_left_node = most_left_node.left


        if "a" == most_left_node.char:
            initial_indentifier = "b"
        else:
            initial_indentifier = "a"


        identifier = [initial_indentifier]
        passed_most_left = [False]

        # Node -> Void
        # The Workhorse for generate_decoding_key_message function
        # It analyzes given node and print out the node's char(identifier if it's char is False)
        # in order to form an entire message that allows decoder to duplicate the huffman node tree and decode hoffman code
        def generate_key_message_accu(node):
            current_node_char = node.char
            #print(current_node_char)
            key = ""

            if passed_most_left[0]:

                if current_node_char == False:
                    key += (identifier[0])
                    key += generate_key_message_accu(node.left)
                    key += generate_key_message_accu(node.right)
                else:
                    key += current_node_char

            else:
                if current_node_char == False:
                    key += (identifier[0])
                    key += generate_key_message_accu(node.left)
                    key += generate_key_message_accu(node.right)
                else:
                    # This single case indicates encoutering the left-most node
                    passed_most_left[0] = True
                    identifier[0] = current_node_char
                    key += current_node_char

            return key


        self.decoding_key_message = initial_indentifier + generate_key_message_accu(self.root_node)




class HuffmanDecoder:

    def __init__(self,root):
        self.root_node = root



    # String String -> void
    # Read encoded message in given path binary form and then decode it
    # Write the decoded message to file at given path
    def decode_and_write_to_path(self,path_to_decode,path_to_write):

        file_to_decode = open(path_to_decode,"rb")
        file_to_write  = open(path_to_write,"w")

        encoded_mes_in_bits = ""

        header = file_to_decode.readline().decode()
        self.generate_node_tree(header[1:],header[0:1])

        byte_list= list(file_to_decode.read())

        for index in range(0,len(byte_list) - 1):
            bitstring = HuffmanDecoder.int_to_8bitstring(byte_list.pop(0))
            encoded_mes_in_bits += bitstring

        encoded_mes_in_bits += bin(byte_list[0])[2:]
        # The last bits which are not padded, otherwise it disrupts the information being encrypted

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

        if not (0 <= n <= 255):
            raise Exception("Input int out of bounds : ", n)

        eight_bitstring = ""

        for bit_index in range(0,8):
            bit_value = 2**(7-bit_index)
            if n >= bit_value:
                eight_bitstring += "1"
                n -= bit_value
            else:
                eight_bitstring += "0"

        return eight_bitstring



    # String Node -> String
    # Uses given root-node and the huffman code tree it contains
    # to decode given message (ex: "001100111010110......")
    def decode(self,encoded_message):

        lochar = []
        lobits= list(encoded_message)

        # [List-of Char] Node-> Void
        # Traversing through the Node by following the
        # list of characters, once an end is reached,
        # append the character to message variable above
        # TERMINATION: When Node's char field is a Character, or when bits_tobe_decoded is ran out
        def decode_one_char(bits_tobe_decoded, node):

            if node.char:
                lochar.append(node.char)
                return
            elif len(bits_tobe_decoded) == 0:
                if node is not self.root_node:
                    raise Exception("This Huffman Code cannot be decoded, either input encrypted message or node tree is wrong")
                else:
                    return
            else:
                current_bit = bits_tobe_decoded.pop(0)
                if current_bit == "0":
                    decode_one_char(bits_tobe_decoded, node.left)
                else:
                    decode_one_char(bits_tobe_decoded, node.right)


        while(len(lobits) > 0):

            decode_one_char(lobits,self.root_node)

        return "".join(lochar)

    # String Character-> Node
    # Take in a String sequence that contains the information to
    # generate a node tree which can decode a specific type of
    # Huffman Code. Use the char as identifier for node that contains no character
    #
    def generate_node_tree(self, string, char):
        
        passed_most_frequent = [False]
        identifier = [char]


        #[List-of Char] Char -> Node
        # Use given identifier for node that contains no character
        # to traverse through the string and build a node-tree for huffman code decoding
        def generate_node_tree_accu(lochar):

            current_node_char= lochar.pop(0)
            #print(current_node_char)

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
