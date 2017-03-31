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
connect = 0


def recupererliste(quoi):  # mdp = users
    text = urllib.request.urlopen('http://baruch.hol.es/loup/' + quoi + '.txt')
    data = text.read()
    data = data.decode().split('\n')
    donnees = {}
    for a in data:
        tuplesep = a.split(" = ")
        donnees[tuplesep[0]] = tuplesep[1]
    return donnees


def envoi(ou, quoi, nom):
    fichier = open(nom, 'w')
    fichier.write(quoi)
    fichier.close()
    ftp = ftplib.FTP('ftp.baruch.hol.es')
    ftp.login('u956207787', 'ftploup')
    ftp.cwd(ou)
    ftp.storlines("STOR " + nom, open(nom, 'rb'))


def creercompte():
    user = input("votre nom ? (a-z uniquement) \n")
    mdpasse = input("mdp ? (a-z uniquement) \n")
    envoi('submit', user + " = " + mdpasse, user + ".txt")
    print("vous avez bien été inscrit")
    menu()


def connection():
    global utilisateur
    utilisateur = input("votre nom ? \n")
    mdpasse = input("mdp ? \n")
    liste = recupererliste('users')
    try:
        vrai = liste[utilisateur]
        if mdpasse == vrai:
            print("bonjour")
            global connect
            connect = 1
            menu()
        else:
            raise KeyError
    except(KeyError):
        print("Mot de passe ou identifiant inconnus - votre compte n'est peut etre pas encore validé")
        menu()


def etat():
    print(connect)
    menu()


def menu():
    if connect == 0:
        print("1 creer compte / 2 se connecter")
        choix = input("choix ? \n")
        creercompte() if choix == '1' else connection() if choix == '2' else menu()
    else:
        print("Bienvenue " + utilisateur + " !")
        liste = recupererliste('roles')
        roleperso = liste[utilisateur]
        print("Vous êtes " + roleperso)
        listedeux = recupererliste('time')
        moment = listedeux['time']
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
                print("Vous voulez tuer " + victime[int(tuer) - 1])

            else:
                print("C'est la nuit, vous dormez !")


menu()
