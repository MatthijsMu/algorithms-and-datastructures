-- Haskell because algebraic datatypes are SOO easy in this language.
-- The syntax can be short and clear, making it both easy to program
-- and easy to read back.

-- A red-black tree (RBT) is:
-- 1. A binary search tree (BST):
--    - a rooted binary tree data structure 
--    - with the key of each internal node being 
--      - <, greater than the keys in the respective node's left subtree 
--      - >, less than the ones in its right subtree
--    - as a consequence, we can only store keys once in a BST.

-- 2. (Wikipedia)
--    - Every node is either red or black.
--    - All Nil nodes are considered black.
--    - A red node does not have a red child.
--    - Every path from a given node to any of its descendant NIL nodes goes through the same number of black nodes.
--    - (Conclusion) If a node N has exactly one child, it must be a red child, because if it were black, its NIL descendants would sit at a different black depth than N's NIL child, violating requirement 4.

data RB_tree k = Red k (RB_tree k) (RB_tree k) | Black k (RB_tree k) (RB_tree k) | Nil

children RB_tree k -> [RB_tree]
children Nil = []
children (Red _ t s) = [t,s]
children (Black _ t s) = [t,s]

valid_RB_tree :: (Eq k, Ord k) => RB_tree k -> Bool
valid_RB_tree Nil =


