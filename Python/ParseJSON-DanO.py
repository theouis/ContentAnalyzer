#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 18:46:46 2019

@author: douimetca.ibm.com
"""

import json
"""
ans = '{"family": {"name": "Mary", "age": "32", "sex": "female","kids": [{"name": "jim","age": "10","sex": "male","dob_year": "2007","ssn": "123-23-1234"},{"name": "jill","age": "6","sex": "female","dob_year": "2011","ssn": "123-23-1235"}]}}'
temp = json.loads(ans)
for kid in temp['family']['kids']:
    # if '1234' in items['ssn']:
    print(kid['name'], kid['ssn'])
"""

import json

with open('/Users/douimetca.ibm.com/Documents/Box Sync/AA - Personal Files/Programming/Datacap/content-analyzer-samples-master/CA/APT001.json') as json_file:
    data = json.load(json_file)
    # Find length of the array containing the KVPTable values
    myArray = (data['pageList'][0]['KVPTable'][0]['Key'])
    lengthArray = len(myArray)
    # Create a loop to print out all KVPs
    
    for i in range(lengthArray):
        """
        # First print line prints the name of the key 
        # the second line prints the value
        # make sure to match the 1st value on line 1 with the last value 
        # on second line
 
       print('Key: ', end='')
        print(data['pageList'][0]['KVPTable'][i]['Key'])
        print('Value: ', end='')
        print(data['pageList'][0]['KVPTable'][i]['Value'])
        print('Keyclass: ', end='')
        print(data['pageList'][0]['KVPTable'][i]['KeyClass'])
        print('Sensitivity: ', end='')
        print(data['pageList'][0]['KVPTable'][i]['Sensitivity'])
        print('Mandatory: ', end='')
        print(data['pageList'][0]['KVPTable'][i]['Mandatory'])
        print()         
        """
        # Print only mandatory fields
        if 'True' in (data['pageList'][0]['KVPTable'][i]['Mandatory']):
            print('Key: ', end='')
            print(data['pageList'][0]['KVPTable'][i]['Key'])
            print('Value: ', end='')
            print(data['pageList'][0]['KVPTable'][i]['Value'])
            print('Keyclass: ', end='')
            print(data['pageList'][0]['KVPTable'][i]['KeyClass'])
            print('Sensitivity: ', end='')
            print(data['pageList'][0]['KVPTable'][i]['Sensitivity'])
            print('Mandatory: ', end='')
            print(data['pageList'][0]['KVPTable'][i]['Mandatory'])
            print() 