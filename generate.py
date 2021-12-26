from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces
import argparse


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
args = parser.parse_args()

# render the file into gcode
curves = parse_file(args.svgin)
gcode_compiler = Compiler(DrawingMachine, movement_speed=10000, cutting_speed=10000, pass_depth=0, unit="mm")
gcode_compiler.append_curves(curves)
gcode = gcode_compiler.compile()

print(gcode)
