// Some utility functions which I hope will be inlined:
template < size_t arity >
constexpr size_t parent(size_t index) {
  return (index - 1)/ arity;
}

template < size_t arity >
constexpr size_t child(size_t index, size_t child_nr) {
  return index * arity + child_nr;
}

// Type requirements:
// - RandomIt must meet the requirements of LegacyRandomAccessIterator.
// - Compare must meet the requirements of Compare.


template< size_t arity, class RandomIt, class Compare >
bool is_heap( RandomIt first, RandomIt last, Compare comp ) {
  /* How to efficiently chek that a random-acces range is a heap?
   * We necessarily need to compare each internal node against its

   * The last internal node is at parent(last - first).
  */

  RandomIt last_internal = parent(last - first);

  // Check internal nodes with a full set of children:
  for (; first < last_internal; first++) {
    for(size_t child_index = 1; child_index <= arity; child_index++) {
      if (!comp(*first, *(first + child_index)))
        return false;
    }
  }

  // Check last internal node, which may not have a full
  // set of arity children:
  for(size_t child_index = 1; child_index <= arity && child(last_internal, child_index) < last; child_index++) {
      if (!comp(*last_internal, *(last_internal + child_index)))
        return false;
  }
  return true;
}


template< class RandomIt, class Compare >
void push_heap( RandomIt first, RandomIt last, Compare comp );
