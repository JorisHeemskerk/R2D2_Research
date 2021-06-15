// CRC32 function from (with fixed int types):
//   https://rosettacode.org/wiki/CRC-32#C.2B.2B

#ifndef CRC32_HPP
#define CRC32_HPP

#include <algorithm>
#include <array>
#include <cstdint>
#include <numeric>
 
// Generates a lookup table for the checksums of all 8-bit values.
std::array<std::uint32_t, 256> generate_crc_lookup_table() noexcept
{
  auto const reversed_polynomial = std::uint32_t{0xEDB88320uL};
 
  // This is a function object that calculates the checksum for a value,
  // then increments the value, starting from zero.
  struct byte_checksum
  {
    std::uint32_t operator()() noexcept
    {
      std::uint32_t checksum{n++};
 
      for (auto i = 0; i < 8; ++i)
        checksum = (checksum >> 1) ^ ((checksum & 0x1u) ? reversed_polynomial : 0);
 
      return checksum;
    }
 
    std::uint32_t n = 0;
  };
 
  auto table = std::array<std::uint32_t, 256>{};
  std::generate(table.begin(), table.end(), byte_checksum{});
 
  return table;
}
 
// Calculates the CRC for any sequence of values. (You could use type traits and a
// static assert to ensure the values can be converted to 8 bits.)
template <typename InputIterator>
std::uint32_t crc32(InputIterator first, InputIterator last)
{
  // Generate lookup table only on first use then cache it - this is thread-safe.
  static auto const table = generate_crc_lookup_table();
 
  // Calculate the checksum - make sure to clip to 32 bits, for systems that don't
  // have a true (fast) 32-bit type.
  return std::uint32_t{0xFFFFFFFFuL} &
    ~std::accumulate(first, last,
      ~std::uint32_t{0} & std::uint32_t{0xFFFFFFFFuL},
        [](std::uint32_t checksum, std::uint32_t value) 
          { return table[(checksum ^ value) & 0xFFu] ^ (checksum >> 8); });
}

#endif
