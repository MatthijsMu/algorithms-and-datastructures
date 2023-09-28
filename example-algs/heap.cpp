#include <vector>

using namespace std;

template<typename T, size_t D>
class AryMaxHeap {
private:
    vector<T> elems;

    // Compute parent index of node n > 0
    constexpr parent(size_t n) const {
        return n / D;
    }

    // Compute index of i-th child of node n.
    // May be out of range, this is not checked. 
    constexpr size_t child(size_t n, size_t i) const {
        return n * D + i;
    }

    // Restores heap property
    void heapify() {

    }

public:
    // Construct empty AryHeap with capacity N
    AryHeap(size_t N) {
        elems = new vector<T>(N);
    }

    T 
}