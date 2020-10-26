import gzip
import json
import glob
import itertools
import ntpath
import time
import os
import shutil
import operator
from math import sqrt
import time



def averageBiasScoreGend(dict, w_ratio):

	counter = 0
	biasSum = 0
	t_ratio = 0

	for t in dict.keys():
		[M, F] = dict[t]
		counter = counter + 1


		if F==0:
			t_ratio = M
		else:
			t_ratio = M/F

		bias = sqrt( ( w_ratio - t_ratio )**2 )
		biasSum = biasSum + bias


	ave_Bias = biasSum / counter

	return round(ave_Bias, 3)



def averageBiasScoreRace(dict, w_ratio):

	counter = 0
	biasSum = 0
	t_ratio = 0

	for t in dict.keys():
		[W, B, A] = dict[t]
		counter = counter + 1


		if (B+A)==0:
			t_ratio = W
		else:
			t_ratio = W/(B+A)

		bias = sqrt( ( w_ratio - t_ratio )**2 )
		biasSum = biasSum + bias


	ave_Bias = biasSum / counter

	return round(ave_Bias, 3)



def averageBiasScoreAge(dict, w_ratio):

	counter = 0
	biasSum = 0
	t_ratio = 0

	for t in dict.keys():
		[A, O, Y, M] = dict[t]
		counter = counter + 1

		if (A+M)==0:
			t_ratio = (O+Y)
		else:
			t_ratio = (O+Y)/(A+M)

		bias = sqrt( ( w_ratio - t_ratio )**2 )
		biasSum = biasSum + bias


	ave_Bias = biasSum / counter

	return round(ave_Bias, 3)


def Normalize(Rl,Rh, minX, maxX, number):
	BminA = Rh-Rl
	Den = maxX-minX

	normalizedNumber =   ( (BminA/Den) * (number - minX) ) + Rl 

	return normalizedNumber


def ImbalanceGender(ClusterDetails, TrendingDetails):
	
	base_weight_male = 0.463
	base_weight_female = 0.537

	balancing_point = (base_weight_male/base_weight_female)

	imbalanceDetails = {}

	for c in ClusterDetails:
		#[M,F] = c
		hashtagList = ClusterDetails[c]

		imbalanceSum = 0

		for h in hashtagList:
			[m,f] = TrendingDetails[h]
			if f!=0:
				imbl = m/f
				########################
				if imbl<=balancing_point:
					norm_imbl = Normalize(-1, 0, 0, balancing_point, imbl)
				else:
					norm_imbl = Normalize(0, 1, balancing_point, 100, imbl)
				########################
				imbalanceSum = imbalanceSum + norm_imbl

		imbalanceDetails[c] = round((imbalanceSum/len(hashtagList)), 3)

	return imbalanceDetails



def ImbalanceRace(ClusterDetails, TrendingDetails):
	
	base_weight_white = 0.2364
	base_weight_black = 0.4694
	base_weight_asian = 0.2943

	balancing_point = base_weight_white/(base_weight_black+base_weight_asian)

	imbalanceDetails = {}

	for c in ClusterDetails:
		#[M,F] = c
		hashtagList = ClusterDetails[c]

		imbalanceSum = 0

		for h in hashtagList:
			[w,b,a] = TrendingDetails[h]
			if (b+a)!=0:
				imbl = w/(b+a)
				########################
				if imbl<=balancing_point:
					norm_imbl = Normalize(-1, 0, 0, balancing_point, imbl)
				else:
					norm_imbl = Normalize(0, 1, balancing_point, 100, imbl)
				########################
				imbalanceSum = imbalanceSum + norm_imbl

		imbalanceDetails[c] = round((imbalanceSum/len(hashtagList)), 3)

	return imbalanceDetails

def ImbalanceAge(ClusterDetails, TrendingDetails):
	
	base_weight_adol = 0.2819
	base_weight_old = 0.0546
	base_weight_young = 0.3753
	base_weight_midAged = 0.2896

	balancing_point = (base_weight_old + base_weight_young)/(base_weight_adol+base_weight_midAged)

	imbalanceDetails = {}

	for c in ClusterDetails:
		#[M,F] = c
		hashtagList = ClusterDetails[c]

		imbalanceSum = 0

		for h in hashtagList:
			[a,o,y,m] = TrendingDetails[h]
			if (a+m)!=0:
				imbl = (o+y)/(a+m)
				########################
				if imbl<=balancing_point:
					norm_imbl = Normalize(-1, 0, 0, balancing_point, imbl)
				else:
					norm_imbl = Normalize(0, 1, balancing_point, 100, imbl)
				########################
				imbalanceSum = imbalanceSum + norm_imbl

		imbalanceDetails[c] = round((imbalanceSum/len(hashtagList)), 3)

	return imbalanceDetails

def biasGender(genderClusters, TrendingDetails):
	base_weight_male = 0.463
	base_weight_female = 0.537

	balancing_point = (base_weight_male/base_weight_female)

	averageBiasDetails = {}

	for c in genderClusters:
		tempHashtags = genderClusters[c]

		averageBias = 0

		for h in tempHashtags:
			[m,f] = TrendingDetails[h]

			if f!=0:
				currentBalance = m/f
				tempBias = sqrt((balancing_point - currentBalance)**2)

				averageBias = averageBias + tempBias

		averageBiasDetails[c] = round((averageBias/len(tempHashtags)), 3)


	return averageBiasDetails



def biasRace(raceClusters, TrendingDetails):
	base_weight_white = 0.2364
	base_weight_black = 0.4694
	base_weight_asian = 0.2943

	balancing_point = base_weight_white/(base_weight_black+base_weight_asian)

	averageBiasDetails = {}

	for c in raceClusters:
		tempHashtags = raceClusters[c]

		averageBias = 0

		for h in tempHashtags:
			[w,b,a] = TrendingDetails[h]

			if (b+a)!=0:
				currentBalance = w/(b+a)
				tempBias = sqrt((balancing_point - currentBalance)**2)

				averageBias = averageBias + tempBias

		averageBiasDetails[c] = round((averageBias/len(tempHashtags)), 3)


	return averageBiasDetails


def biasAge(ageClusters, TrendingDetails):
	base_weight_adol = 0.2819
	base_weight_old = 0.0546
	base_weight_young = 0.3753
	base_weight_midAged = 0.2896

	balancing_point = (base_weight_old + base_weight_young)/(base_weight_adol+base_weight_midAged)

	averageBiasDetails = {}

	for c in ageClusters:
		tempHashtags = ageClusters[c]

		averageBias = 0

		for h in tempHashtags:
			[a,o,y,m] = TrendingDetails[h]

			if (a+m)!=0:
				currentBalance = (o+y)/(a+m)
				tempBias = sqrt((balancing_point - currentBalance)**2)

				averageBias = averageBias + tempBias

		averageBiasDetails[c] = round((averageBias/len(tempHashtags)), 3)


	return averageBiasDetails

def LoadFile(filePath):
	with gzip.open(filePath,'rt') as Temp:
		temp = Temp.read()
	Temp.close()

	statsDictionary = json.loads(temp)

	return statsDictionary


###################################################################################################
start_time = time.time()


# ###Clusters
# clus_gen_norm = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/Cluster_Details/normal_gend_details.gz'
# clus_rac_norm = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/Cluster_Details/normal_race_details.gz'
# clus_age_norm = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/Cluster_Details/normal_age_details.gz'

# clus_gen_bala = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/Cluster_Details/balanced_gend_details.gz'
# clus_rac_bala = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/Cluster_Details/balanced_race_details.gz'
# clus_age_bala = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/Cluster_Details/balanced_age_details.gz'


# #Trending Topics
# trend_gen_norm = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics/normal_gend.gz'
# trend_rac_norm = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics/normal_race.gz'
# trend_age_norm = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics/normal_age.gz'

# trend_gen_bala = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics/balanced_gend.gz'
# trend_rac_bala = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics/balanced_race.gz'
# trend_age_bala = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics/balanced_age.gz'

###Clusters
clus_gen_norm = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/Cluster_Details_comp/normal_gend_details.gz'
clus_rac_norm = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/Cluster_Details_comp/normal_race_details.gz'
clus_age_norm = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/Cluster_Details_comp/normal_age_details.gz'

clus_gen_bala = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/Cluster_Details_comp/balanced_gend_details.gz'
clus_rac_bala = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/Cluster_Details_comp/balanced_race_details.gz'
clus_age_bala = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/Cluster_Details_comp/balanced_age_details.gz'


#Trending Topics
trend_gen_norm = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics_comp/normal_gend.gz'
trend_rac_norm = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics_comp/normal_race.gz'
trend_age_norm = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics_comp/normal_age.gz'

trend_gen_bala = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics_comp/balanced_gend.gz'
trend_rac_bala = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics_comp/balanced_race.gz'
trend_age_bala = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/New_Trending_Topics_comp/balanced_age.gz'



#Load Cluster Files
normal_gender_clusters = LoadFile(clus_gen_norm)
normal_race_clusters = LoadFile(clus_rac_norm)
normal_age_clusters = LoadFile(clus_age_norm)

balanced_gender_clusters = LoadFile(clus_gen_bala)
balanced_race_clusters = LoadFile(clus_rac_bala)
balanced_age_clusters = LoadFile(clus_age_bala)

#Load Trend Files

normal_gender_trends = LoadFile(trend_gen_norm)
normal_race_trends = LoadFile(trend_rac_norm)
normal_age_trends = LoadFile(trend_age_norm)

balanced_gender_trends = LoadFile(trend_gen_bala)
balanced_race_trends = LoadFile(trend_rac_bala)
balanced_age_trends = LoadFile(trend_age_bala)


gender_imbalance_details_normal = ImbalanceGender(normal_gender_clusters, normal_gender_trends)
gender_imbalance_details_balanced = ImbalanceGender(balanced_gender_clusters, balanced_gender_trends)

print("GENDER")
print("\nIMBALANCE: NORMAL")
print(gender_imbalance_details_normal)
print("\n IMBALANCE: BALANCED")
print(gender_imbalance_details_balanced)


race_imbalance_details_normal = ImbalanceRace(normal_race_clusters, normal_race_trends)
race_imbalance_details_balanced = ImbalanceRace(balanced_race_clusters, balanced_race_trends)

print("\nRACE")
print("\nIMBALANCE: NORMAL")
print(race_imbalance_details_normal)
print("\n IMBALANCE: BALANCED")
print(race_imbalance_details_balanced)


age_imbalance_details_normal = ImbalanceAge(normal_age_clusters, normal_age_trends)
age_imbalance_details_balanced = ImbalanceAge(balanced_age_clusters, balanced_age_trends)

print("\nAGE_GROUP")
print("\nIMBALANCE: NORMAL")
print(age_imbalance_details_normal)
print("\n IMBALANCE: BALANCED")
print(age_imbalance_details_balanced)



#############BIAS####################

normGenBias = biasGender(normal_gender_clusters, normal_gender_trends)
balaGenBias = biasGender(balanced_gender_clusters, balanced_gender_trends)
print("\n\n\n\nGENDER")
print("\n NORMAL Average Bias:\n")
print(normGenBias)
print("\n BALANCED Average Bias:\n")
print(balaGenBias)

normRacBias = biasRace(normal_race_clusters, normal_race_trends)
balaRacBias = biasRace(balanced_race_clusters, balanced_race_trends)
print("RACE")
print("\n NORMAL Average Bias:\n")
print(normRacBias)
print("\n BALANCED Average Bias:\n")
print(balaRacBias)

normAgeBias = biasAge(normal_age_clusters, normal_age_trends)
balaAgeBias = biasAge(balanced_age_clusters, balanced_age_trends)
print("AGE")
print("\n NORMAL Average Bias:\n")
print(normAgeBias)
print("\n BALANCED Average Bias:\n")
print(balaAgeBias)



print("\n\nElapsed Time")
print("--- %s seconds ---" % (time.time() - start_time))