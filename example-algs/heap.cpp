#include <vector>

// D-ary heap implementation in C++
// 

template<typename T, size_t D>
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

    // Restores heap property after 
    void heapify() {

    }

public:
    // Construct empty AryHeap with capacity 
    AryHeap(size_t capacity) {
        elems = new vector<T>(capacity);
    }

    T 
}
