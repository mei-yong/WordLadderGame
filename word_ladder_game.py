
"""
Modelling the Word Ladder Game in a Neo4j Graph Database
Author: Mei Yong
https://github.com/mei-yong/neo4j_python_word_ladder
"""

# Initialise the local graph db
from py2neo import Graph 
uri = "bolt://localhost:7687"
user = "neo4j"
password = "password"
graph = Graph(uri=uri, user=user, password=password)


# Function that takes the list of words and finds the ones that are related to each other by 1 character
def identify_relationships(word_list):
    
    # Create the list of buckets for identifying relationships
    bucket_list=[]
    for word in word_list:
        for n in range(len(word)):
            test_word = word[:n] + '_' + word[n+1:]
            if test_word not in bucket_list:
                bucket_list.append(test_word)
    
    # Add words to the buckets
    import re
    bucket_dict={}
    for bucket in bucket_list:
        regex = bucket.replace('_','[A-Za-z]')
        bucket_dict[bucket] = [word for word in word_list if re.search(regex,word)]
    
    # Find the combinations between the words in the buckets
    from itertools import combinations
    rel_dict={}
    for k,v in bucket_dict.items():
        rel_dict[k] = list(combinations(v,2))
        
    return rel_dict


# Function that creates/merges neo4j nodes based on a list of words
def create_nodes(word_list, node_label):
    query = ""
    for word in word_list:
        query += "MERGE(:" + node_label + " {word:'" + word + "'})   "
    tx = graph.begin() # Initialise transaction
    tx.run(query) # Run the Cypher query
    tx.commit() # Commit the Cypher query

# Function that creates/merges neo4j nodes in batches
def create_nodes_in_batches(word_list, node_label, batch_size):
    import math
    start, end = 0, 500
    for batch in range(math.ceil(len(word_list)/500)):
        create_nodes(word_list[start:end], node_label=node_label)
        start += 500
        end += 500

# Function that creates/merges neo4j relationships based on a dictionary of relationships
def create_relationships(rel_dict, node_label):
    for k,v in rel_dict.items():
        if v != []:
            for word_pair in v:
                query = "MATCH (a:" + node_label + "),(b:" + node_label + ") WHERE a.word='" + word_pair[0] + "' and b.word='" + word_pair[1] + "' MERGE (a)-[:STEP]->(b)   "
                graph.run(query)
                #tx = graph.begin() # Initialise transaction
                #tx.run(query) # Run the Cypher query
                #tx.commit() # Commit the Cypher query
    

# Function that takes a whole list of words and creates a neo4j gragh db based on it
def convert_words_into_graphdb(list_of_all_words):
    
    min_len = len(min(list_of_all_words, key=len))
    max_len = len(max(list_of_all_words, key=len))
    
    for word_len in range(min_len, max_len+1):
        
        # Find words of a particular length
        word_list = [word for word in list_of_all_words if len(word)==word_len]
        
        # Find the relationships between the words of a particular length
        rel_dict = identify_relationships(word_list)
        
        # Create nodes in batches of 500
        create_nodes_in_batches(word_list=word_list, node_label='Word'+str(word_len), batch_size=500)
        
        # Create edges
        create_relationships(rel_dict=rel_dict, node_label='Word'+str(word_len))
        
        
#########################################################################################
        
        
# Timing code execution
import time
import datetime
start_time = time.time()


# Import the text file list of dictionary words as a list
# https://stackoverflow.com/questions/14676265/how-to-read-a-text-file-into-a-list-or-an-array-with-python
with open("words.txt", 'r') as f:
    all_words = f.read().splitlines()

# Get only words between 3-6 characters long
all_words_max6 = [word for word in all_words if len(word) in range(3,7)]


# Create nodes and edges based on the list of words
convert_words_into_graphdb(list_of_all_words=all_words_max6)


# Timing code execution
execution_time = time.time() - start_time
print(f"Code execution time: {str(datetime.timedelta(seconds=execution_time))}")



"""
# Testing
start_time = time.time()
wordtest = [word for word in all_words if len(word) in range(3,5)]
convert_words_into_graphdb(list_of_all_words=wordtest)
execution_time = time.time() - start_time
print(f"Code execution time: {str(datetime.timedelta(seconds=execution_time))}")
"""
