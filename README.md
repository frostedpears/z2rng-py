## Zelda 2 Random Number Simulator

### Technology
Written with `Python 3.8.5` and `NumPy 1.21.1`  
Has not been tested with other versions.

### Usage
Run with `python program.py`  
A text file with the program's output will be created at `output/output.txt`  
Uncomment, or add function calls in the `main()` function in order to specify what operations you want to run.

### Files
`program.py` The main script, which should be run to access other functionalities  
`functions.py` Functions for Zelda 2 RNG calculations, as well as functions for outputting Carrock patterns  
`routes.py` A place to string together movement, in order to test what the state of the RNG will be after a prescribed set of actions

### Important Concepts
Zelda 2's RNG consists of 9 bytes. The first 2 bytes are used in determining how the RNG will change each frame.  
*riiyak has a good explanation of the topic here: https://youtu.be/Hbe3JqWdVd4*  
Every time Link enters a new side scrolling area, Byte 1 is set to 0xA5 (165). For that reason, Byte 2 is important, since its value can't be reliably set.  
Byte 7 is used as the X position of Carrock's spawn points.
