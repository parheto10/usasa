from twilio.rest import Client
import random
from tkinter import *
from tkinter import messagebox

class Number_verify(Tk):
    def __init__(self):
        super(Number_verify, self).__init__()
        self.geometry("600x550")
        self.resizable(False, False)
        self.n = random.randint(1000, 9999)
        self.client = Client("AC7538f3cd9e32c282bfe2794c300d3a1b", "a203471476d1f63807e60883fee01140")
        self.client.messages.create(
            to=["+33756227336"],
            from_="33756227336",
            body = self.n
        )

    def Labels(self):
        self.c = Canvas(self, bg ='white', width=400, height=280)
        self.c.place(x=100, y=60)

        self.Login_Title = Label(self, text="VERIFICATION SMS", font="bold, 20", bg="white")
        self.Login_Title.place(x=210, y=90)

    def Entry(self):
        self.Username = Text(self, borderwidth=2, wrap="word", width=29, height=2)
        self.Username.place(x=190, y=160)

    def Buttons(self):
        self.submitButtonImage = PhotoImage(file="push.png")
        self.submitButton = Button(self, image=self.submitButtonImage, command=self.checkOTP, border=0)
        self.submitButton.place(x=208, y=240)

        self.resendOPTImage = PhotoImage(file="reset.png")
        self.resendOPT = Button(self, image=self.resendOPTImage, command=self.resendOPT, border=0)
        self.resendOPT.place(x=208, y=400)

    def checkOTP(self):
        try:
            self.userInput = int(self.Username.get(1.0, "end-1c"))
            if self.userInput == self.n:
                messagebox.showinfo("showinfo", 'Connexion Succes, Bienvenus!')
                self.n = "done"
            elif self.n =="done":
                messagebox.showinfo("showinfo", 'Code déja Utiliser !!')
            else:
                messagebox.showinfo("showinfo", 'Erreur Code, Verifier !!!')
        except:
            messagebox.showinfo("showinfo", 'Code Invalide !!!')


    def resendOPT(self):
        self.n = random.randint(1000, 9999)
        self.client = Client("AC7538f3cd9e32c282bfe2794c300d3a1b", "a203471476d1f63807e60883fee01140")
        self.client.messages.create(
            to=["+225-4-856-6846"],
            from_="+225-4-856-6846",
            body=self.n
        )

if __name__=="__main__":
    window = Number_verify()
    window.Labels()
    window.Entry()
    window.Buttons()
    window.mainloop()