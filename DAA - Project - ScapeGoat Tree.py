import math
class TreeNode:
    def __init__(self, data, parent=None, left=None, right=None):
        self.data = data
        self.parent = parent
        self.left = left
        self.right = right

class ScapegoatTree:
    def __init__(self, root=None):
        self.scape_goat = None
        self.root = root
        self.n = self.q = 0
        self.alpha = 2/3

    #Insert function which then calls the main InsertNode function to insert the the value in tree
    #Takes tree node and value to insert as an argument
    def Insert(self, x, value):
        self.InsertNode(x, value)
        #if rebalanced is called and scapegoat is found then after re-balancing we have to set scapegoat node to None
        if self.scape_goat:
            self.scape_goat = None

    #Insert Node which takes root and value to insert as an argument it then traverse and approaches the appropriate
    #position to insert as in binary search the only difference is that if our tree in not alpha balanced then it
    #search scapegoat node then it runs in order traversal from our scapegoat node and then stores it in array.
    #After storing elements in array it the sets the children of the scapegoat parent whose child is scapegoat
    #to none and then runs re-build tree from scapegoat parent.
    def InsertNode(self, x, value):
        if self.root is None:
            self.n += 1
            self.q += 1
            self.root = TreeNode(value)
            return

        if value == x.data:
            return

        if value > x.data:
            #go right
            if x.right:
                self.InsertNode(x.right, value)
            else:
                self.n += 1
                self.q += 1
                x.right = TreeNode(value)
                x.right.parent = x
                return

        elif value < x.data:
            #go left
            if x.left:
                self.InsertNode(x.left, value)
            else:
                self.n += 1
                self.q += 1
                x.left = TreeNode(value)
                x.left.parent = x
                return

        if not self.Balanced():
            if self.scape_goat:     #if scape goat is already found then we have to skip further search
                return
            self.scape_goat = self.Scape_Goat_Search(x)     #search for the scape gaot in tree
            if self.scape_goat:
                print('Rebuilt starting for insertion..')
                sorted_arr = self.InOrder(x.parent)
                self.n -= len(sorted_arr)
                self.q -= len(sorted_arr)
                re_built_tree_node = x.parent.parent

                if re_built_tree_node.left == x.parent:
                    re_built_tree_node.left = None

                if re_built_tree_node.right == x.parent:
                    re_built_tree_node.right = None
                self.rebuild_tree_inorder_tvr(re_built_tree_node, sorted_arr)

    #A simple search function same as BST which returns the node having data same as value searched
    def Search(self, x, value):
        if value == x.data:
            return x

        if value > x.data:
            # go right
            if x.right:
                self.InsertNode(x.right, value)

        elif value < x.data:
            # go left
            if x.left:
                self.InsertNode(x.left, value)

    #Takes tree node which is parent of scapegoat and an array containing elements in sorted form then insert
    #the mid element of array dividing it into two halves halves and then doing the same till al the mid elements
    #of divided arrays are inserted
    def rebuild_tree_inorder_tvr(self, node, arr):
        start=0
        end=len(arr)
        if start >= end:
            return
        mid = start+end//2
        mid_ele = arr[mid]
        left = arr[:mid]
        right = arr[mid+1:]
        self.InsertNode(node, mid_ele)

        self.rebuild_tree_inorder_tvr(node, left)
        self.rebuild_tree_inorder_tvr(node, right)

    #Returns pre order traversal of tree same as in BST
    def PreOrder(self, x):
        ele=[]

        ele.append(x.data)

        if x.left:
            ele += self.PreOrder(x.left)

        if x.right:
            ele += self.PreOrder(x.right)

        return ele

    #Returns In order traversal of tree same as in BST
    def InOrder(self, x):
        ele = []

        if x.left:
            ele += self.InOrder(x.left)

        ele.append(x.data)

        if x.right:
            ele += self.InOrder(x.right)

        return ele

    #Returns Post order of tree same as in BST
    def PostOrder(self, x):
        ele = []

        if x.left:
            ele += self.PostOrder(x.left)

        if x.right:
            ele += self.PostOrder(x.right)

        ele.append(x.data)

        return ele

    #To calculate height of tree takes a node as parameter goes to the leaf node and then return the one plus
    #value of each node either left or right if its length is greater than the other root height is 1 so is
    #called from other function.
    def Calculate_height(self, x):
        if x is None:
            return 0

        else:
            lDepth = self.Calculate_height(x.left)
            rDepth = self.Calculate_height(x.right)

            if (lDepth > rDepth):
                return lDepth + 1
            else:
                return rDepth + 1

    #Return -1 from the height so that the root node height is cancelled.
    def Height(self, root):
        h_tree = self.Calculate_height(root)
        return h_tree-1

    #Returnes number of node under that particular node.
    def sizeOfSubtree(self, node):
        if node == None:
            return 0
        return 1 + self.sizeOfSubtree(node.left) + self.sizeOfSubtree(node.right)

    #function to check whether the tree is alpha balanced or not returns true if not then false
    #Height < log (1/alpha) * n for a balanced tree.
    def Balanced(self):
        if (self.Height(self.root)) > (math.log(self.n, (1/self.alpha))):
            return False
        return True

    #Scapegoat search function checks if size(x)/size(x.parent) is greater than alpha if so then its scapegoat node
    def Scape_Goat_Search(self, x):
        try:
            chk = self.sizeOfSubtree(x)/self.sizeOfSubtree(x.parent)
            if chk > self.alpha:
                return x.parent
        except ZeroDivisionError:
            return

    #returns the minimum node form the given tree node
    def MinNode(self, x):
        if x is None:
            return
        while x:
            if x.left is None:
                return x
            x = x.left

    #Delete function to call Delete node which then deleted node from the tree and then delete function checks if
    #after deletion n is smaller that half of q if so then rebuilds tree in same way as insert by storing it in
    #array and adding mid elements using build form tree in order traversal.
    def delete(self, root, x):
        self.Delete_Node(root, x)

        if self.n < self.q/2:
            print('Rebuild starting for deletion..')
            sorted_array=self.InOrder(self.root)
            self.root = None
            self.root = TreeNode(sorted_array[(len(sorted_array)//2)])
            print(sorted_array)
            self.q = self.n = 1
            self.rebuild_tree_inorder_tvr(self.root, sorted_array)

    #Deletes node from the given node of tree or tree by finding the node then copying its right node minimum
    #node and the deleting that node.
    def Delete_Node(self, root, x):
        if root is None:
            return root

        if x < root.data:
            root.left = self.Delete_Node(root.left, x)
        elif (x > root.data):
            root.right = self.Delete_Node(root.right, x)

        else:
            if root.left is None:
                self.n -= 1
                temp = root.right
                root = None
                return temp

            elif root.right is None:
                self.n -= 1
                temp = root.left
                root = None
                return temp

            temp = self.MinNode(root.right)
            root.data = temp.data
            root.right = self.Delete_Node(root.right, temp.data)

        return root

if __name__=='__main__':
    b = ScapegoatTree()
    b.Insert(b.root, 12)
    b.Insert(b.root, 11)
    b.Insert(b.root, 13)
    b.Insert(b.root, 10)
    b.Insert(b.root, 14)
    b.Insert(b.root, 7)
    b.Insert(b.root, 6)
    b.Insert(b.root, 9)
    b.Insert(b.root, 5)
    b.Insert(b.root, 8)
    # print(b.Search(b.root, 12))

    print(b.InOrder(b.root))
    # print(f'pre order {b.PreOrder(b.root)}')
    # print(b.n)
    # print(b.q)
    print(f"The height before is :{b.Height(b.root)}")
    print(f"Is a balanced tree :{b.Balanced()}")

    "''____Rebuild Insert Value____''"
    b.Insert(b.root, 8.5)

    # b.delete(b.root, 7)
    # b.delete(b.root, 10)
    # b.delete(b.root, 6)
    # b.delete(b.root, 14)
    # b.delete(b.root, 9)
    #
    # "''____Rebuild Delete Value____''"
    # b.delete(b.root, 5)

    print(b.InOrder(b.root))
    # print(f'pre order {b.PreOrder(b.root)}')
    print(f"The height after is :{b.Height(b.root)}")
    print(f"Is a balanced tree :{b.Balanced()}")
    # print(b.n)
    # print(b.q)