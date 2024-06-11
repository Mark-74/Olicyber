#include <vector>
#include <stdio.h>

class Flag {
    std::vector<char> *flag;
public:
    Flag() {
        flag = new std::vector<char>({102,108,97,103,123,81,85,69,83,84,65,95,70,76,65,71,95,69,39,95,83,73,67,85,82,65,77,69,78,84,69,95,85,78,65,95,70,76,65,71,95,86,69,82,65,125});
    }
};
    
#include <stdio.h>
#include <cstdlib> // for malloc

int main() {
    // get pointer to heap end at the start
    void* heap_before = malloc(1); // Allocate a small amount of memory

    // Instantiate a new Flag object
    Flag myFlag;

    // Get pointer to heap end after instantiation of Flag object
    void* heap_after = malloc(1);

    //printf("%ld", (long)heap_after-(long)heap_before);

    for (int i = 0; i < (long)heap_after-(long)heap_before; i++){
        printf("%c", *((char*)heap_before + i));
    }
    return 0;
}
