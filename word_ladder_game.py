
"""
Modelling the Word Ladder Game in a Neo4j Graph Database
Author: Mei Yong
https://github.com/mei-yong/neo4j_python_word_ladder
"""

# Initialise the graph db
from py2neo import Graph 
uri = "bolt://localhost:7687"
user = "neo4j"
password = "password"
graph = Graph(uri=uri, user=user, password=password)


# Function that takes the list of words and finds the ones that are related to each other by 1 character
def identify_relationships(word_list):
    
    
    """ # broken code to fix
    word_list = word3
    
    # Convert the list of word strings into a list of individual character lists
    split_words = []
    for word in word_list:
        split_words.append(list(word))
        
    duplicate_split_words = [[word] * len(word) for word in split_words]
    duplicate_split_words = [word for nested_list in duplicate_split_words for word in nested_list]
    
    #duplicate_split_words = [['a', 'a', 'a'],['a', 'a', 'a'],['a', 'a', 'a'],['a','b','a']]

    x = 0
    
    for word in duplicate_split_words:
        word[x] = '_'
        if x == (len(word)-1):
            x = 0
        else:
            x += 1
        """
        
            
        
    
    # Create the list of buckets for identifying relationships
    bucket_list=[]
    for word in word_list:
        if '_'+word[-2:] not in bucket_list:
            bucket_list.append('_'+word[-2:])
        if word[0]+'_'+word[2] not in bucket_list:
            bucket_list.append(word[0]+'_'+word[2])
        if word[:2]+'_' not in bucket_list:
            bucket_list.append(word[:2]+'_')
    
    # Add words to the buckets
    import re
    bucket_dict={}
    for bucket in bucket_list:
        regex = bucket.replace('_','[A-Za-z]')
        bucket_dict[bucket] = [word for word in word3 if re.search(regex,word)]
    
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
    

# Function that creates/merges neo4j relationships based on a dictionary of relationships
def create_relationships(rel_dict, node_label):
    for k,v in rel_dict.items():
        if v != []:
            for word_pair in v:
                query = "MATCH (a:" + node_label + "),(b:" + node_label + ") WHERE a.word='" + word_pair[0] + "' and b.word='" + word_pair[1] + "' MERGE (a)-[:STEP]->(b)   "
                tx = graph.begin() # Initialise transaction
                tx.run(query) # Run the Cypher query
                tx.commit() # Commit the Cypher query
    


# Import the text file list of dictionary words as a list
# https://stackoverflow.com/questions/14676265/how-to-read-a-text-file-into-a-list-or-an-array-with-python
with open("words.txt", 'r') as f:
    all_words = f.read().splitlines()


# Get only the 3-letter words
word3 = [word for word in all_words if len(word)==3]

# Get relationships for 3-letter words
rel_dict = identify_relationships(word3)

# Create nodes in batches of 500 or else it kills the local toaster aka laptop - because each transaction creates 500 nodes in one go
import math
start = 0 
end = 500
for batch in range(math.ceil(len(word3)/500)):
    create_nodes(word3[start:end], node_label='Word3')
    start += 500
    end += 500

# Create relationships - not in batches because each transaction only creates 1 relationship
create_relationships(rel_dict, node_label='Word3')



# Do the same but for 4-letter words
word4 = [word for word in all_words if len(word)==4]
rel_dict4 = identify_relationships(word4)

start = 0 
end = 500
for batch in range(math.ceil(len(word4)/500)):
    create_nodes(word4[start:end], node_label='Word4')
    start += 500
    end += 500
    
create_relationships(rel_dict4, node_label='Word4')
