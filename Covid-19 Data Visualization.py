from tkinter import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import requests
import matplotlib.pyplot as plt

window=Tk()
frame = None
frame2=Frame(window, relief=GROOVE,border=5,bg="#01BFBF")
frame2.pack(side="left")

world_url="https://api.covid19api.com/world/total"
res=requests.get(world_url)
world_data=res.json()

info_title=Label(frame,text="Data of World",fg="white", bg="#01BFBF",font="Calibri 10 bold")
info_title.pack(anchor="e")
info = Label(frame,text=world_data, fg="white", bg="#01BFBF",font="Calibri 10 bold")
info.pack(anchor="e")


TotalConfirmed=world_data["TotalConfirmed"]


url="https://api.covid19api.com/countries"
response=requests.get(url)
json_ulkeler=response.json()

url2="https://api.covid19api.com/"

ulkeler_listesi=[]
for ulkeler in json_ulkeler:
    ulkeler_listesi.append(ulkeler["Country"])

ulkeler_listesi.sort()


def cizdir():
    global frame
    if not frame:
        frame = Frame(window,bg="#01BFBF")
        frame.pack(anchor="n")
    else:
        frame.destroy()
        frame = Frame(window,bg="#01BFBF")
        frame.pack(anchor="n")
    ulkesec=listBox1.curselection()
    ulke_ismi=listBox1.get(ulkesec)
    new_api=requests.get(url2+"total/dayone/country/"+ulke_ismi).json()

    dates = []
    for i in new_api:
        dates.append(i["Date"])



    verisec=listBox2.curselection()
    veri_ismi=listBox2.get(verisec)
    conf=[]
    death=[]
    reco=[]
    act=[]

    def grafik(tur):
        fig, ax = plt.subplots()
        ax.plot(dates,tur)
        plt.xticks(range(0, len(dates), 30))
        plt.xticks(rotation=7,fontsize="small")

        fig.set_facecolor("c")
        fig.gca().set_facecolor("black")
        fig.gca().grid(color="gray")
        fig.gca().set_xlabel("Days")
        #fig.gca().set_title(baslik)
        canvas = FigureCanvasTkAgg(figure=fig, master=frame)
        canvas.get_tk_widget().pack(anchor="e", fill="both", expand=True)
        navbar = NavigationToolbar2Tk(canvas=canvas, window=frame)


    if veri_ismi == "Confirmed":
        for i in new_api:
            conf.append(i["Confirmed"])
        grafik(conf)
    elif veri_ismi == "Deaths":
        for i in new_api:
            death.append(i["Deaths"])
        grafik(death)
    elif veri_ismi == "Recovered":
        for i in new_api:
            reco.append(i["Recovered"])
        grafik(reco)
    else:
        for i in new_api:
            act.append(i["Active"])
        grafik(act)
# pencere.state("zoomed")
window.title("Covid-19 Data Visualization")
window.configure(background="#01BFBF")

etiket1=Label(frame2,font="Calibri 12 bold",text="Country Selection",bg="#01BFBF",fg="white")
etiket1.pack(anchor="w")

listBox1 = Listbox(frame2, font="Calibri", selectmode="browse",bg="#01BFBF",exportselection=0)
listBox1.pack(anchor="w")
for i in ulkeler_listesi:
    listBox1.insert(END,i)

etiket2=Label(frame2,font="Calibri 12 bold",text="Data Selection",bg="#01BFBF",fg="white")
etiket2.pack(anchor="w")

listBox2 = Listbox(frame2, font="Calibri", selectmode="browse", bg="#01BFBF",exportselection=0)
listBox2.pack(anchor="w")

listBox2.insert(0,"Confirmed")
listBox2.insert(1,"Deaths")
listBox2.insert(2,"Recovered")
listBox2.insert(3,"Active")


buton=Button(frame2,font="Calibri 12 bold",text="Draw",fg="white",bg="#01BFBF",command=cizdir)
buton.pack(anchor="sw",ipadx=58,ipady=10)



mainloop()