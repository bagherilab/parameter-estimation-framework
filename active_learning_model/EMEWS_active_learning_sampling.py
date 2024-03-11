import numpy as np
from .strategy import Strategy
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
import random


class ActiveLearning(Strategy):

    def __init__(self, dataset, obj_function, max_iter, cross_validation_metric):
        super(ActiveLearning, self).__init__(dataset)
        self.obj_f = obj_function
        self.eval_params = []
        self.regr = RandomForestRegressor(max_depth=2, random_state=0)
        self.max_iter = max_iter
        self.coo_metric = cross_validation_metric

    def query(self, n):
        #initialize model 
        cluster_learner = KMeans(n_clusters=n)
        # get dataset
        np.random.shuffle(self.dataset)
        params_init = self.dataset.pop(0)
        #evaluate
        train_x, train_y = self.obj_f(params_init)
        #add params to evaluated list
        self.eval_params.append(params_init)
        # train model
        self.regr.fit(train_x, train_y)
        
        num_iter = 0

        while self.coo_metric and num_iter < self.max_iter:
            # predict thresholds
            p_thresh = self.regr.predict(self.dataset)
            cluster_learner.fit(p_thresh)
            cluster_idxs = cluster_learner.predict(p_thresh)
            # Get cluster centroids
            centers = cluster_learner.cluster_centers_[cluster_idxs]
            # get labels
            labels = cluster_learner.labels_

            #clustered params
            p_clus = []

            # Iterate over each cluster
            for i in range(cluster_learner.n_clusters):
                cluster_points = cluster_idxs[labels == i]  # Points in the current cluster
                closest_point_index = np.argmin(np.linalg.norm(cluster_points - 0.5, axis=1))  # Index of closest point
                p_clus.append(cluster_points[closest_point_index])
            # random sampling
            random_uneval = [x for x in self.dataset if x not in p_clus]
            random_sample = random.sample(random_uneval, n)

            # union two lists
            new_params = random_sample + p_clus

            #evaluate
            train_x, train_y = self.obj_f(new_params)
            self.eval_params = self.eval_params + new_params
            self.dataset = [i for i in self.dataset if i not in self.eval_params]

            # train model
            self.regr.fit(train_x, train_y)

            num_iter = num_iter + 1
        
        return self.regr.predict(self.dataset)

