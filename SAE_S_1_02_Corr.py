from SAE_S_1_02_RSA import *
from SAE_S_1_02_Bilan import *

import numpy as np,sys

#Enoncé : "La seconde partie est une introduction à la notion de code correcteur. On se concentre sur un exemple simple, dont il faudra illustrer les propriétés. Notez que bien qu’il n’y soit pas explicitement question de code en Python, rien ne vous empêche d’en utiliser, cela étant même fortement encouragé."


if len(sys.argv) == 1:
  phi = input("Voulez-vous voir les vecteurs image de ϕ ?: y/n\n")
  demo = input("Voulez-vous voir la démonstration de la longeur de u+v ?: y/n\n")
else:
  phi = sys.argv[2]
  demo = sys.argv[3]
G = [[1,1,0,1],[1,0,1,1],[1,0,0,0],[0,1,1,1],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

def append_dans_liste(arr, n): #Fonction crée une liste avec arr
    global liste
    stock_arr = []
    for i in range(0, n): 
        if arr[i] == " ":
          break
        stock_arr.append(arr[i])
    liste.append(stock_arr)
    stock_arr =''
 
def gen_binaire(n, arr, i): #Fonction crée une liste qui contient une liste binaire de N bits
    if i == n:
        append_dans_liste(arr, n)
        return
    arr[i] = 0
    gen_binaire(n, arr, i + 1)
 
    arr[i] = 1
    gen_binaire(n, arr, i + 1)


def ensSol(dummy_file): #calcule les vecteurs image de ϕ
  global liste
  global Notu
  global phi
  """Fonction qui la question 2.3"""
  liste = []
  n = 4
  arr = [None] * n
  gen_binaire(n, arr, 0)

  ligne_f = []

  for l in range (len(liste)): #addition muliplication des matrices
    ligne1 = []
    for o in range (7): 
      val1 = 0
      for i in range (n):
        val1 += liste[l][i] * G[o][i]
      ligne1.append(val1)

    ligne1 = patch(ligne1) #remplace les 2 et les 3 par des 0 et des 1
    ligne_f.append(ligne1)

    Notu = ligne_f

  if phi == 'y':
    affiche(ligne_f,liste,dummy_file)
  return ligne_f
  
def affiche(solution,liste,dummy_file): #fonction utile pour affiche dans la consol
  
  print("L'ensemble des vecteurs de l’image de ϕ:\n")
  for i in range (len(solution)):
    print(str(liste[i])+" → "+str(solution[i]), file=dummy_file)
  print("\n", file=dummy_file)

def patch(liste): #si il y a un 3 alors = 1 et si c'est un 2 = 0
  
  for i in range (len(liste)):
    if liste[i] == 2:
      liste[i] = 0
    if liste[i] == 3:
      liste[i] = 1

  return liste

def addition_matrice(liste): #additionne les matrice contenue dans liste si elle sont différente (u != v)
  global demo

  for k in range (len(liste)):
    for o in range (len(liste)):
      matrice_add = []
      if liste[k] != liste[o]:
        for i in range (len(liste[o])):
          matrice_add.append(liste[k][i]+liste[o][i])
        
        matrice_add = patch(matrice_add)
        number = poids(matrice_add)
        
        if demo == "y":
          print(str(liste[k])," + ",str(liste[o])," = ",str(matrice_add)+" → poids("+str(number)+')')

def poids(mat): #détermine le poids de la matrice en argument
  number = 0
  for n in range (len(mat)):
    if mat[n] == 1:
      number += 1
  return number


def main_correct(liste,dummy_file): #fonction qui appelle les autres fonction du code correcteur avec chaque élement de la liste 

  value_f = []
  for o in range (len(liste)):
    matrice = []
    matrice7 = check_lost(liste[o],dummy_file)
    for i in range (len(matrice7)):
      matrice.append(matrice7_to_4(matrice7[i]))
    
    value = conv_bin_int(matrice)
    value_f.append(int(value))
  return value_f

def addition_u_Notu(u,Notu): #avec l'addition la matrice avec la matrice inverse
  l = []
  for i in range (len(u)):
    l.append(u[i]+Notu[i])
  return l

def check_lost(arg,dummy_file): #fonction principale de la détéction et de la correction d'un bruitage
  global G
  global Notu
  

  conv = format(arg, "b") #convertion en binaire
  liste = pack4(conv)

  ligne_f = []

  for l in range (len(liste)): #muliplication de u et v avec u != v
    ligne1 = []
    for o in range (7): 
      val1 = 0
      for i in range (len(liste[0])):
        val1 += int(liste[l][i]) * G[o][i]
      ligne1.append(val1)

    ligne1 = patch(ligne1)
    ligne_f.append(ligne1)

  for j in range (len(ligne_f)):
    ligne_f[j] = noise(ligne_f[j])


  for u in range (len(ligne_f)):
    for k in range (len(Notu)):
      p = poids(patch(addition_u_Notu(ligne_f[u],Notu[k]))) #on supprime les 2 et 3 puis on regard le poids

      if p == 0:
        print("Matrice ",ligne_f[u]," non ébruité", file=dummy_file)
        break
      elif p == 1:
        print("Matrice ",ligne_f[u]," ébruité, matrice corrigé ",Notu[k], file=dummy_file)
        ligne_f[u] = Notu[k]
  
  return ligne_f

def matrice7_to_4(matrice): #permet de passer d'une matrice de longeur 7 à une matrice de longeur 4
  return [matrice[2],matrice[4],matrice[5],matrice[6]]

def conv_bin_int(liste_bin): #passage d'une liste de binaire en int
  stock = ''
  for i in range (len(liste_bin)):
    for k in range (len(liste_bin[i])):
      stock += str(liste_bin[i][k])
  return str(int(stock, 2))
