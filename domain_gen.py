import binascii

domain = "2mdn"
tld = ".net"

bin_repr = bin(int.from_bytes(domain.encode(), 'big'))
bin_repr = bin_repr[2:] #chop off '0b'

for index, bit in enumerate(bin_repr):
    if bit == '1':
        bit = '0'
    else:
        bit = '1'

    new_bin_repr = bin_repr[:index] + bit + bin_repr[index + 1:]
    new_bin_repr = '0b' + new_bin_repr

    n = int(new_bin_repr, 2)
    try:
        new_domain = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
        print(new_domain.lower() + tld)
    except:
        pass
