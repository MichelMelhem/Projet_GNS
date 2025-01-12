with open("backup.txt", "r", encoding="utf-8") as fichier:
    bckup=fichier.readlines()

with open("config_type.cfg", "w", encoding="utf-8") as fichier:
    fichier.writelines(bckup)