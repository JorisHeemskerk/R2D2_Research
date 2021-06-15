#include "hwlib.hpp"
#include "images_old.hpp"
#include <array>

std::array<unsigned int, 3> locate(const std::array<std::array<std::array<uint8_t, 3>, 126>, 126> & image, unsigned int hScale, unsigned int sScale, unsigned int vScale){
    std::array<unsigned int, 3> guess = {0,0,0}; // x, y, score
    unsigned int H = 0;
    unsigned int S = 0;
    unsigned int V = 0;

    for(unsigned int i=0; i<image.size(); i++){
        for(unsigned int j=0; j<image[i].size(); j++){
            H = image[i][j][0] * hScale;
            // if(H <= 128){
            //     H = 2*(128-H) * hScale;
            // }else{
            //     H = 2*(H-128) * hScale;
            // }
            S = image[i][j][1] * sScale;
            V = image[i][j][2] * vScale; 

            if(guess[2] < (H+S+V)){
            guess = {j, i, H+S+V};
            }
            // hwlib::cout << "pixel (" << i <<", "<< j << ") has the following HSV values: " << H <<", "<< S <<", "<< V << "\n";
        }
    }
    return guess;
}

int main( void ){   

    hwlib::wait_ms(1000);
    hwlib::cout << "terminal has started\n";  

    std::array<uint8_t, 2> recentPosition = {};

    for(unsigned int i=0; i<20; i++){
        hwlib::cout << "increasing H value: " << i << '\n';
        std::array<unsigned int, 3> guess = locate(images[0], i, 1, 1);
        hwlib::cout << "The first laser is at: (" << guess[0] << ", " << guess[1] << "), With a score of: " << guess[2] << ".\n";  
        guess = locate(images[1], i, 1, 1);
        hwlib::cout << "The second laser is at: (" << guess[0] << ", " << guess[1] << "), With a score of: " << guess[2] << ".\n";  
    }
    for(unsigned int i=0; i<20; i++){
        hwlib::cout << "increasing S value: " << i << '\n';
        std::array<unsigned int, 3> guess = locate(images[0], 1, i, 1);
        hwlib::cout << "The first laser is at: (" << guess[0] << ", " << guess[1] << "), With a score of: " << guess[2] << ".\n";  
        guess = locate(images[1], 1, i, 1);
        hwlib::cout << "The second laser is at: (" << guess[0] << ", " << guess[1] << "), With a score of: " << guess[2] << ".\n";  
    }
    for(unsigned int i=0; i<20; i++){
        hwlib::cout << "increasing V value: " << i << '\n';
        std::array<unsigned int, 3> guess = locate(images[0], 1, 1, i);
        hwlib::cout << "The first laser is at: (" << guess[0] << ", " << guess[1] << "), With a score of: " << guess[2] << ".\n";  
        guess = locate(images[1], 1, 1, i);
        hwlib::cout << "The second laser is at: (" << guess[0] << ", " << guess[1] << "), With a score of: " << guess[2] << ".\n";  
    }

}
