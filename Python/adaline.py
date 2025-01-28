

import csv
import matplotlib.pyplot as plt
import math
import numpy as np


# versicolor und setosa Daten plotten
iris_list = []

with open("iris_dataset.csv", newline="") as iris_dataset:
    reader = csv.reader(iris_dataset)
    for row in reader:
        iris_list.append(", ".join(row))



setosa_sepal_length = []
versicolor_sepal_length = []

setosa = []
versicolor = []

for i in range(50):
    setosa.append(1)


for i in range(50):
    versicolor.append(0)


for i in iris_list[1:51]:
    setosa_sepal_length.append(float(i[0:3]))

for i in iris_list[51:101]:
    versicolor_sepal_length.append(float(i[0:3]))

# Durchschnittwerte ausrechnen
def durchschnitt(werte):
    gesamt = 0
    anzahl = 0
    for i in werte:
        gesamt += float(i)
        anzahl += 1
    if anzahl > 0:
        return gesamt/anzahl
    else:
        return None

# Sigmoid Aktivierungsfunktion
def sigmoid(x):
    return 1/(1 + np.exp(-x))



# Perzeptron
def perzeptron(trainingswerte_x, trainingswerte_y):
    w = 0.5
    b = 0

    


    return (w, b)

def lineare_funktion(w, x, b):
    return w * x + b

def ableitung_für_w(w, x, y_wahr, b):
    return -2 * x * (y_wahr - (w * x + b))

def ableitung_für_b(w, x, y_wahr, b):
    return -2 * (y_wahr - (w * x + b))

def gradient_descent(x_werte, y_werte, w, b):

    for wiederholen in range(1000):
        for i in range(14):
            x = x_werte[i]
            y = y_werte[i]

            fehler_w = ableitung_für_w(w, x, y, b)
            fehler_b = ableitung_für_b(w, x, y, b)

            w += -0.001 * fehler_w
            
            b += -0.001 * fehler_b
    return (w, b)



trainingswerte_x = [7.0, 6.4, 6.9, 5.1, 4.9, 6.3, 4.4, 5.6, 5.9, 6.1, 6.3, 4.6, 5.1, 4.8,]
trainingswerte_y = [0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1]

sigmoid_versicolor = []
for i in versicolor_sepal_length:
    sigmoid_versicolor.append(sigmoid(i))



x = np.linspace(0, 8, 10)
weight = gradient_descent(trainingswerte_x, trainingswerte_y, 0.5, 0)
y = lineare_funktion(weight[0], x, weight[1])

#werte = perzeptron(trainingswerte_x, trainingswerte_y)
#y = lineare_funktion(werte[0], x, werte[1])

plt.plot(x, y)
plt.plot(versicolor_sepal_length, sigmoid_versicolor, "go")
plt.plot(versicolor_sepal_length, versicolor, "bo")
#plt.plot(setosa_sepal_length, setosa, "ro")
plt.show()
