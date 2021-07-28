# Zelda 2 RNG tools # July 28 2021 # Written by FrostedPears
import numpy as np
import functions as f
import routes as r

# functions.py contains the bulk of the logic
# routes.py is for testing particular combinations of movements
#
# there are no inputs, to use, put the function with the parameters that you want to run 
# into the main method below and run this script

outputFilename = "output/output.txt"

# uncomment any of these functions to use them as written, or write a similar function call
def main():
    # write the value of Byte 2 at each frame for every seed 00-FF
    f.writeByte2Range(outputFilename, 61, 120, f.numberFormat.dec)

    # write the first 20 spawn positions of Carroc for every seed 00-FF
    # f.writeSpawnPatternRange(outputFilename, 20, f.numberFormat.hex)

    # write the Byte 2 value for every seed from 00-FF after performing the actions in the routes.py function
    # r.writeByte2List(outputFilename)

    # print all the RNG Bytes using the starting values and actions in the routes.py function
    # r.printRngResult()
    return

main()