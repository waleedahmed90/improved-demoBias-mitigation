import gzip
import json
import glob
import itertools
from pandas import DataFrame
#import matplotlib.pyplot as plt
import ntpath
import time
import os
import shutil
import operator


def initialValues(dict, vals):

	temp = {}
	i = 0
	for t in dict.keys():
		if (i == vals):
			break
		else:
			temp[t] = dict[t]
			i = i+1

	return temp

def fixGender(dictGend):

	#[male, female]
	temp_list = [0.0, 0.0]
	
	temp_list[0] = round(dictGend["male"]*100, 3)
	temp_list[1] = round(dictGend["female"]*100, 3)

	return temp_list

def fixRace(dictRace):

	#[white, black, asian]
	temp_list = [0.0, 0.0, 0.0]
	
	temp_list[0] = round(dictRace["white"]*100, 3)
	temp_list[1] = round(dictRace["black"]*100, 3)
	temp_list[2] = round(dictRace["asian"]*100, 3)
	
	return temp_list

def fixAge(dictAge):

	#[-20, 65+, 20-40, 40-65]
	temp_list = [0.0, 0.0, 0.0, 0.0]

	temp_list[0] = round(dictAge["-20"]*100, 3)
	temp_list[1] = round(dictAge["65+"]*100, 3)
	temp_list[2] = round(dictAge["20-40"]*100, 3)
	temp_list[3] = round(dictAge["40-65"]*100, 3)

	return temp_list




def extractDemographics(demoFile):

	with gzip.open(demoFile, 'rt') as u:
		demoInfo = u.read()
	u.close()

	demoInfoList = demoInfo.split("\n")

	total_hashtags = len(demoInfoList)-1

	gender = {}
	race = {}
	ageGroup = {}
	user_count = {}

	for h in range(total_hashtags):

		line = demoInfoList[h].split("\t")
		hashtagName = line[0]
		demographics = json.loads(line[1])
		ind_demographics = demographics["independent"]

		user_count[hashtagName] = demographics["valid_users_count"]

		gender[hashtagName] = fixGender(ind_demographics["gender"])
		race[hashtagName] = fixRace(ind_demographics["race"])
		ageGroup[hashtagName] = fixAge(ind_demographics["age_group"])


	return gender, race, ageGroup, user_count



def countPromotersOneStamp(dailyUsage, usageInfoList):
	
	total_Stamps = len(usageInfoList)-1

	for s in range(total_Stamps):
		stamp = usageInfoList[s].split("\t")
		timeStamp = stamp[0]
		Usage = json.loads(stamp[1])

		for t in Usage.keys():
			
			if t in dailyUsage:
				#get the list of usage promoters
				tempList = dailyUsage[t]
				#assign at stamp index s, length of the promoters for that hashtag
				tempList[s] = len(Usage[t])
				#assign that list back to that trend in dailyUsage dictionary
				dailyUsage[t] = tempList

	return dailyUsage



def calculateUsageThreshold(usageFile, UserCountDict):

	with gzip.open(usageFile, 'rt') as f:
		usageInfo = f.read()
	f.close()

	usageInfoList = usageInfo.split("\n")

	total_Stamps = len(usageInfoList)-1

	count_trend = 0
	count_tweet = 0

	dailyUsage = {}

	for s in range(total_Stamps):
		stamp = usageInfoList[s].split("\t")
		timeStamp = stamp[0]
		Usage = json.loads(stamp[1])

		for t in Usage.keys():
			if t in UserCountDict:
				dailyUsage[t] = [0]*96
			count_trend = count_trend + 1
			count_tweet = count_tweet + len(Usage[t])


	# print("Total Trends: ", count_trend)
	# print("Total Tweets: ", count_tweet)
	# print("dailyUsage Length::::::::::::: ", len(dailyUsage))

	dailyUsage = countPromotersOneStamp(dailyUsage, usageInfoList)

	return count_tweet/count_trend, dailyUsage

def adjustedTrendsGender(surge_dict, Demo_Gend):

	weight_male = 0.48
	weight_female = 0.52

	new_Surges = {}

	surgeValues = surge_dict.values()
	maxSurge = max(surgeValues)
	minSurge = min(surgeValues)

	for t in surge_dict.keys():
		surge = surge_dict[t]
		[M,F] = Demo_Gend[t]

		if (M>F):
			contrb_f = ( F * surge ) / 100
			contrb_m = ( M * surge ) / 100

			revised_surge = contrb_f / weight_female

			new_Surges[t] = round(revised_surge, 3)
		
		else:
			contrb_f = ( F * surge ) / 100
			contrb_m = ( M * surge ) / 100

# ###############
			#edge = (F-M)/100
# ###############

			revised_surge = (contrb_m / weight_male)


			#compensation = revised_surge * edge

			#revised_surge = revised_surge + compensation


			new_Surges[t] = round(revised_surge, 3)

	#sorting them in descending order
	sorted_surges = dict(sorted(new_Surges.items(), key=operator.itemgetter(1),reverse=True))

	top_10 = initialValues(sorted_surges, 10)

	return top_10




def	adjustedTrendsRace(surge_dict, Demo_Race):
	
	weight_white = 0.5
	weight_black = 0.3
	weight_asian = 0.2

	new_Surges = {}

	surgeValues = surge_dict.values()
	maxSurge = max(surgeValues)
	minSurge = min(surgeValues)


	for t in surge_dict.keys():
		surge = surge_dict[t]
		[W,B,A] = Demo_Race[t]

		if (W>(B+A)):
			contrb_w = ( W * surge ) / 100
			contrb_b = ( B * surge ) / 100
			contrb_a = ( A * surge ) / 100

			revised_surge = (contrb_b + contrb_a) / (weight_black + weight_asian)

			new_Surges[t] = round(revised_surge, 3)
		
		else:
			contrb_w = ( W * surge ) / 100
			contrb_b = ( B * surge ) / 100
			contrb_a = ( A * surge ) / 100

###############
			#edge = ((B+A)-W)/100
###############

			revised_surge = (contrb_w / weight_white)



			#compensation = revised_surge * edge

			#revised_surge = revised_surge + compensation



			new_Surges[t] = round(revised_surge, 3)


	#sorting them in descending order
	sorted_surges = dict(sorted(new_Surges.items(), key=operator.itemgetter(1),reverse=True))

	top_10 = initialValues(sorted_surges, 10)

	return top_10



	
def	adjustedTrendsAge(surge_dict, Demo_Age):

	weight_ado = 0.40		#(less than 20 years of age) 		#(adolescent)
	weight_old = 0.07 		#(above 65 years of age) 	 		#(old)
	weight_yng = 0.25 		#(between 20 and 40 years of age)	#(young)
	weight_mid = 0.28 		#(between 40 and 65 years of age)	#(mid-aged)


	new_Surges = {}

	surgeValues = surge_dict.values()
	maxSurge = max(surgeValues)
	minSurge = min(surgeValues)

	for t in surge_dict.keys():
		surge = surge_dict[t]
		[A,O,Y,M] = Demo_Age[t]


		if ((O+Y)>(A+M)):
			contrb_o_y = ( (O+Y) * surge ) / 100
			contrb_a_m = ( (A+M) * surge ) / 100

			revised_surge = contrb_a_m / (weight_ado + weight_mid)

			new_Surges[t] = round(revised_surge, 3)

		else:
			contrb_o_y = ( (O+Y) * surge ) / 100
			contrb_a_m = ( (A+M) * surge ) / 100

###############
			#edge = ((A+M)-(O+Y))/100
###############

			revised_surge = (contrb_o_y / (weight_old + weight_yng))



			#compensation = revised_surge * edge

			#revised_surge = revised_surge + compensation




			new_Surges[t] = round(revised_surge, 3)



	#sorting them in descending order
	sorted_surges = dict(sorted(new_Surges.items(), key=operator.itemgetter(1),reverse=True))

	top_10 = initialValues(sorted_surges, 10)

	return top_10





def calculateSurge(dailyUsage, use_thresH, GenderDemo, RaceDemo, AgeDemo):
	Lambda = 0.25 # one eighth (1/8)th

	TOP_GENDER = {}
	TOP_RACE = {}
	TOP_AGE = {}

	exponent = 0
	for s in range(1, 96):

		singleStampSurge = {}

		for t in dailyUsage.keys():
			

			use_list = dailyUsage[t]

			tot_tweets = sum(use_list[:s])

			t_1 = use_list[s]
			t_0 = use_list[s-1]

			if t_0 == 0:
				ratioSurge = t_1
			else:
				ratioSurge = t_1/t_0


			if t_1!=0:
				exponent = 0
			else:
				exponent = exponent + 1

#			surge = (ratioSurge) + ( ( tot_tweets / s ) * ( (use_thresH) ** ( - ( Lambda * s ) ) ) )
			surge = (ratioSurge) + ( ( tot_tweets / s ) * ( (use_thresH) ** ( - ( Lambda * exponent ) ) ) )
#			surge = (ratioSurge) + ( ( tot_tweets ) * ( (use_thresH) ** ( - ( Lambda * s ) ) ) )


			singleStampSurge[t] = surge

		#print("SURGE: ", s)
		sorted_d = dict(sorted(singleStampSurge.items(), key=operator.itemgetter(1),reverse=True))
		
		temp_top_10 = (sorted_d, 10)

		#print("\nBEFORE:")
		#print(temp_top_10)

		#Removing the values with zero surges
		new_surges = {x:y for x,y in sorted_d.items() if y!=0}
		
		Top_10_Gender = adjustedTrendsGender(new_surges, GenderDemo)
		TOP_GENDER.update(Top_10_Gender)
		
		Top_10_Race = adjustedTrendsRace(new_surges, RaceDemo)
		TOP_RACE.update(Top_10_Race)
		
		Top_10_Age = adjustedTrendsAge(new_surges, AgeDemo)
		TOP_AGE.update(Top_10_Age)
		
		#print("\nAFTER:")
		#print(Top_10_Race)
		#input("Press Enter to continue...")

	return TOP_GENDER, TOP_RACE, TOP_AGE
	#return TOP_RACE
	#return TOP_AGE



if __name__== "__main__":
	start_time = time.time()
	
	path_demographics = "/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/hashtag_demographics/*.gz"
	path_usage = "/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/hashtag_Usage_Info/*.gz"


	demographics_files = sorted(glob.glob(path_demographics))
	usage_files =  sorted(glob.glob(path_usage))

	
	GENDER_TRENDING = {}
	RACE_TRENDING = {}
	AGE_TRENDING = {}


	for fn in range(len(usage_files)):

		#current Usage File and current Demographics File
		useFile = usage_files[fn]
		demFile = demographics_files[fn]

		print("Usage File: ", ntpath.basename(useFile))
		print("Demog File: ", ntpath.basename(demFile),"\n")


		Gender, Race, Age, userCount =  extractDemographics(demFile)

		#Calculate usage threshold for the current day
		use_thresH, dailyUsage = calculateUsageThreshold(useFile, userCount)

		#print("Usage Threshold: ", use_thresH)
		
		#print("dailyUsage length: ", len(dailyUsage))

		gender_top_trends, race_top_trends, age_top_trends = calculateSurge(dailyUsage, use_thresH, Gender, Race, Age)
		
		#race_top_trends = calculateSurge(dailyUsage, use_thresH, Gender, Race, Age)
		
		#age_top_trends = calculateSurge(dailyUsage, use_thresH, Gender, Race, Age)
		
		GENDER_TRENDING.update(gender_top_trends)
		RACE_TRENDING.update(race_top_trends)
		AGE_TRENDING.update(age_top_trends)

		#print("Top Race Trends from today: ", len(race_top_trends), "\n")


		#break




	print("Trending Gender:::::: ", len(GENDER_TRENDING))
	print("Trending Race:::::::: ", len(RACE_TRENDING))
	print("Trending Age::::::::: ", len(AGE_TRENDING))


	#/Users/WaleedAhmed/Documents/THESIS_DS_CODE/mitigation DataSets/Demographics_Percentages
	#print(RACE_TRENDING)


	path_perc_gend = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/mitigation DataSets/Demographics_Percentages/Gender_Percentage_User_Demographics.gz'
	path_perc_race = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/mitigation DataSets/Demographics_Percentages/Race_Percentage_User_Demographics.gz'
	path_perc_age = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/mitigation DataSets/Demographics_Percentages/Age_Percentage_User_Demographics.gz'

	with gzip.open(path_perc_gend, 'rt') as g:
		gend_temp = g.read()
	g.close()

	gend_perc_dict = json.loads(gend_temp)
	
	with gzip.open(path_perc_race, 'rt') as r:
		race_temp = r.read()
	r.close()

	race_perc_dict = json.loads(race_temp)
	
	with gzip.open(path_perc_age, 'rt') as a:
		age_temp = a.read()
	a.close()

	age_perc_dict = json.loads(age_temp)




	GENDER_TRENDING_TOP = {}

	for t in gend_perc_dict.keys():
		if t in GENDER_TRENDING.keys():
			GENDER_TRENDING_TOP[t] = gend_perc_dict[t]


	print("Top gender trending:::::::: ", len(GENDER_TRENDING_TOP))


	RACE_TRENDING_TOP = {}

	for t in race_perc_dict.keys():
		if t in RACE_TRENDING.keys():
			RACE_TRENDING_TOP[t] = race_perc_dict[t]


	print("Top race trending:::::::: ",len(RACE_TRENDING_TOP))


	AGE_TRENDING_TOP = {}

	for t in age_perc_dict.keys():
		if t in AGE_TRENDING.keys():
			AGE_TRENDING_TOP[t] = age_perc_dict[t]


	print("Top age trending:::::::: ",len(AGE_TRENDING_TOP))

	path_new_trends_gend = './Mitigation_Trending_UsageData/trending_gend_perc.gz'
	path_new_trends_race = './Mitigation_Trending_UsageData/trending_race_perc.gz'
	path_new_trends_age = './Mitigation_Trending_UsageData/trending_age_perc.gz'


	try:
		os.mkdir('./Mitigation_Trending_UsageData')
	except:
		shutil.rmtree('./Mitigation_Trending_UsageData', ignore_errors=True)
		os.mkdir('./Mitigation_Trending_UsageData')

	
		
	with gzip.open(path_new_trends_gend, 'wb') as f1:
		f1.write(json.dumps(GENDER_TRENDING_TOP).encode('utf-8'))
	f1.close()
	print("<./Mitigation_Trending_UsageData/trending_gend_perc.gz>:::::Written")
	
	with gzip.open(path_new_trends_race, 'wb') as f2:
		f2.write(json.dumps(RACE_TRENDING_TOP).encode('utf-8'))
	f2.close()
	print("<./Mitigation_Trending_UsageData/trending_race_perc.gz>:::::Written")
	
	with gzip.open(path_new_trends_age, 'wb') as f3:
		f3.write(json.dumps(AGE_TRENDING_TOP).encode('utf-8'))
	f3.close()
	print("<./Mitigation_Trending_UsageData/Age_Trtrending_age_percending.gz>:::::Written")


	print("Elapsed Time")
	print("--- %s seconds ---" % (time.time() - start_time))
	
	