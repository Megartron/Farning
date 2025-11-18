import numpy as np
import matplotlib.pyplot as plt
import copy
import ast
import csv
# Softplus:
# Aktivierungsfunktion und deren Ableitung
def softplus(x):
    return np.log(1 + np.exp(x))

def ableitung_softplus(x):
    return 1 / (1 + np.exp(-x))  # sigmoid(x)

def relu(x):
    return np.maximum(0, x)

def ableitung_relu(x):
    return np.where(x > 0, 1, 0)

def leaky_relu(x, alpha=0.01):
    return np.where(x > 0, x, alpha * x)

def leaky_relu_derivative(x, alpha=0.01):
    return np.where(x > 0, 1, alpha)

import numpy as np

def sigmoid(x):
    """Compute the sigmoid function."""
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    """Compute the derivative of the sigmoid function."""
    s = sigmoid(x)
    return s * (1 - s)


#   [[[111, 112, 113], [121, 122, 123]], [[211, 212, 213], [221, 222, 223], [231, 232, 233]], [[311, 312], [321, 322], [331, 332]]]

#        [[11, 12], [21, 22, 23], [31, 32, 33], [41, 42]] # n[0] = x, n[3] = y_schätz 


def training(a, rounds, funktion: str, values, dataset, stop, visual_steps, update_a_start):

    one_time = True
    if funktion == "relu":
        act = relu
        act_deriv = ableitung_relu
    elif funktion == "softplus":
        act = softplus
        act_deriv = ableitung_softplus
    elif funktion == "leaky":
        act = leaky_relu
        act_deriv = leaky_relu_derivative
    elif funktion == "sigmoid":
        act = sigmoid
        act_deriv = sigmoid_derivative
    else:
        raise Exception
    
    progress = visual_steps
    update_a = update_a_start

    # values: (w, b, n, dw, db, dn, dl)
    w, b, neuron_geg, dw_geg, db_geg, dn_geg, dl_geg = values

    dl_copy = copy.deepcopy(dl_geg)
    dw_copy = copy.deepcopy(dw_geg)
    db_copy = copy.deepcopy(neuron_geg)
    dn_copy = copy.deepcopy(neuron_geg)
    neuron_copy = copy.deepcopy(neuron_geg)
    vor_aktivierung_copy = copy.deepcopy(neuron_geg)
    
    for _ in range(rounds):
        l_gesamt = 0

        dl = copy.deepcopy(dl_geg)
        dw = copy.deepcopy(dw_geg)
        db = copy.deepcopy(neuron_geg)
        

        for data in dataset:
            dn = copy.deepcopy(neuron_geg)
            neuron = copy.deepcopy(neuron_geg)
            vor_aktivierung = copy.deepcopy(neuron_geg)
            
            x = data[0]
            y = data[1]

            # Vorwärtsdurchlauf
            for k in range(len(x)):
                vor_aktivierung[0][k] = x[k]
                neuron[0][k] = x[k]

            
            for i in range(len(w)):

                for k in range(len(neuron[i + 1])):
                    z = 0
                    for n in range(len(neuron[i])):
                        z += neuron[i][n] * w[i][n][k]
                    vor_aktivierung[i + 1][k] = z + b[i + 1][k]
                    neuron[i + 1][k] = act(vor_aktivierung[i + 1][k])

            # Fehler berechnen
            for k in range(len(y)):
                dl[k] = -2 * (y[k] - neuron[-1][k])
                l_gesamt += (y[k] - neuron[-1][k])**2

            # Gradientenberechnung
            for k in range(len(dn[-1])):
                dn[-1][k] = dl[k]
            
            # Ableitung nach Neuronen
            for i in range(len(neuron) - 1, 0, -1):
                for j in range(len(dn[i - 1])):
                    for k in range(len(dn[i])):
                        dn[i - 1][j] += dn[i][k] * w[i - 1][j][k] * act_deriv(vor_aktivierung[i][k])
            
            # Ableitung nach Gewichten (Fehlerberechnung)
            for i in range(len(dw)):
                for j in range(len(dw[i])):
                    for k in range(len(dw[i][j])):
                        dw[i][j][k] += neuron[i][j] * dn[i + 1][k] * act_deriv(vor_aktivierung[i + 1][k])
            
            for i in range(1, len(db)):
                for j in range(len(db[i])):
                    db[i][j] += dn[i][j]
        
        

        if (l_gesamt <= stop): break

        for i in range(len(dw)):
            for j in range(len(dw[i])):
                for k in range(len(dw[i][j])):
                    update_w = (dw[i][j][k] / len(dataset)) * a
                    w[i][j][k] -= update_w
        
        
        for i in range(1, len(db)):
            for j in range(len(db[i])):
                update_b = (db[i][j] / len(dataset)) * a
                b[i][j] -= update_b
        
        if (_ > rounds * progress):
            print(round(progress * 100, 1), " Prozent erreicht!")
            progress += visual_steps
            print("Fehler: ", l_gesamt)

            if (progress > update_a):
                update_a += 0.07
                a *= 0.95
                print("Learning rate ist jetzt: ", a)
    print("Endfehler: ", l_gesamt)

    dl = copy.deepcopy(dl_geg)
    dw = copy.deepcopy(dw_geg)
    db = copy.deepcopy(neuron_geg)
    dn = copy.deepcopy(neuron_geg)
    neuron = copy.deepcopy(neuron_geg)
    vor_aktivierung = copy.deepcopy(neuron_geg)

    datensatz = [l_gesamt, w, b, funktion, rounds, update_a_start, dataset]
    with open("zahlen_erkennen/training_results.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(datensatz)
        print("successfully written into file")

    return (w, b, neuron, funktion)

def perzeptron(data, values):

    w, b, neuron, funktion = values

    if funktion == "relu":
        act = relu
    elif funktion == "softplus":
        act = softplus
    elif funktion == "leaky":
        act = leaky_relu
    elif funktion == "sigmoid":
        act = sigmoid
    else:
        raise Exception


    x = data[0]
    y = data[1]

    for k in range(len(x)):
        neuron[0][k] = x[k]

    
    for i in range(len(w)):
        for k in range(len(neuron[i + 1])):
            z = 0
            for n in range(len(neuron[i])):
                z += neuron[i][n] * w[i][n][k]
            neuron[i + 1][k] = act(z + b[i + 1][k])
    
    l_gesamt = 0
    for k in range(len(y)):
        l_gesamt += (y[k] - neuron[-1][k])**2

    return (neuron[-1], y, l_gesamt)

def generate_weights(form: tuple, anzahl_output): # form = ((3, 3), (3, 3, 3), (2, 2, 2))
    n = [[] for _ in range(len(form) + 1)]

    w = [[] for _ in form]
    dw = [[] for _ in form]

    b = [[] for _ in range(len(form) + 1)]

    dl = [0 for _ in range(anzahl_output)]


    for i in range(len(form)):
        for j in range(len(form[i])):
            n[i].append(0)
            b[i].append(float(np.random.uniform(-1, 1)))
            w[i].append(list(np.random.randn(form[i][j])))
            dw[i].append([0 for _ in range(form[i][j])])

    for i in range(anzahl_output):
        n[-1].append(0)
        b[-1].append(float(np.random.uniform(-1, 1)))

    db = dn = n

    return (w, b, n, dw, db, dn, dl)


w = [
 [[-0.23,  0.77, -0.56], [ 0.12, -0.88,  0.45]],
 [[ 0.91, -0.34,  0.67], [-0.11,  0.05, -0.99], [0.44, -0.72,  0.18]],
 [[-0.65,  0.22], [ 0.81, -0.47], [-0.09,  0.33]]
]

b = [[1, 1], [1, 1, 1], [1, 1, 1], [1, 1]]

# Anzahl der Punkte
n = 10
np.random.seed(42)

datensatz = []
for _ in range(n):
    x1 = np.random.uniform(-2, 2)
    x2 = np.random.uniform(-2, 2)
    
    # Nichtlineare Transformation
    y1 = np.sin(x1) + x2**2
    y2 = np.cos(x2) + x1**2
    
    datensatz.append(((x1, x2), (y1, y2)))


datensatz = []

with open("zahlen_erkennen/datensatz.csv", newline="") as iris_dataset:
    reader = csv.reader(iris_dataset)
    for row in reader:
        row_tuple = (ast.literal_eval(row[0]), ast.literal_eval(row[1]))
        datensatz.append(row_tuple)

print(datensatz)

values = training(0.01, 50_000, "sigmoid", generate_weights(
    (
        (16,) * 25, 
        (16,) * 16,
        (10,) * 16
    )
    , 10), tuple(datensatz), 0.01, 0.005, 0.5)



print(perzeptron((
    (1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 
    (0, 0, 0, 0, 0, 0, 0, 0, 1, 0)
    ), values))

"""
x1 = np.linspace(-1, 3, 1000)
y = perzeptron("relu", x1, w_opt, b_opt)

x_echt = [i[0][0] for i in datensatz]
y_echt = [i[1][0] for i in datensatz]


plt.plot(x_echt, y_echt, "ro", label="Trainingsdaten")
plt.plot(x1, y, label="Vorhersage")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Vorhersage des Perzeptrons")
plt.legend()
plt.grid(True)
plt.show()
"""
