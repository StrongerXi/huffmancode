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




class HuffmanCode:

    def __init__(self,message):

        self.__secretMessage = message

        self.frequency_dict = self.get_frequency_dict(message)

        self.ordered_lon = self.get_ordered_lon(self.frequency_dict)

        self.root_node = self.get_root_node(self.ordered_lon)

        self.char_to_code_dict = self.generate_encoding_map(self.root_node)

        self.encode_to_binary()



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

        encoded_file.write(bytes(list_of_base10_code))
        encoded_file.close()


    # String String -> void
    # Read encoded message in given path binary form and then decode it
    # Write the decoded message to file at given path
    def decode_and_write_to_path(self,path_to_decode,path_to_write):

        file_to_decode = open(path_to_decode,"rb")
        file_to_write  = open(path_to_write,"w")

        encoded_mes_in_bits = ""

        list_bytes_in_base10= list(file_to_decode.read())

        for index in range(0,len(list_bytes_in_base10) - 1):
            bitstring = bin(list_bytes_in_base10.pop(0))[2:]
            bitstring = self.fillup_to_8bits(bitstring)
            encoded_mes_in_bits += bitstring

        encoded_mes_in_bits += bin(list_bytes_in_base10[0])[2:] # The last bits which are not padded, otherwise it disrupts the information being encrypted

        decoded_message = self.decode(encoded_mes_in_bits,self.root_node)

        file_to_write.write(decoded_message)

        file_to_write.close()
        file_to_decode.close()


    @staticmethod
    # String -> string
    # Adds 0's on the left of given bitstring
    # until it has 8 bits
    def fillup_to_8bits(bitstring):

        if len(bitstring) < 8:
            bitstring = "0" + bitstring
            return HuffmanCode.fillup_to_8bits(bitstring)
        elif len(bitstring) == 8:
            return bitstring







    # Encode the secretMessage given at construction of HuffmanCode Instance
    # The encoded message is held in the instance variable self.encoded_message
    def encode_to_binary(self):

        message_holder = ""

        chars_tobe_encoded = list(self.__secretMessage)

        while(len(chars_tobe_encoded) > 0):

            message_holder += self.char_to_code_dict[chars_tobe_encoded.pop(0)]

        self.encoded_binary_message = message_holder



    @staticmethod
    # String Node -> String
    # Uses given root-node and the huffman code tree it contains
    # to decode given message (ex: "001100111010110......")
    def decode(encoded_message,root):

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
                if node is not root:
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

            decode_one_char(lobits,root)

        return "".join(lochar)



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
            HuffmanCode.insert_node(lon,node)

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

        while(len(lon) > 1):

            # Left and Right node represents the nodes with
            # lowest and second lowest frequency respectively

            left_node  = lon.pop(0)
            right_node = lon.pop(0)

            # Combine these nodes into a sub-section of one new node,
            # and insert this node back into lon for further processing
            combined_node = Node(left= left_node, right= right_node, frequency= left_node.frequency + right_node.frequency)

            HuffmanCode.insert_node(lon, combined_node)

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
    def generate_decoding_key_message(root):

        key = ""
        pass

        # Node -> Void
        # The Workhorse for generate_decoding_key_message function
        # It analyzes given node and
