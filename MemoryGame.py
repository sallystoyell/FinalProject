from tkinter import *
from tkinter import ttk
import logging
from PIL import Image
import datetime
from tkmacosx import Button
import wx
import time
import os
import random


global subjID

class starterwindow():
    def __init__(self):
        global subjID

        #Create root gui 
        root = Tk()
        root.title("Memory Game")
        root.geometry('750x700')
        root.configure(background="cyan")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        #Put a canvas on top of root
        canvas = Canvas(root, width = 750, height=700, background="cyan")
        canvas.pack()
        Image = PhotoImage(file="Images_Display/MemoryGame_resize.gif")
        canvas.create_image(400, 300, image=Image)

        #Create a Subject box
        subjectLabel = Label(root, bg="cyan", text = "Please enter Subject ID: ", font=("Purisa", 15, "bold")).place(x=160,y=570)
        subject = Entry(root)
        subject.place(x=160, y=600)

        #Command to close the entry window to start the game
        def closeLaunchWindow():
            global subjID
            if subject.get()=="":
                EntryError = Label(root, foreground='red', background='cyan', text = "Please enter Subject ID", font=("Purisa", 15, "bold")).place(x=300,y=650)
            else:
                subjID = (subject.get())
                root.destroy()

        #Create start button
        button1 = Button(root, text = "Go!", highlightbackground = "green", bg = "green", command = lambda: closeLaunchWindow())
        button1.configure(font=("Purisa", 20, "bold"), borderless=1)
        button1.place(x=500, y=600, anchor=CENTER)

        root.mainloop()

class gamewindow():
    def __init__(self):
        global subjID

        #Create new root gui 
        root = Tk()
        root.title("Memory Game")
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.geometry(f'{width}x{height}')
        root.configure(background="cyan")

        #Set up logging
        experimentLog = subjID + '.log'
        logging.basicConfig(filename=experimentLog, level=logging.INFO)
        logging.info('Subject:: ' + subjID)
        logging.info("Date:: " + str(datetime.datetime.now()))
        
        global n_flip
        global flips
        global score
        global pic1_file
        global pic2_file
        global card
        global pic1
        global pic2
        global Button_1
        global Button_2
        global timer_end
        global list_flips_n
        global list_flips_im
        list_flips_n = []
        list_flips_im = []
        card = 12
        n_flip=0
        flips=0
        score=0
        #Define the funtion for flipping a card over
        def flip(j):
            global flips
            global n_flip
            global score
            global pic1_file
            global card
            global pic1
            global pic2
            global Button_1
            global Button_2
            global timer_end
            global sec
            global list_flips_n
            global list_flips_im
            #Change flip number
            flips += 1
            fliptext = Label(root, bg="cyan", text=f"Total flips: {flips}")
            fliptext.grid(row=2, column=(card//3), padx=30, sticky=NE)
            #Logic for if 1st or 2nd flip
            if n_flip == 0: 
                #Unflip cards
                if flips!=1:
                    pic1.destroy()
                    pic2.destroy()
                    pic1_file = ""
                    pic2_file = ""
                n_flip = 1
                pic1_file = card_images[j]
                list_flips_n.append(j)
                list_flips_im.append(pic1_file)
                #Display correct image in correct spot
                pic_image1 = PhotoImage(file=f"Images/{card_images[j]}")
                pic_image1 = pic_image1.subsample((2))
                pic1 = Label(image=pic_image1)
                pic1.image = pic_image1
                if j < card//3:
                    pic1.grid(row=0, column=j, padx = 50, pady = 5)
                elif j < (2*card//3):
                    pic1.grid(row=1, column=j-(card//3), padx = 50, pady = 5)
                else:
                    pic1.grid(row=2, column=j-(2*(card//3)), padx = 50, pady = 5)
                Button_1 = cardbuttons["Button{0}".format(j)]
            elif n_flip == 1:
                pic2_file = card_images[j]
                list_flips_n.append(j)
                list_flips_im.append(pic2_file)
                #Display correct image in correct spot
                pic_image2 = PhotoImage(file=f"Images/{card_images[j]}")
                pic_image2 = pic_image2.subsample((2))
                pic2 = Label(image=pic_image2)
                pic2.image = pic_image2
                if j < card//3:
                    pic2.grid(row=0, column=j, padx = 50, pady = 5)
                elif j < (2*card//3):
                    pic2.grid(row=1, column=j-(card//3), padx = 50, pady = 5)
                else:
                    pic2.grid(row=2, column=j-(2*(card//3)), padx = 50, pady = 5)
                if pic1_file == pic2_file: #i.e. if correct
                    score += 1
                    Scoretext = Label(root, bg="cyan", text=f"Score: {score}")
                    Scoretext.grid(row=2, column=(card//3), padx=15, sticky=NW)
                    Button_2 = cardbuttons["Button{0}".format(j)]
                    destroy_buttons()
                    #Add check marks
                #Reset n_flip
                n_flip = 0
                #Finished, log
                if score == card//2:
                    Congrats = Label(root, fg="red", bg="cyan", text="YOU DID IT!", font=("Purisa", 30, "bold"))
                    Congrats.grid(row=1, column=1)
                    pic1.destroy()
                    pic2.destroy()
                    timer_end = 1
                    logging.info(f'Time:: {sec}')
                    logging.info(f'Flips:: {flips}')
                    logging.info(f'Images:: {list_flips_im}')
                    logging.info(f'Positions:: {list_flips_n}')
            

        def destroy_buttons():
            global Button_1
            global Button_2
            Button_1.grid_forget()
            Button_2.grid_forget()

        #Set up the cards
        cardbuttons = {}
        for i in range(0, card):
            cardbuttons["Button{0}".format(i)] = Button(root, height= 250, width= 180, command = lambda i=i: flip(i))
            cardbuttons["Button{0}".format(i)].configure(borderless=1)
            if i < card//3:
                cardbuttons["Button{0}".format(i)].grid(row=0, column=i, padx = 50, pady = 5)
            elif i < (2*card//3):
                cardbuttons["Button{0}".format(i)].grid(row=1, column=i-(card//3), padx = 50, pady = 5)
            else:
                cardbuttons["Button{0}".format(i)].grid(row=2, column=i-(2*(card//3)), padx = 50, pady = 5)
        root.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='column')
        root.rowconfigure((0, 1, 2), weight=1, uniform='row')

        #Load up card images
        card_images_all = os.listdir("Images/")
        card_images = random.sample(card_images_all, k=card//2)
        card_images.extend(card_images)
        random.shuffle(card_images)

        #Title Image 
        Image = PhotoImage(file="Images_Display/MemoryGame_resize.gif")
        Image = Image.subsample((3))
        label1 = Label(image=Image, bg="cyan")
        label1.image = Image
        label1.grid(row=0, column=(card//3))
        
        #Timer
        global sec
        global minu
        global timer_end
        sec=0
        minu=0
        timer_end=0
        def timer():
            global sec
            global minu
            global timer_end
            if timer_end != 1:
                sec += 1
                Timertext = Label(root, bg="cyan", text="Time Elapsed: {:01d}:{:02d}".format(sec//60, sec % 60))
                Timertext.grid(row=1, column=(card//3))
                root.after(1000, timer)
        timer()
        
        #Put score and flips on the screen from the start
        Scoretext = Label(root, bg="cyan", text=f"Score: {score}")
        Scoretext.grid(row=2, column=(card//3), padx=15, sticky=NW)
        fliptext = Label(root, bg="cyan", text=f"Total flips: {flips}")
        fliptext.grid(row=2, column=(card//3), padx=30, sticky=NE)

        root.mainloop()


#Actually call the two windows
starterwindow()
gamewindow()

#Remove the "INFO:root" at the beginning of each line        
with open (subjID + '.log', 'r') as file:
    filedata=file.read()
    filedata=filedata.replace('INFO:root:', '')
with open (subjID + '.log', 'w') as file:
    file.write(filedata)

