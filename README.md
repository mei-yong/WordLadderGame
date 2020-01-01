# Model the Word Ladder Game in a graph database 

### The Game
Word ladder (also known as Doublets, word-links, change-the-word puzzles, paragrams, laddergrams, or Word golf) is a word game invented by Lewis Carroll. A word ladder puzzle begins with two words, and to solve the puzzle one must find a chain of other words to link the two, in which two adjacent words (that is, words in successive steps) differ by one letter.

### Credit Sources
Words text file: https://github.com/dwyl/english-words <br>
Logic: https://supercompiler.wordpress.com/2014/05/28/implementing-word-ladder-game-using-neo4j/

### NOTE: I built this only for words between 3 to 6 characters long since most people can't think up longer words on the spot when playing the game
### NOTE: It takes at least 15 minutes to complete execution. It might error if your machine does not have enough processing power / memory


### Steps
1) Start up a local Neo4j database - I used default logins for my testing
2) Run the Python file to create all the nodes and relationships
3) In the Neo4j browser, enter the below Cypher query to find and visualise the shortest chain
	* replace start_word and end_word with your words of choice
	* replace Wordx with your word length of choice - i.e. if 5 letters long, use Word5
```cypher
MATCH (a:Wordx {word:'start_word'}),(b:Wordx {word:'end_word'}), path = shortestPath((a)-[*..50]-(b)) RETURN path
```



