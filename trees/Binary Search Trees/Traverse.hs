module Traverse hiding (traverse) where

import 

data TraverseOrder = PreOrder | InOrder | PostOrder

traverse :: TraverseOrder -> BinTree k -> [k]
traverse PreOrder   = preorder'  
traverse InOrder    = inorder'   
traverse PostOrder  = postorder' 

-- Naive inorder traversal:
inorder :: BinTree a -> [a]
inorder Leaf           = []
inorder (Node x lt rt) = inorder lt ++ [x] ++ inorder rt

{-
  Derive
  inorderCat t xs = inorder t ++ xs
-}

inorderCat :: BinTree a -> [a] -> [a]
inorderCat Leaf xs           = xs
inorderCat (Node x lt rt) xs = inorderCat lt (x:(inorderCat rt xs))

-- Derivation of this definition (by equational reasoning)

-- Base Case:
-- inorderCat Leaf xs = inorder Leaf ++ xs = [] ++ xs = xs

-- Inductive Case:
-- inorderCat (Node x lt rt) xs 
-- = inorder (Node x lt rt) ++ xs
-- = inorder lt ++ [x] ++ inorder rt ++ xs
-- = inorder lt ++ x:(inorder rt ++ xs)
-- = inorder lt ++ x:(inorderCat rt xs)
-- = inorderCat lt (x:(inorderCat rt xs))

inorder' :: BinTree a -> [a]
inorder' t = inorderCat t []

-- Naive preorder traversal:
preorder :: BinTree a -> [a]
preorder Leaf           = []
preorder (Node x lt rt) = x : (inorder lt ++ inorder rt)

{-
  Derive
  preorderCat t xs = preorder t ++ xs
-}

preorderCat :: BinTree a -> [a] -> [a]
preorderCat Leaf xs           = xs
preorderCat (Node x lt rt) xs = x: preorderCat lt (preorderCat rt xs)

-- We define elemsCat by the relation:
-- preorderCat t xs = preorder t ++ xs

-- Then we can derive an implementation for preorderCat
-- that is correct by an induction argument:

-- Base Case:
-- preorderCat Leaf xs = [] ++ xs = xs

-- Inductive Case:
-- preorderCat (Node x lt rt) xs 
-- = preorder (Node x lt rt) ++ xs
-- = x : (preorder lt ++ preorder rt) ++ xs
-- = x : preorder lt ++ (preorder rt ++ xs)
-- = x: preorderCat lt (preorderCat rt xs)

preorder' :: BinTree a -> [a]
preorder' t = preorderCat t []

-- Naive postorder traversal:
postorder :: BinTree a -> [a]
postorder Leaf           = []
postorder (Node x lt rt) =  (inorder lt ++ inorder rt) ++ [x]

{-
  Derive
  postorderCat t xs = preorder t ++ xs
-}

postorderCat :: BinTree a -> [a] -> [a]
postorderCat Leaf xs          = xs
postorderCat (Node x lt rt) xs = postorderCat lt (postorderCat rt (x:xs))

-- We define elemsCat by the relation:
-- postorderCat t xs = postorder t ++ xs

-- Then we can derive an implementation for preorderCat
-- that is correct by an induction argument:

-- Base Case:
-- postorderCat Leaf xs = [] ++ xs = xs

-- Inductive Case:
-- postorderCat (Node x lt rt) xs 
-- = postorderCat (Node x lt rt) ++ xs
-- = (postorder lt ++ postorder rt) ++ [x] ++ xs
-- = (postorder lt ++ (postorder rt ++ (x:xs))
-- = postorderCat lt (postorderCat rt (x:xs))

postorder' :: BinTree a -> [a]
postorder' t = postorderCat t []


