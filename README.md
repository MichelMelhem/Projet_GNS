# Projet_GNS
Projet GNS de Louis Alaux et Michel Melhem. Il s'agit de l'automoatisation des configurations de routeurs cisco à partir d'un fichier d'intention.
## Présentation du réseau 
![Capture d’écran du 2025-02-02 15-22-37](https://github.com/user-attachments/assets/7ec24197-5395-4972-ab5c-a84a17a4988c)
Nous avons un réseau comportant 5 AS : 
    -  AS1  :  R1,R2,R3,R7
    -  AS2  :  R4,R5,R6,R8
    -  AS3  :  R9
    -  AS4  :  R10
    -  AS5  :  R11
Toutes sont configurées avec OSPF sauf l'AS1 qui tourne en RIP.
Les AS1 et 2 sont peers entre elles, elles ont l'AS3 en provider et les AS 4 et 5 en customer. On a donc configuré BGP et les local pref des routes en conséquence.
## Exécution du script d'automatisation

A partir du fichier d'intention (data.json) on produit et place les configurations dans les bons répertoires (il faut modifier dans le script la variable de la racine du projet). Il suffit d'exécuter script.py et les configurations se génèrent à partir du json.
