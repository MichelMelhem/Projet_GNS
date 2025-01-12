
def insertion(txt, indicateur, contenu):
    """la fonction pemet d'insérer du texte au niveau d'un contenu 
    (passé en argument). On lui entre la liste du texte (txt) puis le texte indicateur et enfin le contenu à insérer qui est une liste de str"""
    texte=txt
    for i in range(len(texte)):
        if texte[i]==indicateur:
            texte[i]="!\n"
            if len(contenu)>1:
                for j in range(len(contenu)):
                    texte.insert(i+j, contenu[j])
    return texte


