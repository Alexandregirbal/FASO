#!/usr/bin/env python

# -*- coding: utf-8 -*-

import time
from grovepi import *
from affichage-Tkinter import *

##########################################################################################################################################################################

# ___ initialisation ___ #

# donnees: Tableau de Booleens de listes de taches a faire(True tache non faite et False tache faite)
tableauEntree=def_tasks([])
#tableauEntree=modifTableau()	#modifTableau renvoie un tableau de booleens, qui correspond a la liste des taches a faire (WEB)


valRFID=3 #On teste en attendant le programme valRFID() attention il faudra rajouter les "()" dans le main 3 emplacements a modifier

gestionnaire_allume=True #quand on a du courant (on peut eventuellement programmer les horaires d'allumage du gestionnaire)

liste_identifiants=[1,2,3,4,5,6] ########### ca sera des vrais numero RFID enregistres dans la base de donnes des utilisateurs

#passages=modifPassages() #a faire en relation avec WEB pour sotcker les passages et initialiser
passages=[]

validation_de_fin = False

temps_limite = 2 # on choisit 2h au max avant d'avoir fini une tache

#############################################################################################################################################################################

# ___ fonctions utiles ___ #

#post: renvoie 0 si aucun RFID n'est sur le capteur, le numero du badge sinon.
def valRFID():
    if True: #a modifier
        return True #a modifier
    else :
        return 0

#parametre: port de connection du buzzer
#post: ne renvoie rien, le buzzer n'emet pas de son
def eteindreBuzzer(n):
    pinMode(n,"OUTPUT")
    digitalWrite(n,0)


#parametre: port de connection du buzzer; nombre de sons emis; temps d'emission de chaque son
#post: sauf si error, le buzzer sonne comme prevu
def buzzer(n,k,x):    #Activation du buzzer connecte en port Dn pour k fois x sec, a intervalle de 0.7sec
    pinMode(n,"OUTPUT")
    count = 0

    while count<k :
        count+=1
        try:
            digitalWrite(n,1)
            print ('Buzzer ON')
            time.sleep(x)

            digitalWrite(n,0)
            print ('Buzzer OFF')
            time.sleep(x)

        except KeyboardInterrupt:
            digitalWrite(n,0)
            break
        except IOError:
            print ("Error")


#on utilise plus la fonction clignoterLED (probleme pour effectuer 2 taches en meme temps)
def clignoterLED(n): #on fait clignoter la LED 10 fois a intervalle de 0.5sec
    count=0
    while count<10:
        try:
            digitalWrite(n,0)     # Send LOW to switch off LED
            print ("LED OFF!")
            time.sleep(0.5)

            digitalWrite(n,1)     # Send HIGH to switch on LED
            print ("LED ON!")
            time.sleep(0.5)

        except KeyboardInterrupt:   # Turn LED off before stopping
            digitalWrite(n,0)
            break
        except IOError:             # Print "Error" if communication error encountered
            print ("Error")
        count+=1

#parametre: port de connection de la LED en Dn (D1/D2/D3/D4...)
#post: ne renvoie rien, la LED en Dn est allumee
def allumerLED(n):
    time.sleep(0.05)
    pinMode(n,"OUTPUT")
    digitalWrite(n,1)     # on envoie 'HIGH' pour allumer la LED


#parametre: port de connection de la LED en Dn (D1/D2/D3/D4...)
#post: ne renvoie rien, la LED en Dn est eteinte
def eteindreLED(n):
    time.sleep(0.05)
    pinMode(n,"OUTPUT")
    digitalWrite(n,0)
    pinMode(8,"OUTPUT") #on eteint le buzzer sinon ca bug pour la premiere LED
    digitalWrite(8,0)


#parametre: port de connection du boutton ; nombre de secondes pendant lesquels on verifie si le boutton est enclanche ou non
#post: renvoie True si appuye ; False si non appuye
def lectureBoutton(n,k): #on verifie pendant k sec la validation de boutton
    t1=time.time()
    temps=0
    res=False
    while temps<k and res==False:
        time.sleep(0.03)
        if digitalRead(n) == 1:
            res=True
        temps = time.time() - t1
    return (res)


#################################################################################################################################################

# ___ MAIN ___ #

# il faut mettre les LED en ports D2,D3,D4,D5 ; les bouttons en ports D6(changment de selection) et D7(touche validation) ; le buzzer en port D8 .

eteindreBuzzer(8)
countToExit=0
while gestionnaire_allume:
        if valRFID!=0 : # valRFID() renvoie un identifiant, si il n'y a pas de badge vaut 0
                buzzer(8,1,1.5)	# On indique a l'utilisateur qu'il peut intragir avec le gestionnaire
                eteindreBuzzer(8)
                time.sleep(2)

                for i in range(2,6) :	#on initialise pour voir quelles taches sont a faire
                        if tableauEntree[i-2]:
                                allumerLED(i)
                                eteindreBuzzer(8)
                                time.sleep(0.02)
                                print("on allume la LED en ",i)

                # on initialise la boucle:
                j=2
                nonValide=True

                while nonValide and countToExit < 3 :	#temps que on a pas valide de tache ou que l'on est pas parti

                        while not(lectureBoutton(7,1)) and not(lectureBoutton(6,1)): # si on appuie pas sur un des deux boutons ca clignotte
                                digitalWrite(j,0)     # Send LOW to switch off LED
                                print ("LED OFF!")
                                time.sleep(0.1)
                                digitalWrite(j,1)     # Send HIGH to switch on LED
                                print ("LED ON!")
                                time.sleep(0.1)
                                eteindreBuzzer(8)

                        # un fois qu'on sort de la boucle verifie quel touche est appuyee:
                        if lectureBoutton(7,1) and tableauEntree[j-2]: 	#si l'utilisateur a appuye sur entrer
                                heure_debut=time.time() 	#on stock l'heure de debut
                                tableauEntree[j-2]=False 	#modification du tableau d'entree des taches
                                buzzer(8,2,1)
                                eteindreBuzzer(8)
                                nonValide=False # on valide la tache donc on va sortir de la boucle
                                print('on vient de valider la tache num',j-1)


                        elif lectureBoutton(7,1) and not(tableauEntree[j-2]) : #si l'utilisateur veut valider une tache qui n'est pas a faire
                                buzzer(8,1,2) 	#alors ca bipe 1 fois pendant 2 sec
                                countToExit+=1 #si on valide 3 fois une tache non valide on arrete tout sans enregistrer le passage
                                print("on ne peut pas valider une tache non disponible...")

                        elif lectureBoutton(6,1) :
                                if tableauEntree[j-2] == False :
                                    eteindreLED(j) #dans le cas ou la tache n'etait pas a faire
                                if j==5 : 	#Dans le cas ou on est en fin de tableau
                                    j=2
                                else :
                                    j+=1
				print('on selectionne la tache num',j-1)

                if countToExit == 3 :
                    validation_de_fin = True

        while validation_de_fin == False : # temps que l'utilisateur n'a pas repasse le badge rfid
                time.sleep(0.1) #pour pas faire planter la raspberry cherie
                if valRFID!=0 :
                        print("Un badge RFID est capte")
                        validation_de_fin=True
                        gestionnaire_allume=False #pour le moment on teste

                        identifiant = valRFID
                        heure_fin = time.time()
                        temps_actif = heure_fin - heure_debut
                        for i in liste_identifiants:
                                print("on verifie que le badge est bien enregistre:",i)
                                if identifiant==i:
                                        print("Super il est bien enregistre, on ajoute les infos a la bdd.")
                                        passages.append([identifiant,temps_actif,heure_debut,time.time()]) #on ajoute a l'historique des passages
                                        buzzer(8,2,1) # une fois que tout est fini on fait buzzer pour signaler la fini

                elif temps_actif > 60*60*temps_limite : # temps_limite en heure(s)
                        passages.append([identifiant,0,heure_debut,time.time()])
                        tableauEntree[j-2]=True #l'user a eu un probleme et est parti sans valider: on suppose que la tache n'a pas ete effectuee
                        validation_de_fin=True

        print("On va quand meme eteindre les LED.")
        for k in range(2,6):
                eteindreLED(k)

        eteindreBuzzer(8) # pour eviter les bugs
        gestionnaire_allume=False

        print("Bye bye")
        print(passages)

print("Le gestionaire est eteint.")
