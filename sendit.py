import argparse
import sys
import serial
import time


parser = argparse.ArgumentParser()
parser.add_argument('--serialport',help='Serial port to send to', default='/dev/ttyUSB0')
parser.add_argument('--baud',help='Baud rate', default=115200, type=int)
args = parser.parse_args()

def serial_txrx(serial_port, tx):
    # we trim the line down as much as possible to try and avoid tripping CH340 issues
    tx = tx.replace(' ', '').replace(';', '').strip() + '\n'
    serial_port.write(tx.encode('ascii'))

    r = ''
    while True:
        line = serial_port.readline().decode('ascii').strip()
        if line[0] in {'$', '['}:
            r += line + '\n'
            continue
        if line.strip() == 'ok':
            break
        else:
            print(f'Unexpected response to {tx.strip()} -- {line}', file=sys.stderr)
            break

    return r

# setup the serial port
serial_port = serial.Serial(args.serialport, args.baud)
serial_port.write('\r\n\r\n'.encode('ascii'))
time.sleep(2)
serial_port.flushInput()

# see if we get a sensible response to $$
serial_txrx(serial_port, '$$')
serial_txrx(serial_port, '$X')

# send the file at it
for line in sys.stdin:
    line = line.strip()
    serial_txrx(serial_port, line)

# wait for it to become idle
while True:
    serial_port.write('?'.encode('ascii'))
    line = serial_port.readline().decode('ascii').strip()
    if 'Idle' in line:
        break
    time.sleep(0.25)
