import unittest
from huffmancode import HuffmanCode



class huffmancodeTestings(unittest.TestCase):


    def setUp(self):
        self.message = "So we beat on, boats against the current, borne back, ceaselessly into the past."
        self.huffmancode = HuffmanCode(self.message)




    def est_get_frequency_dict(self):

        print(len(self.message))
        print(self.huffmancode.frequency_dict)
        sum = 0
        for key in self.huffmancode.frequency_dict.keys():
            sum += self.huffmancode.frequency_dict[key]
        print(sum)

    def est_get_ordered_lon(self):

        for node in self.huffmancode.ordered_lon:
            print(node)


    def est_get_root_node(self):

        # Node -> Void
        # Prints out the node tree described by given root node
        # The nodes should be printed in increasing order of their respective frequency
        def print_out_node_tree(root):

            if root.char:
                print("   ", end="")
                print(root)
            else:
                print(" ", end="")
                print_out_node_tree(root.left)
                print("   ", end="")
                print_out_node_tree(root.right)


        print_out_node_tree(self.huffmancode.root_node)
        print(self.huffmancode.root_node)

    def test_generate_encoding_map(self):

        print(self.huffmancode.char_to_code_dict)


    def est_encode(self):

        self.huffmancode.encode()
        print(self.huffmancode.encoded_message)
        print(self.huffmancode.encoded_message.__len__())


    def est_decode(self):
        self.huffmancode.encode()

        print(self.huffmancode.decode(self.huffmancode.encoded_message,self.huffmancode.root_node))

    def test_fillup_to_8bits(self):

        self.assertEqual(HuffmanCode.fillup_to_8bits("001101"),"00001101")

if __name__ == "__main__":
    unittest.main()
