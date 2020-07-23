#usr/bin/python

import nltk

# Natural Language Processing Example

input_filepath = '.\john1_plaintext.txt'

with open(input_filepath, 'r') as txt_file:
    text_data = txt_file.read()

# print(text_data)
token_output = nltk.tokenize.sent_tokenize(text_data)
print(token_output)
