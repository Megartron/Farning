import csv
import matplotlib.pyplot as plt
import numpy as np


iris_list = []

with open("iris_dataset.csv", newline="") as iris_dataset:
    reader = csv.reader(iris_dataset)
    for row in reader:
        iris_list.append(", ".join(row))


x_length = []
y_width = []
y_petal_length = []
y_petal_width = []

for i in iris_list[1:30]:
    print(i)
    x_length.append(float(i[0:3]))
    y_width.append(float(i[5:8]))
    y_petal_length.append(float(i[10:13]))
    y_petal_width.append(float(i[15:18]))




def residum(m, werte_x, werte_y):
    residum_summe = 0
    for n in range(len(werte_x)):
        residum_summe += (werte_y[n] - m * werte_x[n])**2
    return residum_summe


#steigungen = []
#residuen = []



def steigung_berechnen(x, y):
    aktuelle_steigung = 1
    aktuelle_residuum = 0

    neue_residuum_plus = 0
    neue_residuum_minus = 0
    neue_residuum = 0

    steigung_anderung = 1

    for i in range(100):
        aktuelle_residuum = residum(aktuelle_steigung, x, y)
        neue_residuum_minus = residum(aktuelle_steigung - steigung_anderung, x, y)
        neue_residuum_plus = residum(aktuelle_steigung + steigung_anderung, x, y)
        neue_residuum = neue_residuum_plus if neue_residuum_plus < neue_residuum_minus else neue_residuum_minus

        if neue_residuum < aktuelle_residuum:
            aktuelle_steigung = aktuelle_steigung + steigung_anderung if neue_residuum_plus < neue_residuum_minus else aktuelle_steigung - steigung_anderung
            #steigungen.append(aktuelle_steigung)
            #residuen.append(neue_residuum)
            print("NEUE RESIDUUM: ", neue_residuum)
        else:
            steigung_anderung = steigung_anderung*0.1
    
    print("STEIGUNG: ", aktuelle_steigung)
    return aktuelle_steigung


steigung = steigung_berechnen(x_length, y_width)
steigung2 = steigung_berechnen(x_length, y_petal_length)
steigung3 = steigung_berechnen(x_length, y_petal_width)

gerade_x_length = np.linspace(0, 6.5, 10)

greade_y = steigung * gerade_x_length
greade_y_petal_length = steigung2 * gerade_x_length
gerade_y_petal_width = steigung3 + gerade_x_length
print(gerade_y_petal_width)

#plt.plot(steigungen, residuen, "bo")
plt.plot(gerade_x_length, greade_y)
plt.plot(gerade_x_length, greade_y_petal_length)
plt.plot(gerade_x_length, gerade_y_petal_width)

plt.plot(x_length, y_petal_width, "bo")
plt.plot(x_length, y_petal_length, "go")
plt.plot(x_length, y_width, "ro")
plt.xlabel("x")
plt.ylabel("y")
plt.show()


#TODO Gradientenverfahren