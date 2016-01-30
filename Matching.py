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
client = ["c9", "Shelter", "Law"]

volunteer = [["v1", "Food"],
             ["v2", "Law"],
             ["v3", "Food", "Shelter"],
             ["v4", "Shelter"],
             ["v5", "Shelter", "Law"]
]

volunteer_score = [0]*(len(volunteer))
#print client
#print volunteer
#print volunteer_score

index = 0
search_index = 1
while search_index < (len(client)):
    for i in volunteer: # check individual volunteers
        print "client search index is: " + str(client[search_index])
        print "i is: " + str(i)
        for j in i: # check each individual trait
            print "\tj is: " + str(j)
            if client[search_index] == j:
                print "\t\tInserting: " + str(client[search_index]) + "in " + str(index)
                volunteer_score[index] = 1
        print "j loop complete."
        index += 1
    print "i loop complete.\n"
    search_index += 1
print "while loop complete. search_index = "+ str(search_index)

    


print volunteer_score
