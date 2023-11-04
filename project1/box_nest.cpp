#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <sstream>

struct Box {
    float d1, d2, d3;
};

std::ostream &operator <<(std::ostream & os, Box &b) {
    os << "{ " << b.d1 << ", " << b.d2 << ", " << b.d3 << "}";
    return os;
}

float volume(Box &b);

size_t nr_final_boxes(std::vector<Box> &boxes, size_t curr_idx, size_t curr_nr);

size_t nr_final_boxes_v2(std::vector<Box> &boxes);

bool operator<(Box &b1, Box &b2);

bool fits(Box &b1, Box &b2);

int main() {
    size_t n;
    std::cin >> n;
    std::cin.get();
    std::vector<Box> boxes(n);
    for (Box &b : boxes) {
        float x[3];
        std::cin >> x[0] >> x[1] >> x[2];
        std::cin.get();
        std::sort(x, x + 3);
        b = {x[0], x[1], x[2]};
    }
    
/*
    std::cout << "Permuted boxes, sorted on volume: " << std::endl;
    for (auto &b : boxes) {
        std::cout << b;
    }
*/
    std::cout << nr_final_boxes_v2(boxes);

    return 0;
}



float volume(Box &b) {
    return b.d1 * b.d2 * b.d3;
}

size_t nr_final_boxes(std::vector<Box> &boxes, size_t curr_idx, size_t curr_nr) {
    // std::cout << "At box idx: " << curr_idx << std::endl;
    if (curr_idx == boxes.size()) {
        // std::cout << "Finished" << std::endl;
        return curr_nr;
    }
    for (int i = curr_idx + 1; i < boxes.size(); i++) {
        if(fits(boxes[curr_idx], boxes[i])) {
            // std::cout << boxes[curr_idx] << " fits inside " << *it << std::endl;
            return nr_final_boxes(boxes, curr_idx + 1, curr_nr);
        }
    }
    return nr_final_boxes(boxes, curr_idx + 1, curr_nr + 1);
}

size_t nr_final_boxes_v2(std::vector<Box> &boxes) {
    std::sort(boxes.begin(), boxes.end());
    size_t nr_final_boxes = 0;
    size_t curr_idx = 0;
    while(curr_idx < boxes.size()) {
        size_t search_idx = curr_idx + 1; 
        while (search_idx < boxes.size())
            if (fits(boxes[curr_idx], boxes[search_idx])) {
                curr_idx ++;
                search_idx = curr_idx + 1;
            }
        curr_idx ++;
        nr_final_boxes ++;
    }
    return nr_final_boxes;
}



bool operator<(Box &b1, Box &b2) {
    return volume(b1) < volume(b2);
}

// returns true iff b1 fits inside b2. This is a partial ordering on the boxes.
bool fits(Box &b1, Box &b2) {
    return b1.d1 < b2.d1 
        && b1.d2 < b2.d2 
        && b1.d3 < b2.d3;
}
