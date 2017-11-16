
from huffmannode import Node



class HuffmanEncoder:

    def __init__(self,message):

        self.__secretMessage = message

        if message:

            self.frequency_dict = self.get_frequency_dict(message)

            self.ordered_lon = self.get_ordered_lon(self.frequency_dict)
            print("nodes generated")

            self.root_node = self.get_root_node(self.ordered_lon)
            print("node tree generated")

            self.char_to_code_dict = self.generate_encoding_map(self.root_node)
            print("encoding map generated")

            self.generate_decoding_key_message()
            print("decoding key message generated")

            self.encode_to_binary()
            print("binary code generated")

        else:
            raise Exception("No input message. Cannot compress an empty file!!!")






    # Encode the secretMessage given at construction of HuffmanCode Instance
    # The encoded message is held in the instance variable self.encoded_message
    def encode_to_binary(self):

        message_holder = ""

        chars_tobe_encoded = list(self.__secretMessage)
        number_of_chars = len(chars_tobe_encoded)

        for index in range(0,number_of_chars):
            print("encoding: ", index, " out of ", number_of_chars)

            message_holder += self.char_to_code_dict[chars_tobe_encoded[index]]

        self.encoded_binary_message = message_holder


    # String -> void
    # Write encoded message in terms of bytes into file
    # at given path in encoded_huffman form.
    def write_encoded_message_to_path(self,path_to_write):

        encoded_file = open(path_to_write,"wb")

        binary_code = self.encoded_binary_message

        #print("bits encoded: ", binary_code)
        #print("map: ", self.char_to_code_dict)

        num_of_bits = len(binary_code)

        number_of_full_bytes = num_of_bits // 8
        left_over_bits = num_of_bits % 8
        list_of_base10_code = [None] * (number_of_full_bytes + 1)


        for index in range(0,num_of_bits,8):

            print("encoding: ", index, " bits out of ", num_of_bits)
            #print(index)
            list_of_base10_code[index//8] = (int(binary_code[index:index+8],2))

        if left_over_bits > 0:
            list_of_base10_code[-1] = int("1" + binary_code[num_of_bits - left_over_bits : ],2) # A 1 is padded at the front to prevent loss of any 0's on the left
            list_of_base10_code.append(1) # Meaning it's padded

        elif left_over_bits == 0:
            list_of_base10_code.pop() # The extra None element generated for potential leftover bits is not required if there's no leftover bits
            list_of_base10_code.append(0)
        else:
            raise Exception("Leftover bit error!!! : ", left_over_bits)


        # The 0 digits at the front of bytes are eliminated here
        # Therefore, they must be padded back when converting byte to 8-bit bitstring

        header_key_message = self.decoding_key_message

        #print("original base10 code: ",list_of_base10_code)

        header_message_length = str(len(header_key_message.encode())) + "\n" # "\n" character serves as a EOF for reading key_length

        header = (header_message_length + header_key_message).encode()

        #print("key header: ", header)

        #print(list_of_base10_code)

        encoded_file.write(header + bytes(list_of_base10_code))
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

        # If there's only a single node, encode the node as either 0 or 1.

        if root.char:
            encoding_dictionary[root.char] = "1"
        else:
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

