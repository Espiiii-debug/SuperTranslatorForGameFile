class ConsoleColors:
    NORMAL = '^[92m' #GREEN
    WARNING = '^[93m' #YELLOW
    ERROR = '^[91m' #RED
    RESET = '^[0m' #RESET COLOR
# Gestion des Imports

import re
import os
import time
import shutil
import colorama
from colorama import Fore
from colorama import Style
from googletrans import Translator
import translators as ts
# ---------------------------------------

# Gestion des variables
lang = 'fr'
originLang = 'en' # Mettre 'auto' si vous souhaitez une détéction automatique
dir = "" # Dossier où toutes les fichiers vont être récupérés
destinationDIR = "" # Dossier où va être copier les fichiers traduits
regularExpression = '"(.*)" => "(.*)"' # Expression régulière selon laquel le programme va traduire le fichier
destinationErrorDIR = "" # Dossier où est envoyé tout les documents sur lequel le programme rencontre des problèmes
# ---------------------------------------


# Fonction qui renvoie une chaine ou une liste de chaine de caractère traduite
#
# /!\ Les caractères spéciaux ne sont pas renvoyez en UTF8 et donc apparaisseront en tant que "?" pour regler ce problème, changez de traducteur.
def traduce(txt):
    
    translator = Translator()
    #translation = translator.translate(txt, dest='fr', src=originLang)
    try:
        translation= ts.alibaba(txt, professional_field='message')
    except:
        translation = txt
    return translation
# ---------------------------------------

# Fonction qui permet de lire un fichier et de les traduire par bloc
def __readFile(file):
    
    # Initialisation de quelques listes
    toTradList = []
    basic = []
    final = []

    # Je lis mon document
    fichier = open(file, "r")
    line = fichier.readlines()

    for i in line:

        # Je cherche mon expression regulière
        e = re.search(regularExpression, i)

        # Je sauvegarde mes valeurs dans deux listes
        toTradList.append(e.group(2))
        basic.append(e.group(1))

    # Traduction de mon élément
    translator = Translator()
    translation = translator.translate(toTradList, dest='fr', src='en')
    for i in translation :
        print(i.text)
    
    # Concaténation de mes chaine de caractère pour en faire une chaine final
    for i in range(len(translation)-1):
        final.append('"' + basic[i] +'" => "' + translation[i].text + '"')
        print(Fore.GREEN + '"' + basic[i] +'" => "' + translation[i].text + '"' + Fore.RESET)
    
    # J'arrete la lecture du document
    fichier.close

    # Je commence l'ecriture de mon document
    fichier = open(file, "w")

    # J'ecris toutes les valeurs de ma list final dans le document
    for i in final:
        fichier.write(i +"\n")
    
    # J'arrete l'ecriture de mon document       
    fichier.close
    return
# ---------------------------------------

# Fonction qui permet de lire un document et de le traduire par ligne
def readFile(file):
    
    # J'initialise ma liste
    final = []

    # Je demarre la lecture de mon document
    fichier = open(file, "r")
    list = fichier.readlines()
    
    # Je recherche mon expression régulière et je la place dans ma liste final
    for i in list:
        final.append(replaceExpression(i, regularExpression))
    
    # J'arrète la lecture de mon document
    fichier.close

    # Je démarre l'écriture de mon document
    fichier = open(file, "w")

    # J'écris toutes les valeurs de ma liste final
    for i in final:
        fichier.write(i +"\n")
    
    # J'arrete la l'ecriture du document
    fichier.close
    return
# ---------------------------------------

# Permet de localiser une expression regulière dans un ligne et en retourner celle-ci traduite.
def replaceExpression(line, type):
    e = re.search(type, line)
    traduction = traduce(e.group(2))
    final = '"' + e.group(1) + '" => "' + traduction + '"'
    print(Fore.GREEN + final + Fore.RESET)
    return final    
# ---------------------------------------

# Fonction qui liste les fichiers d'un répertoire.
def main(dir):
    for i in os.listdir(dir):
        print(Fore.YELLOW + dir + i + Fore.RESET)
        try:
            readFile(dir + i)
        except:
            shutil.move(dir+i, destinationErrorDIR)
            print(Fore.RED + "[@ERROR] File : " + dir+i +" move to " +destinationErrorDIR + Fore.RESET)

        shutil.move(dir+i, destinationDIR)

        # Cooldown (pour eviter de se faire ban MDR)
        time.sleep(1)
        
    return
# ---------------------------------------

# Invocation de la fonction main    
colorama.init()
main(dir)