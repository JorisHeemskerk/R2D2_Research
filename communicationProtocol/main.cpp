#include "crc32.hpp"
#include "protocol-tsy.hpp"
#include "algorithm-tester.hpp"
#include "hwlib.hpp"


// BEFORE RUNNING MAKE SURE TO CHECK THAT THE PINS ARE SET CORRECTLY IN protocol-tsy.hpp OR YOU MIGHT GET UNDEFINED BEHAVIOUR!


int main() {
    hwlib::wait_ms(1'000);
    // turn the onboard led on
    tsy::pin_out{tsy::pins::d13}.write(1);
    protocol comm;
    // hwlib::cout << "pre- for loop1\r\n";
    // hwlib::cout << "pre- for loop2\r\n";
    // hwlib::cout << "pre- for loop3\r\n";
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
