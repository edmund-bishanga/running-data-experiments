#!usr/bin/python

import pprint
# import requests
import sys

# Coding challenge: Th/23.Jul.2020
    # we're looking for 
    # a simple CLI tool 
    # that exercises our API 
    # to allow you to
    # + use our service to SEARCH FOR MATCHES 
    # + input data types: document/URL/text provided by the user. 

    # The API is (briefly) documented in a blog post
    # on our website -- it's a very simple HTTP API, basically only two
    # methods. Use whatever programming language / environment / libraries
    # you prefer. Let me know if you have any more questions about it.

# Get user query/input
user_input = sys.argv[1:]

# validate user input
print("USER INPUT:\n{}\n".format(user_input))
exp_args_length = 2
assert len(user_input) == exp_args_length, "expected args length: {}".format(exp_args_length)
assert isinstance(user_input[0], str), "first arg should be a string"

searchURL = "https://demo.kvasira.com/api/library/LIBRARY_ID/query"
searchTxt = user_input[0]
numResults = user_input[-1]
print("KVASIR QUERY params: \n{}, {}, {}\n".format(searchURL, searchTxt, numResults))

# run query using Kvasir API
# result = requests.get(url=searchURL, params={"query_type": searchTxt, "k": numResults})
# result = result.json()
result = {"foo": "bar", "abc": 123, "matches": {"1": "http://abc", "2": "https://efg", "3": "word123"}}

# present output to user
print("QUERY RESULT:")
pprint.pprint(result)
