import os
from tkinter import *
import tkinter.messagebox
from playsound import playsound
import cmath
import math
import copy
import sounddevice as sd
import numpy as np

uzorak = 32768  # uzorkovat cemo brzinom koja je stepen dvojke
prozor = 32768
korak = 16384
trajanje_prozora = prozor / uzorak
trajanje_uzorka = 1 / uzorak
prozorUzorci = [0 for _ in range(prozor)]

def tuner():
    def nadji_notu(ton):
        note = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
        i = int(np.round(np.log2(ton / 440) * 12))
        najbliza_nota = note[i % 12] + str(4 + (i + 9) // 12)
        najblizi_ton = 440 * 2 ** (i / 12)
        return najbliza_nota, najblizi_ton

    def fft(x):
        N = len(x)

        if N <= 1:
            return x

        par = fft(x[0::2])
        nepar = fft(x[1::2])
        faktor = [cmath.exp(-2j * math.pi * k / N) * nepar[k] for k in range(N // 2)]
        return [par[k] + faktor[k] for k in range(N // 2)] + [par[k] - faktor[k] for k in range(N // 2)]

    def callback(ulazniPodaci, frames, time, status):
        global prozorUzorci
        if any(ulazniPodaci):
            prozorUzorci = np.concatenate((prozorUzorci, ulazniPodaci[:, 0]))
            prozorUzorci = prozorUzorci[len(ulazniPodaci[:, 0]):]
            magnitude = fft(prozorUzorci)
            magnitude = magnitude[:int(len(magnitude) / 2)]

            magnitude_bez_hps = copy.deepcopy(magnitude)
            for i in range(2, 4, 1):
                hps_len = int(np.ceil(len(magnitude) / i))
                magnitude = [i1 * i2 for i1, i2 in zip(magnitude[:hps_len], magnitude_bez_hps[::i])]  # mnozi sa svakim i element

            for i in range(62 // (uzorak // prozor + 1)):
                magnitude[i] = 0  # utisa
                magnitude_bez_hps[i] = 0

            maksimalnaFrek = np.argmax(magnitude)
            najbliza_nota, najblizi_ton = nadji_notu(maksimalnaFrek)
            maksimalnaFrekBH = np.argmax(magnitude_bez_hps)
            najbliza_notaBH, najblizi_tonBH = nadji_notu(maksimalnaFrekBH)

            print(f"Najbliza nota bez HPS: {najbliza_notaBH} {maksimalnaFrek:.1f}/{najblizi_tonBH:.1f}")
            print(f"Najbliza nota sa HPS: {najbliza_nota} {maksimalnaFrek:.1f}/{najblizi_ton:.1f}")
        else:
            print('no input')

    try:
        with sd.InputStream(channels=1, callback=callback,
                            blocksize=korak,
                            samplerate=uzorak):
            while True:
                pass
    except Exception as e:
        print(str(e))




root = Tk()
root.title("Guitar Tuner")
root.geometry('550x650')
root.configure(background='#f7f6f2')

def prva():
    audio_file = os.path.dirname(__file__) + '\\6th_String_E_64kb.mp3'
    playsound(audio_file)

def druga():
    audio_file = os.path.dirname(__file__) + '\\5th_String_A_64kb.mp3'
    playsound(audio_file)

def treca():
    audio_file = os.path.dirname(__file__) + '\\4th_String_D_64kb.mp3'
    playsound(audio_file)

def cetvrta():
    audio_file = os.path.dirname(__file__) + '\\3rd_String_G_64kb.mp3'
    playsound(audio_file)

def peta():
    audio_file = os.path.dirname(__file__) + '\\2nd_String_B__64kb.mp3'
    playsound(audio_file)

def sesta():
    audio_file = os.path.dirname(__file__) + '\\1st_String_E_64kb.mp3'
    playsound(audio_file)

def klik():
    tkinter.messagebox.showinfo('Help','Guitar tuner je aplikacija koja se koristi kao pomoć pri namještanju tonova na vašoj gitari.\n'
                                       'Započnite rad aplikacije pritiskom na dugme Start, pri čemu će se pokrenuti osluškivanje vanjskih zvukova, čiji će se tonovi ispisivati u konzolnom dijelu aplikacije.\n' 
                                       'U aplikaciji je dat prikaz gitare sa tonovima koje bi trebale imati pojedine žice na vašoj gitari, testirajte za svaku dok vam se ne ispiše nota koja odovara žici koju testirate.')

helpButton = Button(root, text="Help", bg='#f7af14',command=klik,height=2, width=8)
helpButton.place(x=30,y=550)

startButton = Button(root, text="Start",bg='#abeb34',command=tuner, height=2, width=8)
startButton.place(x=450, y=550)

stopButton = Button(root, text="Stop and Exit", bg='red', command=root.destroy).place(x=443, y=595)

e2 = Button(root, text="E2", bg='red', command=prva,height=2, width=8)
e2.place(x=20,y=50)
a2 = Button(root, text="A2", bg='blue',command=druga,height=2, width=8)
a2.place(x=20,y=90)
d3 = Button(root, text="D3", bg='green',command=treca,height=2, width=8)
d3.place(x=20,y=130)
g3 = Button(root, text="G3", bg='cyan',command=cetvrta,height=2, width=8)
g3.place(x=20,y=170)
b3 = Button(root, text="B3", bg='magenta',command=peta,height=2, width=8)
b3.place(x=20,y=210)
e4 = Button(root, text="E4", bg='white',command=sesta,height=2, width=8)
e4.place(x=20,y=250)

canvas = Canvas(root, width=300, height=600, bg='#fad78c')
canvas.place(relx=.5, rely=.5, anchor=CENTER)
circle = canvas.create_oval(60,450,250,250,outline='black',fill='#bda45e', width=5)

line1 = canvas.create_line(70,0,70,600,width=6)
line2 = canvas.create_line(105,0,105,600,width=5)
line3 = canvas.create_line(140,0,140,600,width=4)
line4 = canvas.create_line(175,0,175,600,width=3)
line5 = canvas.create_line(210,0,210,600,width=2)
line6 = canvas.create_line(245,0,245,600,width=1)

nota1 = canvas.create_text(55,40, text="E2", fill='red' ,font=('Helvetica','13'))
nota2 = canvas.create_text(90,40, text="A2", fill='blue' ,font=('Helvetica','13'))
nota3 = canvas.create_text(125,40, text="D3", fill='green' ,font=('Helvetica','13'))
nota4 = canvas.create_text(160,40, text="G3", fill='cyan' ,font=('Helvetica','13'))
nota5 = canvas.create_text(195,40, text="B3", fill='magenta' ,font=('Helvetica','13'))
nota6 = canvas.create_text(230,40, text="E4", fill='white' ,font=('Helvetica','13'))

root.mainloop()