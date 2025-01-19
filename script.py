import json
from fonctions import *

#ouverture du fichier par default
path1="config_type.cfg"
with open(path1, "r", encoding="utf-8") as fichier:
    f_default = fichier.readlines()
#chargement du fuchier JSON avec la focntion import_data
path2="data.json"
datas = import_data(path2)

#création des fichiers de config de chaque routeurs
for i in range(1, len(datas)+1):
    r_name = "R" + str(i)
    nb_interfaces = len(datas["R1"].interfaces)
    number = datas[r_name].number
    #protocole de routage (process name = RIPng ou 1)
    igp=datas[r_name].igp
    if igp=="rip":
        pr_name="RIPng"
        bloc_igp=["ipv6 router rip RIPng", "redistribute connected"]
    elif igp=="ospf":
        bloc_igp=["ipv6 router ospf 1", " router-id " + str(number)+"."+ str(number)+"."+ str(number)+"."+ str(number)+".", " redistribute connected"]
        pr_name = "1"
    else:
        pr_name="none"


    #création de chaque intrfaces
    bloc_interface = []
    for j in range(1, nb_interfaces-1):
        int_name=str(j)+"/0"
        address=datas[r_name].interfaces[int_name].ip
        bloc_interface.append("interface GigabitEthernet")
        bloc_interface.append(" no ip address")
        bloc_interface.append(" negotiation auto")
        bloc_interface.append(" ipv6 address "+address)
        bloc_interface.append(" ipv6 "+datas[r_name].igp+" "+pr_name+" enable")

    #création de BGP (avec l'appel de la focntion)
    bloc_bgp = BGP(datas,r_name,pr_name)

    #insertion de chaque bloc dans le contenu du fichier

    

    #écriture finale du fichier du routeur Ri



    print(bloc_interface)
    print(bloc_igp)
    print(bloc_bgp)