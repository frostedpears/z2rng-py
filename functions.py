# Zelda 2 RNG tools # July 28 2021 # Written by FrostedPears
import numpy as np

class frameCount:
    # the number of frames it takes to do a specific action
    walk = 248         # frames from entering Carrocks room to the life bar appearing
    firstSpawn = 47    # frames from life bar appearing to Carrocks first reposition
    spawn = 49         # frames between each spawn
    stab = 30          # frames for stabbing, when stopping your full momentum, and allowing room to gain it again
    crouchStab = 24    # I am not confident of the accuracy of this. I find it hard to perform consistently
    fullRoomWalk = 711 # for walking all the way through the room before Carrock, left to right
    fairyRoom = 712    # for using fairy to go down the elevator and across the room before the room before Carrock
    # directions indicate the direction that the player holds, in order to perform the action,
    # so loopLeft is the number of frames elapsed, staring with the A5 frame when entering a room to the right, 
    # and holding left until you get the next A5 frame from entering a room to the left
    loopLeft = 86
    loopRight = 92
    elevatorLoopDown = 56
    elevatorLoopUp = 50

# options for writeArray
class numberFormat:
    hex = "hex"
    dec = "dec"

class valueSeparator:
    tab = "\t"
    newline = "\n"

# return an array of bits for holding rng values, 9 bytes long
# the default values are A5,0,0,0,0,0,0,0,0
def newBitArray(byte1 = 0xA5, byte2 = 0, byte3 = 0, byte4 = 0,
        byte5 = 0, byte6 = 0, byte7 = 0, byte8 = 0, byte9 = 0):
    hexArray = np.array([byte1, byte2, byte3, byte4,
        byte5, byte6, byte7, byte8, byte9], dtype=np.uint8)
    bitArray = np.unpackbits(hexArray)
    #print(bitArray)
    #print("{:02X} {:02X}".format(hexArray[0], hexArray[1]))
    return bitArray

# sets a byte at the given index to the given value
# 0 indexed, so to change the first byte, use index 0
def setByte(bitArray, index = 0, byteValue = 0):
    hexArray = np.packbits(bitArray)
    hexArray[index] = byteValue
    bitArray = np.unpackbits(hexArray)
    return bitArray

# convenience method to set Byte 1 of the array to A5, as when entering a new room
def setByte1ToA5(bitArray):
    bitArray = setByte(bitArray, 0, 0xa5)
    return bitArray

# returns the value of the byte at the given index
# 0 indexed, so to get the first byte, use index 0
def getByte(bitArray, index = 0):
    byte = np.packbits(bitArray[index * 8 : (index*8) + 7])[0]
    return byte


# steps forward a given number of frames, applying the proper rng formula each frame
# note that if Byte 1 is set to A5 on a frame, it is done after that frames rng is applied
def shiftRng(bitArray, frames):
    for i in range (0, frames):
        x = np.bitwise_xor(bitArray[6], bitArray[14])

        bitArray = np.delete(bitArray, len(bitArray)-1)
        bitArray = np.insert(bitArray, 0, x)
    return bitArray

# prints out the hex values of each byte in the array
def printHex(bitArray):
    hexArray = np.packbits(bitArray)
    print("{:02X} {:02X} {:02X} {:02X} {:02X} {:02X} {:02X} {:02X} {:02X}"
        .format(hexArray[0], hexArray[1], hexArray[2], hexArray[3],
        hexArray[4], hexArray[5], hexArray[6], hexArray[7], hexArray[8]))
    return

# writes an array of hex bytes to a file, separated by tabs or newlines
# used by writeSpawnPattern to write a list of spawn positions
# used by writeByte2 to write a list of Byte2 values
# calling with writeSeed = True will start each row with the original seed
def writeArray(array, filename, seed = 0, writeSeed = False, format = numberFormat.hex, separator = valueSeparator.tab):
    file = open(filename, "a")
    if (writeSeed == True):
        if (format == numberFormat.hex):
            seedString = "{:02X}".format(seed)
        else:
            seedString = str(seed)

        file.write(seedString + separator)

    for b in array:
        if (format == numberFormat.hex):
            byteString = "{:02X}".format(b)
        else:
            byteString = str(b)
            
        file.write(byteString + separator)
    file.write("\n")
    file.close

# writes the spawn positions of Carrock, given a seed, 
# which is the value of Byte 2 at the A5 frame upon entering
# Carrock's room
# use writeSpawnPatternRange to get a a table of spawn patterns
# for every starting seed 00-FF
def writeSpawnPattern(seed, filename, numberOfSpawns = 20, format = numberFormat.hex):
    spawnByteArray = []
    bitArray = newBitArray(0xa5, seed)

    # this will shift the rng a number of frames equal to
    # the time it takes to walk from the door to Carrock.
    # add additional shiftRng lines to test different
    # numbers of frames, for instance, add stab to see what spawns
    # you would get if you stabbed during the walk
    bitArray = shiftRng(bitArray, frameCount.walk)
    bitArray = shiftRng(bitArray, frameCount.firstSpawn)

    # Carrock always appears at b0 first
    spawnByteArray.append(0xb0)

    spawnByte = getByte(bitArray, 6)
    spawnByteArray.append(spawnByte)

    for i in range(0, numberOfSpawns):
        bitArray = shiftRng(bitArray, frameCount.spawn)
        spawnByte = getByte(bitArray, 6)
        spawnByteArray.append(spawnByte)

    writeArray(spawnByteArray, filename, seed, True, format)
    return

# calls writeSpawnPattern for every starting seed 00-FF 
def writeSpawnPatternRange(filename, numberOfSpawns = 20, format = numberFormat.hex):
    for i in range(0, 256):
        writeSpawnPattern(i, filename, numberOfSpawns, format)
    return

# writes the value of Byte 2 for every frame from firstFrame to lastFrame, 
# given a seed, using the value of A5 for Byte 1
# use writeByte2Range to get a table of Byte 2 values for every seed from 00-FF
def writeByte2(seed, filename, firstFrame = 0, lastFrame = 60, format = numberFormat.hex):
    byte2Array = []
    bitArray = newBitArray(0xa5, seed)
    # start by advancing to the given first frame
    if (firstFrame > 0):
        bitArray = shiftRng(bitArray, firstFrame)
        byte2 = getByte(bitArray, 1)
        byte2Array.append(byte2)

    # advance frames equal to the difference between the first and last frame, 1 at a time
    for i in range(firstFrame, lastFrame):
        bitArray = shiftRng(bitArray, 1)
        byte2 = getByte(bitArray, 1)
        byte2Array.append(byte2)
    
    writeArray(byte2Array, filename, seed, True, format)
    return

# calls writeSpawnPattern for every starting seed 00-FF 
def writeByte2Range(filename, firstFrame = 0, lastFrame = 60, format = numberFormat.hex):
    for seed in range(0,256):
        writeByte2(seed, filename, firstFrame, lastFrame, format)
    return

# for use with the output of an emulator script, which logged the value of Byte 2 every frame
# this function counts the frequency of each value
# probably not useful. This is when I was trying to improve the chance of survival, before
# learning that a guaranteed damageless method existed
def countSeeds(filename):
    with open(filename) as seedFile:
        rngArray = np.loadtxt(seedFile, dtype=int, delimiter="\n", )

    print(np.bincount(rngArray).argmax())
    unique, frequency = np.unique(rngArray, return_counts = True)
    for i in range(0, len(unique)):
        print("{0}\t{1}".format(unique[i], frequency[i]))
    return