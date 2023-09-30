#include <vector>

// D-ary heap implementation in C++
// We implement it as a concrete class that internally stores its elements in a
// vector. The reason to prefer this over a bare array is the interface that this
// already provides for resizing etc.

// Heaps are fundamental data structures with many application. They are for example 
// an efficient back-end for priorityqueues. The STL also provides a way of making 
// heaps, but not as a class itself: a heap is a random-accessible container that
// satisfies the heap invariant. There are algorithms for maintaining this invariant
// which interact with the container via the uniform interface of Random Access Iterators.
// 

template<typename T, size_t D>
// type T should be be comparable and swappable.
class AryMaxHeap {
private:
    std::vector<T> elems;

    // Compute parent index of node n > 0
    constexpr parent(size_t n) const {
        return n / D;
    }

    // Compute index of i-th child of node n.
    // May be out of range, this is not checked. 
    constexpr size_t child(size_t n, size_t i) const {
        return n * D + i;
    }

    // Restores max-heap property after update to element n
    // of the heap.

    // There is also a recursive version of this function, which just calls
    // max_heapify (biggest) after swapping from with biggest.
    // Since there are no operations after the recursive call,
    // the compiler should be able to do tail-call optimization on this
    // (i.e. reuse the stack frame for the next recursive call).
    // But since a tail-recursive function can just as easily be implemented
    // in a while-loop which is by default compiled to such a constant stack-
    // frame, I choose for the iterative implementation.
    void max_heapify (size_t from) {
        size_t biggest = from;

        while (biggest < elems.size()) {
            // loop over children, see which of the parent `from` and its
            // children is biggest
            for (size_t i = 1; i <= d; child(from,i) < elems.size())
                if (elens[child(n,i)] > elems[biggest])
                    biggest = child(n,i);

            
            if (biggest != from) {
                // if one of the children is largest, 
                // swap `from` with its biggest child
                // and repeat pushing down on `from <- biggest`
                swap(&elems[from], &elems[biggest]);
                from = biggest;
            } else {
                break;
            }
        }

        return;
    }


public:
    // Construct empty AryHeap with capacity 
    AryHeap(size_t capacity) {
        elems = new vector<T>(capacity);
    }

    bool empty() {
        return elems.empty();
    }

    T extract_max() {
        // get the maximum element.
        T max = A[0];

        // put the last element into A[0],
        // truncate and
        // restore the max-heap property using
        // max-heapify(0)
        elems[0] = elems[elems.size() - 1];
        elems.resize(elems.size() - 1);
        max_heapify(0);

        return max;
    }

    // insert key into heap while maintaining heap invariant.
    void insert(T key) {
        elems.resize(elems.size() + 1);
        size_t index = elems.size() - 1;
        elems[index] = key;

        // restore heap property by pushing up the element for
        // as long as necessary.
        while (index > 0) {
            swap(&elems[index], &elems[parent(index)]);
            index = parent(index);
        }

        return;
    }

    // change the value of a key at index i while maintaining heap 
    // invariant. 
    // Will push down using max_heapify if the key value is decreased.
    // Will push up if the key value is increased.
    // Will throw an std:out_of_range if the index is not in the heap's range
    void change_key(size_t index, T key) {
        if (index >= elems.size())
            throw std::out_of_range;
        if (key < elems[i]) {
            // change key value at index
            elems[index] = key;
            // push down element until not smaller
            // than any of its children.
            max_heapify(index);
        }
        if (key == elems[i])
            return;
        if (key > elems[index]) {
            // change key value at index
            elems[index] = key;

            // push up until not smaller than its parent
            while(index != 0 and elems[parent(index)] > key) {// the first check is kind of redundant since parent(0) = 0 by default
                swap(A, index, parent(index));
                index = parent(index);
            }
        }
    }
}

// Since I am a fan of the STL, and really like the idea of providing iterators as interfaces 
// to containers, 
