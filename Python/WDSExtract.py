#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 18:46:46 2019

@author: douimetca.ibm.com

What does this file do? 
- Find identified Headers and send them to NLU for analysis

Application flow:
1 - Parse the CA JSON output file
2- Look for LineHeaderAttributes that have returned as VERY HIGH (match)
3- Find those titles in the WDS section of the JSON file
4- Extract the Title and Content of those matched WDS entries into a CSV file
5- Run those same values through NLU ans save the results to a new JSON output file

"""
import os.path
import json
import csv
from pathlib import Path

# FILENAME AND PATHS USED IN THIS FILE
# Filename used for CSV output file of the WDS values
wdsFileName = ('/Users/douimetca.ibm.com/Documents/Box Sync/Programming/BACA/CA/Output/WDS.csv')
# Filename used for NLU output
nluOutFileName=('/Users/douimetca.ibm.com/Documents/Box Sync/Programming/BACA/CA/Output/WatsonNLUOut.JSON')
# JSON file from Content Analyzer
JSONInFilename=('/Users/douimetca.ibm.com/Documents/Box Sync/Programming/BACA/CA/Output/Input/json/Website Maintenance Contract.json')
#test
# open the JSON file and read contents
with open(JSONInFilename) as json_file:
    data = json.load(json_file)
#
   # Find length of the array containing the KVPTable values
    numPages = len((data['pageList'])) -1
    # Find length of the array containing the KVPTable values
    numLDA = len((data['pageList'][0]["BlockList"][0]['LineList'][0]['LineHeaderAttributes']['HeaderText']))
    # Find length of the array containing the LineHeaderAttributes values
    numBlocks = len((data['pageList'][0]['BlockList'])) -1
    wdsWatsonValues = ""
    # Print the lengths - you can remove/comment these. TRhey are mostly for debugging
    print('Number of pages: ', numPages)
    print('Number of blocks: ', numBlocks)
    print('Number of LDAs: ', numLDA)

    # Begin iterating throught the JSON values
    for pgNumber in range(numPages):
        #print('Page No: ', pgNumber) # you can remove - used for debugging
        for blockNumber in range(numBlocks):
            #print('Page No: ', pgNumber) # you can remove - used for debugging
            #print('Block Number :', blockNumber) # you can remove - used for debugging
            try:
                # --------- start of debugging print block, prints all the values.
                #print('entering try')
                #print('Testing block number: ',blockNumber)
                #print('   HeaderText: ',(data['pageList'][0]["BlockList"][blockNumber]['LineList'][0]['LineHeaderAttributes']['HeaderText']))
                #print('   HeaderConfidence: ', (data['pageList'][0]["BlockList"][blockNumber]['LineList'][0]['LineHeaderAttributes']['HeaderConfidence']))
                #print('   HeaderClass: ', (data['pageList'][0]["BlockList"][blockNumber]['LineList'][0]['LineHeaderAttributes']['HeaderClass']))
                #print('=====================')
                # --------- end debugging print block

                # Test to see if there is a value in this block. If there is, run the IF, otherwise, try the next one
                b = (data['pageList'][0]["BlockList"][blockNumber]['LineList'][0]['LineHeaderAttributes']['HeaderText'])
                if "Very High" == (data['pageList'][0]["BlockList"][blockNumber]['LineList'][0]['LineHeaderAttributes']['HeaderConfidence']):
                    # --------- start of debugging print block, prints only VERY HIGH confidence values.
                    #print('=====================')
                    #print('VERY HIGH found in block: ', blockNumber)
                    #print('   HeaderText: ',(data['pageList'][0]["BlockList"][blockNumber]['LineList'][0]['LineHeaderAttributes']['HeaderText']))
                    #print('   HeaderConfidence: ', (data['pageList'][0]["BlockList"][blockNumber]['LineList'][0]['LineHeaderAttributes']['HeaderConfidence']))
                    #print('   HeaderClass: ', (data['pageList'][0]["BlockList"][blockNumber]['LineList'][0]['LineHeaderAttributes']['HeaderClass']))
                    # --------- end of debugging print block, prints only VERY HIGH confidence values.

                    # Now that we found some VERY HIGH LHAs, let's pull out the related WDS Title and Content for the matching entry
                    wdsValue=(data['pageList'][0]["BlockList"][blockNumber]['LineList'][0]['LineHeaderAttributes']['HeaderText'])
                    wdsRange = (len(data['WDS']))-1
                    #print(wdsValue) # you can remove - used for debugging
                    #print(len(data['WDS']))  # you can remove - used for debugging
                    # Loop through
                    for wdsItems in range (wdsRange):
                        # Quick check to see if there is a value to extract
                        if wdsValue == (data['WDS'][wdsItems]['Title']):
                            print('=====================')
                            print('     Title: ', (data['WDS'][wdsItems]['Title']))
                            print('     Content: ', (data['WDS'][wdsItems]['Content']))
                            
                            wdsWatsonValues = wdsWatsonValues + (data['WDS'][wdsItems]['Content'])
                            try:
                                my_file = Path(wdsFileName)
                                if my_file.is_file():
                                    with open(wdsFileName,mode='a') as csv_file:
                                        # Append values to the file with the header
                                        fieldnames = ['Title', 'Content']
                                        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                                        writer.writerow({'Title': (data['WDS'][wdsItems]['Title']), 'Content': (data['WDS'][wdsItems]['Content'])})
                                else:
                                    with open(wdsFileName,mode='a') as csv_file:
                                        # Append values to the file without adding the header
                                        fieldnames = ['Title', 'Content']
                                        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                                        writer.writeheader()
                                        writer.writerow({'Title': (data['WDS'][wdsItems]['Title']),
                                                         'Content': (data['WDS'][wdsItems]['Content'])})
                            except:
                                print('Problem opening / creating CSV file')
                else:
                    continue
            except:
                continue

# Pass WDS values to NLU for analysis
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
    import Features, EntitiesOptions, KeywordsOptions,ConceptsOptions,CategoriesOptions,RelationsOptions, SemanticRolesOptions

try:
    naturalLanguageUnderstanding = NaturalLanguageUnderstandingV1(
        version='2018-11-16',
        iam_apikey='E87U7OBeyXoAyNG1nLVzvT7EMr6Es-812AHaLlvtE0-R',
        url='https://gateway.watsonplatform.net/natural-language-understanding/api')
    
    response = naturalLanguageUnderstanding.analyze(
        text=wdsWatsonValues,
        features=Features(
            entities=EntitiesOptions(emotion=False, sentiment=False, mentions=True, limit=50),
            keywords=KeywordsOptions(emotion=False, sentiment=False,limit=20),
            concepts=ConceptsOptions(limit=2),
            categories=CategoriesOptions(limit=2),
            relations=RelationsOptions(),
            semantic_roles=SemanticRolesOptions())).get_result()
    
    
    with open(nluOutFileName,'w') as outfile:
        json.dump(response, outfile)
except:
    print('No line headers found. No values in WDS. Watson cannot provide any entities')
