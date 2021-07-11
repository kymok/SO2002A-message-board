try:
    from smbus2 import SMBus
except ModuleNotFoundError:
    print('No smbus2 found. Running dummy')

    # Dummy Class
    class SMBus:
        def __init__(self, bus) -> None:
            print('### DUMMY ###')
            print('bus:', bus)
            pass

        def write_i2c_block_data(self, address, offset, data):
            print('### DUMMY ###')
            print('address:', address)
            print('offset:', offset)
            print('data:', data)

bus = SMBus(1)
address = 0x3c
n_cols = 20
n_lines = 2

def reset(showCursor=False, address=address) :
    if(showCursor):
        bus.write_i2c_block_data(address, 0, [0x01, 0x02, 0x0f]) # turn on with cursor
    else:
        bus.write_i2c_block_data(address, 0, [0x01, 0x02, 0x0c]) # turn on without cursor

def write_line(line, address=address):
    line_justified = line.ljust(n_cols)[:n_cols]
    data = list(map(ord, line_justified))
    bus.write_i2c_block_data(address, 0x40, data)

def write_lines(lines, address=address):
    data = lines[:n_lines]
    for line in data:
        write_line(line, address)