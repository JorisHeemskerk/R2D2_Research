#ifndef ALGORITHM_TESTER_HPP
#define ALGORITHM_TESTER_HPP

#include "hwlib.hpp"

constexpr unsigned int imageWidth = 126;
constexpr unsigned int imageHeight = 126;

std::array<unsigned int, 3> locate(std::array<std::uint8_t, imageWidth*imageHeight*3 + 4u> & image, unsigned int hScale, unsigned int sScale, unsigned int vScale){
    std::array<unsigned int, 3> guess = {0,0,0}; // x, y, score
    unsigned int H = 0;
    unsigned int S = 0;
    unsigned int V = 0;

    for(unsigned int i=0; i<imageWidth; i++){
        for(unsigned int j=0; j<imageHeight; j++){
            H = image[(i+(j*imageHeight))*3+4] * hScale;    // +4 to ignore the 4 checksum bytes up front
            // if(H <= 128){                // Compensation for both 
            //     H = 2*(128-H) * hScale;  // really low and really 
            // }else{                       // high H values being 
            //     H = 2*(H-128) * hScale;  // close to pure red.
            // }
            S = image[(i+(j*imageHeight))*3+1+4] * sScale;
            V = image[(i+(j*imageHeight))*3+2+4] * vScale; 

            if(guess[2] < (H+S+V)){
            guess = {j, i, H+S+V};
            }
            // hwlib::cout << "pixel (" << i <<", "<< j << ") has the following HSV values: " << H <<", "<< S <<", "<< V << "\n";
        }
    }
    return guess;
}

void test_algorithm(std::array<std::uint8_t, 126*126*3 + 4u> & image, const unsigned int & scaleStart=0, const unsigned int & scaleEnd=10){
    uint_fast64_t startTime = 0;
    uint_fast64_t endTime = 0;
    for(unsigned int h=scaleStart; h<scaleEnd; h++){
        for(unsigned int s=scaleStart; s<scaleEnd; s++){
            for(unsigned int v=scaleStart; v<scaleEnd; v++){
                startTime = hwlib::now_us();
                std::array<unsigned int, 3> guess = locate(image, h, s, v);
                endTime = hwlib::now_us(); //Very important to do before we start printing.
                hwlib::cout << hwlib::dec << "[" << guess[0] << ", " << guess[1] << ", " << endTime - startTime << "],\r\n";
            }
        }
    }
}


#endif // ALGORITHM_TESTER_HPP
