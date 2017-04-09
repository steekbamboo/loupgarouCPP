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
from random import *
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

    def getchoixlistegarous(self):
        self.retour = self.listeloups.curselection()
        print("Vous voulez tuer " + self.victime[self.retour[0]])

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
            vivants = []
            nb_tours = 0 #T'as une idée de moyen de compter les tours ? En comptant le nb de votes, mais après comment ça se code ?
            if nb_tours == 0:
                nb_loups_depart = 0
                for role in liste:
                    if role == garou:
                        nb_loups_depart += 1
            
            for erg in list(liste.keys()):
                if liste[erg] != 'mort':
                    vivants.append(erg)
            if roleperso == 'mort':
                messagemort = Label(self.welcome, text="Vous êtes mort ! Vous avez accès aux informations de base (qui meurt, quelle heure il est...) mais vous ne pouvez pas participer aux votes ni aux débats.")
                messagemort.pack()

            else:
                
                if moment == 'start':
                    
                    messagewait = Label(self.welcome, text="Le jeu vient de commencer. Une fois tout le monde prêt, la nuit commencera !")
                    messagewait.pack()
                    
                if moment == 'garous':
                    
                    print("Les loups-garous se réveillent et choisissent une victime à dévorer...")
                    
                    if roleperso == 'garou':
                        i = 0
                        self.victime = []
                        messagechoixloups = Label(self.welcome, text="Voici les personnages qui ne sont pas des loups-garous.")
                        messagechoixloups.pack()
                        self.listeloups = Listbox(self.welcome)
                        for erg in list(liste.keys()):
                            if liste[erg] != 'garou':
                                self.victime.append(erg)
                                i += 1
                                self.listeloups.insert(END, (str(i) + " : " + erg))
                        self.listeloups.pack()
                        Label(text="Qui voulez vous tuer ?").pack()
                        Button(text="Voter", command=self.getchoixlistegarous).pack()

                    elif roleperso == 'fille':
                        garous = []
                        for erg in list(liste.keys()):
                            if liste[erg] == 'garou':
                                garous.append(erg)
                        print("Voulez-vous observer discrètement les loups-garous ? Répondez 1 pour oui")
                        answ = input(">>>") #Interface graphique plz
                        try:
                            if int(answ) == 1:
                                ok = 0
                                while ok = 0: # Boucle pour que la fille voie le meme loup maximum 3 fois
                                # /!\ Je n'ai pas encore prévu le cas où la petite fille a déjà vu tous les loups 3 fois    
                                    joueur = garous[randrange(len(garous))]
                                    dejavu = 0
                                    dejavus = []
                                    for a in dejavus.txt: #Probablement pas la bonne syntaxe là non plus
                                        joueur_djv = a.split('\n')
                                        dejavus.append(joueur_djv)
                                    for djv in dejavus:
                                        if djv == joueur:
                                            dejavu += 1
                                    if dejavu <= 2:
                                        ok = 1
                                self.envoi('submit',joueur+'\n','dejavus.txt') #Pas sur d'avoir bien compris la syntaxe de cette fonction
                                tmp = 0
                                joueurcrypt = ''
                                for lettre in joueur:
                                    if tmp % 3 == dejavu or tmp % 3 == dejavu - 1 or tmp % 3 == dejavu - 2 :
                                        joueurcrypt = joueurcrypt + lettre
                                    else:
                                        joueurcrypt = joueurcrypt + '*'
                                    tmp += 1
                                print('Vous semblez distinguer...',joueurcrypt,'...')
                                risque = len(dejavus) / (4 * nb_loups_depart)
                                if random() < risque:
                                    fillevue += 1 # Il faut stocker cette variable quelque part sur le serveur
                                    if fillevue == 1:
                                        print("Les loups garous commencent à se sentir observés...")
                                    if fillevue == 2:
                                        print("Les loups garous commencent à retrouver votre piste...")
                                    if fillevue == 3:
                                        print("Les loups garous vous ont identifiée, attendez-vous au pire...")
                                else:
                                    print('Vos chances de vous faire repérer ont augmenté...')
                    
                if moment == 'cupidon':
                    
                    print("Cupidon se réveille et choisit deux personnes à lier par l'amour...")
                    
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
                                    self.envoi('submit',amoureux+'\n'+amoureuse,'amour.txt')
                                    print("Par vos flèches et par l'amour, vous avez lié", vivants[
                                          amoureux], 'et', vivants[amoureuse], "pour la vie, jusqu'à la mort.")
                                    break
                                except:
                                    print("Saisie invalide. Veuillez recommencer l'opération.")
                                    self.menu()
                
                if moment == 'voyante':
                    
                    print("La voyante se réveille et choisit la personne dont elle veut découvrir la véritable identité...")
                    if roleperso == voyante :
                        for i in range(len(vivants)):
                            print(i + 1,'-',vivants[i])
                        print('Qui choisissez-vous ?')
                        choix = input('>>>')
                        print(vivants[choix - 1],'est',liste[choix - 1])
                
            self.welcome.mainloop()


Client()
