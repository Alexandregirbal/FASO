import RPi.GPIO as GPIO
import time
from Tkinter import *
GPIO.setmode(GPIO.BOARD)
init = 0
table_taches = # on doit initialisé ce tableau

#https://singleblogcomputer.com/allumer-une-led-sur-son-raspberry
def allumer(table_taches,N): #entree: tableau de booleen des taches (True = à faire)
    n=int(N)                 # N est le decalage des input du GPIO (positif ou négatfif)
    for j in range(len(table_taches)):   #Attention, il faut bien faire en sorte que les numéros des GPIO correspondent avec j.
        GPIO.setup(j+n,GPIO.OUT)
        if table_taches[j]:
            GPIO.output(j+n,True)
        else:
            GPIO.output(j,False)
    return() #sortie: le tableau d'affichage est correctement allumé


def selection(): #https://openclassrooms.com/forum/sujet/python-detecter-les-touches-pressees-sur-le-clavier-13179
    root=Tk()
    root.bind("<Left>",goleft) #fonction goleft permet de selectionner la case de gauche
    root.bind("<Right>",goright) #de meme à droite
    return()

def goleft(init,N):   #on considère le curseur placé en position 'init' défini en debut d'exécution
    n=int(N)
    if init==0:
        return('error')
    else:
        GPIO.setup(n+init,GPIO.OUT)
        count=0
        while count<3: #on fait clignoter 3 fois la LED pour afficher la selection
            GPIO.output(n+init,True)
            time.sleep(0.5)
            GPIO.output(n+init,False)
            time.sleep(0.5)
            count += 1
            print count
        init -= 1   #puis on incremente la valeur de init pour la prochaine action
    return()    #la LED selectionnee a clignotee 3 fois, on a changé la valeur de init de -1

def goright(init,N):   #on considère le curseur placé en position 'init' défini en debut d'exécution
    n=int(N)
    if init==len(table_taches):
        return('error')
    else:
        GPIO.setup(n+init,GPIO.OUT)
        count=0
        while count<3: #on fait clignoter 3 fois la LED pour afficher la selection
            GPIO.output(n+init,True)
            time.sleep(0.5)
            GPIO.output(n+init,False)
            time.sleep(0.5)
            count += 1
            print count
        init += 1   #puis on incremente la valeur de init pour la prochaine action
    return()    #la LED selectionnee a clignotee 3 fois, on a changé la valeur de init de +1
