# cis191project

This is a project for a vim learning tool implemented in python. 

Dependencies include pygame which can be installed here: https://www.pygame.org/wiki/GettingStarted

After downloading the files, the game can be run from the command line with '''python3 vim_game.py'''

This brings you to the initial screen with level select. Each button takes you to a different level.

To navigate back, simply type :q 

Availible vim commands: 
  :q to navigate back to home
   dd to delete row
   dw to delete word from cursor to end of word
   x to delet character 
   z not implemented in vim, this button will check if you solved the puzzle. If so, it will take you to a victory screen and then the next level. Otherwise it will reset the puzzle. 

Level 1:
  Teaches you how to use the x command, simply remove the dashes
Level 2:
  Teaches you how to use the dd command, simply remove gibberish rows
Level 3:
  Teaches you how to use dw command, remove all instances of the word fruit except the first one.

After completeing level 3, you will be able to see a victory screen. Then you can nagivate back to the main page. 
