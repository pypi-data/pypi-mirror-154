# Copyright (c) 2017, 2020 Pieter Wuille
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Platon Bech32 address implementation.
"""

from typing import Iterable, List, Optional, Tuple, Union

CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def _bech32_polymod(values: Iterable[int]) -> int:
    """
    Internal function that computes the Bech32 checksum.
    """
    generator = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for value in values:
        top = chk >> 25
        chk = (chk & 0x1ffffff) << 5 ^ value
        for i in range(5):
            chk ^= generator[i] if ((top >> i) & 1) else 0
    return chk


def _bech32_hrp_expand(hrp: str) -> List[int]:
    """
    Expand the HRP into values for checksum computation.
    """
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def _bech32_verify_checksum(hrp: str, data: Iterable[int]) -> bool:
    """
    Verify a checksum given HRP and converted data characters.
    """
    return _bech32_polymod(_bech32_hrp_expand(hrp) + list(data)) == 1


def _bech32_create_checksum(hrp: str, data: Iterable[int]) -> List[int]:
    """
    Compute the checksum values given HRP and data.
    """
    values = _bech32_hrp_expand(hrp) + list(data)
    polymod = _bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]


def _bech32_encode(hrp: str, data: Iterable[int]) -> str:
    """
    Compute a Bech32 string given HRP and data values.
    """
    combined = list(data) + _bech32_create_checksum(hrp, data)
    return hrp + "1" + "".join([CHARSET[d] for d in combined])


def _bech32_decode(bech: str) -> Union[Tuple[None, None], Tuple[str, List[int]]]:
    """
    Validate a Bech32 string, and determine HRP and data.
    """
    if (any(ord(x) < 33 or ord(x) > 126 for x in bech)) or (
            bech.lower() != bech and bech.upper() != bech
    ):
        return None, None
    bech = bech.lower()
    pos = bech.rfind("1")
    if pos < 1 or pos > 83 or pos + 7 > len(bech):  # or len(bech) > 90:
        return None, None
    if not all(x in CHARSET for x in bech[pos + 1:]):
        return None, None
    hrp = bech[:pos]
    data = [CHARSET.find(x) for x in bech[pos + 1:]]
    if not _bech32_verify_checksum(hrp, data):
        return None, None
    return hrp, data[:-6]


def _convertbits(data: Iterable[int], frombits: int, tobits: int, pad: bool = True) -> Optional[List[int]]:
    """
    General power-of-2 base conversion.
    """
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    max_acc = (1 << (frombits + tobits - 1)) - 1
    for value in data:
        if value < 0 or (value >> frombits):
            return None
        acc = ((acc << frombits) | value) & max_acc
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        return None
    return ret


def bech32_decode(addr: str, hrp: str = None) -> Union[Tuple[None, None], Tuple[int, List[int]]]:
    """
    Decode a platon address.
    """
    hrpgot, data = _bech32_decode(addr)
    if hrp and hrpgot != hrp:
        return None, None
    assert data is not None
    decoded = _convertbits(data[:], 5, 8, False)
    if decoded is None or len(decoded) < 2 or len(decoded) > 40:
        return None, None
    if len(decoded) != 20 and len(decoded) != 32:
        return None, None
    return hrpgot, decoded


def bech32_encode(witprog: Iterable[int], hrp: str) -> Optional[str]:
    """
    Encode a platon address.
    """
    five_bit_witprog = _convertbits(witprog, 8, 5)
    if five_bit_witprog is None:
        return None
    ret = _bech32_encode(hrp, five_bit_witprog)
    if bech32_decode(ret, hrp) == (None, None):
        return None
    return ret
