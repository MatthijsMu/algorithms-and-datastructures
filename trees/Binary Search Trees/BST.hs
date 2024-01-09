module BinTree where

data BinTree k = Node {key :: k , left :: BinTree k, right :: BinTree k} | Leaf


