import json
from fonctions import *


path="config_type.cfg"

with open(path, "r", encoding="utf-8") as fichier:
    texte = fichier.readlines()
print(texte)

texte = insertion(texte, "!hostname position\n", ["hostname RX\n","test\n"," test décalé\n"])


with open(path, "w",encoding="utf-8") as fichier:
    fichier.writelines(texte)
