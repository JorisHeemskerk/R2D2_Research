#include "crc32.hpp"
#include "protocol-tsy.hpp"
#include "algorithm-tester.hpp"
#include "hwlib.hpp"


// BEFORE RUNNING MAKE SURE TO CHECK THAT THE PINS ARE SET CORRECTLY IN protocol-tsy.hpp OR YOU MIGHT GET UNDEFINED BEHAVIOUR!
// These have been changed around occasionally due to broken pins on some of our teensys.
// They should match the spec in our README initially, but it cant hurt to check. (they are defined in protocol-tsy.hpp, lines 48-61)
// Also if you appear to get the wrong value start by checking wether all your pins are O.K., 
// they have been known to break from soldering due to excessive heat.

// Make sure to check the README for additional information and instructions!


int main() {
    hwlib::wait_ms(1'000);
    // turn the onboard led on
    tsy::pin_out{tsy::pins::d13}.write(1);
    protocol comm;
    for (;;) {
        // hwlib::cout << "receiving data...\r\n";
        auto const succesful_receive{comm.receive()};
        hwlib::cout << hwlib::hex << crc32(
            comm.get_data().cbegin() + 4,
            comm.get_data().cbegin() + 126*126*3 + 4u) << "\r\n";
        if(succesful_receive){
            //hwlib::cout << "success\r\n";
            // std::array<std::uint8_t, 126*126*3 + 4u> image;
            // for(unsigned int i=0; i<126*126*3 + 4u; i++){
            //     image[0] = i % 0xFF;
            // }
            test_algorithm(comm.get_data());
        }
        

    }
    tsy::pin_out{tsy::pins::d13}.write(0);
    return 0;
}
