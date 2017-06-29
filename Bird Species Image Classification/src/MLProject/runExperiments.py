import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import metrics

names = ['plane','auto','bird','cat','deer','dog','frog','horse','ship','truck']
names = np.asarray(names)

distances = ['euclidean', 'cosine', 'manhattan', 'braycurtis', 'canberra', 'chebyshev', 'correlation', 'mahalanobis', 'minkowski', 'seuclidean', 'sqeuclidean']

map = dict()
file = 'C:/Users/sagar/OneDrive/Clustering_Kaveri/compressed_data_batch_' + str(1) + '.npz'
#file = 'data_batch_' + str(i) + '.npz'
file = np.load(file)
d = file
y_train = file['y']
rep_train = file['representations']

#===============================================================================
# km = KMeans(n_clusters = len(names), init= 'k-means++').fit(rep_train)
# 
# y_pred = km.labels_.astype(np.int)
# rand_score = metrics.adjusted_rand_score(y_train, y_pred)
# mutual_info = metrics.adjusted_mutual_info_score(y_train, y_pred)
# v_measure = metrics.v_measure_score(y_train, y_pred)
# 
# print 'Kmeans (rand_dist):: ' + str(rand_score)
# print 'Kmeans (mutual_info):: ' + str(mutual_info)
# print 'Kmeans (v_measure):: ' + str(v_measure)
# print ''
# 
# # plt.bar(range(len(rand_score)), rand_score.values(), align='center')
# # plt.xticks(range(len(rand_score)), rand_score.keys())
# # plt.show()
# 
# map['kmeans'] = {'pred' : y_pred, 'rand_score' : rand_score, 'plot' : plt}
#===============================================================================

#Nearest Cnetroid Clustering
# from sklearn.neighbors.nearest_centroid import NearestCentroid
# for d in distances:
# 	knn = NearestCentroid(metric=d).fit(rep_train, y_train)

# 	y_pred = knn.predict(rep_train).astype(np.int)
# 	rand_score = metrics.adjusted_rand_score(y_train, y_pred)
# 	mutual_info = metrics.adjusted_mutual_info_score(y_train, y_pred)
# 	v_measure = metrics.v_measure_score(y_train, y_pred)
# #	print knn.centroids_
# 	print 'NCC (rand_dist)- ' + d + ' :: ' + str(rand_score)
# 	print 'NCC (mutual_info)- ' + d + ' :: ' + str(mutual_info)
# 	print 'NCC (v_measure)- ' + d + ' :: ' + str(v_measure)
# 	print ''


# print ''
# print ''
# print 'K- Nearest Neighbors'
# #KNN

# from sklearn.neighbors import NearestNeighbors
# for d in distances:
# 	knn = NearestNeighbors(metric=d, n_neighbors=10000, algorithm='kd_tree').fit(rep_train)

# 	y_pred = knn.kneighbors(rep_train)[1][:,1].astype(np.int)
# 	rand_score = metrics.adjusted_rand_score(y_train, y_pred)
# 	mutual_info = metrics.adjusted_mutual_info_score(y_train, y_pred)
# 	v_measure = metrics.v_measure_score(y_train, y_pred)
# #	print knn.centroids_
# 	print y_pred
# 	print 'KNN (rand_dist)- ' + d + ' :: ' + str(rand_score)
# 	print 'KNN (mutual_info)- ' + d + ' :: ' + str(mutual_info)
# 	print 'KNN (v_measure)- ' + d + ' :: ' + str(v_measure)
# 	print ''

# print ''
# print 'Agglomerative'
# #AGG

# from sklearn.cluster import AgglomerativeClustering
# agg = AgglomerativeClustering(n_clusters=len(names)).fit_predict(rep_train)

# y_pred = agg.labels_.astype(np.int)
# rand_score = metrics.adjusted_rand_score(y_train, y_pred)
# mutual_info = metrics.adjusted_mutual_info_score(y_train, y_pred)
# v_measure = metrics.v_measure_score(y_train, y_pred)
# #	print knn.centroids_
# print y_pred
# print 'AGG (rand_dist)- ' + d + ' :: ' + str(rand_score)
# print 'AGG (mutual_info)- ' + d + ' :: ' + str(mutual_info)
# print 'AGG (v_measure)- ' + d + ' :: ' + str(v_measure)
# print ''


# Gaussian Mixture Models

import itertools
from scipy import linalg
import matplotlib as mpl
import matplotlib.cm as cm

from sklearn import mixture

color_iter = itertools.cycle(['blue','g','r','navy', 'c', 'cornflowerblue', 'gold',
                              'darkorange','black','magenta'])


def plot_results(X, Y_, means, covariances, index, title):
    splot = plt.subplot(2, 1, 1 + index)
    for i, (mean, covar, color) in enumerate(zip(
            means, covariances, color_iter)):
        v, w = linalg.eigh(covar)
        v = 2. * np.sqrt(2.) * np.sqrt(v)
        u = w[0] / linalg.norm(w[0])
        # as the DP will not use every component it has access to
        # unless it needs it, we shouldn't plot the redundant
        # components.
        if not np.any(Y_ == i):
            continue
        plt.scatter(X[Y_ == i, 0], X[Y_ == i, 1], .8, color=color)

        # Plot an ellipse to show the Gaussian component
        angle = np.arctan(u[1] / u[0])
        angle = 180. * angle / np.pi  # convert to degrees
        ell = mpl.patches.Ellipse(mean, v[0], v[1], 180. + angle, color=color)
        ell.set_clip_box(splot.bbox)
        ell.set_alpha(0.5)
        splot.add_artist(ell)

    plt.xlim(-9., 5.)
    plt.ylim(-3., 6.)
    plt.xticks(())
    plt.yticks(())
    plt.title(title)


# Fit a Gaussian mixture with EM using five components
gmm = mixture.GaussianMixture(n_components=10, covariance_type='full').fit(rep_train)
y_pred = gmm.predict(rep_train)
rand_score = metrics.adjusted_rand_score(y_train, y_pred)
print 'GMM',rand_score
plot_results(rep_train, gmm.predict(rep_train), gmm.means_, gmm.covariances_, 0,
             'Gaussian Mixture')

# Fit a Dirichlet process Gaussian mixture using five components
dpgmm = mixture.BayesianGaussianMixture(n_components=10,
                                        covariance_type='full').fit(rep_train)
plot_results(rep_train, dpgmm.predict(rep_train), dpgmm.means_, dpgmm.covariances_, 1,
             'Bayesian Gaussian Mixture with a Dirichlet process prior')
y_pred = dpgmm.predict(rep_train)
y_pred = np.nan_to_num(y_pred)
rand_score = metrics.adjusted_rand_score(y_train, y_pred)
print 'Dirichlet GMM',rand_score
plt.show()

#t-SNE
#===============================================================================
# from sklearn.manifold import TSNE
# model = TSNE(n_components=len(names), random_state=0)
# print model.fit_transform(rep_train) 
# print model.fit_predict(rep_train)
#===============================================================================