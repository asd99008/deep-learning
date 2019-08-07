# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 18:00:46 2019

@author: Lenovo
"""

class KMcluster():
    def __init__(self, X, y, n_clusters=3, initialize="random", max_iters=20):
        self.X = X
        self.y = y
        self.n_clusters = n_clusters
        self.initialize = initialize
        self.max_iters = max_iters

    # 随机初始化中心点
    def init_random(self):

        n_samples, n_features = self.X.shape
        centroids = self.X[np.random.choice(n_samples, 4)]
        return centroids

    # KMeans++ 初始化中心点
    def init_kmeans_plusplus(self):
        n_samples, n_features = self.X.shape

        # step 1: 随机选取第一个中心点
        centroids = self.X[np.random.choice(n_samples, 1)]

        # 计算其余的中心点
        for k in range(0, self.n_clusters-1):
            distances = np.zeros((n_samples, k+1))

            for i in range(len(centroids)):
                distances[:, i] = np.sqrt(np.sum(np.square(self.X - centroids[i]), axis=1))

            dist = np.min(distances, axis=1)

            total = np.sum(dist) * np.random.rand()
            for j in range(n_samples):
                total -= dist[j]
                if total > 0:
                    continue
                centroids = np.r_[centroids, self.X[j].reshape(-1, 2)]
                break

        # print(centroids)
        return centroids

    def assignment(self, centroids):
        n_samples = self.X.shape[0]
        distances = np.zeros((n_samples, self.n_clusters))
        for i in range(self.n_clusters):
            distances[:,i] = np.sum(np.square(self.X - centroids[i]), axis=1)
        return np.argmin(distances, axis=1)

    def update_center(self, flag, centroids):
        new_centroids = np.zeros_like(centroids)
        for i in range(self.n_clusters):
            new_centroids[i] = np.mean(self.X[flag==i], axis=0)
        return new_centroids

    def train(self):
        # step 1: generate center
        if self.initialize == "kmeans++":
            centroids = self.init_kmeans_plusplus()
        else:
            centroids = self.init_random()

        colmap = [i for i in range(self.n_clusters)]
        for i in range(self.max_iters):
            # step 2: assign centroid for each source data
            flag = self.assignment(centroids)

            plt.scatter(self.X[:,0], self.X[:,1], c=flag, marker=".", alpha=0.5)
            plt.scatter(centroids[:, 0], centroids[:, 1], c=colmap, marker="o", linewidths=6)
            plt.show()

            # step 3: re-caculate center
            new_centroids = self.update_center(flag, centroids)

            if (new_centroids == centroids).all():
                break
            else:
                centroids = new_centroids

            print("iters: ", i, ", center point: ", centroids)


if __name__=="__main__":

    # 生成数据集: X[2000, 2], y[2000], 4 clusters
    X, y = sklearn.datasets.make_blobs(n_samples=1000,
                                       n_features=2,
                                       centers=4,
                                       random_state=40,
                                       cluster_std=(2, 2, 2, 2))

    km = KMcluster(X, y, n_clusters=4, initialize="random", max_iters=50)
    # km = KMcluster(X, y, n_clusters=4, initialize="kmeans++", max_iters=50)
    km.train()
