import csv
import matplotlib.pyplot as plt
import numpy as np
import random

class Adaline:
    def __init__(self, datensatz: list):
        self.datensatz = datensatz
        self.trainingsdatensatz = []
        self.w1 = 1
        self.w2 = 1
        self.b1 = 1
    
    def trainningsdaten_erstellen(self, anzahl: int, rand: bool, trainigsdatensatz: list):
        if rand:
            kopie = []
            for k in self.datensatz:
                kopie.append(k)
            random.shuffle(kopie)
            for i in range(anzahl):
                self.trainingsdatensatz.append(kopie[i])
            print("Benutzer Datensatz: ", self.trainingsdatensatz)
        else:
            self.trainingsdatensatz = trainigsdatensatz

        return self.trainingsdatensatz
    
    def perzeptron(self, stop: float, max_iterationen: int):
        a = 0.015
        l = len(self.trainingsdatensatz)
        for j in range(max_iterationen):
            gesamt_fehler = 0
            fehler_w1 = 0
            fehler_w2 = 0
            fehler_b1 = 0
            
            for i in range(l):

                x1 = self.trainingsdatensatz[i][0]
                x2 = self.trainingsdatensatz[i][1]
                y = self.trainingsdatensatz[i][2]

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
        print(gesamt_fehler/l)
        return (self.w1, self.w2, self.b1)
    
    # Prüfen wie gut das Perzeptron schätzen kann
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
    
    # Daten für das Plotten
    def get_spalte_echt(self, spalte: int):
        return [s[spalte] for s in self.datensatz]
    
    def get_spalte_training(self, spalte: int):
        return [s[spalte] for s in self.trainingsdatensatz]


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

    if i[20:] == "Iris-setosa":
        reihe.append(lenght)
        reihe.append(width)
        reihe.append(1)
    else:
        reihe.append(lenght)
        reihe.append(width)
        reihe.append(-1)


    datensatz.append(reihe)

trainingsdatensatz = []

for i in range(10):
    trainingsdatensatz.append(datensatz[i])
    trainingsdatensatz.append(datensatz[i+50])
trainingsdatensatz.append([4.5, 2.3, 1])
trainingsdatensatz.append([5.4, 3.0, -1])

a = Adaline(datensatz)
a.trainningsdaten_erstellen(10, True, [[6.3, 2.3, -1], [5.7, 2.6, -1], [5.4, 3.4, 1], [4.3, 3.0, 1], [6.4, 3.2, -1], [5.0, 3.4, 1], [5.7, 3.0, -1], [6.0, 2.7, -1], [5.5, 2.4, -1], [6.3, 2.5, -1]])
richtig, falsch = a.prüfung()
print(f"(Nicht trainiert) Richtig: {richtig}; Falsch: {falsch}")

w1, w2, b1 = a.perzeptron(0.001, 1_000_000)

richtig, falsch = a.prüfung()
print(f"(Trainiert) Richtig: {richtig}; Falsch: {falsch}")

x1 = a.get_spalte_echt(0)
x2 = a.get_spalte_echt(1)
y = a.get_spalte_echt(2)

plt.figure(figsize=(8, 6))

x_line = np.linspace(3.5, 7, 100)
y_line = - (w1 / w2) * x_line - (b1 / w2) # 2D Entscheidungsgrenze: 0 = w1x1 + w2x2 +b, x_line = x1, y_line = x2
plt.plot(x_line, y_line, label="Entscheidungsgrenze")

farbe = ["green" if y_wert == 1 else "red" for y_wert in y]
plt.scatter(x1, x2, c=farbe)

plt.xlabel("Sepal Length")
plt.ylabel("Sepal Width")
plt.title("ADALINE")
plt.legend()

plt.show()
