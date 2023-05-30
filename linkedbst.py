"""
File: linkedbst.py
Author: Ken Lambert
"""
from random import sample
from timeit import default_timer as timer
from math import log
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        self.containings = sourceCollection
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node is not  None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            if item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)
    
    def my_finder(self, item):
        node = self._root

        while True:
            if node is None:
                return None
            if item == node.data:
                return node.data
            elif item < node.data:
                node = node.left
            else:
                node = node.right

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def my_adder(self, item):
        if self.isEmpty():
            self._root = BSTNode(item)
        else:
            node = self._root
            while True:
                if item < node.data:
                    if node.left is None:
                        node.left = BSTNode(item)
                        break
                    node = node.left
                else:
                    if node.right is None:
                        node.right = BSTNode(item)
                        break
                    node = node.right
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            """
            Replace top's datum with the maximum datum in the left subtree
            Pre:  top has a left child
            Post: the maximum node in top's left subtree
                  has been removed
            Post: top.data = maximum value in top's left subtree
            """
            parent = top
            current_node = top.left
            while not current_node.right is None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node is None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left is None \
                and not current_node.right is None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            if probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if not top.right and not top.left:
                return 0
            return 1 + max(height1(ele) for ele in [top.right, top.left] if ele)

        if self.isEmpty():
            return -1
        return height1(self._root)


    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        lyst = []

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return self.height() < (2*log(len(lyst) +1, 2) - 1)


    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        node_lst = [i for i in self.inorder()]
        start, finish = node_lst.index(low), node_lst.index(high)
        return node_lst[start:finish+1]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        if self.isEmpty():
            return None
        node_lst = list(self.inorder())
        self.clear()

        def node_adder(node_lst):
            center = len(node_lst)//2

            self.add(node_lst[center])
            node_lst.remove(node_lst[center])

            lst1,lst2 = node_lst[:center], node_lst[center:]
            for ele in [lst1, lst2]:
                if len(ele)>1:
                    node_adder(ele)
                else:
                    for ele in ele:
                        self.add(ele)

        return node_adder(node_lst)
    
    def rebalance_while(self):
        if self.isEmpty():
            return None
        node_lst = [sorted(self.containings)]
        self.clear()

        while any(len(ele) > 2 for ele in node_lst):
            for ele in node_lst:
                if len(ele) > 2:
                    center = len(ele)//2
                    node_lst += [[ele.pop(center)]]

                    lst1, lst2 = ele[:center], ele[center:]
                    node_lst.remove(ele)

                    node_lst.append(lst1)
                    node_lst.append(lst2)
        value_lst = [j for i in node_lst for j in i]
        for ele in value_lst:
            self.my_adder(ele)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """

        node_lst = sorted([i for i in self.inorder()] + [item])
        num = node_lst.index(item) if node_lst.count(item) == 1 else\
                node_lst.index(item)+node_lst.count(item)-1

        return node_lst[num+1] if num+1 < len(node_lst) else None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        node_lst = sorted([i for i in self.inorder()] + [item])
        num = node_lst.index(item)

        return node_lst[num-1] if num > 0 else None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, 'r') as file:
            res = [line.split('\n')[0] for line in file]
        random_res = sample(res, len(res))
        # res = sample(res, 10000)
        rand_words = sample(res, 1)
        # list
        start = timer()
        finder1 = [res.index(ele) for ele in rand_words if ele in res]
        end = timer()
        time1 = end-start

        # ordered tree
        ordered_tree = LinkedBST(res)
        start = timer()
        finder2 = [ordered_tree.my_finder(ele) for ele in rand_words]
        end = timer()
        time2 = end-start

        # unordered tree
        unordered_tree = LinkedBST(random_res)
        start = timer()
        finder3 = [unordered_tree.my_finder(ele) for ele in rand_words]
        end = timer()
        time3 = end-start


        #rebalanced tree
        ordered_tree.rebalance_while()
        start = timer()
        finder4 = [ordered_tree.my_finder(ele) for ele in rand_words]
        end = timer()
        time4 = end-start

        print(f"In list: {time1}\n"
              f"In ordered binary tree: {time2}\n"
              f"In unordered binary tree: {time3}\n"
              f"In rebalanced tree: {time4}")

LinkedBST().demo_bst('words.txt')
