#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# Je ne suis pas un capitaliste,
# alors j'ai laissé le code source visible
# Entierement.
# Ce qui signifie que vous pouvez voir le programme
# Et, en réfléchissant un peu, trouver les roles de tout le monde.
#
# Cela ne sert à rien, à par tuer le jeu.
#
# Vous êtes libres, mais est-ce que ça en vaut vraiment la peine ?
#
#
#
#
# Bon jeu !
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

import urllib.request
import ftplib
from tkinter import *
connect = 0


class Client():
    def __init__(self):
        self.menu()

    def recupererliste(self, quoi):  # mdp = users
        text = urllib.request.urlopen('http://baruch.hol.es/loup/' + quoi + '.txt')
        data = text.read()
        data = data.decode().split('\n')
        donnees = {}
        for a in data:
            tuplesep = a.split(" = ")
            donnees[tuplesep[0]] = tuplesep[1]
        return donnees

    def envoi(self, ou, quoi, nom):
        fichier = open(nom, 'w')
        fichier.write(quoi)
        fichier.close()
        ftp = ftplib.FTP('ftp.baruch.hol.es')
        ftp.login('u956207787', 'ftploup')
        ftp.cwd(ou)
        ftp.storlines("STOR " + nom, open(nom, 'rb'))

    def creercompte(self):
        self.welcome.destroy()
        self.welcome.quit()
        entreecreation = self.doublechamp("Bonjour ! Choisissez vos identifiants. \n Attention : n'utilisez que les caractères de A à Z. \n Les mots de passe sont stockés sur un serveur non protegé : \n n'utilisez pas un mot de passe important.", "Valider")
        user = entreecreation[0]
        mdpasse = entreecreation[1]
        self.envoi('submit', user + " = " + mdpasse, user + ".txt")
        print("vous avez bien été inscrit")
        self.menu()

    def validationdoublechamp(self):
        self.entreeuser = self.entreeuser.get()
        self.entreemdp = self.entreemdp.get()
        self.fenetre.destroy()
        self.fenetre.quit()

    def doublechamp(self, message, validation):
        self.fenetre = Tk()
        plop = Label(self.fenetre, text=message)
        plop.pack()
        self.entreeuser = StringVar()
        self.entreemdp = StringVar()
        self.dialoguser = Entry(self.fenetre, textvariable=self.entreeuser, width=15)
        self.dialogmdp = Entry(self.fenetre, textvariable=self.entreemdp, width=15, show='*')
        self.dialoguser.pack()
        self.dialogmdp.pack()
        self.confirmation = Button(self.fenetre, text=validation, command=self.validationdoublechamp)
        self.confirmation.pack()
        self.fenetre.mainloop()
        return(self.entreeuser, self.entreemdp)

    def connection(self):
        self.welcome.destroy()
        self.welcome.quit()
        entreeconnection = self.doublechamp("Bonjour, veuillez vous connecter !", "Se connecter")
        mdpasse = entreeconnection[1]
        self.utilisateur = entreeconnection[0]
        liste = self.recupererliste('users')
        try:
            vrai = liste[self.utilisateur]
            if mdpasse == vrai:
                global connect
                connect = 1
                self.menu()
            else:
                raise KeyError
        except(KeyError):
            print("Mot de passe ou identifiant inconnus - votre compte n'est peut etre pas encore validé")
            self.menu()

    def etat(self):
        print(connect)
        self.menu()

    def menu(self):
        if connect == 0:
            self.welcome = Tk()
            self.welcome.title("Menu")
            messageplop = Label(self.welcome, text="Bonjour, et bienvenue sur le Loup-Garou du CPP ! \n Vous pouvez vous connecter, ou \n vous inscrire à la prochaine partie. \n \n")
            messageplop.pack()
            boutoncreation = Button(self.welcome, text="S'inscrire à la prochaine partie", command=self.creercompte)
            boutonconnection = Button(self.welcome, text="Se connecter", command=self.connection)
            boutoncreation.pack()
            boutonconnection.pack()
            credits = Label(text=" \n \n Un jeu crée par Loic Faucher et Baruch Byrdin. \n Nous sommes ouverts à vos suggestions !")
            credits.pack()
            self.welcome.mainloop()
        else:
            self.welcome = Tk()
            self.welcome.title("Menu")
            messageplopun = Label(self.welcome, text="Bienvenue " + self.utilisateur + " !")
            liste = self.recupererliste('roles')
            roleperso = liste[self.utilisateur]
            messageplopdeux = Label(self.welcome, text="Vous êtes " + roleperso)
            messageplopun.pack()
            messageplopdeux.pack()
            listedeux = self.recupererliste('time')
            moment = listedeux['time']
            moment = 'garous'
            vivants = []

            for erg in list(liste.keys()):
                if liste[erg] != 'mort':
                    vivants.append(erg)
            if roleperso == 'mort':
                print("Vous êtes mort ! Vous avez accès aux informations de base (qui meurt, quelle heure il est...) mais vous ne pouvez pas participer aux votes ni aux débats.")
            else:
                if moment == 'start':
                    print("Le jeu vient de commencer. Une fois tout le monde prêt, la nuit commencera !")
                if moment == 'garous':
                    if roleperso == 'garou':
                        i = 0
                        victime = []
                        print("Voici les personnages qui ne sont pas garous")
                        for erg in list(liste.keys()):
                            if liste[erg] != 'garou':
                                victime.append(erg)
                                i += 1
                                print(str(i) + " : " + erg)
                        print("Qui tuez vous ?")
                        tuer = input(">>>")
                        try:
                            print("Vous voulez tuer " + victime[int(tuer) - 1])
                        except:
                            print("Saisie invalide. Veuillez recommencer l'opération.")
                            self.menu()
                    elif roleperso == 'fille':
                        garous = []
                        for erg in list(liste.keys()):
                            if liste[erg] == 'garou':
                                garous.append(erg)
                        print("Voici les personnes que vous semblez distinguer :")
                        for joueur in garous:
                            tmp = 0
                            joueurcrypt = ''
                            for lettre in joueur:
                                if tmp % 3 == 0:
                                    joueurcrypt = joueurcrypt + lettre
                                else:
                                    joueurcrypt = joueurcrypt + '*'
                                tmp += 1
                            print('...', joueurcrypt, '...')
                    else:
                        print("C'est la nuit, vous dormez !")
                if moment == 'cupidon':
                    if roleperso == 'cupidon':
                        print('Voici la liste des personnes en vie.')
                        i = 0
                        for i in range(len(vivants)):
                            print(i + 1, '-', vivants[i])
                        print("Choisissez la première personne à rendre amoureuse")
                        amoureux = int(input(">>>")) - 1
                        while True:
                            print("Choisissez de qui", vivants[amoureux], "sera amoureux")
                            amoureuse = int(input('>>>')) - 1
                            if amoureuse == amoureux:
                                print('Saisie erronnée : vous devez choisir une personne différente de',
                                      vivants[amoureux])
                            else:
                                try:
                                    print("Par vos flèches et par l'amour, vous avez lié", vivants[
                                          amoureux], 'et', vivants[amoureuse], "pour la vie, jusqu'à la mort.")
                                    break
                                except:
                                    print("Saisie invalide. Veuillez recommencer l'opération.")
                                    self.menu()
                    else:
                        print("C'est la nuit, vous dormez !")
            
            self.welcome.mainloop()


Client()
