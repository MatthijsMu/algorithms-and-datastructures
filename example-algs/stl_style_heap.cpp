/*
A d-ary heap with respect to comp (max heap) is a random-access range [first, last) that has the following properties:

 - Given N as last - first, for all integer i where 0 < i < N, bool(comp(first[(i - 1) / d], first[i])) is false.

 - A new element can be added using std::push_heap in O(log N) time.

 - *first can be removed using std::pop_heap in O(log N) time.

*/
// Type requirements:
// - RandomIt must meet the requirements of LegacyRandomAccessIterator.
// - Compare: comparison function object (i.e. an object that satisfies the requirements of Compare) which returns true if the first argument is less than the second.


// Some utility functions which I hope will be inlined:
template < size_t arity >
constexpr size_t parent(size_t index) {
  return (index - 1)/ arity;
}

template < size_t arity >
constexpr size_t child(size_t index, size_t child_nr) {
  return index * arity + child_nr;
}



// Checks whether [first, last) is a (max) heap w.r.t. comp
template< size_t arity, class RandomIt, class Compare >
bool is_heap( RandomIt first, RandomIt last, Compare comp ) {
  /* How to efficiently chek that a random-acces range is a heap?
   * We necessarily need to compare each internal node against its
   * children, and this is sufficient
   * The last internal node is at parent(last - first).
  */

  const size_t N = last - first;
  for (size_t i = 1; i < N; i++) {
    if (comp(first[parent<arity>(i)], first[i]))
      return false;

  return true;
}

// Inserts the element at the position last - 1 into the heap [first, last - 1). The heap after the insertion will be [first, last).
template< size_t arity, class RandomIt, class Compare >
void push_heap( RandomIt first, RandomIt last, Compare comp ) {
  size_t index = last - 1 - first;
  while (index != 0 && comp(first[parent<arity>(index)], first[index)) {
    std::swap(&first[index], &first[parent<arity>(index)]);
    last = first + parent<arity>(last - first);
  }
}

// Inserts element at position first + 0 into the heap [first + 1, last). The heap after the insertion will be [first, last)
template< size_t arity, class RandomIt, class Compare >
void heapify( RandomIt first, RandomIt last, Compare comp ) {
   size_t index = 0; 
   size_t N = last - first
   while (first + index < last) {
     size_t biggest = index;
     // loop over children, see which of the parent `from` and its
            // children is biggest
     for (size_t i = 1; i <= d && child<arity>(index,i) < N; i++)
       if (comp(first[index],first[child<arity>(index,i)]))
          biggest = child<arity>(index,i);
            
     if (biggest != first + index) {
       swap(first + index, biggest);
       from = biggest;
     } else {
       break;
     }
   }
}



// Swaps the value in the position first and the value in the position last - 1 and makes the subrange [first, last - 1) into a heap. 
// This has the effect of removing the first element from the heap [first, last).
// Interesting: this function does not return (reference of) *first.
// So retrieving the largest element is something the programmer has to do in an extra step, 
// e.g. `pop_heap(v.begin(), v.end()); auto x = v.back();`
template< size_t arity, class RandomIt, class Compare >
void pop_heap( RandomIt first, RandomIt last, Compare comp ) {
  std::swap(first, last - 1);
  heapify<arity, RandomIt, Compare>(first, last - 1, comp);
}
