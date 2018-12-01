#!/usr/bin/env python

# -*- coding: utf-8 -*-

import time
from grovepi import *

# donnees: Tableau de Booleens de listes de taches a faire(True tache non faite et False tache faite)
tableauEntree=[True,True,False,True]
#tableauEntree=modifTableau()	#modifTableau renvoie un tableau de booleens, qui correspond a la liste des taches a faire (WEB) 


valRFID=3 #On teste en attendant le programme valRFID() attention il faudra rajouter les "()" dans le main 3 emplacements a modifier

gestionnaire_allume=True #quand on a du courant (on peut eventuiellement programmer les horaires d'allumage du gestionnaire

liste_identifiants=[1,2,3,4,5,6] ########### ca sera des vrais numero RFID enregistres dans la base de donnes des utilisateurs

#passages=modifPassages() #a faire en relation avec WEB pour sotcker les passages et initialiser 
passages=[]

validation_de_fin = False

############################################################################################################################################################################################################################



def eteindreBuzzer(n):
    pinMode(n,"OUTPUT")
    digitalWrite(n,0)

def buzzer(n,k,x):    #Activation du buzzer connecte en port Dn pour k fois x sec, a intervalle de 0.7sec
    
    buzzer = n
    pinMode(buzzer,"OUTPUT")
    count = 0
    while count<k :
        try:
            digitalWrite(buzzer,1)
            print ('buzzer on')
            time.sleep(x)

            digitalWrite(buzzer,0)
            print ('buzzer off')
            time.sleep(0.5)

        except KeyboardInterrupt:
            digitalWrite(buzzer,0)
            break
        except IOError:
            print ("Error")
        count+=1

########### on utilise plus clignoter LED #####################"        
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

def allumerLED(n): #il faut connecter la LED en Dn (D1/D2/D3/D4...) 
    time.sleep(0.05)
    pinMode(n,"OUTPUT")
    digitalWrite(n,1)     # Send HIGH to switch on LED

def eteindreLED(n): #il faut connecter la LED en Dn (D1/D2/D3/D4...) 
    time.sleep(0.05)
    pinMode(n,"OUTPUT")
    digitalWrite(n,0)
    pinMode(8,"OUTPUT") #on eteint le buzzer sinon ca bug 
    digitalWrite(8,0)

def lectureBoutton(n): #on verifie pendant 2 sec la validation de boutotn
    t1=time.time()
    temps=0
    res=False
    while temps<2 and res==False:
        time.sleep(0.03)
        if digitalRead(n) == 1:
            res=True
        temps=time.time()-t1
    return (res)



##################################### on met les LED en ports D2,D3,D4,D5 ; les bouttons en ports D6(changment de selection),D7(touche validation) ; le buzzer en port D8 ####################################################

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

                        while not(lectureBoutton(7)) and not(lectureBoutton(6)):
                                for r in range(10):
                                            digitalWrite(j,0)     # Send LOW to switch off LED
                                            print ("LED OFF!")
                                            time.sleep(0.08)
                                            digitalWrite(j,1)     # Send HIGH to switch on LED
                                            print ("LED ON!")
                                            time.sleep(0.08)
                                eteindreBuzzer(8)
                        
                        if lectureBoutton(7) and tableauEntree[j-2]: 	#si l'utilisateur a appuye sur entrer (5secondes disponibles pour appuyer)
                                heure_debut=time.time() 	#on stock l'heure de debut
                                tableauEntree[j-2]=False 	#modification du tableau d'entree des taches
                                buzzer(8,2,1)
                                eteindreBuzzer(8)
                                nonValide=False # on valide la tache donc on va sortir de la boucle
                                print('on vient de valider la tache num',j-1)

                                
                        elif lectureBoutton(7) and not(tableauEntree[j-2]) : #si l'utilisateur veut valider une tache qui n'est pas a faire
                                buzzer(8,1,2) 	#alors ca bipe 1 fois pendant 2 sec
                                eteindreBuzzer(8)
                                countToExit+=1 #si on valide 3 fois une tache non valide on arrete tout sans enregistrer le passage
                                print("on ne peut pas valider une tache non disponible...")
                                
                        elif lectureBoutton(6) :
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
                        print("on est dans ce if")
                        validation_de_fin=True
                        gestionnaire_allume=False #pour le moment on teste
                        
                        identifiant=valRFID
                        heure_fin=time.time()
                        temps_actif=heure_fin - heure_debut
                        for i in liste_identifiants:
                                print("on est dans ce for",i)
                                if identifiant==i: #on verifie que l'utilisateur est bien enregistre 
                                        print("et dans ce if")
                                        passages.append([identifiant,temps_actif,heure_debut,time.time()]) #on ajoute a l'historique des passages
                        print("on va quand meme eteindre les led")
                        for k in range(2,6): #user est parti donc on eteint toutes les LED
                                eteindreLED(k)
                        buzzer(8,2,1) 

                elif temps_actif > 7200 : #7200 sec = 2h 
                        passages.append([identifiant,0,heure_debut,time.time()])
                        tableauEntree[j-2]=True #l'user a eu un probleme et est parti sans valider: on suppose que la tache n'a pas ete effectuee donc elle est a faire
                        validation_de_fin=True
                        gestionnaire_allume=False
                        for k in range (2,6):
                                eteindreLED(k)
        for k in range (2,6):
            eteindreLED(k)
        gestionnaire_allume=False
        print("Bye bye")

print("THE END")
        











                                        
