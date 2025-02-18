import csv
import matplotlib.pyplot as plt
import math
import numpy as np

class Adaline:
    def __init__(self, trainingswerte_x1, trainingswerte_x2, trainingswerte_y):
        self.trainingswerte_x1 = trainingswerte_x1
        self.trainingswerte_x2 = trainingswerte_x2
        self.trainingswerte_y = trainingswerte_y
        self.w1 = 1
        self.w2 = 1
        self.b1 = 1

    def trainingsdaten_erstellen(self):
        return
    
    def perzeptron(self, stop):
        a = 0.01
        
        for j in range(10_000):
            gesamt_fehler = 0
            fehler_w1 = 0
            fehler_w2 = 0
            fehler_b1 = 0
            l = len(self.trainingswerte_y)
            for i in range(l):
                x1 = self.trainingswerte_x1[i]
                x2 = self.trainingswerte_x2[i]
                y = self.trainingswerte_y[i]

                # Vorhersage
                y_schätz = self.w1 * x1 + self.w2 * x2 + self.b1

                # Fehlerberechnung
                fehler = y_schätz - y
                gesamt_fehler += fehler**2
                

                # Gradientenberechnung
                fehler_w1 += fehler * x1
                fehler_w2 += fehler * x2
                fehler_b1 += fehler

            # Parameter-Update (Gradient Descent)
            self.w1 -= a * (fehler_w1/l)
            self.w2 -= a * (fehler_w2/l)
            self.b1 -= a * (fehler_b1/l)

            if gesamt_fehler/l < stop:
                break
        
        return (self.w1, self.w2, self.b1)
    
    
    def prufung(self, echte_werte_x1, echte_werte_x2, lösung):
        richtig = 0
        falsch = 0
        
        for i in range(len(lösung)):
            x1 = echte_werte_x1[i]
            x2 = echte_werte_x2[i]
            y_echt = lösung[i]

            y_geschätzt = self.w1 * x1 + self.w2 * x2 + self.b1
            
            y_geschätzt = 1 if y_geschätzt >= 0 else -1

            if y_geschätzt == y_echt:
                richtig += 1
            else:
                falsch += 1
        
        return (richtig, falsch)



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


trainingswerte_sepal_y = []
trainingswerte_sepal_lenght_x1 = []

trainingswerte_sepal_width_x2 = []

for i in range(50):
    if i % 2 == 0:
        trainingswerte_sepal_y.append(1)
        trainingswerte_sepal_lenght_x1.append(setosa_sepal_length[i])

        trainingswerte_sepal_width_x2.append(setosa_sepal_width[i])

    else:
        trainingswerte_sepal_y.append(-1)
        trainingswerte_sepal_lenght_x1.append(versicolor_sepal_length[i])

        trainingswerte_sepal_width_x2.append(versicolor_sepal_width[i])

a = Adaline(trainingswerte_sepal_lenght_x1, trainingswerte_sepal_width_x2, trainingswerte_sepal_y)

a.perzeptron(0.001)