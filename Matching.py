# =====================================================================
# Matching.py
#
# matchVolunteer [client's attributes] [[volunteer's atts],...]
#
# Preconditions: Volunteer and Client will share the same language
# and location. Attributes lists must have at least two attributes.                           =
# There are no duplicate attributes in a list.
#
# This algorithm will match volunteers to clients depending on their
# conditions.
# =====================================================================

def matchVolunteer(client, volunteer):
    # Create a new list of Integers, which represents how compatible
    # each volunteer is with the client. The higher the score, the
    # more compatible.
    volunteer_score = [0]*(len(volunteer))
    index = 0
    search_index = 1
    while search_index < (len(client)):
        for i in volunteer: # check individual volunteers
            for j in i: # check each individual attributes
                if client[search_index] == j:
                    volunteer_score[index] += 1
            index += 1
        index = 0
        search_index += 1

    # Find the volunteer most compatible with the client. 
    highest_score = 0
    for i in volunteer_score:
        if i > highest_score:
            highest_score = i
    result = volunteer[volunteer_score.index(highest_score)]

    # Returns False if there is no volunteer that can take the client.
    if highest_score == 0:
        return False
    else:
        return result[0]
