#include "crc32.hpp"
#include "protocol-tsy.hpp"
#include "hwlib.hpp"

int main() {
    hwlib::wait_ms(1'000);
    // turn the onboard led on
    tsy::pin_out{tsy::pins::d13}.write(1);
    protocol comm;

    for (;;) {
        hwlib::cout << "receiving data...\r\n";
        auto const on_success{comm.receive()};
        hwlib::cout << "  checksum: " << hwlib::hex << crc32(
            comm.get_data().cbegin() + 4,
            comm.get_data().cbegin() + 126*126*3 + 4u) << "\r\n";
        // for (auto i = 0u; i < 4; ++i) {
        //     hwlib::cout << hwlib::hex << comm.get_data()[i] << ' ';
        //     crc32(comm.get_data().cbegin() + 4,
        //         comm.get_data()cbegin() + 126*126*3 + 4u);
        // }
        // hwlib::cout << "\r\n";
        on_success
            ? hwlib::cout << "  data received successfully\r\n"
            : hwlib::cout << "  data received failed\r\n";
        // hwlib::cout << "data: ";
        // for (auto const byte : comm.get_data()) {
        //     hwlib::cout << hwlib::hex << byte << ' ';
        //     if (byte == 0xFF) break;
        // }
        // hwlib::cout << "\r\n";
    }
    return 0;
}
