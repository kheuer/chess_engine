# Chess Engine
This is a simple Chess Engine you can play against. The algortithms used are MiniMax and Monte Carlo Tree Search.
The difficulty level is determined by the AI opponent chosen, it can also be changed during a match. 

The available AI opponents are:
- random: This always chooses a random move and will perform worse than any player
- minimax_2: This chooses the strongest move while looking 1 turn ahead without making mistakes.
- terrible_player: This generally uses minimax_2 but sometimes blunders by making a random move. This is equivalent to a complete novice players style. 
- minimax_3 / minimax_4 / minimax_5: This chooses the strongest move while looking 3 - 5 moves ahead. On this difficulty it can beat a new to intermediary player.
- minimax_auto: This plays the minimax_5 algorithm but looks an additional turn ahead in the endgame where computation is easier.
- mcts_1s / mcts_3s / mcts_6 / mcts_10s: This performs a Monte Carlo Tree search which will be abrupted after 1-10 seconds respectively.

## MiniMax Algorithm
The algorithm used for most opponents is the MiniMax Algorithm, a popular backtracking algorithm in Game Theory and Artificial Intelligence. A requirement for this is being able to express each position reachable in game as a numeric score describing how favourable it is for each player. It then considers each possible chess move, every possible response of the opponent, the AI´s responses to the opponents response and so on. It then assumes that the opponent will try to win the game for itself and always play perfectly without making any mistakes.
The AI is called the maximiser because it will try to maximize its score and the opponent is called the Minimizer because he will try to minimize the AI´s score. The best move can be found at any point in the game because of both players predictable behaviour. The maximiser makes the choice leading to its highest available terminal score knowing the Minimizer´s predictable moves in advance.

![Visualization of MiniMax Algorithm](https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Minimax.svg/600px-Minimax.svg.png)

In theory chess can be completely solved using this algorithm, meaning that the objectively best move is known by both players at any point and any party with knowledge of those moves would never lose any game. However, this is not realistically feasible because of the computational complexity. It is estimated that the number of possible chess positions is approximately 10^40, meaning that pre-calculating an entire game would be impossible even with the fastest supercomputers.
Because for every move the Maximiser makes a whole different set of moves must be considered the algorithm can only look a few turns into the future.
To reduce the computational complexity of the algorithm I employed a method called Alpha-Beta pruning. As seen in the illustration below if a moves leads to a score higher than allowed by the Minimizer because he would prevent the state being reached or lower than the Maximiser would allow to reach all computation going deeper can be cut-off because the state won´t ever be reached. This behaviour is relative to previously evaluated positions. 
![Visualization of Alpha-Beta Pruning](https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/AB_pruning.svg/1920px-AB_pruning.svg.png)
To further make use of this behaviour, I changed the load order in which moves are evaluated to start with capture moves. This increases the likelihood of impactful moves being evaluated early meaning that more moves can be cutoff by the Alpha-Beta Pruning Algorithm.

## Position Evaluation
As explained above, the MiniMax Algorithm requires any state of the chess board to be representable as single floating point number indicating the strength of both players. 
To create this number I consider both players Material advantage i.e. the pieces still in the game and the positional advantage resulting from where Pieces and Pawns are located i.e. Pawns towards the enemies base line are more valuable and in the early-to-middlegame the King is more valuable if he Castled.

## Quirks of the Algorithm
Some unique challenges I encountered with this implementation are related to:
### Move Order Robustness
Even though not all positions may be calculated, Alpha-Beta Pruning will always return the best move, a branch can be pruned if it leads to a better or worse position than considered before respectively. 
Consequently, considering moves earlier that are likely to be strong reduces the computational complexity while keeping results the same. To make use of this behaviour I let the algorithm evaluate capture moves before non-capture moves as they are statistically more likely to be impactfull.
### Horizon Effect
An interesting property in Game Theory is the Horizon Effect: A case where an undesirable event is unavoidable but can be delayed for a few turns, causing an algorithm to not realize the events inevitably as its occurrence is pushed outside the frontier that is evaluated.
In Chess this can mostly be observed where the algorithm considers a capture move at the frontier but does not realize that a recapture move is available for the opponent, causing it to consider moves that lead to blundering pieces only to later realize the recapture threat and to dismiss the plan. To avoid this behaviour I removed all capture moves at the frontier from the consideration set where the opponent has the next turn, in rare cases this can cause good moves not being considered but on average this will cause the moves played to be more robust. 
### Checkmate Prioritization
As the state where the Game has ended due to checkmate cannot accurately be described with Material and Positional advantages as usual I had to assign them manual values. 
Early on in development I defined this state as 1000000 for a win and -1000000 for a loss to ensure it is always the highest or lowest number in the frontier. 
However, this causes the algorithm to always prioritize the first checkmate it reaches in evaluation, even if checkmates are available that occur earlier in the Game. To prevent this I slightly nudge the score of checkmate by the number of turns it takes to reach it.

## Monte Carlo Tree Search
Monte Carlo Tree Search (MCTS) is a heuristic search algorithm commonly used in decision-making processes for games and optimization problems. It combines the principles of tree search and random simulation to efficiently explore the search space. The algorithm starts with a tree structure representing the possible states and actions of the game. By iteratively selecting nodes, expanding the tree, and simulating random playouts from these nodes, MCTS gradually builds up knowledge about the game and identifies promising actions. The exploration-exploitation tradeoff is balanced by using upper confidence bounds, such as the Upper Confidence Bound for Trees (UCT), to guide the selection of nodes during the search. The root node of the tree is the game state as it is and children of any node are the game states resulting from any legal move at this state.
The phases of MCTS are: <br>
1. Selection: Starting from the root node the highest scored child is selected until a child is reached which does not have any further children.
2. Expansion: If the node is not terminal, a child node is created for all legal moves and a random one is returned
3. Rollout: For the node that was returned an entire game is simulated, meaning that sequentially both players take turns making random moves until either player wins or the game is drawn
4. Backpropagation: The results of this simulation are given to all parent nodes, influencing the score for future iterations.
<br>
These steps are then repeated until a threshold number of games simulated or time elapsed is reached. This allows Monte Carlo Tree Search to be interrupted at any point while still yielding a useful prediction for the next best move which cannot be done for the MiniMax algorithm.

## User Interface
The user Interface opens with a chess board on the left side on which a figure can be moved by clicking on it and then on the field it should move to, the user can start the game by making a move for white, upon which the AI will respond for black.
On the left sides are controls for the AI, there the type of AI can be chosen for each color, moves can be taken back or recommended. \
To play black an AI turn can be made using the top button upon which the user may move the black pieces. There are also some information about the ongoing game, past turns and the algorithms evaluation of the board.
