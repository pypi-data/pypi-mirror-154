"""
binary search tree implementation.

----------------------------------
*           june 2022            *
*    developed by maslenchenko   *
*          with love XX          *
----------------------------------

https://github.com/maslenchenko/binary-search-tree.git
"""

class TreeNode:
    """
    representation of a binary search\
    tree node.

    attributes:
    -----------
    data: any data type
        data which node contains

    right: TreeNode object
        right child of a node

    left: TreeNode object
        left child of a node
    """
    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None

    def _children(self, data=False):
        """
        returns a list of children\
        (TreeNode) objects for specific\
        tree node.
        """
        children = []
        if data is False:
            if self.left is not None:
                children.append(self.left)
            else:
                children.append("_")
            if self.right is not None:
                children.append(self.right)
            else:
                children.append("_")
        else:
            if self.left is not None:
                children.append(self.left.data)
            else:
                children.append("_")
            if self.right is not None:
                children.append(self.right.data)
            else:
                children.append("_")
        return children

class BinarySearchTree:
    """
    representation of a binary search tree.

    methods:
    --------
    get_root(self):
        returns a root of\
        the binary search tree.

    add(self, element, start_point):
        adds element to the binary\
        search tree.

    get_leaves(self):
        returns a list of leaves.

    _children(self, node):
        returns a list of children\
        (TreeNode) objects for specific\
        tree node.

    bfs(self):
        breadth first search function.
        returns a list which consists of\
        list of node levels. 
        if tree node is none, it is marked\
        as '_'.

    path_to_element(self):
        returns a path (a list of\
        elements) to the specific node.

    _up(self):
        returns a father of a node.

    inorder(self, root):
        inorder traversal.
        traverse from the left subtree to\
        the root then to the right subtree.

    _recurse_for_inorder(self, current, inorder):
        recursive algorithm for the inorder traversal.

    postorder(self, root):
        postorder
        traverse from the left subtree to\
        the right subtree then to the root.

    _recurse_for_postorder(self, current, postorder):
        recursive algorithm for the postorder traversal.

    preorder(self, root):
        preoder traversal.
        traverse from the root then  to the left\
        subtree then to the right subtree.

    _recurse_for_preorder(self, current, preorder):
        recursive algorithm for the preorder traversal.

    nodes_num(self):
        total number of nodes in\
        binary search tree.

    _is_leaf(self, value):
        checks if tree node is leaf.

    rebalance(self):
        changes existing binary search tree.
        returns rebalanced one.

    delete_all_nodes(self):
        deletes all nodes in binary search tree.
        return empty tree.

    _recurse_for_deleting(self, node):
        recursive function for deleting all nodes.

    delete_node(self, node):
        deletes specific node and returns\
        rebalanced tree.

    attributes:
    -----------
    _root: TreeNode object
        binary search tree root
    """
    def __init__(self, root=None):
        """
        constructs all necessary attributes\
        for BinarySearchTree object.

        attributes:
        -----------
        _root: TreeNode object
            binary search tree root
        """
        self._root = TreeNode(root)
        self.nodes = 0
        if self._root is not None:
            self.nodes = 1

    def get_root(self, data=False):
        """
        returns a root of\
        the binary search tree.
        """
        if data is True:
            return self._root.data
        return self._root

    def add(self, element, start_point=None):
        """
        adds element to the binary\
        search tree.
        """
        if start_point is None:
            self._root = TreeNode(element)
            self.nodes += 1
        else:
            if start_point.data > element:
                if start_point.left is None:
                    start_point.left = TreeNode(element)
                    self.nodes += 1
                else:
                    self.add(element, start_point.left)
            elif start_point.data < element:
                if start_point.right is None:
                    start_point.right = TreeNode(element)
                    self.nodes += 1
                else:
                    self.add(element, start_point.right)
            else:
                print("this element already exists in binary search tree")

    def get_leaves(self):
        """
        returns a list of leaves.
        """
        levels = self.bfs()
        leaves = levels[-1]
        for element in leaves[::-1]:
            if element == "_":
                leaves.remove(element)
        return leaves

    def path_to_element(self, value):
        """
        returns a path (a list of\
        elements) to the specific node.
        """
        levels = self.bfs(object=True)
        node = None
        for level in levels:
            for element in level:
                if isinstance(element, TreeNode):
                    if element.data == value:
                        node = element
        if node is not None:
            path = [value]
            while self._up(node) is not None:
                path.append(self._up(node).data)
                node = self._up(node)
            if len(path) > 0:
                return path[::-1]
            else:
                return "element does not exist"

    def _up(self, node):
        """
        returns a father of a node.
        """
        levels = self.bfs(object=True)
        level = -1
        for ind in range(len(levels)):
            for element in levels[ind]:
                if isinstance(element, TreeNode):
                    if element.data == node.data:
                        level = ind
        if level != -1:
            father_level = level - 1
            if father_level == -1:
                return None
            for element in levels[father_level]:
                if element != "_":
                    if node.data in element._children(data=True):
                        return element
        else:
            return None

    def bfs(self, object=False):
        """
        breadth first search function.
        returns a list which consists of\
        list of node levels. 
        if tree node is none, it is marked\
        as '_'.
        """
        levels = []
        level = [self._root]
        while level.count("_") != len(level):
            next_level = []
            for element in level:
                if element != "_":
                    next_level.extend(element._children())
                else:
                    next_level.extend(["_", "_"])
            levels.append(level)
            level = next_level
        if object is False:
            for element in levels:
                for ind in range(len(element)):
                    node = element[ind]
                    try:
                        element[ind] = node.data
                    except:
                        pass
        return levels

    def __str__(self):
        """
        returns string representation\
        of binary search tree.
        """
        if self._root is None:
            return "the tree is empty"
        levels = self.bfs()
        max_len = len(levels[-1]) * 2 - 1
        result = ""
        for level in levels:
            length = len(level)
            if length == 1:
                result += "_ " * int(((max_len - 1)/2))
                result += f"{level[0]}"
                result += "_ " * int(((max_len - 1)/2))
                result += "\n"
            else:
                result += "_ " * int(((max_len - len(level))/2))
                sub_str = ""
                for el in level:
                    sub_str += f"{el} _ "
                sub_str = sub_str[:-2]
                result += sub_str
                result += "_ " * int(((max_len - len(level))/2))
                result += "\n"
        return result[:-1]

    def inorder(self, root):
        """
        inorder traversal.
        traverse from the left subtree to\
        the root then to the right subtree.
        """
        inorder = []
        if root == self._root.data:
            self._recurse_for_inorder(self._root, inorder)
        return inorder
       
    def _recurse_for_inorder(self, current, inorder):
        """
        recursive algorithm for the inorder traversal.
        """
        if current is not None:
            if current.left is None:
                self._recurse_for_inorder(current.right, inorder)
                inorder.append(current.data)
            elif current.right is None:
                self._recurse_for_inorder(current.left, inorder)
                inorder.append(current.data)
            else:
                self._recurse_for_inorder(current.left, inorder)
                inorder.append(current.data)
                self._recurse_for_inorder(current.right, inorder)

    def postorder(self, root):
        """
        postorder
        traverse from the left subtree to\
        the right subtree then to the root.
        """
        postorder = []
        if root == self._root.data:
            self._recurse_for_postorder(self._root, postorder)
        return postorder
       
    def _recurse_for_postorder(self, current, postorder):
        """
        recursive algorithm for the postorder traversal.
        """
        if current is not None:
            self._recurse_for_postorder(current.left, postorder)
            self._recurse_for_postorder(current.right, postorder)
            postorder.append(current.data)

    def preorder(self, root):
        """
        preoder traversal.
        traverse from the root then  to the left\
        subtree then to the right subtree.
        """
        preorder = []
        if root == self._root.data:
            self._recurse_for_preorder(self._root, preorder)
        return preorder
       
    def _recurse_for_preorder(self, current, preorder):
        """
        recursive algorithm for the preorder traversal.
        """
        if current is not None:
            preorder.append(current.data)
            self._recurse_for_preorder(current.left, preorder)
            self._recurse_for_preorder(current.right, preorder)

    def nodes_num(self):
        """
        total number of nodes in\
        binary search tree.
        """
        return self.nodes

    def _is_leaf(self, value):
        """
        checks if tree node is leaf.
        """
        levels = self.bfs(object=True)
        for level in levels:
            for node in level:
                if node != "_":
                    if node.data == value:
                        tree_node = node
        if tree_node:
            return tree_node.left is None and tree_node.right is None
        else:
            return None

    def rebalance(self, node_val=None):
        """
        changes existing binary search tree.
        returns new rebalanced tree.
        """
        nodes = self.inorder(self._root.data)
        nodes.sort()
        if node_val is not None:
            try:
                nodes.remove(node_val)
            except:
                print("the tree does not contain this node value")
        self.delete_all_nodes()
        if len(nodes) % 2 == 1:
            middle = int((len(nodes) - 1) / 2)
        else:
            middle = int(len(nodes) / 2)
        first_part = nodes[:middle]
        root = nodes[middle]
        second_part = nodes[middle+1:]
        self.add(root)
        while len(first_part) != 0 or len(second_part) != 0:
            length1 = len(first_part)
            length2 = len(second_part)
            root = self.get_root()
            if length1 == 0:
                pass
            else:
                if length1 % 2 == 1:
                    middle1 = int((length1 - 1) / 2)
                else:
                    middle1 = int(length1 / 2)
                self.add(first_part.pop(middle1), root)
            if length2 == 0:
                pass
            else:
                if length2 % 2 == 1:
                    middle2 = int((length2 - 1) / 2)
                else:
                    middle2 = int(length2 / 2)
                self.add(second_part.pop(middle2), root)

    def delete_all_nodes(self):
        """
        deletes all nodes in binary search tree.
        return empty tree.
        """
        self._recurse_for_deleting(self._root)
        self._root = None
        self.nodes = 0

    def _recurse_for_deleting(self, node):
        """
        recursive function for deleting all nodes.
        """
        if node is not None:
            self._recurse_for_deleting(node.left)
            self._recurse_for_deleting(node.right)
            node.left = None
            node.right = None

    def delete_node(self, node):
        """
        deletes specific node and returns\
        rebalanced tree.
        """
        self.rebalance(node_val=node)
