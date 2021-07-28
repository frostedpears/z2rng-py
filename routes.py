# Zelda 2 RNG tools # July 28 2021 # Written by FrostedPears
import numpy as np
import functions as f

# writes the value of Byte 2 after executing
def writeByte2List(filename):
    file = open(filename, "a")
    byte2Array = []

    for i in range(0,256):
        # start with A5 frame
        bitArray = f.newBitArray(0xa5,i)
        # if we start from Carrock's room, we don't record the left movement, since
        # we only start once we get the A5 frame going into the room on the left.
        # by then, we are holding right, and therefore use the loopRight timing
        bitArray = f.shiftRng(bitArray, f.frameCount.stab)
        bitArray = f.shiftRng(bitArray, f.frameCount.loopRight)
        bitArray = f.setByte1ToA5(bitArray)
        # now we have the A5 frame going right, so we record the delay for re-entry 
        # holding left
        bitArray = f.shiftRng(bitArray, f.frameCount.loopLeft)
        bitArray = f.setByte1ToA5(bitArray)
        # perform the stab, right again
        bitArray = f.shiftRng(bitArray, f.frameCount.stab)
        bitArray = f.shiftRng(bitArray, f.frameCount.loopRight)
        bitArray = f.setByte1ToA5(bitArray)
        #
        byte2 = f.getByte(bitArray, 1)
        byte2Array.append(byte2)
    
    f.writeArray(byte2Array, filename, i, False, f.numberFormat.dec, f.valueSeparator.newline)
    return

def printRngResult():
    bitArray = f.newBitArray(0xa5,0x11,0x9b,0xb8,0x8f,0xfe)
    bitArray = f.shiftRng(bitArray, f.frameCount.fullRoomWalk)
    bitArray = f.setByte(bitArray, 0, 0xa5)
    f.printHex(bitArray)
    return
