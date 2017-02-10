# BatAlgorithm_Tetris_Pong
This is my TIPE project for the ENS admission exam.  
 
I used several different evolutionary algorithms (especially genetic algorithm, differential evolution and bat algorithm) to train tetris and pong agents to play the game. To run the program, this directory should be in the python path and pygame and pybrain are needed (therefore all their dependancies are also needed).  
 
One must replace the pybrain/optimization/poplationbased/ga.py file by the one that appears here. It's not quite a good way to do things but I did it just like this. Then, for example, by calling Tetris_display().display(bot,b9) you can see a tetris agent trained by the (improved) bat algorithm playing the game. (Tetris_display from tetris/tetris_AI/tetris_evalu.py, bot from tetris/tetris_AI/tetris_bot.py and b9 from tetris/tetris_training/tetris_training_functions.py)  

Besides, I picked up several online open source projects as the base of the different parts of my implementations.  

If you're really interested and if you understand French, you can see the pdf file for more details.
