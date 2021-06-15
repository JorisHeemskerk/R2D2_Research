#include "hwlib.hpp"
#include "images_old.hpp"
#include <array>

std::array<unsigned int, 3> search(const std::array<std::array<std::array<uint8_t, 3>, 126>, 126> & image, std::array<unsigned int, 3> prevLaser, unsigned int patchSize, unsigned int hScale, unsigned int sScale, unsigned int vScale){
    std::array<unsigned int, 3> guess = {0,0,0}; // x, y, score
    unsigned int H = 0;
    unsigned int S = 0;
    unsigned int V = 0;

    for(unsigned int i=0; i<image.size(); i++){
        // if(i > prevLaser[0]-patchSize && i < prevLaser[0]+patchSize){
        //     continue;
        // }
        for(unsigned int j=0; j<image[i].size(); j++){
            // if(i > prevLaser[1]-patchSize && i < prevLaser[1]+patchSize){
            //     continue;
            // }
            H = image[i][j][0] * hScale;
            S = image[i][j][1] * sScale;
            V = image[i][j][2] * vScale; 

            if(guess[2] < (H+S+V)){
            guess = {j, i, H+S+V};
            }
        }
    }
    return guess;
}

std::array<unsigned int, 3> patchSearch(const std::array<std::array<std::array<uint8_t, 3>, 126>, 126> & image, std::array<unsigned int, 3> prevLaser, unsigned int patchSize, unsigned int hScale, unsigned int sScale, unsigned int vScale){
    std::array<unsigned int, 3> guess = {0,0,0}; // x, y, score
    unsigned int H = 0;
    unsigned int S = 0;
    unsigned int V = 0;

    for (unsigned int i = 0; i < 2; i++){
        if(prevLaser[i] - patchSize < 0){
            prevLaser[i] -= prevLaser[i] - patchSize;
        }
        if(prevLaser[i] + patchSize >= image.size()){
            prevLaser[i] -= prevLaser[i] + patchSize - image.size()-1;
        }
    }

    for(unsigned int i=prevLaser[0]-patchSize; i<prevLaser[0]+patchSize; i++){
        for(unsigned int j=prevLaser[1]-patchSize; j<prevLaser[1]+patchSize; j++){
            H = image[i][j][0] * hScale;
            S = image[i][j][1] * sScale;
            V = image[i][j][2] * vScale; 

            if(guess[2] < (H+S+V)){
            guess = {j, i, H+S+V};
            }
        }
    }
    if(guess[2]*100 > 90*prevLaser[2]){
        return guess;
    }else{
        return search(image, prevLaser, patchSize, hScale, sScale, vScale);
    }
    
}

int main( void ){   

    hwlib::wait_ms(1000);
    hwlib::cout << "terminal has started\n";  

    unsigned int patchSize = 21;
    std::array<unsigned int, 3> prevLaser = {0,0,0};
    for(;;){
        std::array<unsigned int, 3> guess = patchSearch(images[0], prevLaser, patchSize, 2, 2, 1);
        hwlib::cout << "The laser is at: (" << guess[0] << ", " << guess[1] << "), With a score of: " << guess[2] << ".\n";
        prevLaser = guess;  
        guess = patchSearch(images[1], prevLaser, patchSize, 2, 2, 1);
        hwlib::cout << "The second laser is at: (" << guess[0] << ", " << guess[1] << "), With a score of: " << guess[2] << ".\n";  
        prevLaser = guess; 
    }

    // for(unsigned int i=0; i<20; i++){
    //     hwlib::cout << "increasing H value: " << i << '\n';
    //     std::array<unsigned int, 3> guess = search(images[0], i, 1, 1);
    //     hwlib::cout << "The first laser is at: (" << guess[0] << ", " << guess[1] << "), With a score of: " << guess[2] << ".\n";  
    //     guess = search(images[1], i, 1, 1);
    //     hwlib::cout << "The second laser is at: (" << guess[0] << ", " << guess[1] << "), With a score of: " << guess[2] << ".\n";  
    // }
    // for(unsigned int i=0; i<20; i++){
    //     hwlib::cout << "increasing S value: " << i << '\n';
    //     std::array<unsigned int, 3> guess = search(images[0], 1, i, 1);
    //     hwlib::cout << "The first laser is at: (" << guess[0] << ", " << guess[1] << "), With a score of: " << guess[2] << ".\n";  
    //     guess = search(images[1], 1, i, 1);
    //     hwlib::cout << "The second laser is at: (" << guess[0] << ", " << guess[1] << "), With a score of: " << guess[2] << ".\n";  
    // }
    // for(unsigned int i=0; i<20; i++){
    //     hwlib::cout << "increasing V value: " << i << '\n';
    //     std::array<unsigned int, 3> guess = search(images[0], 1, 1, i);
    //     hwlib::cout << "The first laser is at: (" << guess[0] << ", " << guess[1] << "), With a score of: " << guess[2] << ".\n";  
    //     guess = search(images[1], 1, 1, i);
    //     hwlib::cout << "The second laser is at: (" << guess[0] << ", " << guess[1] << "), With a score of: " << guess[2] << ".\n";  
    // }

}

