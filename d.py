import csv
import matplotlib.pyplot as plt
import numpy as np


iris_list = []

with open("iris_dataset.csv", newline="") as iris_dataset:
    reader = csv.reader(iris_dataset)
    for row in reader:
        iris_list.append(", ".join(row))


x = []
y = []

for i in iris_list[1:10]:
    print(i)
    x.append(float(i[0:3]))
    y.append(float(i[5:8]))



def f(x, m):
    return m * x

m = 0.65







print("x: ",x)
print(y)





def residum(m, werte_x, werte_y):
    residum_summe = 0
    for n in range(len(werte_x)):
        residum_summe += (werte_y[n] - m * werte_x[n])**2
    print(residum_summe)
    return residum_summe



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
        print("NEUE RESIDUUM: ", neue_residuum)
    else:
        steigung_anderung = steigung_anderung*0.1

print("STEIGUNG: ", aktuelle_steigung)


aktuelle_steigung = 0.68

    #print(residum(x[n], y[n], m))
    #residum_x.append(y[n])

gerade_x = [0,4, 6]
greade_y = [0,f(4.1, aktuelle_steigung), f(6.2, aktuelle_steigung)]



plt.plot(gerade_x, greade_y)
plt.plot([2,10], [2, 10], "bo")
plt.plot(x, y, "ro")
plt.xlabel("x")
plt.ylabel("y")
plt.show()

#residuum durchschnitt berechnen

