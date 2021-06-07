#ifndef PROTOCOL_HPP
#define PROTOCOL_HPP

#include "crc32.hpp"
#include "hwlib.hpp"
#include <utility>

namespace tsy = hwlib::target;

namespace {
constexpr bool debug{
    // true // uncomment this to enable debugging
};
static unsigned msg_id{};

template<typename... Ts>
constexpr void dbg(Ts&&... args) {
    if constexpr (debug) {
        hwlib::cout << "[dbg#" << hwlib::dec << msg_id++ << ']';
        ((hwlib::cout << std::forward<Ts>(args)), ...) << "\r\n";
    }
}

template<typename... Ts>
constexpr void dbgx(unsigned interval, int wait_ms, Ts&&... args) {
    if constexpr (debug) {
        if ((msg_id % interval) == 0) {
            dbg(std::forward<Ts>(args)...);
        } else {
            ++msg_id;
        }
        hwlib::wait_ms(wait_ms);
    }
}
} // anonymous-namespace

class protocol {
    static constexpr auto max_buff_size{126*126*3 + 4u};

    using ring_buff = struct {
        std::uint8_t& operator[](unsigned index)
        { return data[index % max_buff_size]; }

        std::array<std::uint8_t, max_buff_size> data;
    };
public:
    protocol():
        bit0{tsy::pins::d14},
        bit1{tsy::pins::d15},
        bit2{tsy::pins::d22},
        bit3{tsy::pins::d17},
        bit4{tsy::pins::d18},
        bit5{tsy::pins::d19},
        bit6{tsy::pins::d20},
        bit7{tsy::pins::d21},
        bus{hwlib::port_in_from(
            bit0, bit1, bit2, bit3, bit4, bit5, bit6, bit7)},
        pi_ready{tsy::pins::d11},
        tsy_ready{tsy::pins::d10},
        start_signal{tsy::pins::d8},
        stop_signal{tsy::pins::d9}
    {}

    bool receive() {
        start_signal.write(1);
        dbg("start signal on");

        // wait for stop signal off from Pi
        while (stop_signal.read()) {
            dbgx(20, 100, "stop signal on");
        }
        for (auto index = 0u;;) {
            if (stop_signal.read()) {
                dbg("stop signal on");
                auto const valid_crc32 = is_crc32_valid(index);

                if (not valid_crc32) {
                    // set Teensy ready on, when crc32 is invalid
                    tsy_ready.write(1);
                    dbg("crc32 mismatch");
                }
                start_signal.write(0);
                dbgx(1, 1'000, "start signal off");
                return valid_crc32;
            }
            if (pi_ready.read()) {
                dbg("pi ready on");
                // read data from the bus
                buff[index] = bus.read();
                dbg("data received: ", hwlib::hex, buff[index]);
                ++index;
                // signal Pi that we are ready
                tsy_ready.write(1);
                dbgx(1, 1'000, "teensy ready on");
                // wait for Pi to clear its ready signal
                while (pi_ready.read()) {
                    dbgx(20, 100, "pi ready on");
                }
                // clear our own ready signal
                tsy_ready.write(0);
                dbg("teensy ready off");
            } else {
                dbgx(20, 100, "stop signal off, pi ready off");
            }
        }
    }

    decltype(ring_buff::data) const& get_data() const
    { return buff.data; }
private:
    bool is_crc32_valid(unsigned bytes_read) const {
        using crc_type = std::uint32_t;
        auto const crc_size = sizeof(crc_type);
        dbg("bytes read: ", bytes_read);

        if (bytes_read <= crc_size) {
            dbg("too few bytes read");
            return false;
        }
        if (crc_size >= buff.data.size()) {
            dbg("buffer size too small");
            return false;
        }
        auto const checksum_data = buff.data[3]
            | static_cast<crc_type>(buff.data[2]) << 8
            | static_cast<crc_type>(buff.data[1]) << 16
            | static_cast<crc_type>(buff.data[0]) << 24;
        dbg("received checksum: ", hwlib::hex, checksum_data);
        auto const checksum_gen = crc32(
            buff.data.cbegin() + crc_size,
            buff.data.cbegin() + bytes_read);
        dbg("generated checksum: ", hwlib::hex, checksum_gen);
        return checksum_data == checksum_gen;
    }

    tsy::pin_in bit0;
    tsy::pin_in bit1;
    tsy::pin_in bit2;
    tsy::pin_in bit3;
    tsy::pin_in bit4;
    tsy::pin_in bit5;
    tsy::pin_in bit6;
    tsy::pin_in bit7;
    hwlib::port_in_from_pins_t bus;

    tsy::pin_in pi_ready;
    tsy::pin_out tsy_ready;

    tsy::pin_out start_signal;
    tsy::pin_in stop_signal;

    ring_buff buff;
};

#endif
