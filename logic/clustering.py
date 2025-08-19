import json
import os
import pickle
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.cluster import KMeans, MiniBatchKMeans, BisectingKMeans, AgglomerativeClustering


def cluster():
    lsa = make_pipeline(TruncatedSVD(n_components=100, random_state=42, algorithm='arpack'), Normalizer(copy=False))

    try:
        with open("Data/tfidf_matrix.pkl", "rb") as file:
            tfidf_matrix = pickle.load(file)
    except IOError as ex:
        print(f"An error occurred: {ex}")
        return

    X_lsa = lsa.fit_transform(tfidf_matrix)                 #Perform of LSA for dimensionality reduction and identification of thematic areas
    print("Finished LSA transformation")

    ks = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 10000]     # Define the different k values for clustering

    os.makedirs("Data/clustering", exist_ok=True)

    with open('Data/term_idf_dict.json', 'r', encoding='utf-8') as term_file:   # Load terms from the term_idf_dict.json file
        json_obj = json.load(term_file)
        terms = list(json_obj.keys())                                           # Convert dict_keys to a list for indexing

    with open("Data/clustering/kmeans.txt", "w", encoding="utf-8") as file:     # Open file to write clustering results
        for k in ks:
            kmeans = KMeans(n_clusters=k, max_iter=100, random_state=42).fit(X_lsa)    # Perform KMeans clustering

            cluster_ids, cluster_sizes = np.unique(kmeans.labels_, return_counts=True)             # Get cluster sizes and SSE (sum of squared errors)
            sse = kmeans.inertia_

            #print(f"k is: {k}", f"cluster_sizes: {cluster_sizes}", f"SSE: {sse}")

            file.write(f"k is: {k}\n")                                                              # Write results to the file
            file.write(f"Number of elements assigned to each cluster: {cluster_sizes}\n")
            file.write(f"SSE is: {sse}\n\n")

            original_space_centroids = lsa[0].inverse_transform(kmeans.cluster_centers_)             # Inverse transform the centroids to the original space
            order_centroids = original_space_centroids.argsort()[:, ::-1]

            for i in range(k):                                                                   # Write the top 10 terms for each cluster
                file.write(f"Cluster {i}: ")
                #print(f"Cluster {i}: ", end="")
                for ind in order_centroids[i, :10]:
                    term = terms[ind] if ind < len(terms) else "N/A"
                    #print(f"{term} ", end="")
                    file.write(f"{term} ")
                #print()
                file.write("\n")

    #---------------------------------------------------------------------------------------

    # with open("Data/clustering/mini_batch_kmeans.txt", "w", encoding="utf-8") as file:
    #
    #     for k in ks:
    #
    #         mini_batch_kmeans = MiniBatchKMeans(n_clusters=k, max_iter=100, random_state=42).fit(X_lsa)
    #
    #         cluster_ids, cluster_sizes = np.unique(mini_batch_kmeans.labels_, return_counts=True)
    #
    #         sse = mini_batch_kmeans.inertia_
    #
    #         print(f"k is: {k}", f"cluster_sizes: {cluster_sizes}", f"SSE : {sse}")
    #
    #         file.write(f"k is: {k}" + "\n")
    #         file.write(f"Number of elements assigned to each cluster: {cluster_sizes}" + "\n")
    #         file.write("SSE score is: " + str(sse))
    #         file.write("\n")
    #
    #     #---------------------------------------------------------------------------------------
    # with open("Data/clustering/bisecting_kmeans.txt", "w", encoding="utf-8") as file:
    #
    #     for k in ks:
    #
    #         bisecting_kmeans = BisectingKMeans(n_clusters=k, max_iter=100, random_state=42).fit(X_lsa)
    #
    #         cluster_ids, cluster_sizes = np.unique(bisecting_kmeans.labels_, return_counts=True)
    #
    #         sse = bisecting_kmeans.inertia_
    #
    #         print(f"k is: {k}", f"cluster_sizes: {cluster_sizes}", f"SSE : {sse}")
    #
    #         file.write(f"k is: {k}" + "\n")
    #         file.write(f"Number of elements assigned to each cluster: {cluster_sizes}" + "\n")
    #         file.write("SSE score is: " + str(sse))
    #         file.write("\n")

    #---------------------------------------------------------------------------------------

    # hierachical = AgglomerativeClustering(n_clusters=k, metric='euclidean', linkage='complete').fit(X_lsa)
    #
    # cluster_ids, cluster_sizes = np.unique(hierachical.labels_, return_counts=True)
    #
    # with open("Data/clustering/hierachical.txt", "w", encoding="utf-8") as file:
    #     file.write(f"k is: {k}" + "\n")
    #     file.write(f"Number of elements assigned to each cluster: {cluster_sizes}" + "\n")
    #     file.write("\n")
