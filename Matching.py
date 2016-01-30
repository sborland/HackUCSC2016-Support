# ==================================
# Matching.py
# 
# Matching.py [Victim's Attributes] [[Volunteer's Atts],...]
# 
# Lists must have at least three attributes 
#
# This algorithm will match volunteers
# to victims depending on their
# conditions.
# ==================================

#Initialize the people
victim = ["9999999999", "Shelter"]

volunteer = [["1111111111", "Food"],
             ["2222222222", "Law"],
             ["3333333333", "Shelter"],
             ["4444444444", "Shelter"]
]

volunteer_score = []
print victim
print volunteer
print volunteer_score

index = 0
for x in volunteer:
    if victim[1] == x[1]:
        volunteer_score.insert(0,"Match found at {0}".format(x))
        index = index + 1




print volunteer_score


# Precondition: Volunteer and Victim will share the same language.

# 1 VICTIM
# Choose from list of volunteers
# If there is no available volunteer, then it goes to the next
# volunteer with the least amount of victims.
# City
# Tags



#function stableMatching {
#    Initialize all m E M and w E W to free
#    while 3 free man m who still has a woman w to propose to {
#       w = first woman on m's list to whom m has not yet proposed
#       if w is free
#         (m, w) become engaged
#       else some pair (m', w) already exists
#        if w prefers m to m'
#            m' becomes free
#           (m, w) become engaged 
#         else
#           (m', w) remain engaged
#    }
#}
