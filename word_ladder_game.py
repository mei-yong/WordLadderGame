
"""
Modelling the Word Ladder Game in a Neo4j Graph Database
Author: Mei Yong
https://github.com/mei-yong/neo4j_python_word_ladder
"""

# Import libraries
from py2neo import Graph, #Node, Relationship

# Initialise the graph db
uri = "bolt://localhost:7687"
user = "neo4j"
password = "password"
graph = Graph(uri=uri, user=user, password=password)


# https://stackoverflow.com/questions/14676265/how-to-read-a-text-file-into-a-list-or-an-array-with-python
with open("words.txt", 'r') as f:
    all_words = f.read().splitlines()

word3 = [word for word in all_words if len(word)==3]

# take only a sample because I don't want to kill my local toaster (aka laptop)
from random import sample
word3 = sample(word3, 500)

#word3 = ['ace','ice','bce','ate','abe','act','ack'] #test


# Create the list of buckets for identifying relationships
bucket_list=[]
for word in word3:
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
    
    
# Go through the list of 3-letter words and create/merge neo4j nodes
query = ""
for word in word3:
    query += "MERGE(:Word3 {word:'" + word + "'})   "
tx = graph.begin() # Initialise transaction
tx.run(query) # Run the Cypher query
tx.commit() # Commit the Cypher query


# Go through the dictionary of buckets and the relationships under said buckets and create/merge neo4j relationships
for k,v in rel_dict.items():
    if v != []:
        for word_pair in v:
            query = "MATCH (a:Word3),(b:Word3) WHERE a.word='" + word_pair[0] + "' and b.word='" + word_pair[1] + "' MERGE (a)-[:STEP]->(b)   "
            tx = graph.begin() # Initialise transaction
            tx.run(query) # Run the Cypher query
            tx.commit() # Commit the Cypher query
    








