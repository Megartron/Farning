

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

setosa_sepal_width = []
versicolor_sepal_width = []


setosa_sepal_length_y = []
versicolor_sepal_lenght_y = []

setosa_sepal_widht_y = []
versicolor_sepal_width_y = []

for i in range(50):
    setosa_sepal_length_y.append(1)


for i in range(50):
    versicolor_sepal_lenght_y.append(-1)


for i in iris_list[1:51]:
    setosa_sepal_length.append(float(i[0:3]))

    setosa_sepal_width.append(float(i[5:8]))

for i in iris_list[51:101]:
    versicolor_sepal_length.append(float(i[0:3]))
    
    versicolor_sepal_width.append(float(i[5:8]))


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
def perzeptron(x_werte_sepal_lenght, y_werte_sepal_lenght, x_werte_sepal_width):

    w2 = 0.5
    w1 = 0.5
    b1 = 0
    for j in range(10000):
        for i in range(30):
            x1 = x_werte_sepal_lenght[i]
            x2 = x_werte_sepal_width[i]
            y = y_werte_sepal_lenght[i]

            y_schätz = w1 * x1 + w2 * x2 + b1

            fehler_w2 = ableitung_für_w(y_schätz, x2, y)
            fehler_w1 = ableitung_für_w(y_schätz, x1, y)
            fehler_b1 = ableitung_für_b(y_schätz, y)


            w2 += -0.01 * fehler_w2
            w1+= -0.01 * fehler_w1
            b1 += -0.01 * fehler_b1
        
        if abs(fehler_b1) < 0.01 and abs(fehler_w1) < 0.01 and abs(fehler_w2) < 0.01:
            break
    
    print((w1, w2, b1))
    return (w1, w2, b1)



def lineare_funktion(w, x, b):
    return w * x + b

def ableitung_für_w(y_schätz, x, y_wahr):
    return -2 * x * (y_wahr - y_schätz)

def ableitung_für_b(y_schätz, y_wahr):
    return -2 * (y_wahr - y_schätz)



def prüfung(w, b, x, y):
    richtig = 0
    falsch = 0
    
    print(y)
    for i in range(50):
        x_wert = x[i]
        y_echt = y[i]

        y_geschätzt = w * x_wert + b
        
        y_geschätzt = 1 if y_geschätzt >= 0 else -1

        if y_geschätzt == y_echt:
            richtig += 1
        else:
            falsch += 1
    
    return (richtig, falsch)
        






"""
def gradient_descent(x_werte, y_werte, w, b):

    #for wiederholen in range(1000):
    while(True):
        for i in range(14):
            x = x_werte[i]
            y = y_werte[i]

            fehler_w = ableitung_für_w(w, x, y, b)
            fehler_b = ableitung_für_b(w, x, y, b)

            w += -0.001 * fehler_w
            b += -0.001 * fehler_b
        if abs(fehler_b) < 0.01 and abs(fehler_w) < 0.01:
            break
    return (w, b)
"""





#trainingswerte_x = [7.0, 6.4, 6.9, 5.1, 4.9, 6.3, 4.4, 5.6, 5.9, 6.1, 6.3, 4.6, 5.1, 4.8,]
#trainingswerte_y = [-1, -1, -1, 1, 1, -1, 1, -1, -1, -1, -1, 1, 1, 1]

trainingswerte_sepal_lenght_y = []
trainingswerte_sepal_lenght_x = []

trainingswerte_sepal_width_x = []

for i in range(30):
    if i % 2 == 0:
        trainingswerte_sepal_lenght_y.append(1)
        trainingswerte_sepal_lenght_x.append(setosa_sepal_length[i])

        trainingswerte_sepal_width_x.append(setosa_sepal_width[i])

    else:
        trainingswerte_sepal_lenght_y.append(-1)
        trainingswerte_sepal_lenght_x.append(versicolor_sepal_length[i])

        trainingswerte_sepal_width_x.append(versicolor_sepal_width[i])


print(trainingswerte_sepal_width_x)

sigmoid_versicolor = []
for i in versicolor_sepal_length:
    sigmoid_versicolor.append(sigmoid(i))



x = np.linspace(0, 8, 10)
weight = perzeptron(trainingswerte_sepal_lenght_x, trainingswerte_sepal_lenght_y, trainingswerte_sepal_width_x)
y = lineare_funktion(weight[0], x, weight[1])

print(prüfung(weight[0], weight[1], setosa_sepal_length, setosa_sepal_length_y))
print(prüfung(weight[0], weight[1], versicolor_sepal_length, versicolor_sepal_lenght_y))



#plt.plot(x, y)

plt.plot(versicolor_sepal_length, versicolor_sepal_width, "go")
plt.plot(setosa_sepal_length, setosa_sepal_width, "ro")
plt.title("Grün: -1; Rot: 1")
plt.show()
