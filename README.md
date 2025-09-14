# amazon

PROBLEM STATEMENT:
With millions of songs available on platforms like Amazon, manually categorizing tracks into genres is impractical. The goal of this project is to automatically group similar songs based on their audio characteristics using clustering techniques. By analyzing patterns in features such as tempo, energy, danceability, and more, learners will develop a model that organizes songs into meaningful clusters, potentially representing different musical genres or moods—without any prior labels.


The data set has been checked for the missing values and duplicates and the  commpleted EDA has been performed and the  songs are clustered using K means. The number of clusters has been determined by elbow method and silhoutte score.The alternate clustering method DB SCAN is also used for clustering but the clusters were overlapping and so I used K means for the clustering and then recommendation of the palylist is done by using cosine similarity and the streamlit app is built for visualising the recommendation of playlist.
