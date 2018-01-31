import math
class weapon:
    def __init__(self,name,dmg_type,dmg_l_mod,dmg_h_mod,acc):
        self.dmg_type = dmg_type
        self.dmg_l_mod = dmg_l_mod
        self.dmg_h_mod = dmg_h_mod
        self.acc = acc
        self.name = name

    def chnce_to_ht(self,rnge,prp_trns):
        chnce = 100*math.exp(-rnge/(10+prp_trns))



        
#for turns_aiming in range(3):
#    print("TURNS AIMING:", turns_aiming)
#    for i in range(20):
#        print(i,100*math.exp(-i/(10+turns_aiming)))
