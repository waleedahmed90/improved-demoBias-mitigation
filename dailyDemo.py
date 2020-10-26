#Calculates the daily demographic information saves in files
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

###############################################
##############FLOW BEGINS HERE#################
###############################################
start_time = time.time()

path_demographics = "/Users/WaleedAhmed/Documents/THESIS_DS_CODE/Additional Work/hashtag_demographics/*.gz"
demographics_files = sorted(glob.glob(path_demographics))

daily_demographics_gen = "./GenderDailyDemographics/"
daily_demographics_rac = "./RaceDailyDemographics/"
daily_demographics_age = "./AgeDailyDemographics/"
daily_demographics_uc = "./UserCountDailyDemographics/"

#gender
try:
	os.mkdir(daily_demographics_gen)
except:
	shutil.rmtree(daily_demographics_gen, ignore_errors=True)
	os.mkdir(daily_demographics_gen)

#race
try:
	os.mkdir(daily_demographics_rac)
except:
	shutil.rmtree(daily_demographics_rac, ignore_errors=True)
	os.mkdir(daily_demographics_rac)

#age
try:
	os.mkdir(daily_demographics_age)
except:
	shutil.rmtree(daily_demographics_age, ignore_errors=True)
	os.mkdir(daily_demographics_age)

#userCount
try:
	os.mkdir(daily_demographics_uc)
except:
	shutil.rmtree(daily_demographics_uc, ignore_errors=True)
	os.mkdir(daily_demographics_uc)


for fn in range(len(demographics_files)):
	demFile = demographics_files[fn]
	
	FileName = ntpath.basename(demFile)
	#print("Demog File: ", ntpath.basename(demFile))

	Gender, Race, AgeGroup, user_count = extractDemographics(demFile)
	print(FileName)

	print(len(user_count))
	
	path_new_trends_gend = daily_demographics_gen+FileName
	path_new_trends_race = daily_demographics_rac+FileName
	path_new_trends_age = daily_demographics_age+FileName
	path_new_trends_uc = daily_demographics_uc+FileName
		
	with gzip.open(path_new_trends_gend, 'wb') as f1:
		f1.write(json.dumps(Gender).encode('utf-8'))
	f1.close()
	
	with gzip.open(path_new_trends_race, 'wb') as f2:
		f2.write(json.dumps(Race).encode('utf-8'))
	f2.close()
	
	with gzip.open(path_new_trends_age, 'wb') as f3:
		f3.write(json.dumps(AgeGroup).encode('utf-8'))
	f3.close()

	with gzip.open(path_new_trends_uc, 'wb') as f4:
		f4.write(json.dumps(user_count).encode('utf-8'))
	f4.close()



print("Elapsed Time")
print("--- %s seconds ---" % (time.time() - start_time))