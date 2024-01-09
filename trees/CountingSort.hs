module CountingSort where

import Data.Array
import Data.Ord
import Data.List
import Data.Maybe

class Rankable key where
  rank :: [(key,a)] -> [[a]] 
  -- puts a's with the same key in the same sublist, 
  -- where sublists are ordered w.r.t. key
  -- Requirement: x :: a and y :: a with equal keys
  -- in the original list should in their sublist remain
  -- in the same order as they were in the original list.
  -- This is required for a counting sort on a Rankable 
  -- to be stable.  

countSortOn :: (Rankable key) => (v -> key) -> [v] -> [v]
countSortOn f = concat . rank . map (\x->(f x, x))

defaultRank :: Ord key => [(key,a)] -> [[a]]
defaultRank = map (map snd) . groupBy (\x -> (==) (fst x) . fst) . sortOn fst -- O(n log n)

data Digit = Zero | One 
  deriving (Eq, Ord, Show, Enum)

instance Rankable Digit where
  rank = map reverse . rankIntermediate [[],[]] where
    rankIntermediate [l1, l2] [] = [l1, l2]
    rankIntermediate [l1, l2] (x:xs) 
      | fst x == One  = rankIntermediate [l1, (snd x):l2] xs
      | fst x == Zero = rankIntermediate [(snd x):l1, l2] xs

class Digitable d where
  digit :: Int -> d -> Digit 
  -- compute the n-th significant digit in the binary representation of d
  -- (d= 0, ... N-1, so 0-based where N is the length of the representation)
  -- we can return Zero if the integer is too big or negative.
  
radixSort :: (Digitable d) => Int -> [d] -> [d]
radixSort maxN = foldl (.) id [countSortOn (digit i) | i <- [0..maxN]]

instance Digitable Int where
  digit p n = case (n `mod` (2^(p+1))) `div` (2^p) of
    0 -> Zero
    1 -> One


instance Rankable Int where
  rank = defaultRank -- O(n log n), note |K| ~ 6.5 *10^4
  
instance Rankable Char where
  rank = defaultRank -- O(n log n), note |K| = 256
  
instance Rankable Bool where
  rank = map reverse . rankIntermediate [[],[]] where
    rankIntermediate [l1, l2] [] = [l1, l2]
    rankIntermediate [l1, l2] (x:xs) 
      | fst x = rankIntermediate [l1, (snd x):l2] xs
      | otherwise = rankIntermediate [(snd x):l1, l2] xs
  -- rank splices the list into two sublists for key= True,
  --  key=False, traverses the list only once => O(n + 2)


-- Radix sort: perform countsort over the entire list, 
-- one one position at a time (digit, whatever you want to call it)
-- starting at the least significant digit until the most significant
-- digit. For |key| = N with radix d, this requires
-- log(K) / log(d) passes of complexity O(n + d) where n
-- is the length of the list, so the algorithm is 
-- O(log(K)/log(d) * (n+d)), making it interesting for K small.

-- Radix sort is equivalent to a lexicographical sort, where the 
-- keys are all given the same length by padding them with 
-- "leading zeroes".

-- A lexicographic rank (that is also stable if key1 and key2 implement
-- stable ranks: rank on key1 first, on key2 second.
instance (Rankable key1, Rankable key2) => Rankable (key1,key2) where
  rank = concat . map rank . rank . map assoc where
    assoc ((a1, a2), a3) = (a1, (a2, a3))

-- A helper rank instance for Maybe: we would like to handle variable-
-- length words as keys (i.e. lists of keys), using
-- uncons :: [a] -> Maybe (a, [a]). But this may return nothing, in
-- particular when some words are shorter than others and will be
-- emptied in a sooner radix pass.
instance Rankable key => Rankable (Maybe key) where
  rank l = [v| (mk, v) <- l , isNothing mk]:(rankNotNothing l) where 
    rankNotNothing = rank . map (\(mk,v) -> (fromJust  mk , v)) . filter (not . isNothing . fst) 
  
-- A rank instance for lists of keys. This is about equivalent to lexicographic sort,
-- in that it performs log_d(|K|) passes over the list. It is not entirely as
-- efficient, since it will end up with |K| buckets, whereas in radix sort, we
-- merge the intermediate buckets and then sort again. It is not equivalent to 
-- radix sort, unless we pad all the [key]'s with "0" (i.e. minimum) keys at the 
-- 
instance Rankable key => Rankable [key] where
  rank l = filter (not . null) (rank [(uncons k, v) | (k,v) <- l])

  
  


