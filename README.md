# Tetris-Game
A tetris game written in python

## Setting up

A conda environment is created, install conda from [here]() you can clone it by using:

`conda env create -f environment.yml`

After installation, activate the environment using

`activate game`

And finally, run the application:

`python Tetris.py`

## Compiling from source

With environment activated, run:

`python setup.py build`

A build folder will be created containing an EXE file
Make sure `python36.dll` is included, if not, copy to the same folder as the EXE

## Known bugs
- Zone color is assigned as the first falling block appends to it´s zone, therefore,
it is possible to have the same color in more than 1 zone.


## Future implementations
- Game don't closes at Game Over
- Blocks generate at random positions