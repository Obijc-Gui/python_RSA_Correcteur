from random import randint,choice
from math import sqrt
import numpy as np

#Enoncé : "La première partie se concentre sur le chiffrage et le déchiffrage d’informations avec un système de clé publique et clé privée. Concernant cette partie, vous aurez un certain nombre de fonctions Python à réaliser pour mettre en œuvre le chiffrage et le déchiffrage d’un message."

#Une fonction list_prime(n) qui renvoie l’ensemble des nombres premiers inférieurs ou égaux à n.


def estPremier(p): #vérifie si p est premier
    for i in range(2,int(sqrt(p))+1):
        if p%i == 0 :
            return False
    return True

def list_prime(n):
  tab = []
  for i in range(2,n+1):
    if estPremier(i):
      tab.append(i)
  return tab

def divEuclidienne(a,b):
  return (a//b, a%b)

#Une fonction extended_gcd(a,b) qui prend en entrée 2 entiers a et b et qui retourne trois entiers d, u, v tels que au + bv = d.

def extended_gcd(a,b):
    u0, u1 = 1, 0
    v0, v1 = 0, 1
    q,r = divEuclidienne(a,b)
    if r == 0 :
        return b, u1, v1
    while r!=0:
        q,r = divEuclidienne(a,b)
        if r == 0 :
            return b, u1, v1
        a, b = b, r
        u2 = u0 - q * u1
        v2 = v0 - q * v1
        u0 = u1
        v0 = v1
        u1 = u2
        v1 = v2

'''
Il existe aussi une manière plus compacte, mais moins compréhensible :
    r, u, v = a, 1, 0
    rp, up, vp = b, 0, 1
    while rp != 0:
        q = r//rp
        rs, us, vs = r, u, v
        r, u, v = rp, up, vp
        rp, up, vp = (rs - q*rp), (us - q*up), (vs - q*vp)
    return (r, u, v)
'''

#Une fonction key_creation(), créant une clé publique et une clé privée (n,pub,priv) grâce à deux nombres premiers p et q choisis aléatoirement entre 2 et 1000 en interne dans la fonction.

def key_creation():
  p,q = choice(list_prime(1000)), choice(list_prime(1000)) #choix de deux nombres premier aléatoire
  phi = (p-1)*(q-1)
  n = p*q
  
  r=10
  priv=0
  
  while r != 1 or priv <= 2 or priv >= phi: 
    pub = randint(1,1000)
    r, priv, v = extended_gcd(pub,phi)
    
  n, pub, priv = int(n), int(pub), int(priv)

  return (n, pub, priv)
  
#Une fonction encryption(n,pub,msg) qui prend en entrée la clé publique (n,pub) et un message texte msg et qui renvoie le message chiffré (qui pourra prendre la forme d’une liste de nombres). 

#Pour cela, vous pourrez notamment utiliser une fonction convert_msg(msg) codée par vos soins qui transforme le message textuel msg en une liste de nombres, qui seront ensuite chacun chiffrés

def convert_msg(msg,dummy_file):
  liste_nbr = []
  for elt in msg:
    if ord(elt) < 100:
      liste_nbr.append("0"+str(ord(elt)))
    else :  
      liste_nbr.append(str(ord(elt)))
  
  print("Message en valeur ASCII:\n",liste_nbr,"\n", file=dummy_file)
  liste_nbr = pack4(liste_nbr)
  print("Message en blocs de 4:\n",liste_nbr,"\n", file=dummy_file)
  return liste_nbr

def de_convert_msg(liste):
  elt = []
  carac = '' 
  for i in range (len(liste)):
    elt.append(chr(int(liste[i])))
    carac += chr(int(liste[i]))
  return elt ,carac

#Une fonction decryption(n,pub,msg) qui prend en entrée la clé privée (n,priv) et un message chiffré msg et qui renvoie le message décrypté.

def encryption(n, pub, msg,dummy_file):
  msg = convert_msg(msg,dummy_file)
  liste = []
  for elt in (msg):
    liste.append((int(elt)**pub) % n)
  return liste 

def decryption(n,priv,msg):
  liste = []
  for elt in (msg):
    calcul = (elt **priv) % n
    liste.append(calcul)

  liste = depack4(liste)
  return liste

def pack4(liste):#change des blocs de 3 en blocs de 4 pour l'envoie
  
  stock = ''
  for i in range (len(liste)):
    stock += liste[i]

  while len(stock) % 4 != 0: #ajoute des 0 pour que len(liste)%4 == 0
    stock = '0' + stock
  
  l_f = []
  stock2 = ''
  for o in range (len(stock)):
    stock2 += stock[o]
    if len(stock2) == 4:
      l_f.append(stock2)
      stock2 = ''

  return l_f

def depack4(liste): #passe une liste de blocs de 4 en une liste de blocs de 3

  for k in range (len(liste)): #ajoute des 0 pour que len(liste)%4 == 0
    liste[k] = str(liste[k])
    while len(liste[k]) % 4 != 0:
      liste[k] = '0' + liste[k]

  stock = ''
  for i in range (len(liste)):  
    stock += liste[i]

  l_f = []
  stock2 = ''
  for o in range (len(stock)-1,-1,-1): #parcours de la liste de la fin vers le début
    stock2 += stock[o]
    if len(stock2) == 3:
      if stock2 != '000':
        l_f.append(stock2[::-1]) #inverse la position des 3 éléments de stock2
      stock2 = ''

  l_f.reverse() #inverse les positions des liste du tableau
  return l_f

