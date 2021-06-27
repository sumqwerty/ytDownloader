import tkinter as tk
from tkinter import ttk
from scrollFrame import *
import tkinter.font as tkFont
from tkinter import messagebox
from pytube import YouTube
from pytube import Playlist


class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.fntStyle = tkFont.Font(size=12)
        self.geometry('940x540')
        self.anchr = "nw"
        self.resizable(False, False)
        self.title("ytPlaylistDw")
        # self.testScroll()
        self.urlGetter()

    def testScroll(self):
        tk.Entry(self.main_area, width=10, bd=4).pack(side=tk.LEFT, padx=10, pady=5, anchor=self.anchr)
        tk.Entry(self.main_area, width=10, bd=4).pack(side=tk.LEFT, padx=10, pady=5, anchor=self.anchr)
        tk.Entry(self.main_area, width=10, bd=4).pack(padx=10, pady=5, anchor=self.anchr)
        tk.Entry(self.main_area, width=10, bd=4).pack(side=tk.BOTTOM, padx=10, pady=5, anchor=self.anchr)
    
    
    def loaderText(self,cnt,txt):
        # loading text font 
        fnt = self.fntStyle.copy()
        fnt.configure(size=11)
        
        # Loading... and number of videos loaded text
        loading_message = tk.Label(cnt, font=fnt, text=txt)
        #loading_message.pack(anchor=self.anchr, padx=10)
        
        return loading_message
    
    
    
    def download_all_av(self, allVids):
        numOfVids = 0
        dwnlMessage = self.loaderText(self,"Downloading... "+"("+str(numOfVids)+"/"+str(len(allVids))+" Donwloaded)")
        dwnlMessage.place(x=550, y=45, anchor=self.anchr)
        for vid in allVids:
            self.update_idletasks()
            vid["audioVideo"].filter(resolution=max([stream.resolution for stream in vid["audioVideo"]]))[0].download()
            numOfVids += 1
            dwnlMessage.config(text="Downloading... "+"("+str(numOfVids)+"/"+str(len(allVids))+" Donwloaded)")
        
        dwnlMessage.destroy()
        
    def download_all_a(self, allVids):
        numOfVids = 0
        dwnlMessage = self.loaderText(self,"Downloading... "+"("+str(numOfVids)+"/"+str(len(allVids))+" Donwloaded)")
        dwnlMessage.place(x=550, y=45, anchor=self.anchr)        
        for vid in allVids:
            self.update_idletasks()
            vid["audio"][-1].download()
            numOfVids += 1
            dwnlMessage.config(text="Downloading... "+"("+str(numOfVids)+"/"+str(len(allVids))+" Donwloaded)")
        
        dwnlMessage.destroy()            
            
            
    def listVideos(self, pList):
        #print("hi")
        #pList = Playlist(plUrl) # playlist Object
        allVids = [] # all videos
        
        # frame to place progress bar
        progressBarContainer = tk.Frame(self,width=self.winfo_width())
        progressBarContainer.place(x=0,y=78)
        
        # loading text font 
        fnt = self.fntStyle.copy()
        fnt.configure(size=11)
        
        # Loading... and number of videos loaded text
        numOfVids = 0
        loading_message = self.loaderText(progressBarContainer,"Loading... "+str(numOfVids)+"/"+str(len(pList)))
        #loading_message = tk.Label(progressBarContainer, font=fnt, text=)
        loading_message.pack(anchor=self.anchr, padx=10)
        
        
        # progress bar
        lg = progressBarContainer.winfo_reqwidth()
        progress = ttk.Progressbar(progressBarContainer, orient=tk.HORIZONTAL, length=lg, mode='determinate')
        progress.pack()
        
        
        
        
        x = 0
        interval = 100/len(pList)
        for vid in pList:
            x += interval
            self.update_idletasks()
            progress['value'] = x
            temp = {}
            temp["title"] = vid.title
            temp["audio"] = vid.streams.filter(only_audio=True)
            temp["audioVideo"] = vid.streams.filter(progressive=True)
            allVids.append(temp)
            numOfVids += 1
            loading_message.config(text="Loading... "+str(numOfVids)+"/"+str(len(pList)))
            
        
        progress.pack_forget()
        loading_message.pack_forget()
        progressBarContainer.pack_forget()
        
        # container for showing the videos in the playlist
        yOff = 100
        videoContainer = ScrollableFrame(self, width=self.winfo_width()-25, height=self.winfo_height()-yOff-5, innerbdThickness=4, innerbdColor="green")
        videoContainer.place(x=0,y=yOff-20)
        
        tk.Button(self, text="donwload all audio video", command=lambda: self.download_all_av(allVids)).place(x=10, y=40, anchor=self.anchr)
        tk.Button(self, text="donwload all audio only", command=lambda: self.download_all_a(allVids)).place(x=250, y=40, anchor=self.anchr)
        
        for i in range(len(allVids)):
            vid = allVids[i]
            frm = tk.Frame(videoContainer.frame)
            frm.pack(anchor=self.anchr,padx=10, pady=10)
            tk.Label(frm,text=str(i+1)+". "+vid["title"]).grid(row=0, column=0,padx=5)
            tk.Button(frm,text="donwload audio video", command=lambda vi=vid: self.download_all_av([vi])).grid(row=0, column=1,padx=5)
            tk.Button(frm,text="donwload audio only", command=lambda ad=vid: self.download_all_a([ad])).grid(row=0, column=2,padx=5)
            
            
            
    
    def chkLink(self, url):
        try:
            pList = Playlist(url)
            self.listVideos(pList.videos)
            
        except Exception as e:
            self.listVideos([YouTube(url)])
    
    def urlGetter(self):
        fnt = self.fntStyle.copy()
        fnt.configure(size=11)
        yOff = 6
        getButton = tk.Button(self, text="Get",command=lambda: self.chkLink(self.url.get()), width=10)
        getButton.pack(side=tk.RIGHT, padx=12, pady=yOff,anchor=self.anchr)
        
        
        self.url = tk.Entry(self, width=80, bd=4)
        self.url.pack(side=tk.RIGHT, pady=yOff,anchor=self.anchr)
        #self.url.insert(0, "https://www.youtube.com/playlist?list=PL437A0B80F0F8301A")
        self.url.insert(0, "https://www.youtube.com/playlist?list=PLxFt1oL-gcoeHvNKiNlWqUPKA_JByY9nX")
        urlLabel = tk.Label(self,text="Video/Playlist URL: ",font=fnt)
        urlLabel.pack(padx=4, pady=yOff, anchor=self.anchr)
        


mw = MainWindow()
mw.mainloop()
