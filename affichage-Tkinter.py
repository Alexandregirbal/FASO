#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
import time

def def_tasks(tasks):

    if len(tasks)<4:
        tasks=[True,True,True,False]

    fenetre = Tk()

    label_titre = Label(fenetre, text="POTAGERE")
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

    bouton_quitter = Button(fenetre, text="VALIDER", command=fenetre.quit)
    bouton_quitter.pack()

    fenetre.mainloop()

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


print (def_tasks([True,True,False,True]))
input()
