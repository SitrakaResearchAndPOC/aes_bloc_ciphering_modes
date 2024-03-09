# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 20:22:48 2022

@author: SEBA
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 09:14:22 2022

@author: SEBA
"""

import os
import sys
import cv2
import numpy as np 
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
#from Crypto.Protocol.KDF import scrypt
from Crypto.Util.Padding import pad,unpad
from base64 import b64encode
from base64 import b64decode
from Crypto.Util import Counter
import hashlib
from tkinter import*
from tkinter import filedialog
#from functools import partial
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from tkinter import font
#from tkinter import Frame, Canvas
import customtkinter
from PIL import Image, ImageTk   
import socket
import os
import time
import threading
from datetime import datetime
global filename

# s = ttk.Style()
# s.configure('User.TLabelframe', boredercolor='red')
# s.configure('User.TLabelframe.Label', foreground='blue')

CLIENT_DATA_PATH = "save"
image_size = 23
PATH = os.path.dirname(os.path.realpath(__file__))
customtkinter.set_appearance_mode("light") 
BUFFER_SIZE = 1024 * 1024  # The size in bytes that we read, encrypt and write to at once

window=customtkinter.CTk()
window.title("Cryptosysteme")
#window.iconbitmap("7.ico")
crypto_image = ImageTk.PhotoImage(Image.open(PATH + "/images/67.png").resize((image_size,image_size), Image.ANTIALIAS))
window.iconphoto(False,crypto_image)
#window.geometry("620x500")
#window.config(background="#3498db")
windowWidth = 620
windowHeight = 535
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()
xCordinate = int((screenWidth/2) - (windowWidth/2))
yCordinate = int((screenHeight/2) - (windowHeight/2))
window.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, xCordinate, yCordinate))
window.resizable(width=False, height=False)

#bg = PhotoImage(file="H:/Simulation/fond.png")
bg = ImageTk.PhotoImage(Image.open(PATH + "/images/109.jpg"))
bg1 = ImageTk.PhotoImage(Image.open(PATH + "/images/104.png"))
ouvrir_image = ImageTk.PhotoImage(Image.open(PATH + "/images/16.png").resize((15,15), Image.ANTIALIAS))
aide_image = ImageTk.PhotoImage(Image.open(PATH + "/images/24.png").resize((22,22), Image.ANTIALIAS))
apropos_image = ImageTk.PhotoImage(Image.open(PATH + "/images/23.png").resize((image_size, image_size), Image.ANTIALIAS))
partage_image = ImageTk.PhotoImage(Image.open(PATH + "/images/34.png").resize((image_size, image_size), Image.ANTIALIAS))
partage_fond = ImageTk.PhotoImage(Image.open(PATH + "/images/25.png"))
login_image = ImageTk.PhotoImage(Image.open(PATH + "/images/42.png").resize((image_size, image_size), Image.ANTIALIAS))
chat_image = ImageTk.PhotoImage(Image.open(PATH + "/images/57.png").resize((image_size, image_size), Image.ANTIALIAS))
envoi_image = ImageTk.PhotoImage(Image.open(PATH + "/images/86.png").resize((25,25), Image.ANTIALIAS))
#demarre_image = ImageTk.PhotoImage(Image.open(PATH + "/images/84.png").resize((80,29 ), Image.ANTIALIAS))


# def tab1():
#     canvas = Canvas(window, width = 620, height = 540)
#     canvas.pack(fill = "both", expand = True)
#     canvas.create_image(0, 0, image = bg, anchor = "nw")
def tab2():
    # canvas.destroy()
    # demarrer.destroy()
 
    canvas1 = Canvas(window, width = 620, height = 540)
    canvas1.pack(fill = "both", expand = True)
    canvas1.create_image(0, 0, image = bg1, anchor = "nw")
    
    class Fichier:
        def __init__(self,master,fichier  = 'none'):
           self.frame1 = ttk.LabelFrame(master, text='Séléction du fichier', width=570, height=70)
           self.frame1.pack()
           self.frame1.place(x = 25, y = 135)
           #self.browseFiles = browseFiles
           self.fichier = fichier
           self.fichier_url = StringVar()
           self.barre1 = ttk.Entry(self.frame1, text="Fichier à crypter ou à décrypter...",font =("",14),width=38,textvariable=self.fichier_url)
           #self.barre1 = customtkinter.CTkEntry(self.frame1,
                                                #width=420,textvariable=self.fichier_url,
                                                #placeholder_text="")
           self.barre1.pack()
           self.barre1.place(x = 130, y = 9)
           self.barre1.insert(0,"Fichier à crypter ou à décrypter...")
           self.barre1.config(state=tk.DISABLED)
           
           # self.labelFile = tk.Label(self.frame1, bg="#ABB2B9", height=2,width=60) 
   		
           # self.labelFile.place(x = 130, y = 8)
   		
           # self.fileLocation = tk.Label(self.labelFile, 
           #                         text = "Choose file to send",
           #                         bg = "#2C3E50", 
           #                         fg = "#EAECEE", 
           #                         font = "Helvetica 11",height=2,width=48)
           # self.fileLocation.place(x = -1, y = -1)
           
           #self.ouvrir = tk.Button(self.frame1, text="Ouvrir", command=self.fichier1,width=10,bg="#3498db",fg="#ffffff",bd=2,relief=tk.FLAT,font =("",10) )
           self.ouvrir = customtkinter.CTkButton(self.frame1, image=ouvrir_image, text="OUVRIR", width=90,
                                              compound="right", fg_color="#3895d0", hover_color="#41a9eb",
                                              command=self.fichier1)
           self.ouvrir.pack()   
           self.ouvrir.place(x = 20, y = 8)
        def fichier1(self):
            
            self.fichier = filedialog.askopenfilename(title="Selection du fichier",)
            self.barre1.config(state=tk.NORMAL)
            self.barre1.delete(0, "end")
            self.barre1.insert(0, str(self.fichier))
            self.barre1.config(state=tk.DISABLED)
            #self.fileLocation.configure(text=self.fichier)
    fichier = Fichier(window)
    
    class AlgoAES(Fichier):
        def __init__(self,master,fichier ='none',key = ''):
            Fichier.__init__(self, master,fichier)
            self.key = key
            self.frame2 = ttk.LabelFrame(master, text='Mot de passe', width=570, height=70)
            self.frame2.pack()
            self.frame2.place(x = 25, y = 210)
            self.motdepasse = StringVar()
            self.saisir = tk.Label(self.frame2, text="Saisir :", anchor=tk.W,font =("",10))
            self.saisir.pack()
            self.saisir.place(x = 70, y = 10)
            self.password = ttk.Entry(self.frame2, textvariable=self.motdepasse,show="*", font =("",14),width=38)        
            #self.password = customtkinter.CTkEntry(self.frame2,
                                                #width=420,textvariable=self.motdepasse,show="*",
                                                #placeholder_text="")
            self.password.pack()
            self.password.place(x = 130, y = 8)
            self.frame3 = ttk.LabelFrame(master, text='Fonction de hashage', width=570, height=60)
            self.frame3.pack()
            self.frame3.place(x = 25, y = 285)
            self.hashage = IntVar()
            self.sha = ttk.Radiobutton(self.frame3, text = 'SHA', value = 1, variable = self.hashage)
            self.sha.pack()
            #self.sha.place(x = 170, y = 7)
            self.sha.place(x = 170, y = 7)
            self.blake = ttk.Radiobutton(self.frame3, text = 'BLAKE', value = 2, variable = self.hashage)
            self.blake.pack()
            #self.blake.place(x = 370, y = 7)
            self.blake.place(x = 370, y = 7)
            # self.shake = ttk.Radiobutton(self.frame3, text = 'SHAKE', value = 3, variable = self.hashage)
            # self.shake.pack()
            # self.shake.place(x = 370, y = 7)
            self.frame4 = ttk.LabelFrame(master, text='Modes', width=570, height=60)
            self.frame4.pack()
            self.frame4.place(x = 25, y = 350)
            self.mode = IntVar()
            self.gcm = ttk.Radiobutton(self.frame4, text = 'GCM', value = 1, variable = self.mode)
            self.gcm.pack()
            self.gcm.place(x = 20, y = 6)
            self.cfb = ttk.Radiobutton(self.frame4, text = 'CFB', value = 2, variable = self.mode)
            self.cfb.pack()
            self.cfb.place(x = 120, y = 6)
            self.ofb = ttk.Radiobutton(self.frame4, text = 'OFB', value = 3, variable = self.mode)
            self.ofb.pack()
            self.ofb.place(x = 220, y = 6)
            self.cbc = ttk.Radiobutton(self.frame4, text = 'CBC', value = 4, variable = self.mode)
            self.cbc.pack()
            self.cbc.place(x = 320, y = 6)
            self.cbc = ttk.Radiobutton(self.frame4, text = 'ECB', value = 5, variable = self.mode)
            self.cbc.pack()
            self.cbc.place(x = 420, y = 6)
            self.cbc = ttk.Radiobutton(self.frame4, text = 'CTR', value = 6, variable = self.mode)
            self.cbc.pack()
            self.cbc.place(x = 520, y = 6)
            self.frame5 = ttk.LabelFrame(master,text='Cryptage/Decryptage', width=570, height=70)
            self.frame5.pack()
            self.frame5.place(x = 25, y = 415)
            #self.crypte_b = tk.Button(self.frame5, text="CRYPTE", command=self.getcrypte,width=10,bg="#27ae60",fg="#ffffff",bd=2,relief=tk.FLAT,font =("",10))
            self.crypte_b = customtkinter.CTkButton(self.frame5, text="CRYPTE", width=90,
                                               compound="right", fg_color="#54a24a", hover_color="#71c466",
                                               command=self.crypte)
            self.crypte_b.pack()
            self.crypte_b.place(x=180, y=8)
            #self.decrypte_b = tk.Button(self.frame5, text="DECRYPTE", command=self.getdecrypte,width=10,bg="#27ae60",fg="#ffffff",bd=2,relief=tk.FLAT,font =("",10))
            self.decrypte_b = customtkinter.CTkButton(self.frame5, text="DECRYPTE", width=90,
                                               compound="right", fg_color="#54a24a", hover_color="#71c466",
                                               command=self.decrypte)
            self.decrypte_b.pack()
            self.decrypte_b.place(x=296, y=8)
            self.frame6 = Frame(master, width=570, height=45)
            self.frame6.pack()
            self.frame6.place(x = 25, y = 488)
            #self.reset_b=tk.Button(self.frame6,text='RESET',command=self.reset,width=10,bg="#f56e6e",fg="#ffffff",bd=2,relief=tk.FLAT,font =("",10) )
            self.reset_b = customtkinter.CTkButton(self.frame6, text="RESET", width=90,
                                               compound="right", fg_color="#D35B58", hover_color="#f66d6d",
                                               command=self.reset)
            self.reset_b.place(x = 240, y = 7)
            self.apropos_b=customtkinter.CTkButton(self.frame6, image=apropos_image, text="", width=10, height=10,
                                               corner_radius=10, fg_color="#f0f0f0", hover_color="#f0f0f0", command=self.apropos)
            #self.apropos_b=tk.Button(self.frame6,text='A propos',command=self.apropos,width=6,bg="#a69e9e",fg="#ffffff",bd=2,relief=tk.FLAT,font =("",10) )
            self.apropos_b.place(x = 505, y = 9)
            self.aides_b=customtkinter.CTkButton(self.frame6, image=aide_image, text="", width=10, height=10,
                                               corner_radius=10, fg_color="#f0f0f0", hover_color="#f0f0f0", command=self.aides)
           
            #self.aides_b=tk.Button(self.frame6,text='Aide',command=self.aides,width=5,bg="#a69e9e",fg="#ffffff",bd=2,relief=tk.FLAT,font =("",10) )
            self.aides_b.place(x = 535, y = 9)
             
                
        def hashmotdepasse(self, password):
            if(self.hashage.get() == 1):
                self.p_word = password.get()
                self.key = hashlib.sha256(self.p_word.encode())
                print(self.key.hexdigest())
                return self.key.digest() 
            elif (self.hashage.get() == 2):
                self.p_word = password.get()
                self.key = hashlib.blake2s(self.p_word.encode())
                print(self.key.hexdigest())
                return self.key.digest()
            # elif (self.hashage.get() == 3):
            #     self.p_word = password.get()
            #     self.key = hashlib.shake_256(self.p_word.encode())
            #     print(self.key.hexdigest(16))
            #     return self.key.digest(16)
            
        def crypte(self):
            if self.barre1.get() == "Fichier à crypter ou à décrypter...":
                messagebox.showinfo("Erreur", "Veuillez selectionner le fichier.")
            elif len(self.password.get()) == 0:
                messagebox.showinfo("Erreur", "Veuillez saisir le mot de passe.")
            else:
                if not self.hashage.get():
                    messagebox.showinfo("Erreur", "Veuillez selectionner un fonction de hashage.")
                else:
                    if(self.mode.get() == 1):
                        keySize = 32
                        ivSize = AES.block_size  
                        #ivSize = 0
                        imageOrig = cv2.imread(self.fichier)
                        rowOrig, columnOrig, depthOrig = imageOrig.shape
                        minWidth = (AES.block_size + AES.block_size) // depthOrig + 1
                        if columnOrig < minWidth:
                            print('The minimum width of the image must be {} pixels, so that IV and padding can be stored in a single additional row!'.format(minWidth))
                            sys.exit()
                        # Conversion du donnée image en bit
                        imageOrigBytes = imageOrig.tobytes()
                        # Cryptage
                        self.key =  self.hashmotdepasse(self.password)
                        print(self.key)
                        
                        iv = get_random_bytes(ivSize)
                        cipher = AES.new(self.key, AES.MODE_GCM, iv) 
                        #cipher.update(aad)
                        imageOrigBytesPadded = pad(imageOrigBytes, AES.block_size)
                        # aut Tag
                        #TAG_LENGTH = 16
                        #ciphertext, tag = cipher.encrypt_and_digest(imageOrigBytesPadded)
                        ciphertext = cipher.encrypt(imageOrigBytesPadded)
                        #tag_e = cipher.digest()  # Signal to the cipher that we are done and get the tag
                        #print("Tag encryption: "+ str(tag))
                        # Conversion des bits chiffrées en image données
                        paddedSize = len(imageOrigBytesPadded) - len(imageOrigBytes)
                        void = columnOrig * depthOrig - ivSize - paddedSize
                        ivCiphertextVoid = iv + ciphertext + bytes(void)
                        imageEncrypted = np.frombuffer(ivCiphertextVoid, dtype = imageOrig.dtype).reshape(rowOrig + 1, columnOrig, depthOrig)
                        # Sortie image cryptée
                        cv2.imshow("Image crypte", imageEncrypted)
                        cv2.imwrite(self.fichier +'.bmp' , imageEncrypted)
                        cv2.waitKey()
                        # return {
                        #     'tag':b64encode(tag).decode('utf-8')
                        #     }
                  
                    elif (self.mode.get() == 2):
                         
                        keySize = 32
                        ivSize = AES.block_size  
                        imageOrig = cv2.imread(self.fichier)
                        rowOrig, columnOrig, depthOrig = imageOrig.shape
                        minWidth = (AES.block_size + AES.block_size) // depthOrig + 1
                        if columnOrig < minWidth:
                            print('The minimum width of the image must be {} pixels, so that IV and padding can be stored in a single additional row!'.format(minWidth))
                            sys.exit()
                        # Conversion du donnée image en bit
                        imageOrigBytes = imageOrig.tobytes()
                        # Cryptage
                        self.key =  self.hashmotdepasse(self.password)
                        print(self.key)
                        iv = get_random_bytes(ivSize)
                        cipher = AES.new(self.key, AES.MODE_CFB, iv)  
                        imageOrigBytesPadded = pad(imageOrigBytes, AES.block_size)
                        ciphertext = cipher.encrypt(imageOrigBytesPadded)
                        # Conversion des bits chiffrées en image données
                        paddedSize = len(imageOrigBytesPadded) - len(imageOrigBytes)
                        void = columnOrig * depthOrig - ivSize - paddedSize
                        ivCiphertextVoid = iv + ciphertext + bytes(void)
                        imageEncrypted = np.frombuffer(ivCiphertextVoid, dtype = imageOrig.dtype).reshape(rowOrig + 1, columnOrig, depthOrig)
                        # Sortie image cryptée
                        cv2.imshow("Image crypte", imageEncrypted)
                        cv2.imwrite(self.fichier + ".bmp", imageEncrypted)
                        cv2.waitKey()
                    elif(self.mode.get() == 3):
                        keySize = 32
                        ivSize = AES.block_size  
                        imageOrig = cv2.imread(self.fichier)
                        rowOrig, columnOrig, depthOrig = imageOrig.shape
                        minWidth = (AES.block_size + AES.block_size) // depthOrig + 1
                        if columnOrig < minWidth:
                            print('The minimum width of the image must be {} pixels, so that IV and padding can be stored in a single additional row!'.format(minWidth))
                            sys.exit()
                        # Conversion du donnée image en bit
                        imageOrigBytes = imageOrig.tobytes()
                        # Cryptage
                        self.key =  self.hashmotdepasse(self.password)
                        print(self.key)
                        iv = get_random_bytes(ivSize)
                        cipher = AES.new(self.key, AES.MODE_OFB, iv)  
                        imageOrigBytesPadded = pad(imageOrigBytes, AES.block_size)
                        ciphertext = cipher.encrypt(imageOrigBytesPadded)
                        # Conversion des bits chiffrées en image données
                        paddedSize = len(imageOrigBytesPadded) - len(imageOrigBytes)
                        void = columnOrig * depthOrig - ivSize - paddedSize
                        ivCiphertextVoid = iv + ciphertext + bytes(void)
                        imageEncrypted = np.frombuffer(ivCiphertextVoid, dtype = imageOrig.dtype).reshape(rowOrig + 1, columnOrig, depthOrig)
                        # Sortie image cryptée
                        cv2.imshow("Image crypte", imageEncrypted)
                        cv2.imwrite(self.fichier + ".bmp", imageEncrypted)
                        cv2.waitKey()
                    
                    elif(self.mode.get() == 4):
                        keySize = 32
                        ivSize = AES.block_size  
                        imageOrig = cv2.imread(self.fichier)
                        rowOrig, columnOrig, depthOrig = imageOrig.shape
                        minWidth = (AES.block_size + AES.block_size) // depthOrig + 1
                        if columnOrig < minWidth:
                            print('The minimum width of the image must be {} pixels, so that IV and padding can be stored in a single additional row!'.format(minWidth))
                            sys.exit()
                        # Conversion du donnée image en bit
                        imageOrigBytes = imageOrig.tobytes()
                        # Cryptage
                        self.key =  self.hashmotdepasse(self.password)
                        print(self.key)
                        iv = get_random_bytes(ivSize)
                        cipher = AES.new(self.key, AES.MODE_CBC, iv)  
                        imageOrigBytesPadded = pad(imageOrigBytes, AES.block_size)
                        ciphertext = cipher.encrypt(imageOrigBytesPadded)
                        # Conversion des bits chiffrées en image données
                        paddedSize = len(imageOrigBytesPadded) - len(imageOrigBytes)
                        void = columnOrig * depthOrig - ivSize - paddedSize
                        ivCiphertextVoid = iv + ciphertext + bytes(void)
                        imageEncrypted = np.frombuffer(ivCiphertextVoid, dtype = imageOrig.dtype).reshape(rowOrig + 1, columnOrig, depthOrig)
                        # Sortie image cryptée
                        cv2.imshow("Image crypte", imageEncrypted)
                        cv2.imwrite(self.fichier + ".bmp", imageEncrypted)
                        cv2.waitKey()
                    elif(self.mode.get() == 5):
                        keySize = 32
                        ivSize = AES.block_size  
                        imageOrig = cv2.imread(self.fichier)
                        rowOrig, columnOrig, depthOrig = imageOrig.shape
                        minWidth = (AES.block_size + AES.block_size) // depthOrig + 1
                        if columnOrig < minWidth:
                            print('The minimum width of the image must be {} pixels, so that IV and padding can be stored in a single additional row!'.format(minWidth))
                            sys.exit()
                        # Conversion du donnée image en bit
                        imageOrigBytes = imageOrig.tobytes()
                        # Cryptage
                        self.key =  self.hashmotdepasse(self.password)
                        print(self.key)
                        iv = get_random_bytes(ivSize)
                        cipher =   AES.new(self.key, AES.MODE_ECB)
                        imageOrigBytesPadded = pad(imageOrigBytes, AES.block_size)
                        ciphertext = cipher.encrypt(imageOrigBytesPadded)
                        # Conversion des bits chiffrées en image données
                        paddedSize = len(imageOrigBytesPadded) - len(imageOrigBytes)
                        void = columnOrig * depthOrig - ivSize - paddedSize
                        ivCiphertextVoid = iv + ciphertext + bytes(void)
                        imageEncrypted = np.frombuffer(ivCiphertextVoid, dtype = imageOrig.dtype).reshape(rowOrig + 1, columnOrig, depthOrig)
                        # Sortie image cryptée
                        cv2.imshow("Image crypte", imageEncrypted)
                        cv2.imwrite(self.fichier + ".bmp", imageEncrypted)
                        cv2.waitKey()

                    elif(self.mode.get() == 6):
                        keySize = 32
                        ivSize = AES.block_size  
                        imageOrig = cv2.imread(self.fichier)
                        rowOrig, columnOrig, depthOrig = imageOrig.shape
                        minWidth = (AES.block_size + AES.block_size) // depthOrig + 1
                        if columnOrig < minWidth:
                            print('The minimum width of the image must be {} pixels, so that IV and padding can be stored in a single additional row!'.format(minWidth))
                            sys.exit()
                        # Conversion du donnée image en bit
                        imageOrigBytes = imageOrig.tobytes()
                        # Cryptage
                        self.key =  self.hashmotdepasse(self.password)
                        print(self.key)
                        iv = get_random_bytes(ivSize)
                        ctr = Counter.new(AES.block_size*8)
                        cipher =   AES.new(self.key, AES.MODE_CTR,counter=ctr)
                        imageOrigBytesPadded = pad(imageOrigBytes, AES.block_size)
                        ciphertext = cipher.encrypt(imageOrigBytesPadded)
                        # Conversion des bits chiffrées en image données
                        paddedSize = len(imageOrigBytesPadded) - len(imageOrigBytes)
                        void = columnOrig * depthOrig - ivSize - paddedSize
                        ivCiphertextVoid = iv + ciphertext + bytes(void)
                        imageEncrypted = np.frombuffer(ivCiphertextVoid, dtype = imageOrig.dtype).reshape(rowOrig + 1, columnOrig, depthOrig)
                        # Sortie image cryptée
                        cv2.imshow("Image crypte", imageEncrypted)
                        cv2.imwrite(self.fichier + ".bmp", imageEncrypted)
                        cv2.waitKey()
                    else:
                        messagebox.showinfo("Erreur", "Veuillez choisir un mode")
        #return self.crypte
                
        def decrypte(self):
            if self.barre1.get() == "Fichier à crypter ou à décrypter...":
                messagebox.showinfo("Erreur", "Veuillez selectionner le fichier")
            elif len(self.password.get()) == 0:
                messagebox.showinfo("Erreur", "Veuillez saisir le mot de passe")
            else:
                if not self.hashage.get():
                    messagebox.showinfo("Erreur", "Veuillez selectionner un fonction de hashage")
                else:
                    if(self.mode.get() == 1):
                        
                        keySize = 32
                        ivSize = AES.block_size  
                        imageEncrypted = cv2.imread(self.fichier)
                        #rowOrig, columnOrig, depthOrig = imageEncrypted.shape
                        self.key =  self.hashmotdepasse(self.password)
                        print(self.key)
                        aad = b'aadaad'
                        iv = get_random_bytes(ivSize)
                        
                        # Conversion du donnée image cryptée en bit cryptée
                        rowEncrypted, columnOrig, depthOrig = imageEncrypted.shape 
                        rowOrig = rowEncrypted - 1
                        encryptedBytes = imageEncrypted.tobytes()
                        iv = encryptedBytes[:ivSize]
                        imageOrigBytesSize = rowOrig * columnOrig * depthOrig
                        paddedSize = (imageOrigBytesSize // AES.block_size + 1) * AES.block_size - imageOrigBytesSize
                        encrypted = encryptedBytes[ivSize : ivSize + imageOrigBytesSize + paddedSize]
                         
                        # Decryptage
                        cipher = AES.new(self.key, AES.MODE_GCM, iv)
                        #cipher.update(aad)
                        #try:
                            #aut Tag
                        # encrypted = [encrypted,tag]
                        #encrypted, tag = encrypted
                        # tag = encrypted[-16:]
                        # print(tag)
                        ###decryptedImageBytesPadded  = cipher.decrypt_and_verify(encrypted,tag)
                        decryptedImageBytesPadded = cipher.decrypt(encrypted)
                        #tag_d = cipher.digest()  # Signal to the cipher that we are done and get the tag
                        #print("Tag decryption: "+ str(tag_d))
                        decryptedImageBytes = unpad(decryptedImageBytesPadded, AES.block_size)

                        #Conversion des bits en image donnée decryptée
                        decryptedImage = np.frombuffer(decryptedImageBytes, imageEncrypted.dtype).reshape(rowOrig, columnOrig, depthOrig)
                        # Sortie d'image decryptée
                        cv2.imshow("Image decrypte", decryptedImage)
                        cv2.imwrite(self.fichier, decryptedImage)
                        cv2.waitKey()
                        #except(ValueError,KeyError):
                            #messagebox.showinfo("Information","Mot de passe incorrect ou l'image n'est pas authentifié.")
                            #print("Error mot de passe.")
                
                    elif(self.mode.get() == 2):
                        try:
                            keySize = 32
                            ivSize = AES.block_size  
                            imageEncrypted = cv2.imread(self.fichier)
                            self.key =  self.hashmotdepasse(self.password)
                            print(self.key)
                            iv = get_random_bytes(ivSize)
                            
                            # Conversion du donnée image cryptée en bit cryptée
                            rowEncrypted, columnOrig, depthOrig = imageEncrypted.shape 
                            rowOrig = rowEncrypted - 1
                            encryptedBytes = imageEncrypted.tobytes()
                            iv = encryptedBytes[:ivSize]
                            imageOrigBytesSize = rowOrig * columnOrig * depthOrig
                            paddedSize = (imageOrigBytesSize // AES.block_size + 1) * AES.block_size - imageOrigBytesSize
                            encrypted = encryptedBytes[ivSize : ivSize + imageOrigBytesSize + paddedSize]

                            # Decryptage
                            cipher = AES.new(self.key, AES.MODE_CFB, iv)  
                            decryptedImageBytesPadded = cipher.decrypt(encrypted)
                            decryptedImageBytes = unpad(decryptedImageBytesPadded, AES.block_size)

                            #Conversion des bits en image donnée decryptée
                            decryptedImage = np.frombuffer(decryptedImageBytes, imageEncrypted.dtype).reshape(rowOrig, columnOrig, depthOrig)
                            # Sortie d'image decryptée
                            cv2.imshow("Image decrypte", decryptedImage)
                            cv2.imwrite(self.fichier, decryptedImage)
                            cv2.waitKey()
                        except(ValueError,KeyError):
                            messagebox.showinfo("Information","Mot de passe incorrect.")
                            print("Error mot de passe.")

                    elif(self.mode.get() == 3):
                 
                        try:
                            keySize = 32
                            ivSize = AES.block_size  
                            imageEncrypted = cv2.imread(self.fichier)
                            self.key =  self.hashmotdepasse(self.password)
                            print(self.key)
                            iv = get_random_bytes(ivSize)
                            
                            # Conversion du donnée image cryptée en bit cryptée
                            rowEncrypted, columnOrig, depthOrig = imageEncrypted.shape 
                            rowOrig = rowEncrypted - 1
                            encryptedBytes = imageEncrypted.tobytes()
                            iv = encryptedBytes[:ivSize]
                            imageOrigBytesSize = rowOrig * columnOrig * depthOrig
                            paddedSize = (imageOrigBytesSize // AES.block_size + 1) * AES.block_size - imageOrigBytesSize
                            encrypted = encryptedBytes[ivSize : ivSize + imageOrigBytesSize + paddedSize]

                            # Decryptage
                            cipher = AES.new(self.key, AES.MODE_OFB, iv)  
                            decryptedImageBytesPadded = cipher.decrypt(encrypted)
                            decryptedImageBytes = unpad(decryptedImageBytesPadded, AES.block_size)

                            #Conversion des bits en image donnée decryptée
                            decryptedImage = np.frombuffer(decryptedImageBytes, imageEncrypted.dtype).reshape(rowOrig, columnOrig, depthOrig)
                            # Sortie d'image decryptée
                            cv2.imshow("Image decrypte", decryptedImage)
                            cv2.imwrite(self.fichier, decryptedImage)
                            cv2.waitKey()
                        except(ValueError,KeyError):
                            messagebox.showinfo("Information","Mot de passe incorrect.")
                            print("Error mot de passe.")
                        
                    elif(self.mode.get() == 4):
                        try:
                            keySize = 32
                            ivSize = AES.block_size  
                            imageEncrypted = cv2.imread(self.fichier)
                            self.key =  self.hashmotdepasse(self.password)
                            print(self.key)
                            iv = get_random_bytes(ivSize)
                            
                            # Conversion du donnée image cryptée en bit cryptée
                            rowEncrypted, columnOrig, depthOrig = imageEncrypted.shape 
                            rowOrig = rowEncrypted - 1
                            encryptedBytes = imageEncrypted.tobytes()
                            iv = encryptedBytes[:ivSize]
                            imageOrigBytesSize = rowOrig * columnOrig * depthOrig
                            paddedSize = (imageOrigBytesSize // AES.block_size + 1) * AES.block_size - imageOrigBytesSize
                            encrypted = encryptedBytes[ivSize : ivSize + imageOrigBytesSize + paddedSize]

                            # Decryptage
                            cipher = AES.new(self.key, AES.MODE_CBC, iv)  
                            decryptedImageBytesPadded = cipher.decrypt(encrypted)
                            decryptedImageBytes = unpad(decryptedImageBytesPadded, AES.block_size)

                            #Conversion des bits en image donnée decryptée
                            decryptedImage = np.frombuffer(decryptedImageBytes, imageEncrypted.dtype).reshape(rowOrig, columnOrig, depthOrig)
                            # Sortie d'image decryptée
                            cv2.imshow("Image decrypte", decryptedImage)
                            cv2.imwrite(self.fichier, decryptedImage)
                            cv2.waitKey()
                        except(ValueError,KeyError):
                            messagebox.showinfo("Information","Mot de passe incorrect.")
                            print("Error mot de passe.")     
                    elif(self.mode.get() == 5):
                        try:
                            keySize = 32
                            ivSize = AES.block_size  
                            imageEncrypted = cv2.imread(self.fichier)
                            self.key =  self.hashmotdepasse(self.password)
                            print(self.key)
                            iv = get_random_bytes(ivSize)
                            
                            # Conversion du donnée image cryptée en bit cryptée
                            rowEncrypted, columnOrig, depthOrig = imageEncrypted.shape 
                            rowOrig = rowEncrypted - 1
                            encryptedBytes = imageEncrypted.tobytes()
                            iv = encryptedBytes[:ivSize]
                            imageOrigBytesSize = rowOrig * columnOrig * depthOrig
                            paddedSize = (imageOrigBytesSize // AES.block_size + 1) * AES.block_size - imageOrigBytesSize
                            encrypted = encryptedBytes[ivSize : ivSize + imageOrigBytesSize + paddedSize]

                            # Decryptage
                            cipher = AES.new(self.key, AES.MODE_ECB)  
                            decryptedImageBytesPadded = cipher.decrypt(encrypted)
                            decryptedImageBytes = unpad(decryptedImageBytesPadded, AES.block_size)

                            #Conversion des bits en image donnée decryptée
                            decryptedImage = np.frombuffer(decryptedImageBytes, imageEncrypted.dtype).reshape(rowOrig, columnOrig, depthOrig)
                            # Sortie d'image decryptée
                            cv2.imshow("Image decrypte", decryptedImage)
                            cv2.imwrite(self.fichier, decryptedImage)
                            cv2.waitKey()
                        except(ValueError,KeyError):
                            messagebox.showinfo("Information","Mot de passe incorrect.")
                            print("Error mot de passe.")   
                    elif(self.mode.get() == 6):
                        try:
                            keySize = 32
                            ivSize = AES.block_size  
                            imageEncrypted = cv2.imread(self.fichier)
                            self.key =  self.hashmotdepasse(self.password)
                            print(self.key)
                            iv = get_random_bytes(ivSize)
                            
                            # Conversion du donnée image cryptée en bit cryptée
                            rowEncrypted, columnOrig, depthOrig = imageEncrypted.shape 
                            rowOrig = rowEncrypted - 1
                            encryptedBytes = imageEncrypted.tobytes()
                            iv = encryptedBytes[:ivSize]
                            imageOrigBytesSize = rowOrig * columnOrig * depthOrig
                            paddedSize = (imageOrigBytesSize // AES.block_size + 1) * AES.block_size - imageOrigBytesSize
                            encrypted = encryptedBytes[ivSize : ivSize + imageOrigBytesSize + paddedSize]

                            # Decryptage
                            ctr = Counter.new(AES.block_size*8)
                            cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr) 
                            decryptedImageBytesPadded = cipher.decrypt(encrypted)
                            decryptedImageBytes = unpad(decryptedImageBytesPadded, AES.block_size)

                            #Conversion des bits en image donnée decryptée
                            decryptedImage = np.frombuffer(decryptedImageBytes, imageEncrypted.dtype).reshape(rowOrig, columnOrig, depthOrig)
                            # Sortie d'image decryptée
                            cv2.imshow("Image decrypte", decryptedImage)
                            cv2.imwrite(self.fichier, decryptedImage)
                            cv2.waitKey()
                        except(ValueError,KeyError):
                            messagebox.showinfo("Information","Mot de passe incorrect.")
                            print("Error mot de passe.")
                    else:
                        messagebox.showinfo("Erreur", "Veuillez choisir un mode")
        def reset(self):
            self.fichier_url.set("Fichier à crypter ou à décrypter...")
            self.hashage.set(3)
            self.mode.set(7)
            self.motdepasse.set("")
        def apropos(self):
            messagebox.showinfo(
                "A propos",
                """Il s'agit d'un logiciel pour securiser les données en utilisant la methode de cryptage AES""",)
        def aides(self):
            messagebox.showinfo(
                "Aides",
                """
1.Ouvrir l'application et cliquer sur le boutton Ouvrir pour selectionner un fichier.
2.Saisir le mot de passe et ne l'oublier pas lors du decryptage du fichier si non le fichier reste crypté pour toujours.
3.Choisir un fonction de hashage pour hasher le mot de passe.
4.Choisir un mode qui definir l'algorithme de cryptage et decryptage.
5.Clicker le boutton CRYPTE pour crypte le fichier.
6.Clicker le boutton DECRYPTE pour decrypte le fichier.
7.Clicker le boutton RESET pour reinitialiser le système.""",)
                     
    aes = AlgoAES(window)
    #demarrer=tk.Button(window,text='DEMARRER',font=('Times_New_Roman',10),command=tab2,width=10,bg="#f56e6e",fg="#ffffff",bd=2,relief=tk.FLAT)
    # demarrer = customtkinter.CTkButton(window, text="DEMARRER", width=90,
    #                                     compound="right", fg_color="#54a24a", hover_color="#71c466",
    #                                     command=tab2)
    # # demarrer=customtkinter.CTkButton(window, image=demarre_image, text="", width=10, height=10,
    # #                                     corner_radius=10, fg_color="#f0f0f0", hover_color="#f0f0f0", command=tab2)
    # #demarrer.pack()
    # demarrer.place(x = 266, y = 496)
  
tab2()     
window.mainloop()