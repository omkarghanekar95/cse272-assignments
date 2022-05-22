import numpy as np, pandas as pd


subset_file = "dataset/reviews_subset.json"
full_dataset = "Cell_Phones_and_Accessories_5.json"

subset_csv_file = "dataset/cell_phone_reviews.csv"
full_csv_file = "dataset/Cell_Phones_and_Accessories.csv"

def read_data_file():
	cell_phones_data = pd.read_json(full_dataset,lines=True)

	#print(cell_phones_data.head())

	print(cell_phones_data.dtypes)
	print('Minimum rating is: %d' %(cell_phones_data.overall.min()))
	print('Maximum rating is: %d' %(cell_phones_data.overall.max()))
	print('Number of missing values across columns: \n',cell_phones_data.isnull().sum())# dataframe.to_csv('reviews.csv', sep=',', index=False)

	print("Total data ")
	print("-"*50)
	print("\nTotal no of ratings :",cell_phones_data.shape[0])
	print("Total No of Users   :", len(np.unique(cell_phones_data.reviewerID)))
	print("Total No of products  :", len(np.unique(cell_phones_data.asin)))


	cell_phone =  cell_phones_data[["overall", "reviewerID", "asin"]]
	cell_phone.asin = cell_phone.asin.apply(lambda x: x[:-1] if 'X' in x else x)

	print(cell_phone)


	#Analysis of rating given by the user 

	no_of_rated_products_per_user = cell_phone.groupby(by='reviewerID')['overall'].count().sort_values(ascending=False)

	# print(no_of_rated_products_per_user.head())
	print(no_of_rated_products_per_user.shape)
	print(no_of_rated_products_per_user.describe())

	print('\n No of rated product more than 50 per user : {}\n'.format(sum(no_of_rated_products_per_user >= 5)) )



## read_ratings file
def read_ratings_file():
	cell_csv_data=pd.read_csv(full_dataset)
	cell_csv_data.head()

	print(cell_csv_data.dtypes)

	cell_csv_data.drop(['timestamp'], axis=1,inplace=True)

	return cell_csv_data
