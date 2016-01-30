# ==================================
# Matching.py
# 
# Matching.py [client's Attributes] [[Volunteer's Atts],...]
# 
# Lists must have at least three attributes 
#
# This algorithm will match volunteers
# to clients depending on their
# conditions.
# ==================================

# Precondition: Volunteer and client will share the same language and location.

# 1 client that chooses from list of volunteers
# If there is no available volunteer, then it goes to the next
# volunteer with the least amount of clients.

#Initialize the people

client = ["c9", "Food", "Shelter", "Law"]

volunteer = [["v0", "Food"],
             ["v1", "Law"],
             ["v2", "Food", "Shelter"],
             ["v3", "Shelter"],
             ["v4", "Shelter", "Law"],
             ["v5", "Food", "Law"],
             ["v6", "Shelter", "Law", "Food"]
]


#def matchVolunteer(client, volunteer):
volunteer_score = [0]*(len(volunteer))
index = 0
search_index = 1
while search_index < (len(client)):
    for i in volunteer: # check individual volunteers
        for j in i: # check each individual trait
            if client[search_index] == j:
                volunteer_score[index] += 1
        index += 1
    index = 0
    search_index += 1

highest_score = 0
for i in volunteer_score:
    if i > highest_score:
        highest_score = i

 
result = volunteer[volunteer_score.index(highest_score)]

print result[0]
    
