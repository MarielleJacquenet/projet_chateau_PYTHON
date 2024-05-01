# -*- coding: utf-8 -*-
"""
Projet chateau Mooc Python
    Marielle Jacquenet - mars 2024

Escape game simple avec déplacements dans un labyrinthe, récupération d'objets (indices)
et portes à franchir en répondant à des questions sur python
"""

######################################
#         INITIALISATIONS            #
######################################

#récupérer les constantes enregistrées dans configs.py
import CONFIGS
#print (CONFIGS.ZONE_PLAN_MINI)


#importer le module turtle
import turtle

turtle.tracer(0)
f = turtle.Screen()

#donner les caratéristiques de la fenêtre
#titre
turtle.title("Château du Python des neiges")

#taille et position
f.setup(540, 540, 0, 500)

#créer un objet tortue pour tracer les cases du labyrinthe
t = turtle.Turtle()

#créer un objet tortue pour le personnage
tp = turtle.Turtle()

#créer un objet tortue pour les annonces
ta = turtle.Turtle()

#créer un objet tortue pour l'inventaire
ti = turtle.Turtle()

#position en cours pour l'inventaire
pos_encours_inventaire = (70, 190)


######################################
#         FONCTIONS NIV 1            #
######################################

def lire_matrice(fichier):
    """ 
    Lit le plan dans un fichier texte et renvoie la matrice correspondante
    
    Paramètre
    ----------
    fichier : fichier texte contenant le plan à tracer

    Retour
    -------
    matrice (liste de listes représentant chacune une ligne horizontale)

    """
      
    #construire la matrice à partir des lignes du fichier
    #créer la matrice vide
    matrice = []
    
    #ouvrir le fichier en lecture
    #chaque ligne du fichier lue donne une ligne de la matrice 
    with open(fichier,"r", encoding='utf-8') as f:
        for lignef in f:
            lignem = [int(elem) for elem in lignef.split() ]
            """
            for elem in lignef:
                if type(elem) == integer:
                    lignem.append(int(elem))
            """        
            matrice.append(lignem)    
            
    #renvoyer la matrice 
    return matrice
    
  
def afficher_matrice(matrice):
    """
    Fonction non demandée - Affiche une matrice ligne par ligne

    Paramètres
    ----------
    matrice : liste de listes
 
    Retour
    -------
    None.

    """
    
    for elem in matrice:
        print(elem)
  
    
def calculer_pas(matrice):
    """
    Calcule la dimension à donner aux cases pour que le plan tienne dans la 
    zone de la fenêtre 

    Paramètre
    ----------
    matrice : liste de listes 
        Chaque sous liste représente une ligne horizontale 

    Retour
    -------
    pas : entier
        Dimension d'une case

    """
    # test recup constantes
    #print (CONFIGS.ZONE_PLAN_MINI)
    
    
    #diviser la largeur et la hauteur de la zone en question 
    #par le nombre de cases qu’elle doit accueillir
    nb_cases_largeur = len(matrice[1])
    nb_cases_hauteur = len(matrice)
    #print(nb_cases_largeur)
    #print(nb_cases_hauteur)
    
    largeur_zone = CONFIGS.ZONE_PLAN_MAXI[0] - CONFIGS.ZONE_PLAN_MINI[0]
    hauteur_zone = CONFIGS.ZONE_PLAN_MAXI[1] - CONFIGS.ZONE_PLAN_MINI[1]
    #print(largeur_zone)   
    #print(hauteur_zone)   
    
    #retenir la plus faible de ces deux valeurs
    pas = min(largeur_zone/nb_cases_largeur,hauteur_zone/nb_cases_hauteur )
    #print("pas :",pas)
    
    #la renvoyer
    return(round(pas))

def coordonnees(case, pas):
    """
    Calcule et renvoie les coordonnées d'une case donnée

    Paramètres
    ----------
    case : tuple
        Numéros de ligne et de colonne de la case
    pas : entier
        Taille du côté d'une case

    Retour
    -------
    coordonnees : tuple
        Coordonnées en pixel du coin inférieur gauche d'une case

    """

    #x = x coin haut gauche + pas * numéro colonne de la case
    #y = y coin haut gauche + pas * numéro ligne de la case
    #ajouter pas à y pour avoir le coin inférieur gauche
    x_depart = CONFIGS.ZONE_PLAN_MINI[0]
    y_depart = CONFIGS.ZONE_PLAN_MAXI[1]
    x = x_depart + case[1]* pas
    y = y_depart - case[0]* pas - pas
    
    return (x,y)
    
    
def tracer_carre(dimension):
    """
    Trace un carré dont la dimension en pixels turtle est donnée

    Paramètre
    ----------
    dimension : entier
        Taille du côté d'une case

    Retour
    -------
    None.

    """    

    #Trace un carré de côté donné à l'endroit où est la tortue
    for i in range(4):
        t.forward(dimension)
        t.left(90)
    
    
def tracer_case(case, couleur, pas):
     """
     Trace un carré d’une certaine couleur et taille à un certain endroit.

     Paramètres
     ----------
     case : tuple
         couple de coordonnées dans la matrice contenant le plan
     couleur : TYPE ?
         Couleur à utiliser pour tracer la case
     pas : entier
         Taille d'un côté de la case

     Retour
     -------
     None.

     """

     coord_case = coordonnees(case, pas)
     #print("coordonnées : ",coord_case)

     t.color(couleur)
     t.fillcolor(couleur)
     t.begin_fill()

     # aller aux coordonnées données
     t.penup()
     t.goto(coord_case)
     t.pendown()

     #tracer la case
     tracer_carre(pas)

     #fin du tracé de la case
     t.end_fill()

     #cacher la tortue
     t.hideturtle()
     

    
def afficher_plan(matrice):
    """
    Trace le  plan du château avec le module turtle
    
    Paramètre
    ----------
    matrice : liste de listes
        DESCRIPTION.

    Retour
    -------
    None

    """

    #print("Dans afficher_plan") 

    # calculer le pas 
    pas = calculer_pas(matrice)  ############global pas ???
    #print("pas = ", pas)

    #appelle tracer case pour chaque élément de la matrice
    #pour chaque ligne de la matrice
    for i in range(len(matrice)):
        #pour chaque élément d'une ligne de la matrice
        for j in range(len(matrice[i])):
            #récupérer la couleur de la case
            code_couleur = matrice[i][j]
            couleur = CONFIGS.COULEURS[code_couleur]
                 
            #print((i,j),couleur)
            
            #tracer une case de la couleur indiquée dans la matrice
            tracer_case((i,j), couleur, pas)
  

######################################
#         FONCTIONS NIV 2            #
######################################


def mettre_a_jour_position(nouvelle_position):
    """
    Modifie le tuple qui mémorise la case où se trouve actuellemnt le personnage (var globale)

    Paramètre
    ----------
    nouvelle_position : tuple
        Couple d'entiers indiquant la case où est le personnage

    Retour
    -------
    None.

    """

    global position

    l = list(nouvelle_position)
    position = tuple(l)


def deplacer_gauche():
    """
    Déplace le personnage vers la gauche

    Paramètres
    ----------
    None.
    

    Retour
    -------
    None.

    """
    
    global matrice, position 
    
    turtle.onkeypress(None, "Left")   # Désactive la touche Left

    # Appel de la fonction déplacer en précisant un mouvement vers la gauche
    nouvelle_position = deplacer(matrice, position, (0,-1))
    if nouvelle_position != position:
        mettre_a_jour_position(nouvelle_position)
        
    turtle.onkeypress(deplacer_gauche, "Left")   # Réassocie la touche Left à la fonction deplacer_gauche

    
def deplacer_droite():
    """
    Déplace le personnage vers la droite

    Paramètres
    ----------
    None.


    Retour
    -------
    None.

    """
    
    global matrice, position 
    
    turtle.onkeypress(None, "Right")   # Désactive la touche Right

    # Appel de la fonction déplacer en précisant un mouvement vers la droite
    nouvelle_position = deplacer(matrice, position, (0,1))
    if nouvelle_position != position:
        mettre_a_jour_position(nouvelle_position)
        
    turtle.onkeypress(deplacer_droite, "Right")   # Réassocie la touche Left à la fonction deplacer_droite

    
def deplacer_haut():
    """
    Déplace le personnage vers le haut

    Paramètres
    ----------
    None.


    Retour
    -------
    None.

    """
        
    global matrice, position 
    
    turtle.onkeypress(None, "Up")   # Désactive la touche Up

    # Appel de la fonction déplacer en précisant un mouvement vers le haut
    nouvelle_position = deplacer(matrice, position, (-1,0))
    if nouvelle_position != position:
        mettre_a_jour_position(nouvelle_position)

    turtle.onkeypress(deplacer_haut, "Up")   # Réassocie la touche Up à la fonction deplacer_haut

    
def deplacer_bas():
    """
    Déplace le personnage vers le bas

    Paramètres
    ----------
    None.


    Retour
    -------
    None.

    """
        
    global matrice, position 
    
    turtle.onkeypress(None, "Down")   # Désactive la touche Down

    # Appel de la fonction déplacer en précisant un mouvement vers le bas
    nouvelle_position = deplacer(matrice, position, (1,0))
    if nouvelle_position != position:
        mettre_a_jour_position(nouvelle_position)
        
    turtle.onkeypress(deplacer_bas, "Down")   # Réassocie la touche Down à la fonction deplacer_bas

    
def deplacer(matrice, position, mouvement):
    """
    Gère le déplacement du personnage en fonction du type de case vers laquelle il  se dirige

    Paramètres
    ----------
    matrice : liste de listes
        Matrice décrivant le château
    position : tuple
        Entiers correspondant à la position (case) où est le personnage
    mouvement : tuple
        Entiers représentant le sens du mouvement du personnage

    Retour
    -------
    None.

    """
      
    ########## AJOUTER GESTION OBJECTIF ############
    
    
    pas = calculer_pas(matrice)
    taille = pas * CONFIGS.RATIO_PERSONNAGE
    couleur_personnage = CONFIGS.COULEUR_PERSONNAGE
        
    #calculer quelle est la case où l'utilisateur veut se déplacer
    nouvelle_case = (position[0] + mouvement[0], position[1] + mouvement[1])

    #print("de ",position, "à ", nouvelle_case)

    #tester si le personnage peut se déplacer sur cette case
    #vérifier qu'on reste dans les limites du labyrinthe 
    if (nouvelle_case[0] >= 0) and (nouvelle_case[0] < len(matrice)) and (nouvelle_case[1] >= 0) and (nouvelle_case[1] < len(matrice[0])): 
        #print("on reste dans le labyrinthe")
        
        #récupérer le code couleur de la case
        type_case = matrice[nouvelle_case[0]][nouvelle_case[1]]
    
        #si la case est un couloir ou un objet ou l'objectif 
        if (type_case == 0) or (type_case == 2) or (type_case == 4): 
            #déplacer le personnage sur la nouvelle case
            afficher_personnage(nouvelle_case, taille, couleur_personnage)
            
            #si la case est l'objectif, le joueur a gagné
            if (type_case == 2):
                fin_du_jeu()
            
            #sinon si la case est un objet, on le récupère et on le retire du château
            elif (type_case == 4):
                ramasser_objet(nouvelle_case, matrice)
                
            return nouvelle_case
        
        #sinon si la case est une porte
        elif (type_case == 3): 
            #gérer la tentative d'ouverture de la porte avec qustion/réponse
            ouverture = poser_question(matrice, nouvelle_case, mouvement)
            
            #si la porte est ouverte, le personnage se déplace sur l'emplacement de la porte
            if (ouverture == True):    
                afficher_personnage(nouvelle_case, taille, couleur_personnage) 
                return nouvelle_case
       # else :    
            #print("tentative de sortie du labyrinthe")
        
    #sinon pas de déplacement
    return position
    
  
    
def position_personnage(case, pas):
    """
    Calcule et renvoie la position où il faut placer le personnage

    Paramètres
    ----------
    case : tuple
        Case où se trouve le personnage

    pas : entier
        Dimension d'une case

    Retour
    -------
    None.

    """

    #calculer les coordonnées du coin inférieur gauche de la case où est le personnage
    position = coordonnees(case, pas)
    #print(position)
    
    #renvoyer position du centre de la case
    return (position[0] + pas//2, position[1] + pas//2)


def afficher_personnage(case, taille, couleur):
    """
    Affiche le personnage dans le labyrinthe en fonction des paramètres donnés 

    Paramètres
    ----------
    position : tuple
        Case où on doit afficher le personnage
    taille : entier
        taille du rond représentant le personnage
    couleur : chaine
        Couleur du personnage

    Retour
    -------
    None.

    """

    #effacer le point précédent
    tp.reset()

    #chercher la position où doit être placé le personnage 
    pas = calculer_pas(matrice)
    position = position_personnage(case, pas)
     
    #déplacer la tortue au bon endroit pour dessiner le personnage
    tp.penup()
    tp.goto(position)
    tp.pendown()
    
    #Afficher le rond avec taille et la couleur données
    tp.dot(taille, couleur)
 
    
######################################
#         FONCTIONS NIV 3            #
######################################

def creer_dictionnaire_des_objets(fichier_des_objets):
    """
    Crée un dictionnaire d’objets à partir du fichier donné

    Paramètre
    ----------
    fichier_des_objets : fichier
        Fichier contenant les informations sur les objets à récupérer

    Retour
    -------
    Dictionnaire des objets contenus dans le fichier

    """

    #construire le dictionnaire à partir des lignes du fichier
    #créer le dictionnaire vide
    dictionnaire = {}
    
    #ouvrir le fichier en lecture
    #chaque ligne du fichier lue donne un élément du dictionnaire
    with open(fichier_des_objets,"r", encoding='utf-8') as f:
        for lignef in f:
            coordonnees, objet = eval(lignef)
            #print (coordonnees)
            #print (objet)
            dictionnaire[coordonnees] = objet
            
    #renvoyer le dictionnaire 
    return dictionnaire


def ramasser_objet(case, matrice):
    """
    Efface l'objet dans la case (dictionnaire, plan du château) 
    et ajoute l'objet à l'inventaire des objets trouvés

    Retour
    -------
    None.

    """

    global dictionnaire_des_objets

    #lire le dictionnaire pour récupérer l'objet
    objet = dictionnaire_des_objets[case]

    #annoncer qu'un objet a été trouvé
    ecrire_message("Vous avez trouvé : "+objet)

    #ajouter le nouvel objet trouvé dans l'inventaire
    ajout_inventaire(objet)

    #effacer l'objet enregistré pour la case donnée dansle dictionnaire
    del dictionnaire_des_objets[case]
      
    #changer la couleur de la case dans la matrice (mettre couleur couloir) 
    matrice[case[0]][case[1]] = 0

    #changer la couleur de la case sur le plan et réafficher le personnage
    tracer_case(case, CONFIGS.COULEUR_COULOIR, calculer_pas(matrice))

    #réafficher le personnage dans la case ############ Appeler fonction ?????
    pas = calculer_pas(matrice)
    taille = pas * CONFIGS.RATIO_PERSONNAGE
    couleur_personnage = CONFIGS.COULEUR_PERSONNAGE
    afficher_personnage(case, taille, couleur_personnage)


def ecrire_message(message):
    """
    Affiche le message indiquant qu'un objet a été trouvé

    Paramètre
    ----------
    objet : chaine
        Chaine correspondant message à afficher

    Returns
    -------
    None.

    """

    #effacer le message précédent
    ta.reset()

    #écrire le message à l'endroit prévu pour les annonces dans la fenêtre
    ta.penup()
    ta.goto(-240, 240)
    ta.pendown()
    ta.write(message, font=("Arial", 12, "normal"))


def ajout_inventaire(objet):
    """
    Affiche l'objet à la suite de l'inventaire

    Paramètre
    ----------
    objet : chaine
        chaine décrivant l'objet trouvé

    Retour
    -------
    None.

    """
    
    global pos_encours_inventaire
    
    #ajouter l'objet à l'affichage de l'inventaire
    ti.penup()
    print(pos_encours_inventaire)
    x = pos_encours_inventaire[0]
    y = pos_encours_inventaire[1]
    ti.goto(x,y)
    ti.pendown()
    ti.write(objet)
    
    #modifier la position en cours pour écrire un objet dans l'inventaire
    l = list(pos_encours_inventaire)
    l[1]-= 15
    pos_encours_inventaire = tuple(l)
    
    

######################################
#         FONCTIONS NIV 4            #
######################################

def creer_dictionnaire_questions_portes(fichier_questions):
    """
    Crée un dictionnaire des questions / réponses à partir du fichier donné

    Paramètre
    ----------
    fichier_des_objets : fichier
        Fichier contenant les questions et réponses correspondant à chaque porte

    Retour
    -------
    Dictionnaire des questions / réponses contenues dans le fichier

    """

    #construire le dictionnaire à partir des lignes du fichier
    #créer le dictionnaire vide
    dictionnaire = {}
    
    #ouvrir le fichier en lecture
    #chaque ligne du fichier lue donne un élément du dictionnaire
    with open(fichier_questions,"r", encoding='utf-8') as f:
        for lignef in f:
            coordonnees, question_reponse = eval(lignef)
            #print (coordonnees)
            #print (question_reponse)
            dictionnaire[coordonnees] = question_reponse
            
    #renvoyer le dictionnaire 
    return dictionnaire


def poser_question(matrice, case, mouvement):
    """
    Pose la question liée à la porte et teste la réponse

    Paramètres
    ----------
    matrice : TYPE
        DESCRIPTION.
    case : TYPE
        DESCRIPTION.
    mouvement : TYPE
        DESCRIPTION.

    Retour
    -------
    None.

    """
    
    global dictionnaire_questions_portes
    
    #afficher dans le bandeau d'annonces que la porte est fermée
    ecrire_message("La porte est fermée")
    
    #récupérer la question
    question_reponse = dictionnaire_questions_portes[case]
    question = question_reponse[0]
    reponse_attendue = question_reponse[1]
    
    #poser la question correspondant à la porte et saisir la réponse
    reponse_utilisateur = turtle.textinput("Question", question)
    
    #remettre en place l'évènement d'écoute
    turtle.listen()

    #si la réponse est bonne
    if (reponse_utilisateur == reponse_attendue):
        #remplacer la porte par une case couloir dans la matrice
        matrice[case[0]][case[1]] = 0

        #changer la couleur de la case sur le plan et réafficher le personnage
        tracer_case(case, CONFIGS.COULEUR_COULOIR, calculer_pas(matrice))

        #afficher dans le bandeau d'annonces que la porte est ouverte
        ecrire_message("Bonne réponse, vous avez ouvert la porte")
        
        #retourner true pour signaler l'ouverture
        return True
        
    #sinon 
    else:
        #afficher que la réponse est mauvaise 
        ecrire_message("Mauvaise réponse, la porte reste fermée")
        
        #renvoyer false
        return False
    

def fin_du_jeu():
    """
    Affiche au joueur qu'il a gagné et termine le jeu

    Paramètres
    ----------
    Aucun    

    Retour
    -------
    None.
    """

    #effacer la fenêtre
    turtle.clearscreen()

    #afficher le message de gain de partie
    t.penup()
    t.goto(-240,10)
    t.pendown()
    t.pencolor("red")
    t.write("BRAVO !", font=("Arial", 18, "normal"))
    t.penup()
    t.goto(-240,-20)
    t.pendown()
    t.write("Vous avez réussi à sortir du château !", font=("Arial", 14, "normal"))

    #fin de l'utilisation de la tortue - l'utilisateur peut fermer la fenêtre
    turtle.done()
    

######################################
#               TESTS                #
######################################

# 1-test lire_matrice
"""
matrice = lire_matrice("plan_chateau.txt")
afficher_matrice(matrice)
"""

# 2-test calculer_pas
"""
pas = calculer_pas(matrice)
#print("Dimension du côté d'une case : ", pas)
"""

# 3-test coordonnees
"""
print(coordonnees((0,0), pas))
print(coordonnees((0,1), pas))
print(coordonnees((0,2), pas))
print(coordonnees((1,0), pas))
print(coordonnees((2,0), pas))
"""

# 4-test tracer_carre
# OK testé ici puis dans tracer_case


# 5-test tracer_case
"""
tracer_case((0,0), "green", pas)
tracer_case((1,1), "yellow", pas)
tracer_case((2,2), "red", pas)
"""


# 6-test afficher_plan
"""
afficher_plan(matrice)
"""

# test creer_dictionnaire_des_objets
"""
dictionnaire_des_objets = creer_dictionnaire_des_objets(CONFIGS.fichier_objets)
print(dictionnaire_des_objets)
"""

# test écrire message
"""
ecrire_message("Vous avez trouvé : un objet super utile")
ecrire_message("Vous avez trouvé : un deuxième objet")
"""

# test ajout inventaire
"""
ti.penup()
ti.goto(70, 210)
ti.pendown()
ti.write("objet1")

ti.penup()
ti.goto(70, 195)
ti.pendown()
ti.write("objet2")

ti.penup()
ti.goto(70, 180)
ti.pendown()
ti.write("objet3")

ti.penup()
ti.goto(70, 165)
ti.pendown()
ti.write("objet4")
"""
"""
ajout_inventaire("Inventaire")
ajout_inventaire("objet 1")
ajout_inventaire("objet 2")
ajout_inventaire("objet 3")
"""

#test creer_dictionnaire_questions_portes
"""
dico_questions = creer_dictionnaire_questions_portes(CONFIGS.fichier_questions)
print(dico_questions)
"""



######################################
#        PROGRAMME PRINCIPAL         #
######################################

# Récupérer le plan du château dans une variable matrice
matrice = lire_matrice("plan_chateau.txt")
afficher_plan(matrice)

# Récupérer le dictionnaire des objets
dictionnaire_des_objets = creer_dictionnaire_des_objets(CONFIGS.fichier_objets)

# Récupérer le dictionnaire des questions/réponses liées au portes
dictionnaire_questions_portes = creer_dictionnaire_questions_portes(CONFIGS.fichier_questions)

#Initialiser l'inventaire
ajout_inventaire("INVENTAIRE")
ajout_inventaire("---------------")

# Afficher le personnage à la position de départ
case_perso = CONFIGS.POSITION_DEPART
taille = calculer_pas(matrice) * CONFIGS.RATIO_PERSONNAGE
couleur_personnage = CONFIGS.COULEUR_PERSONNAGE

afficher_personnage(case_perso, taille, couleur_personnage)

# Définir la variable qui enregistra la case sur laquelle sera le personnage au fur et à mesure des déplacements
position = case_perso

# Ecouter les évènements pour déplacer le personnage
turtle.listen()    # Déclenche l’écoute du clavier
turtle.onkeypress(deplacer_gauche, "Left")   # Associe à la touche Left une fonction appelée deplacer_gauche
turtle.onkeypress(deplacer_droite, "Right")
turtle.onkeypress(deplacer_haut, "Up")
turtle.onkeypress(deplacer_bas, "Down")
turtle.mainloop()    # Place le programme en position d’attente d’une action du joueur 


#fin de l'utilisation de la tortue - l'utilisateur peut fermer la fenêtre
turtle.done()

 