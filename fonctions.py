from dataclasses import dataclass
from typing import Dict, List
import json
import os

@dataclass
class Interface:
    ip: str

@dataclass
class Router:
    number: int
    interfaces: Dict[str, Interface]
    use_bgp: bool
    is_border_router: bool
    as_number: int
    igp: str
    eBGP_neighbor: List[str]

def insertion(txt, indicateur, contenu):
    """la fonction pemet d'insérer du texte au niveau d'un indicateur 
    (passé en argument). On lui entre la liste du texte (txt) puis le texte indicateur et enfin le contenu à insérer qui est une liste de str"""
    texte=txt
    for i in range(len(texte)):
        if texte[i]==indicateur:
            texte[i]="!\n"
            if len(contenu)>1:
                for j in range(len(contenu)):
                    texte.insert(i+j, contenu[j]+"\n")
    return texte


def parse_router(data: dict) -> Router:
    interfaces = {key: Interface(**value) for key, value in data["interfaces"].items()}
    return Router(
        number=data["number"],
        interfaces=interfaces,
        use_bgp=data["use_bgp"],
        is_border_router=data["is_border_router"],
        as_number=data["as_number"],
        igp=data["igp"],
        eBGP_neighbor=data.get("eBGP_neighbor", [])
    )

def parse_routers(data: dict) -> Dict[str, Router]:
    return {key: parse_router(value) for key, value in data.items()}

def import_data(path: str) -> Dict[str, Router]:
    """
    Importer et mettre dans une structure (class) les routeurs d'un fichier JSON

    Argument:
        path, le chemin vers le fichier JSON

    Renvoie:
        un dictionaire de routeurs (où les clés sont les attribus et les valeurs les valeurs)
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return parse_routers(data)

def BGP(datas: Dict[str, Router], r_name: str, igp_process_name: str):
    """
    Permet d'ajouter la config iBGP aux routeurs qui ne sont pas ceux de bordure
    Arguments: 
        - les données extraites du json
        - le nom du routeur concerné 
        - le nom du preocessus IGP (ex: "RIPng" ou "1"), ce doit être une chaine de caractère
    Renvoie :
        -le bloc de lignes pour BGP
    """
    r_number = datas[r_name].number
    nb_interfaces = len(datas[r_name].interfaces)
    #recherche des voisins du routeur à partir de son as number et ajout dans une liste d'adresses
    n_list = []
    for i in range(1, len(datas)+1):
        if(datas["R" + str(i)].as_number==datas[r_name].as_number)&(("R"+str(i))!=r_name):
            n_list.append(datas["R" + str(i)].interfaces["Loopback0"].ip)

    #creéation du bloc de commandes à écrire dans le fichier de config
    as_n = datas[r_name].as_number
    BGP_bloc = ["router bgp " + str(as_n),
        " bgp router-id " + str(r_number) + "." +str(r_number) + "." +str(r_number) + "." + str(r_number),
        " bgp log-neighbor-changes",
        " no bgp default ipv4-unicast"]
    for i in n_list:
        BGP_bloc.append(" neighbor " + i.split('/')[0] + " remote-as " + str(as_n))
        BGP_bloc.append(" neighbor " + i.split('/')[0] + " update-source Loopback0")
    if datas[r_name].is_border_router == True: #test si il faut mettre eBGP (routeur de bordure)
        for i in range(len(datas[r_name].eBGP_neighbor)):
            BGP_bloc.append(" neighbor " + datas[datas[r_name].eBGP_neighbor[i]].interfaces["1/0"].ip.split('/')[0] + " remote-as "+str(datas[datas[r_name].eBGP_neighbor[i]].as_number))
    BGP_bloc.append(" address-family ipv6")
    for i in n_list:
        BGP_bloc.append("  neighbor " + i.split('/')[0] + " activate")
    if datas[r_name].is_border_router == True: #test si il faut mettre eBGP (routeur de bordure)
        for i in range(len(datas[r_name].eBGP_neighbor)):
            BGP_bloc.append("  neighbor " + datas[datas[r_name].eBGP_neighbor[i]].interfaces["1/0"].ip.split('/')[0] + " activate")
    #BGP_bloc.append("  redistribute connected")
    #BGP_bloc.append("  redistribute " + datas[r_name].igp + " " + igp_process_name)
    BGP_bloc.append(" network "+datas[r_name].interfaces["Loopback0"].ip.split("::")[0] + "::/" + datas[r_name].interfaces["Loopback0"].ip.split("/")[1])
    for i in range(1,nb_interfaces):
        BGP_bloc.append(" network "+datas[r_name].interfaces[str(i)+"/0"].ip.split("::")[0] + "::/" + datas[r_name].interfaces[str(i)+"/0"].ip.split("/")[1])  
    BGP_bloc.append("  redistribute " + datas[r_name].igp + " " + igp_process_name)  
    BGP_bloc.append(" exit-address-family")
    return BGP_bloc

def clear():
    datas=import_data("data.json")
    for i in range(1,len(datas)):
        path="R"+str(i)+".cfg"
        if os.path.exists(path):
            os.remove(path)
        else:
            print("Impossible de supprimer le fichier car il n'existe pas")
