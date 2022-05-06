## Dots and Boxes (with weightage)

### Original Game rules:
1) Players take turns joining two horizontally or vertically adjacent dots by a line
2) A player that completes the fourth side of a square (a box) colors that box and must play again
3) When all boxes have been colored, the game ends, and the player who has colored more boxes wins

### Variant Game rules:
1) Each square in the grid will be assigned either a 0 or a positive integer or a negative integer. The entire board will just contain one zero, and a minimum of three negative integers
2) The score calculation will be done by multiplying all the numbers present in the captured squares. The player who has the maximum score at the end wins the game
3) The player who makes the last line to complete the box captures that square
4) Upon acquiring a square, the player gets another turn
5) The player with the highest score wins the game


<p align="center">
  <img width="460" height="500" src="https://user-images.githubusercontent.com/77983487/167226866-6cf17e15-56aa-4075-9721-bea07e2961f3.gif">
</p>


### Game Code:
There are 3 files in the code:
#### File 1: main.py 
<p align="center">
  <img src= "https://user-images.githubusercontent.com/77983487/167226269-eff2bd0d-cdca-4327-a985-196c9cfad15e.png">
</p>
This file is for the two AI players playing against each other
Player 1 
This player is implemented using some predefined strategies
1) Look for any boxes where three edges are occupied
2) Mark an edge on box with maximum score 
3) Do not form the last edge on box with zero score
4) Do not mark edge on box with two occupied edges
Player 2 
This player is implemented using minimax algorithm

#### File 2: AI_player_strategy.py  
Player 1 is human player
Player 2 is AI player implemented with some predefined strategies

#### File 3: AI_player_with_minimax.py
Player 1 is human player
Player 2 is AI player implemented using minimax algorithm

### Big-O Analysis:
Big-O for the heuristic function in the MinMax algorithm: O(n), where n is the number of boxes in the game board.

The heuristic score is evaluated by substracting the score of player1(strategies based player) from the score of player2(player based on minmax) at any given game state. But to evaluate the score of each player for a particular game state it is necessary to check the board status which is stored in a numpy 2D array and it depicts how many edges of the box are occupied. 
Each element in the numpy array represents a box initially depicted with a 0. This count increases as the the number of edges occupied increases. As the box becomes fully occupied, this count becomes 4.

Time taken to search the occupied boxes depends on the total number of boxes on the board. Hence the Big-O for MinMax heuristic function is O(n) where n is the number of boxes.

### Challenges:
While implementing minimax algorithm, the major challenge that we faced was we were not able to create a deepcopy of the class which had objects belonging to tkinter library. (GUI library)
We got the this exception: TypeError: cannot pickle '_tkinter.tkapp' object ( [reference](https://stackoverflow.com/questions/50568880/cant-pickle-tkinter-tkapp-objects-error-when-trying-to-create-multiple-instanc) )
To overcome this problem, we had to create a separate file called utility.py with all the tkinter objects excluded and duplicate functions included(functions from the main.py file) to keep a track of the board and play the game using minimax algorithm. 
This is the reason why minimax player fails to win the game at times.

### Refrences:
https://github.com/aqeelanwar/Dots-and-Boxes
https://github.com/Armando8766/Dots-and-Boxes





