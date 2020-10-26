
import time
start_time = time.time()

import gzip
import json
import numpy as np

from pandas import DataFrame
from sklearn.cluster import KMeans
import os
import shutil



def ClusterSimilarity(dict1, dict2):

	list1 = dict1.keys()
	list2 = dict2.keys()

	sim = 0

	for r in list1:
		for c in list2:
			set1 = set(dict1[r])
			set2 = set(dict2[c])

			sim = round((len(set1.intersection(set2))/len(set1.union(set2))), 3)

			print(r," :: ",c," = ", sim)
		print("\n")




#This function counts the top_h hashtags assigned to every cluster centroid
def topHashtagsPerCluster(top_h, Cluster_details, Sorted_Dictionary, T_Count):

	keys__1 = list(T_Count.keys())
	for cent in Cluster_details:
		hash_list = Cluster_details[cent]
		print("\nCLUSTER: ",cent, ": ", keys__1[cent])
		TEMP_DICT = {}

		for h in hash_list:
			TEMP_DICT[h] = Sorted_Dictionary[h]

		temp_sort_demo = sorted(TEMP_DICT.items(), key = lambda x: x[1], reverse=True)

		flag_1 = 0
		for i in temp_sort_demo:
			if not flag_1==top_h:
				print(i[0], " ::: ", i[1])
				flag_1 = flag_1+1


def nameClusterRoundOff(list_cent_r):
	x = list_cent_r
	y = [round(i, 3) for i in x]
	clus_name = str(y)
	return clus_name

def printClusterAssignmentDetails(clus_detail):
	for i in clus_detail:
		print(i,": ", clus_detail[i])



def clusterGrouping (hashtags, labels, centroids, n_clus):
	#has
	clusterDetails = {}

	for i in range(0, n_clus):
		clusterDetails[i]=[]
	

	for p in range(len(labels)):

		cluster_number = labels[p]
		hashtagName = hashtags[p]
	
		clusterDetails[cluster_number].append(hashtagName)	

	return clusterDetails



def clustering (dataset, n_clus):
	#dataset: dictionary of stats
	#n_clus: No of cluster

	df = DataFrame(dataset, columns=dataset.keys())
	df = df.T

	kmeans = KMeans(n_clusters=n_clus).fit(df)
	
	#cluster centers
	centroids = kmeans.cluster_centers_
	#assined clusters
	labels = kmeans.labels_
	#names of hashtags
	hashtag_names = df.index.values


	#function call
	clusterDetails = clusterGrouping(hashtag_names, labels, centroids, n_clus)



	return df, centroids, clusterDetails, labels, hashtag_names





# normal_gender = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics/normal_gend.gz' 
# normal_race = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics/normal_race.gz'
# normal_age = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics/normal_age.gz'

# balanced_gender = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics/balanced_gend.gz' 
# balanced_race = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics/balanced_race.gz'
# balanced_age = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics/balanced_age.gz'



normal_gender = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics_comp/normal_gend.gz' 
normal_race = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics_comp/normal_race.gz'
normal_age = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics_comp/normal_age.gz'

balanced_gender = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics_comp/balanced_gend.gz' 
balanced_race = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics_comp/balanced_race.gz'
balanced_age = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics_comp/balanced_age.gz'




####NORMALS

with gzip.open(normal_gender, 'rt') as g1:
	demo_gender_temp = g1.read()
g1.close()
gender_normal = json.loads(demo_gender_temp)

with gzip.open(normal_race, 'rt') as r1:
	demo_race_temp = r1.read()
r1.close()
race_normal = json.loads(demo_race_temp)

with gzip.open(normal_age, 'rt') as a1:
	demo_age_temp = a1.read()
a1.close()
age_normal = json.loads(demo_age_temp)


#######BALANCED

with gzip.open(balanced_gender, 'rt') as g2:
	demo_gender_temp1 = g2.read()
g2.close()
gender_balanced = json.loads(demo_gender_temp1)

with gzip.open(balanced_race, 'rt') as r2:
	demo_race_temp1 = r2.read()
r2.close()
race_balanced = json.loads(demo_race_temp1)

with gzip.open(balanced_age, 'rt') as a2:
	demo_age_temp1 = a2.read()
a2.close()
age_balanced = json.loads(demo_age_temp1)




dataset_g1 = gender_normal
dataset_g = gender_balanced
n_clus_g = 4

dataset_r1 = race_normal
dataset_r = race_balanced
n_clus_r = 5

dataset_a1 = age_normal
dataset_a = age_balanced
n_clus_a = 5


df_g1, centroids_g1, clusterDetails_g1, labels_g1, hashtag_names_g1 = clustering (dataset_g1, n_clus_g)
df_r1, centroids_r1, clusterDetails_r1, labels_r1, hashtag_names_r1 = clustering (dataset_r1, n_clus_r)
df_a1, centroids_a1, clusterDetails_a1, labels_a1, hashtag_names_a1 = clustering (dataset_a1, n_clus_a)

df_g, centroids_g, clusterDetails_g, labels_g, hashtag_names_g = clustering (dataset_g, n_clus_g)
df_r, centroids_r, clusterDetails_r, labels_r, hashtag_names_r = clustering (dataset_r, n_clus_r)
df_a, centroids_a, clusterDetails_a, labels_a, hashtag_names_a = clustering (dataset_a, n_clus_a)


######Trend_counts######
T_Count_Gender1 = {}
T_Count_Race1 = {}
T_Count_Age1 = {}
######Trend_counts######
T_Count_Gender = {}
T_Count_Race = {}
T_Count_Age = {}

#Clusters:
Gender_Clusters1 = {}
Race_Clusters1 = {}
Age_Clusters1 = {}

#Clusters:
Gender_Clusters = {}
Race_Clusters = {}
Age_Clusters = {}


list_cent_g1 = centroids_g1.tolist()
list_cent_r1 = centroids_r1.tolist()
list_cent_a1 = centroids_a1.tolist()

list_cent_g = centroids_g.tolist()
list_cent_r = centroids_r.tolist()
list_cent_a = centroids_a.tolist()




for c in clusterDetails_g1:
	temp_clus_name = nameClusterRoundOff(list_cent_g1[c])
	T_Count_Gender1[temp_clus_name] = len(clusterDetails_g1[c])
	Gender_Clusters1[temp_clus_name] = clusterDetails_g1[c]

for c in clusterDetails_r1:
	temp_clus_name = nameClusterRoundOff(list_cent_r1[c])
	T_Count_Race1[temp_clus_name] = len(clusterDetails_r1[c])
	Race_Clusters1[temp_clus_name] = clusterDetails_r1[c]

for c in clusterDetails_a1:
	temp_clus_name = nameClusterRoundOff(list_cent_a1[c])
	T_Count_Age1[temp_clus_name] = len(clusterDetails_a1[c])
	Age_Clusters1[temp_clus_name] = clusterDetails_a1[c]

####Balanced
for c in clusterDetails_g:
	temp_clus_name = nameClusterRoundOff(list_cent_g[c])
	T_Count_Gender[temp_clus_name] = len(clusterDetails_g[c])
	Gender_Clusters[temp_clus_name] = clusterDetails_g[c]

for c in clusterDetails_r:
	temp_clus_name = nameClusterRoundOff(list_cent_r[c])
	T_Count_Race[temp_clus_name] = len(clusterDetails_r[c])
	Race_Clusters[temp_clus_name] = clusterDetails_r[c]

for c in clusterDetails_a:
	temp_clus_name = nameClusterRoundOff(list_cent_a[c])
	T_Count_Age[temp_clus_name] = len(clusterDetails_a[c])
	Age_Clusters[temp_clus_name] = clusterDetails_a[c]



print("GENDER_CLUSTERS_HASHTAGS_COUNTS")
printClusterAssignmentDetails(T_Count_Gender1)

print("\nRACE_CLUSTERS_HASHTAGS_COUNTS")
printClusterAssignmentDetails(T_Count_Race1)

print("\nAGE_CLUSTERS_HASHTAGS_COUNTS")
printClusterAssignmentDetails(T_Count_Age1)

######

print("\n\nBALANCED")
print("GENDER_CLUSTERS_HASHTAGS_COUNTS")
printClusterAssignmentDetails(T_Count_Gender)

print("\nRACE_CLUSTERS_HASHTAGS_COUNTS")
printClusterAssignmentDetails(T_Count_Race)

print("\nAGE_CLUSTERS_HASHTAGS_COUNTS")
printClusterAssignmentDetails(T_Count_Age)



print("\n\nInter Cluster and Across Custer Similarity Score\n")

print("Gender (Normal).   vs.    Gender (Balanced):\n")
ClusterSimilarity(Gender_Clusters1, Gender_Clusters)

print("\nRace (Normal).   vs.    Race (Balanced):\n")
ClusterSimilarity(Race_Clusters1, Race_Clusters)

print("\nAge (Normal).   vs.    Age (Balanced):\n")
ClusterSimilarity(Age_Clusters1, Age_Clusters)




#Writing cluster details dictionaries into json files

#cluster_details_path = './Cluster_Details/'

cluster_details_path = './Cluster_Details_comp/'

try:
	os.mkdir(cluster_details_path)
except:
	shutil.rmtree(cluster_details_path, ignore_errors=True)
	os.mkdir(cluster_details_path)

#######NORMAL

with gzip.open(cluster_details_path+'normal_gend_details.gz', 'wb') as g1:
	g1.write(json.dumps(Gender_Clusters1).encode('utf-8'))
g1.close()

with gzip.open(cluster_details_path+'normal_race_details.gz', 'wb') as r1:
	r1.write(json.dumps(Race_Clusters1).encode('utf-8'))
r1.close()

with gzip.open(cluster_details_path+'normal_age_details.gz', 'wb') as a1:
	a1.write(json.dumps(Age_Clusters1).encode('utf-8'))
a1.close()

#######NORMAL

with gzip.open(cluster_details_path+'balanced_gend_details.gz', 'wb') as g2:
	g2.write(json.dumps(Gender_Clusters).encode('utf-8'))
g2.close()

with gzip.open(cluster_details_path+'balanced_race_details.gz', 'wb') as r2:
	r2.write(json.dumps(Race_Clusters).encode('utf-8'))
r2.close()

with gzip.open(cluster_details_path+'balanced_age_details.gz', 'wb') as a2:
	a2.write(json.dumps(Age_Clusters).encode('utf-8'))
a2.close()






#print(Gender_Clusters1)

# with gzip.open('./SortedDict/Sorted_Dictionary.gz', 'rt') as T4:
# 	Sorted_Dictionary_temp = T4.read()
# T4.close()

# Sorted_dictionary = json.loads(Sorted_Dictionary_temp)

# #########################################################

# #Gender
# top_h = 13
# Cluster_details = clusterDetails_g
# T_Count = T_Count_Gender
# print("\n\n#########################################")
# print("GENDER [MALE, FEMALE]")
# topHashtagsPerCluster(top_h, Cluster_details, Sorted_dictionary, T_Count)

# #Race
# top_h=13
# Cluster_details = clusterDetails_r
# T_Count = T_Count_Race
# print("\n\n#########################################")
# print("RACE [WHITE, BLACK, ASIAN]")
# topHashtagsPerCluster(top_h, Cluster_details, Sorted_dictionary, T_Count)

# #Age
# top_h = 13
# Cluster_details = clusterDetails_a
# T_Count = T_Count_Age
# print("\n\n#########################################")
# print("AGE ['-20', '65+', '20-40', '40-65']")
# topHashtagsPerCluster(top_h, Cluster_details, Sorted_dictionary, T_Count)


# try:
# 	os.mkdir('./Clusters_Demographics')
# except:
# 	shutil.rmtree('./Clusters_Demographics', ignore_errors=True)
# 	os.mkdir('./Clusters_Demographics')


# with gzip.open('./Clusters_Demographics/Gender_Clusters.gz', 'wb') as f1:
# 	f1.write(json.dumps(Gender_Clusters).encode('utf-8'))
# f1.close()
# print("<./Clusters_Demographics/Gender_Clusters.gz>:::::Written")
	
# with gzip.open('./Clusters_Demographics/Race_Clusters.gz', 'wb') as f2:
# 	f2.write(json.dumps(Race_Clusters).encode('utf-8'))
# f2.close()
# print("<./Clusters_Demographics/Race_Clusters.gz>:::::Written")

# with gzip.open('./Clusters_Demographics/Age_Clusters.gz', 'wb') as f3:
# 	f3.write(json.dumps(Age_Clusters).encode('utf-8'))
# f3.close()
# print("<./Clusters_Demographics/Age_Clusters.gz>:::::Written")


print("Elapsed Time")
print("--- %s seconds ---" % (time.time() - start_time))