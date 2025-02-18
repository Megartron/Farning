import csv
import matplotlib.pyplot as plt
import math
import numpy as np
import random

class Adaline:
    def __init__(self, datensatz: list):
        
        self.datensatz = datensatz

        self.trainingswerte_x1 = []
        self.trainingswerte_x2 = []
        self.trainingswerte_y = []
        self.w1 = 1
        self.w2 = 1
        self.b1 = 1
    
    

    def trainingsdaten_erstllen(self, anzahl):
        for i in range(anzahl):
            if i % 2 == 0:
                self.trainingswerte_y.append(self.echt_y_1[i])
                self.trainingswerte_x1.append(self.echt_x1_1[i])
                self.trainingswerte_x2.append(self.echt_x2_1[i])
            else:
                self.trainingswerte_y.append(self.echt_y_2[i])
                self.trainingswerte_x1.append(self.echt_x1_2[i])
                self.trainingswerte_x2.append(self.echt_x2_2[i])

        return (self.trainingswerte_x1, self.trainingswerte_x2, self.trainingswerte_y)
    
    def trainningsdaten_erstellen(self, anzahl: int, shuffle: bool):
        if shuffle:
            random.shuffle(self.datensatz)

        for i in range(anzahl):
            x1 = self.datensatz[i][0]
            x2 = self.datensatz[i][1]
            y = self.datensatz[i][2]

            self.trainingswerte_x1.append(x1)
            self.trainingswerte_x2.append(x2)
            self.trainingswerte_y.append(y)
    
    def perzeptron(self, stop):
        a = 0.01
        
        for j in range(1_000):
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
    
    # Prüfen wie gut das Perzeptron schätzen kann
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
    
    def prüfung(self):
        richtig = 0
        falsch = 0

        for i in range (len(self.datensatz)):
            x1 = self.datensatz[i][0]
            x2 = self.datensatz[i][1]
            y = self.datensatz[i][2]

            y_geschätzt = self.w1 * x1 + self.w2 * x2 + self.b1

            y_geschätzt = 1 if y_geschätzt >= 0 else -1

            if y_geschätzt == y:
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


species = 0
datensatz = []
for i in iris_list[1:101]:
    reihe = []
    lenght = float(i[0:3])
    width = float(i[5:8])

    if i[20:] == "setosa":
        reihe.append(lenght)
        reihe.append(width)
        reihe.append(1)
    else:
        reihe.append(lenght)
        reihe.append(width)
        reihe.append(-1)


    datensatz.append(reihe)





"""
setosa_sepal_length = []
versicolor_sepal_length = []

setosa_sepal_width = []
versicolor_sepal_width = []


setosa_sepal_y = []
versicolor_sepal_y = []

for i in range(50):
    setosa_sepal_y.append(1)


for i in range(50):
    versicolor_sepal_y.append(-1)


for i in iris_list[1:51]:
    setosa_sepal_length.append(float(i[0:3]))

    setosa_sepal_width.append(float(i[5:8]))

for i in iris_list[51:101]:
    versicolor_sepal_length.append(float(i[0:3]))
    versicolor_sepal_width.append(float(i[5:8]))


a = Adaline(setosa_sepal_length, setosa_sepal_width, versicolor_sepal_length, versicolor_sepal_width, setosa_sepal_y, versicolor_sepal_y)

daten = a.trainingsdaten_erstellen(5)
print(daten)





weight = a.perzeptron(0.001)

richtig, falsch = a.prufung(setosa_sepal_length, setosa_sepal_width, setosa_sepal_y)
print(f"Richtig: {richtig}; Falsch: {falsch}")

richtig, falsch = a.prufung(versicolor_sepal_length, versicolor_sepal_width, versicolor_sepal_y)
print(f"Richtig: {richtig}; Falsch: {falsch}")

w1, w2, b1 = weight
plt.figure(figsize=(8, 6))

x_line = np.linspace(3.5, 7, 100)
y_line = - (w1 / w2) * x_line - (b1 / w2) # 2D Entscheidungsgrenze: 0 = w1x1 + w2x2 +b, x_line = x1, y_line = x2


plt.plot(x_line, y_line, label="Entscheidungsgrenze")
plt.plot(versicolor_sepal_length, versicolor_sepal_width, "go")
plt.plot(setosa_sepal_length, setosa_sepal_width, "ro")

plt.xlabel("Sepal Length")
plt.ylabel("Sepal Width")
plt.title("ADALINE")
plt.legend()

plt.show()


[
    [1, 1, -1], 
    [2, 0, 1],
    [0.5, 1, 1],

]

"""
