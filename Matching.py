# ==================================
# Matching.py
# 
# matchVolunteer [client's attributes] [[volunteer's atts],...]
# 
# Precondition: Volunteer and Client will share the same language and location.
# Attributes lists must have at least two attributes.
# There are no duplicate attributes in a list.
#
# This algorithm will match volunteers to clients depending on their
# conditions.
# ==================================

#Test Cases:
#client = ["c9", "t0", "t3", "t1", "t2"]
#volunteer = [["v0", "t1", "t5"],
#             ["v1", "t9", "t2", "t3"],
#             ["v2", "t1", "t0", "t2"],
#             ["v3", "t0"],
#             ["v4", "t4", "t0", "t2"],
#             ["v5", "t1", "t2"],
#             ["v6", "t0", "t2", "t1"]
#]

def matchVolunteer(client, volunteer):
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

    if highest_score == 0:
        return False
    else:
        return result[0]

#def main():
#    print matchVolunteer(client, volunteer)
    
#main()
