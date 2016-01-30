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

def matchVolunteer():
    volunteer_score = [0]*(len(volunteer))
    index = 0
    search_index = 1
    while search_index < (len(client)):
        for i in volunteer: # check individual volunteers
            #print "client search index is: " + str(client[search_index])
            #print "i is: " + str(i)
            for j in i: # check each individual trait
                #print "\tj is: " + str(j)
                if client[search_index] == j:
                    #print "\t\tInserting: " + str(client[search_index]) + " in " + str(index)
                    volunteer_score[index] += 1
            #print "j loop complete."
            index += 1
        #print "i loop complete.\n"
        index = 0
        search_index += 1
    #print "while loop complete. search_index = "+ str(search_index)

    highest_score = 0
    for i in volunteer_score:
        if i > highest_score:
            highest_score = i

 
    result = volunteer[volunteer_score.index(highest_score)]

    return result[0]
