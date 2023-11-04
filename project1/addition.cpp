#include <iostream>


int main() {
    size_t n;
    long sum = 0;
    std::cin >> n;
    std::cin.get();
    for(size_t i = 0; i < n; i ++) {
        long a;
        std::cin >> a;
        sum += a;
    }

    std::cout << sum;

    return 0;
}