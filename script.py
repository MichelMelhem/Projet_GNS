import shutil
from fonctions import *
import gns3fy

GNS3_SERVER_URL = "http://127.0.0.1:3080"
PROJECT_NAME = "louisgns"  
PROJECT_PATH = "/home/louis/GNS3/projects/louisgns"


gns3_server = gns3fy.Gns3Connector(GNS3_SERVER_URL)

# Load the project
project = gns3fy.Project(name=PROJECT_NAME, connector=gns3_server)
project.get()



#ouverture du fichier par default
path1="config_type.cfg"
with open(path1, "r", encoding="utf-8") as fichier:
    f_default = fichier.readlines()
#chargement du fuchier JSON avec la focntion import_data
path2="data.json"
datas = import_data(path2)

#suppression des fichiers restants si il exitstes
clear()

#création des fichiers de config de chaque routeurs
for i in range(1, len(datas)+1):
    f_curent = list(f_default) 
    r_name = "R" + str(i)
    nb_interfaces = len(datas[r_name].interfaces)
    number = datas[r_name].number

    #protocole de routage (process name = RIPng ou 1)
    igp=datas[r_name].igp
    if igp=="rip":
        pr_name="RIPng"
        bloc_igp=["ipv6 router rip RIPng", " redistribute connected"]
    elif igp=="ospf":
        bloc_igp=["ipv6 router ospf 1", " router-id " + str(number)+"."+ str(number)+"."+ str(number)+"."+ str(number), " redistribute connected"]
        pr_name = "1"
        for i in datas[r_name].border_interfaces:
            bloc_igp.insert(-1, " passive-interface "+"GigagbitEthernet"+i)
    else:
        pr_name="none"
        bloc_igp=["!"]


    #création de chaque intrfaces
    bloc_interface = []
    for j in range(1, nb_interfaces):
        int_name=str(j)+"/0"
        address=datas[r_name].interfaces[int_name].ip
        bloc_interface.append("interface GigabitEthernet"+str(j)+"/0")
        bloc_interface.append(" no ip address")
        bloc_interface.append(" negotiation auto")
        bloc_interface.append(" ipv6 address "+address)
        if igp=="ospf":
            bloc_interface.append(" ipv6 ospf " +pr_name +" area " +str(datas[r_name].as_number))
        bloc_interface.append(" ipv6 "+igp+" "+pr_name+" enable")
        bloc_interface.append("!")
    bloc_interface.append("interface Loopback0")
    bloc_interface.append(" no ip address")
    bloc_interface.append(" ipv6 address 2001::"+str(number)+"/128")
    bloc_interface.append(" ipv6 "+igp+" "+pr_name+" enable")
    #création de BGP (avec l'appel de la focntion)
    bloc_bgp = BGP(datas,r_name,pr_name)

    #création des routes maps 
    as_number=datas[r_name].as_number
    rtemap_bloc=[]
    rtemap_bloc.append("ip bgp-community new-format\r")
    for a,b,c in (("CUSTOMER_POLICY","200",str(as_number)+":100"),("PEER_POLICY","150",str(as_number)+":200"),("PROVIDER_POLICY","100",str(as_number)+":300")):
        rtemap_bloc.append(f"route-map {a} permit 10\r")
        rtemap_bloc.append(f" set local-preference {b}\r")
        rtemap_bloc.append(f" set community {c} additive\r")

    #insertion de chaque bloc dans le contenu du fichier

    #hostname
    insertion(f_curent, "!hostname\n",["hostname "+r_name,"!"])

    #igp
    insertion(f_curent, "!igp\n", bloc_igp)

    #interfaces
    insertion(f_curent, "!interfaces\n", bloc_interface)

    #bgp
    insertion(f_curent, "!bgp\n", bloc_bgp)

    #routes maps
    insertion(f_curent, "!routes maps\n", rtemap_bloc)

    #écriture finale du fichier du routeur Ri

    with open(r_name+".cfg", "w", encoding="utf-8") as config:
        config.writelines(f_curent) 

#copie des fichiers de config dans les routeurs et redémarage des routeurs

print("Deploying the configuration files to the routers :")

for node in project.nodes :
    print(f"Deploying the configuration file to the router {node.name} ...")
    routerNumber = datas[node.name].number
    node.stop() 
    dst = PROJECT_PATH + "/project-files/dynamips/" + node.node_id + "/configs/" +  f"i{routerNumber}_startup-config.cfg"
    if os.path.exists(dst):
        print(f"Destination file {dst} already exists. It will be overwritten.")
        os.remove(dst)
    shutil.copy("./" + node.name + ".cfg", dst)
    node.start()   
    print(f"Configuration file deployed to the router {node.name}.")

   # print(bloc_interface)
   # print(bloc_igp)
   # print(bloc_bgp)