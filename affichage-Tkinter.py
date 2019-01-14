#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
import time

def interface_gestion(tasks,pas):

    if len(tasks)<4:
        tasks=[True,True,True,False]

### --- fentre interactive --- ###

    fenetre = Tk()
    fenetre.title("Interface de gestion")
    fenetre.geometry("300x200")

    menubar = Menu(fenetre)
    fenetre.config(menu=menubar)
    menufichier = Menu(menubar,tearoff=0)
    menubar.add_cascade(label="Passages", command=lambda: liste_passages(pas))
    menufichier.add_command(label="Consulter les passages")

    label_titre = Label(fenetre, text="POTAGERE",fg="green")
    label_titre.pack()

    buttonsb=[]

    b1 = IntVar()
    b2 = IntVar()
    b3 = IntVar()
    b4 = IntVar()
    #b5 = IntVar()

    buttonsb.append(b1)
    buttonsb.append(b2)
    buttonsb.append(b3)
    buttonsb.append(b4)
    #buttonsb.append(b5)

    boutton1=Checkbutton(fenetre, text="Cocher si la tache est à faire",variable=b1 )
    boutton2=Checkbutton(fenetre, text="Cocher si la tache est à faire",variable=b2 )
    boutton3=Checkbutton(fenetre, text="Cocher si la tache est à faire",variable=b3 )
    boutton4=Checkbutton(fenetre, text="Cocher si la tache est à faire",variable=b4 )
    #boutton5=Checkbutton(fenetre, text="Cocher si la tache est à faire",variable=b5 )

    for c in range(0,4):
        if tasks[c]:
            buttonsb[c].set(1)

    boutton1.pack()
    boutton2.pack()
    boutton3.pack()
    boutton4.pack()
    #boutton5.pack()

    #bouton_quitter = Button(fenetre, text="VALIDER", command=lambda: liste_tasks(tasks))
    #bouton_quitter.pack()

    #boutton_passages = Button(fenetre, text="AFFICHER LES PASSAGES", command=liste_passages(pas),fg="orange")
    #boutton_passages.pack()

    fenetre.mainloop()

### --- FIN fentre interactive --- ###


    tasks_button=[]

    tasks_button.append(b1.get())
    tasks_button.append(b2.get())
    tasks_button.append(b3.get())
    tasks_button.append(b4.get())
    #tasks_button.append(b5.get())

    for i in range(0,len(tasks_button)):
        if tasks_button[i] == 1:
            tasks[i]=True
        elif tasks_button[i] == 0:
            tasks[i]=False


    return(tasks)


def liste_passages(pas):

    fenetre1 = Tk()

    label_titre = Label(fenetre1, text="POTAGERE",fg="green")
    label_titre.pack()

    taille = len(pas)
    tymax=(50+30*taille)
    can=Canvas(fenetre1,width=600,height=tymax)
    can.pack()
    ### -- init -- ###
    can.create_line(0, 10, 600, 10, fill="red")
    can.create_line(0, tymax, 600, tymax, fill="red")
    can.create_line(2, 10, 2, tymax, fill="red")
    can.create_line(125, 10, 125, tymax, fill="red")
    can.create_line(275, 10, 275, tymax, fill="red")
    can.create_line(425, 10, 425, tymax, fill="red")
    can.create_line(600, 10, 600, tymax, fill="red")

    can.create_text(60, 25, text="IDENTIFIANTS")
    can.create_text(200, 25, text="TEMPS ACTIF")
    can.create_text(350, 25, text="HEURE DEBUT")
    can.create_text(500, 25, text="HEURE FIN")

    ### -- fin init -- ###

    for i in range(taille):
        can.create_line(0, 10+30*(i+1), 600, 10+30*(i+1), fill="red")
        id=pas[i][0]
        tmps_a=pas[i][1]
        h_dbt=pas[i][2]
        h_fin=pas[i][3]
        y=50+30*i
        can.create_text(20, y, text=id)
        can.create_text(175, y, text=tmps_a)
        can.create_text(325, y, text=h_dbt)
        can.create_text(475, y, text=h_fin)

    fenetre1.mainloop()

    return(pas)


res=interface_gestion([True,True,False,True],[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16],[17,18,19,20]])
input()
