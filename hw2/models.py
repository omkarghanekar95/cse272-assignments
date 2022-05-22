from surprise import KNNWithMeans
from surprise import Dataset, accuracy, Reader
import os
from surprise.model_selection import train_test_split
from read_data import read_ratings_file

from surprise import prediction_algorithms, SVD, NMF
from collections import defaultdict

#Reading the dataset
cellphones_csv = read_ratings_file()
# reader = Reader(line_format="overall reviewerID asin", sep=' ', rating_scale=(1, 5),skip_lines=1)
reader = Reader(rating_scale=(1, 5),skip_lines=1)
#data = Dataset.load_from_df(cell_phone[['overall', 'reviewerID', 'asin']], reader)
data = Dataset.load_from_df(cellphones_csv, reader)


#Splitting the dataset
trainset, testset = train_test_split(data, test_size=0.2,random_state=10)

def item_basedCF():
	# Use user_based true/false to switch between user-based or item-based collaborative filtering
	algo = KNNWithMeans(k=40, sim_options={'name': 'pearson_baseline', 'user_based': False})
	algo.fit(trainset)

	# run the trained model against the testset
	test_pred = algo.test(testset)

	print("Item-based Model : Test Set")
	accuracy.rmse(test_pred, verbose=True)
	accuracy.mae(test_pred, verbose=True)

def user_basedCF():
	# Use user_based true/false to switch between user-based or item-based collaborative filtering
	user_basedCF = KNNWithMeans(k=40, sim_options={'name': 'pearson_baseline', 'user_based': True})
	user_basedCF.fit(trainset)

	# run the trained model against the testset
	user_basedCF_test_pred = user_basedCF.test(testset)

	print("User-based Model : Test Set")
	accuracy.rmse(user_basedCF_test_pred, verbose=True)
	accuracy.mae(user_basedCF_test_pred, verbose=True)

def SVD_matrix():
	algo_SVD = SVD(n_factors = 11)
	algo_SVD.fit(trainset)


	# Predict ratings for all pairs (i,j) that are NOT in the training set.
	SVD_testset = trainset.build_anti_testset()

	predictions = algo_SVD.test(SVD_testset)

	# subset of the list  predictions
	print(predictions[:5])
	return predictions

def get_top_n(predictions, userId, n = 10):# movies_df, ratings_df,
    '''Return the top N (default) movieId for a user,.i.e. userID and history for comparisom
    Args:
    Returns: 
  
    '''
    #Peart I.: Surprise docomuntation
    
    #1. First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    #2. Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key = lambda x: x[1], reverse = True)
        top_n[uid] = user_ratings[: n ]

    return top_n


item_basedCF()
user_basedCF()
predictions = SVD_matrix()
print(get_top_n(predictions, 9638762632))