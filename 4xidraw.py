from os import read
from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces
import argparse
import sys
import serial
import time


class DrawingMachine(interfaces.Gcode):
    def __init__(self):
        super().__init__()
        self.precision = 4

    def laser_off(self):
        return "M5\nG4P0.5"

    def set_laser_power(self, power):
        if power == 0:
            return f"M5\nG4P0.5"

        else:
            return f"M3 S255\nG4P0.5"


parser = argparse.ArgumentParser()
parser.add_argument('svgin', help="SVG file to process")
parser.add_argument('--gcodeout', help="GCode file to output (will use stdout if omitted")
parser.add_argument('--serialport',help='Serial port to send to', default='/dev/ttyUSB0')
parser.add_argument('--baud',help='Baud rate', default=115200, type=int)
args = parser.parse_args()

# render the file into gcode
curves = parse_file(args.svgin)
gcode_compiler = Compiler(DrawingMachine, movement_speed=10000, cutting_speed=10000, pass_depth=0, unit="mm")
gcode_compiler.append_curves(curves)
gcode = gcode_compiler.compile()

print(gcode)
exit(0)

# def serial_txrx(serial_port, tx):
#     tx = tx.replace(' ', '').replace(';', '').strip() + '\n'
#     serial_port.write(tx.encode('ascii'))

#     r = ''
#     while True:
#         line = serial_port.readline().decode('ascii').strip()
#         if line[0] in {'$', '['}:
#             r += line + '\n'
#             continue
#         if line.strip() == 'ok':
#             break
#         else:
#             print(f'Unexpected response to {tx.strip()} -- {line}', file=sys.stderr)
#             break

#     return r

# # setup the serial port
# serial_port = serial.Serial(args.serialport, args.baud)
# serial_port.write('\r\n\r\n'.encode('ascii'))
# time.sleep(2)
# serial_port.flushInput()

# # see if we get a sensible response to $$
# serial_txrx(serial_port, '$$')
# serial_txrx(serial_port, '$X')

# # send the file at it
# for line in gcode.split('\n'):
#     line = line.strip()
#     serial_txrx(serial_port, line)

# # wait for it to become idle
# while True:
#     serial_port.write('?'.encode('ascii'))
#     line = serial_port.readline().decode('ascii').strip()
#     if 'Idle' in line:
#         break
#     time.sleep(0.25)

# # FIXME: need to wait until it is empty
# # if args.gcodeout:
# #     gcode_compiler.compile_to_file(args.gcodeout)
# # else:
# #     sys.stdout.write(gcode_compiler.compile())
