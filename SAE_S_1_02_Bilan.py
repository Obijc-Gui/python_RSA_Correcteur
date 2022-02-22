#Enoncé : "La dernière partie est une mise en œuvre simultanée de ces deux outils afin de simuler comment a lieu une communication sécurisée en ligne.
import numpy as np

def noise(vect_msg):
  """
  prend un vecteur vect_msg et renvoie ce vecteur potentiellement bruite
   """
  ### on fait une copie du vecteur initial
  vect = vect_msg.copy()
  ### une chance sur quatre de ne pas bruiter le vecteur
  test = np.random.randint(0,4)
  if test>0:
    index = np.random.randint(0,np.size(vect))
    vect[index] = (vect[index] +1)%2
  return vect