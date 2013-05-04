Twitter Community Detection
===========================

Finds Communities within the Twitter domain using Spectral Clustering
and Influence. 

Steps:
 1. Harvest Tweets using streaming API (stream.py), store tweets in MongoDB
 2. Remove any tweets that do not have a retweet/mention
 3. Construct a graph from the remaining tweets
 4. Use Spectral Clustering to find the best clusters
 5. Evaluation Clustering using the Silhouette score 

Requires the following modules:
 - tweepy
 - pymongo
 - networkx
 - matplotlib
 - numpy
 - sklearn


Peter J. Rousseeuw (1987). “Silhouettes: a Graphical Aid to the
Interpretation and Validation of Cluster Analysis”. Computational and
Applied Mathematics 20: 53–65. doi:10.1016/0377-0427(87)90125-7.
