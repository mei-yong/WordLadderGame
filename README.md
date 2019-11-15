## Modelling the Word Ladder Game in a Neo4j Graph Database
Word ladder (also known as Doublets, word-links, change-the-word puzzles, paragrams, laddergrams, or Word golf) is a word game invented by Lewis Carroll. A word ladder puzzle begins with two words, and to solve the puzzle one must find a chain of other words to link the two, in which two adjacent words (that is, words in successive steps) differ by one letter.

NOTE: At the moment, this code only works for 3-letter words

To find and visualise the shortest chain, run the below query in the Neo4j browser using the below Cypher query - replace start_word and end_word
```cypher
MATCH (a:Word3 {word:'start_word'}),(b:Word3 {word:'end_word'}), path = shortestPath((a)-[*..50]-(b)) RETURN path
```
