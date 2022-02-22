
import timeit ,sys, io,os

dummy_file = io.StringIO()

from SAE_S_1_02_Bilan import *
from SAE_S_1_02_Corr import *
from SAE_S_1_02_RSA import *


print("\n\n========================================================================\n", file=dummy_file)
#print(list_prime(25))
#print(extended_gcd(210,55))

if len(sys.argv) == 1:
  msg = input("Donnez votre message: ")
else:
  msg = sys.argv[1]

def main_for_test(msg): #fonction principale
  global crypto
  global dummy_file

  n , pub , priv = key_creation() #generaton des clées
  print("\nClés:\n",n,pub,priv,"\n", file=dummy_file)
  

  crypto = encryption(n, pub, msg,dummy_file) #cryptage
  print("Message crypté:\n",crypto,"\n", file=dummy_file)

  addition_matrice(ensSol(dummy_file)) #utile pour afficher les vecteurs image de ϕ

  bru = main_correct(crypto,dummy_file) #fonction principale du code correcteur

  liste = decryption(n,priv,bru) 
  liste , carac = de_convert_msg(liste)
  print("\n-----------------------------------------\nMessage final:\n",carac,"\n-----------------------------------------\n\nTemps d'exuction de la partie:", file=dummy_file)

print(timeit.timeit("main_for_test(msg)", number=1, globals=locals()), file=dummy_file) #temps d'execution"

console = dummy_file.getvalue()
print(console)

os.remove("log.txt")
f = open("log.txt", "a")
f.write(console)
f.close()