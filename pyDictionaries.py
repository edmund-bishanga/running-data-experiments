#!usr/bin/python

import pprint

# Exploring dictionaries, as a Data Structure.

# initiate
friends = dict()

# add
# friends["John"] = 34
# pprint.pprint(friends)

# augment
new_pals = {"Mary": 36, "Barigye": 75, "Ssekandi": 55}
# friends.update(new_pals)
# pprint.pprint(friends)

fam_friends = {"Herbert": 44, "Bernard": 42, "Lilian": 46, "Gordon": 40, "Joseline": 38, "Edmund": 36, "Loyce": 34, "Perez": 32}
friends.update(fam_friends)
pprint.pprint(friends)
