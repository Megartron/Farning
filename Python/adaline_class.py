import csv
import matplotlib.pyplot as plt
import numpy as np
import random

class Adaline:
    def __init__(self, datensatz: list, weights: list, animiert: bool):
        self.datensatz = datensatz
        self.trainingsdatensatz = []
        self.ws = weights
        self.b1 = 1
        self.animiert = animiert
    
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
        
        if len(self.trainingsdatensatz[0]) - 1 != len(self.ws):
            raise Exception("Anzahl der Gewichte stimmen nicht mit dem Trainingsdatensatz überein!")

        return self.trainingsdatensatz
    
    def perzeptron(self, stop: float, max_iterationen: int, e: int = 1.00042):
        a = 0.015
        l = len(self.trainingsdatensatz)
        
        # Zum Zeigen des Lernprozesses
        iteration = e - 1
        
        for j in range(max_iterationen):
            if self.animiert:
                plt.clf()
            fehler_w = [0, 0, 0, 0, 0, 0]
            gesamt_fehler = 0
            fehler_b1 = 0
            
            for i in range(l):
                x = self.trainingsdatensatz[i]
                y = self.trainingsdatensatz[i][-1]

                # Vorhersage

                y_schätz = self.b1
                for k in range(len(self.ws)):
                    y_schätz += self.ws[k] * x[k]


                # Fehlerberechnung
                fehler = y_schätz - y
                gesamt_fehler += fehler**2
                

                # Gradientenberechnung
                fehler_b1 += fehler
                for k in range(len(self.ws)):
                     fehler_vorher = fehler_w[k]
                     fehler_w[k] = fehler_vorher + fehler * x[k]

            # Parameter-Update (Gradient Descent)
            self.b1 -= a * (fehler_b1/l)
            for k in range(len(self.ws)):
                w_vorher = self.ws[k]
                self.ws[k] = w_vorher - a * (fehler_w[k]/l)

            if gesamt_fehler/l < stop:
                break

            if j >= max_iterationen*iteration and self.animiert:
                e *= e
                iteration += e - 1
                self.entscheidungsgrenze_plotten(new = False)
        if self.animiert:
            plt.clf()
            self.entscheidungsgrenze_plotten(new = False)
            self.animiert = False
            
        return (self.ws, self.b1)
    
    # Prüfen wie gut das Perzeptron schätzen kann
    def prüfung(self):
        richtig = 0
        falsch = 0
        print(self.ws)
        for i in range (len(self.datensatz)):
            x = self.datensatz[i]
            y = self.datensatz[i][-1]

            y_geschätzt = self.b1
            for k in range(len(self.ws)):
                y_geschätzt += self.ws[k] * x[k]

            y_geschätzt = 1 if y_geschätzt >= 0 else -1

            if y_geschätzt == y:
                richtig += 1
            else:
                falsch += 1
        return (richtig, falsch)
    
    def entscheidungsgrenze_plotten(self, welcher: str = "training", new: bool = True):
        if len(self.ws) != 2:
            print("Entscheidungsgrenze kann nur in bei zwei Gewichten geplotted werden!")
            return

        w1 = self.ws[0]
        w2 = self.ws[1]

        if welcher == "training":
            x1 = self.get_spalte_training(0)
            x2 = self.get_spalte_training(1)
            y = self.get_spalte_training(-1)
        else:
            x1 = self.get_spalte_echt(0)
            x2 = self.get_spalte_echt(1)
            y = self.get_spalte_echt(-1)
        
        
        
        x_line = np.linspace(0, 100, 2)
        y_line = - (w1 / w2) * x_line - (self.b1 / w2) # 2D Entscheidungsgrenze: 0 = w1x1 + w2x2 +b, x_line = x1, y_line = x2
        farbe = ["green" if y_wert == 1 else "red" for y_wert in y]

        if new:
            plt.figure()

        plt.plot(x_line, y_line, label="Entscheidungsgrenze")
        plt.scatter(x1, x2, c=farbe)
        plt.gca().set_xlim(min(self.get_spalte_echt(0)) - 0.2, max(self.get_spalte_echt(0)) + 0.2)
        plt.gca().set_ylim(min(self.get_spalte_echt(1)) - 0.2, max(self.get_spalte_echt(1)) + 0.2)

        plt.xlabel("Sepal Length")
        plt.ylabel("Sepal Width")
        plt.title("ADALINE")
        plt.legend()

        if not self.animiert:
            plt.show()
        else:
            plt.pause(0.5)


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
datensatz = []
for i in iris_list[1:101]:
    reihe = []
    lenght = float(i[0:3])
    width = float(i[5:8])
    petal_lenght = float(i[10:13])
    petal_width = float(i[15:18])

    reihe.append(lenght)
    reihe.append(width)
    reihe.append(petal_lenght)
    reihe.append(petal_width)
    if i[20:] == "setosa":
        reihe.append(1)
    else:
        reihe.append(-1)

    datensatz.append(reihe)

trainingsdatensatz = []

for i in range(10):
    trainingsdatensatz.append(datensatz[i])
    trainingsdatensatz.append(datensatz[i+50])
trainingsdatensatz.append([4.5, 2.3, 1])
trainingsdatensatz.append([5.4, 3.0, -1])

a = Adaline(datensatz, [1, 1, 1, 1], False)
trainingsdatensatz_1 = [[6.3, 2.3, -1], [5.7, 2.6, -1], [5.4, 3.4, 1], [4.3, 3.0, 1], [6.4, 3.2, -1], [5.0, 3.4, 1], [5.7, 3.0, -1], [6.0, 2.7, -1], [5.5, 2.4, -1], [6.3, 2.5, -1]] # 2 weights
trainingsdatensatz_2 = [[6.7, 3.1, 4.4, -1], [5.6, 3.0, 4.1, -1], [5.8, 2.6, 4.0, -1], [5.0, 3.6, 1.4, 1], [5.7, 2.6, 3.5, -1], [6.2, 2.2, 4.5, -1], [6.5, 2.8, 4.6, -1], [4.9, 3.1, 1.5, 1], [5.6, 2.5, 3.9, -1], [6.0, 2.7, 5.1, -1]] # 3 weights
trainingsdatensatz_3 = [[5.5, 4.2, 1.4, 0.2, 1], [5.7, 2.9, 4.2, 1.3, -1], [5.4, 3.9, 1.7, 0.4, 1], [6.2, 2.2, 4.5, 1.5, -1], [6.0, 2.9, 4.5, 1.5, -1], [6.2, 2.9, 4.3, 1.3, -1], [4.6, 3.4, 1.4, 0.3, 1], [4.3, 3.0, 1.1, 0.1, 1], [6.7, 3.1, 4.7, 1.5, -1], [5.6, 2.9, 3.6, 1.3, -1]] # 4 weights
a.trainningsdaten_erstellen(10, False, trainingsdatensatz_3)
richtig, falsch = a.prüfung()
print(f"(Nicht trainiert) Richtig: {richtig}; Falsch: {falsch}")

werte = a.perzeptron(0.001, 10_000, 1.0001)

richtig, falsch = a.prüfung()
print(f"(Trainiert) Richtig: {richtig}; Falsch: {falsch}, mit folgenden Gewichten: {werte}")

a.entscheidungsgrenze_plotten(welcher = "echt", new = True)
