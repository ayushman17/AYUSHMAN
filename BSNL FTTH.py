import tkinter
from tkinter import TOP, BOTTOM, HORIZONTAL, END
from tkinter import messagebox, ttk, PhotoImage
from requests import post, get, exceptions
from re import findall
from functools import wraps
from threading import Thread
from webbrowser import open as openlink
import os
import tempfile
import base64
import atexit
#thisisimportfiles
__author__ = "Ayushman Singh Chauhan"
__version__ = "1.0.0"

#this is themain code
class main(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(f"BSNL FTTH v{__version__}")
        self.geometry("650x420")
        self.resizable(False, False)
        nameoficon = self.makeicon()
        self.iconbitmap(nameoficon.name)
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar",
                    foreground='red', background='red')
        self.bind("<Escape>", lambda e: e.widget.quit())
        self.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(nameoficon))

    def makeicon(self):
        iconhexdata = b'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'

        with tempfile.NamedTemporaryFile(delete=False) as iconfile:
            iconfile.write(base64.b64decode(iconhexdata))

        return iconfile

    def on_closing(self, iconfile):
        try:
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.destroy()
                os.remove(iconfile.name)
        except Exception:
            pass


class frameTOP(tkinter.Frame,):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(side=TOP)


class INFObox(tkinter.Toplevel):
    def __init__(self,):
        super().__init__(root)
        self.title(f"Credits")
        # self.geometry("365x400")
        self.resizable(False, False)
        self.widget()

    def widget(self):
        tkinter.Label(self, text="Ayushman Singh Chauhan :)", font=(
            "TkDefaultFont", 15)).grid(row=0, column=0, columnspan=2, padx=10, pady=(25, 5))

        tkinter.Button(self, text=f'Play Store', height="2", width="10", command=lambda: openlink(
            "https://play.google.com/store/apps/dev?id=6829475143276494298")).grid(row=1, column=0, columnspan=2, padx=30, pady=30)

        tkinter.Label(self, text="Ayushman Singh Chauhan (Owner)", font=("TkDefaultFont", 15)).grid(
            row=2, column=0, columnspan=2, padx=10, pady=(25, 5))
        tkinter.Label(self, text="ascb508@gmail.com", font=("TkDefaultFont", 10)).grid(
            row=3, column=0, columnspan=2, padx=10, pady=(5, 15))

        tkinter.Button(self, text=f'Github', height="2", width="10", command=lambda: openlink(
            "https://github.com/ayushman17")).grid(row=4, column=0, padx=30, pady=30)
        tkinter.Button(self, text=f'Website', height="2", width="10", command=lambda: openlink(
            "https://github.com/ayushman17/ayushman17")).grid(row=4, column=1, padx=30, pady=30)


class frameBOTTOM(tkinter.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(side=BOTTOM)

        self.processtest = tkinter.StringVar()

        self.isupdateaviable = tkinter.StringVar()
        self.isupdateaviable.set(f"<--- Click For Updates")

        self.widget()

        Thread(target=self.refresh).start()

    def SoftwareUpdate(self):
        ver = self._http("get", "https://raw.githubusercontent.com/MayankFawkes/BSNL_FTTH/master/"
                         "latest.json?flush_cache=True")
        if ver["latest"] == __version__:
            self.isupdateaviable.set("Update Not Available")
        else:
            openlink(ver["download"])
            self.isupdateaviable.set(f'Latest v{ver["latest"]} Available')

    def _http(self, type, url):
        types = {"get": get, "post": post}
        try:
            return types[type](url).json()
        except exceptions.ConnectionError:
            messagebox.showerror("Connection", "Internet not connected")

    def fetch(self):
        r = self._http(
            "post", "https://redirect2.bbportal.bsnl.co.in/portal/fetchUserQuotaPM.do")
        data = dict()
        print(r)
        data["status"] = r["resultCode"]
        data["msg"] = r["msg"]
        data["row"] = [{}]
        if "records" in r.keys():
            data["records"] = r["records"]
            for n in r["rows"]:
                if n["serviceType"] == "BASE":
                    data["row"][0]["today"] = n["dailyTotalUsage"]
                    data["row"][0]["totalUsed"] = n["totalUsage"]
                    data["row"][0]["serviceName"] = n["serviceName"]
                    tup = findall(
                        r"U-([0-9]+)G-([0-9]+)Mbps-R-([0-9]+)Mbps", n["serviceName"])[0]
                    for k, l, m in zip(tup, ["total", "speed", "afterspeed"], ["GB", "MBPS", "MBPS"]):
                        data["row"][0][l] = f"{k} {m}"
            return data
        return data

    def convert(self, val, type):
        if type == "GB":
            return float(val)
        return float(val)/1024.0

    def refresh(self):
        data = self.fetch()
        print(data)
        avia = True
        values = {
            "today": self.Today,
            "totalUsed": self.TotalUsed,
            "serviceName": self.Service,
            "total": self.Total,
            "speed": self.Speed,
            "afterspeed": self.FUP
        }

        if data["status"] is not 200:
            messagebox.showerror("Error", str(data["msg"]))
            avia = False

        if "records" in data.keys():
            if data["records"] < 1:
                messagebox.showerror("Error", str("No records found"))
                avia = False
        if avia:
            for n, m in data["row"][0].items():
                self.updateEntry(values[n], m)

            usedtillnow, typeU = findall(
                '([0-9]+.?[0-9]*) ([A-Z]{2})', data["row"][0]["totalUsed"])[0]
            totalwehave, typeT = findall(
                '([0-9]+.?[0-9]*) ([A-Z]{2})', data["row"][0]["total"])[0]

            usedtillnow = self.convert(usedtillnow, typeU)
            totalwehave = self.convert(totalwehave, typeT)

            print(usedtillnow, totalwehave)

            percentage = (usedtillnow * 100)/totalwehave

            percentage = float(f"{percentage:.3f}")
            self.progress['value'] = percentage
            self.update_idletasks()
            self.processtest.set(
                f'{percentage}% USED   {totalwehave-usedtillnow}GBs LEFT')

    def updateEntry(self, obj, s):
        obj["state"] = "normal"
        obj.delete(0, END)
        obj.insert(0, s)
        obj["state"] = "disable"

    def widget(self):
        self.progress = ttk.Progressbar(
            self, orient=HORIZONTAL, style="red.Horizontal.TProgressbar", length=400, mode='determinate')
        self.progress.grid(row=0, column=0, columnspan=4,
                           padx=10, pady=(25, 2))

        tkinter.Label(self, textvariable=self.processtest).grid(
            row=1, column=0, columnspan=4, padx=10, pady=(2, 25))
        labels = ["Today", "Total Used", "Service Name",
                  "Total GBs", "Speed", "FUP Speed"]

        c = 0

        for n in range(2, int(len(labels)/2)+2):
            for m in [0, 2]:
                tkinter.Label(self, text=labels[c]).grid(
                    row=n, column=m, padx=10, pady=10)
                c += 1

        self.Today = tkinter.Entry(
            self, state="disable", disabledforeground="black")
        self.Today.grid(row=2, column=1, padx=10, pady=10)

        self.TotalUsed = tkinter.Entry(
            self, state="disable", disabledforeground="black")
        self.TotalUsed.grid(row=2, column=3, padx=10, pady=10)

        self.Service = tkinter.Entry(
            self, state="disable", disabledforeground="black")
        self.Service.grid(row=3, column=1, padx=10, pady=10)

        self.Total = tkinter.Entry(
            self, state="disable", disabledforeground="black")
        self.Total.grid(row=3, column=3, padx=10, pady=10)

        self.Speed = tkinter.Entry(
            self, state="disable", disabledforeground="black")
        self.Speed.grid(row=4, column=1, padx=10, pady=10)

        self.FUP = tkinter.Entry(
            self, state="disable", disabledforeground="black")
        self.FUP.grid(row=4, column=3, padx=10, pady=10)

        tkinter.Button(self, text="REFRESH", height=2, width=10, command=lambda: Thread(
            target=self.refresh).start()).grid(row=5, column=0, padx=10, pady=20)

        tkinter.Button(self, text="INFO", height=2, width=10,
                       command=INFObox).grid(row=5, column=1, padx=10, pady=20)

        tkinter.Button(self, text="UPDATE", height=2, width=10, command=lambda: Thread(
            target=self.SoftwareUpdate).start()).grid(row=5, column=2, padx=10, pady=20)

        tkinter.Label(self, textvariable=self.isupdateaviable).grid(
            row=5, column=3, padx=10, pady=20)


class reglabel(tkinter.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid(row=0, column=0, columnspan=2, padx=10, pady=(15, 5))
        self.config(font=("TkDefaultFont", 25))


class reglabel1(tkinter.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid(row=1, column=0, columnspan=2, pady=(5, 10))
        self.config(font=("TkDefaultFont", 12))


if __name__ == '__main__':
    root = main()
    FrameOnTop = frameTOP(root)

    reglabel(FrameOnTop, text="My BSNL FTTH Data Usage")
    reglabel1(FrameOnTop, text="- By Ayushman Singh Chauhan")

    FrameOnBOTTOM = frameBOTTOM(root)

    root.mainloop()
