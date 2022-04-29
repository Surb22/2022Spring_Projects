## Dots and Boxes (with weightage)

### Original rules 
1) Players take turns joining two horizontally or vertically adjacent dots by a line
2) A player that completes the fourth side of a square (a box) colors that box and must play again
3) When all boxes have been colored, the game ends, and the player who has colored more boxes wins

### Variant rules:
1) Each square in the grid will be assigned either a 0 or a positive integer or a negative integer. The entire board will just contain one zero, and a minimum of three negative integers
2) The score calculation will be done by multiplying all the numbers present in the captured squares. The player who has the maximum score at the end wins the game

### Game Code:
#### Player1: 
AI chooses move based on MinMax Algorithm
#### Player2: 
AI chooses move based on following strategy:
1) Look for any boxes where three edges are occupied
2) Mark an edge on box with maximum score 
3) Do not form the last edge on box with zero score
4) Do not mark edge on box with two occupied edges

