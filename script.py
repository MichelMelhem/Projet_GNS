import json
from fonctions import *


path1="config_type.cfg"

with open(path1, "r", encoding="utf-8") as fichier:
    f_default = fichier.readlines()

datas = import_data("data.json")

print(BGP(datas,"R1","RIPng"))
l_test = BGP(datas,"R1","RIPng")
f_test = ["!iBGP"]
f_test=insertion(f_test, "!iBGP",l_test)
with open("test.cfg", "w", encoding="utf-8") as test:
    test.writelines(f_test)
