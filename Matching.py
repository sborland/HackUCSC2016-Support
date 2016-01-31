# =====================================================================
# Matching.py
#
# matchVolunteer client_name [c_tags] [volunteer_name] [[v_tags]]
# function       String      [String] [String]         [[String]]
#
# This algorithm will match volunteers to clients depending on their
# tags.
#
# Preconditions:
#   Tags lists must have at least one element.
#   There are no duplicate tags in a list.
#   The length of volunteer_name must be equal to the length of
#   volunteer_tags.
#   The indices of volunteer_name must correspond to the indices of
#   volunteer_tags.
#
# Postconditions:
#   The name of the volunteer with the best compatibility with the
#   client is returned.
# =====================================================================
# EXAMPLE INPUT
# client_name = "c9"
# client_tag = ["Law", "Food", "Shelter"]
#
# volunteer_name = ["v0","v1", "v2","v3","v4","v5","v6"]
# volunteer_tag = [["Food"],
#                  ["Law"],
#                  ["Shelter"],
#                  ["Food", "Shelter"],
#                  ["Shelter", "Law"],
#                  ["Food", "Law"],
#                  ["Shelter", "Food", "Law"]
# ]
# =====================================================================

def matchVolunteer(c_name, c_tags, v_name, v_tags):
    # Create a new list of Floats, which represents how compatible
    # each volunteer is with the client. The higher the score, the
    # more compatible.

    if v_name is None:
        return False

    volunteer_score = [0.0] * (len(v_name))
    
    index = 0
    search_index = 0
    while search_index < (len(c_tags)):
        for i in v_tags:     # Check individual volunteers
            for j in i:      # Check each individual tag
                if c_tags[search_index] == j:
                    volunteer_score[index] += 1
            index += 1
        index = 0
        search_index += 1

    # Find the volunteer most compatible with the client, while
    # being efficient with volunteer's resources.
    highest_score = 0
    index = 0
    for i in volunteer_score:
        # Weight each volunteer by the number of tags.
        current_length = len(v_tags[index])
        if len(c_tags) > current_length:
            i = i / len(c_tags)
        else:
            i = i / current_length
        volunteer_score[index] = i
        
        # Rank volunteer by their compatibility with client.
        if i > highest_score:
            highest_score = i
        index += 1
    result = v_name[volunteer_score.index(highest_score)]
    
    
    # Returns False if there is no volunteer that can take the client.
    if highest_score == 0:
        return False
    else:
        return result
