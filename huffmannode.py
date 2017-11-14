

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

