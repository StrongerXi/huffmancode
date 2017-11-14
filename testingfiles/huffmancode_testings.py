import unittest
from huffmanencoder import HuffmanEncoder
from huffmandecoder import HuffmanDecoder



class huffmancodeTestings(unittest.TestCase):


    def setUp(self):
        self.message = "Hello World\nhey"
        self.huffmanencoder = HuffmanEncoder(self.message)
        self.huffmandecoder = HuffmanDecoder(self.huffmanencoder.root_node)



    def est_get_frequency_dict(self):

        print(len(self.message))
        print(self.huffmanencoder.frequency_dict)
        sum = 0
        for key in self.huffmanencoder.frequency_dict.keys():
            sum += self.huffmanencoder.frequency_dict[key]
        print(sum)

    def test_get_ordered_lon(self):

        for node in self.huffmanencoder.ordered_lon:

            print("lon",node.__str__())


    def test_get_root_node(self):

        print(self.huffmanencoder.root_node.get_node_tree_string())


    def est_generate_encoding_map(self):

        print(self.huffmanencoder.char_to_code_dict)


    def est_encode(self):

        print(self.huffmanencoder.encoded_binary_message)
        print(self.huffmanencoder.encoded_binary_message.__len__())


    def test_decode(self):
        self.huffmandecoder.generate_node_tree("aaaaWrWH WWhyWd\nWWeol","a")

        print(self.huffmandecoder.decode(self.huffmanencoder.encoded_binary_message))


    def est_int_to_8bitstring(self):

        self.assertEqual(HuffmanDecoder.int_to_8bitstring(13),"00001101")
    
    def est_generate_node_tree(self):
        
        self.huffmandecoder.generate_node_tree("**ABACD","*")
        print(self.huffmandecoder.root_node.get_node_tree_string())

        self.huffmanencoder.generate_decoding_key_message()
        self.huffmandecoder.generate_node_tree(self.huffmanencoder.decoding_key_message[1:], self.huffmanencoder.decoding_key_message[0])
        print(self.huffmandecoder.root_node.get_node_tree_string())



    def test_generate_decoding_key_message(self):

        self.huffmanencoder.generate_decoding_key_message()
        print(self.huffmanencoder.decoding_key_message)



if __name__ == "__main__":
    unittest.main()
