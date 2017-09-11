# Tetris-Game
A Tetris game written in python, with a twist

![alt text](.\Preview.PNG "A triple Tetris!")
## Setting up

A conda environment is used for development, install conda from [here](https://docs.continuum.io/anaconda/install/windows) 

After installation, you can clone the environment by using:

`conda env create -f environment.yml`

After installation, activate the environment using

`activate game`

And finally, run the application:

`python Tetris.py`

## Compiling from source

**This will overwrite everything in `build`**

With environment activated, run:

`python setup.py build`



A build folder will be created containing an EXE file
Make sure `python36.dll` is included, if not, copy to the same folder as the EXE

This dll should be fine, however, if problems arise, please copy from your environment, located in:

`C:\Users\User\.conda\envs\game`

## Known bugs
- Zone color is assigned as the first falling block appends to its zone, therefore,
it is possible to have the same color in more than 1 zone.


## Future implementations
- Don't close game at Game Over
   - Currently game exits at game over
- Blocks generate at random rotations

## Original requirements

- [x] 7 pieces exist
- [x] 3 different colors for pieces
- [x] 3 zones exists
- [x] Score goes up at each line made
   - Falling speed is affected by score, the higher the score, the faster the fall
   - Around Score = 35 falling time is around 3 seconds top to bottom
- [x] Pieces and color are generated randomly
- [x] Pieces fall automatically
- [x] Piece should appear at top center of screen
- [x] Switch columns in game, free mechanic
   - CTRL and ALT keys on left side of keyboard are used for this
- [x] Break piece if misplaced, keep 2 squares
- [x] After breaking, append randomly to each other column
   - Called "Outliers" here on
- [x] Outliers can't complete a line
- [x] Outliers are removed on scoring a line
   - Penalty removal is implemented as `SCORE % 3` for column selection
   - If column has no outliers, try one more time with its neighbor
   - Outlier removal is random once a column is selected
- [x] If outlier has something above it, fall down
- [x] If lines are made due fall after outlier, treat them as player made
- [x] Documentation and player controls
   - This file is documentation, also included as a PDF
   - Commit logs in `Commit_Logs.txt` shows commits made until completion
   - Player controls are in game
- [x] Executable file
   - Contained in build/exe.win-amd64-3.6/Tetris.exe