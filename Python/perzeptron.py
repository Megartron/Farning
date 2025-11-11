import numpy as np
import matplotlib.pyplot as plt
import copy

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

#   [[[111, 112, 113], [121, 122, 123]], [[211, 212, 213], [221, 222, 223], [231, 232, 233]], [[311, 312], [321, 322], [331, 332]]]

#        [[11, 12], [21, 22, 23], [31, 32, 33], [41, 42]] # n[0] = x, n[3] = y_schätz 


def training(a, rounds, funktion: str, values, dataset, stop, visual_steps):

    if funktion == "relu":
        act = relu
        act_deriv = ableitung_relu
    elif funktion == "softplus":
        act = softplus
        act_deriv = ableitung_softplus
    elif funktion == "leaky":
        act = leaky_relu
        act_deriv = leaky_relu_derivative
    else:
        raise Exception
    
    progress = visual_steps
    update_a = 0.05

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
                update_a += 0.05
                a *= 0.8185
                print("Learning rate ist jetzt: ", a)
    print("Endfehler: ", l_gesamt)

    dl = copy.deepcopy(dl_geg)
    dw = copy.deepcopy(dw_geg)
    db = copy.deepcopy(neuron_geg)
    dn = copy.deepcopy(neuron_geg)
    neuron = copy.deepcopy(neuron_geg)
    vor_aktivierung = copy.deepcopy(neuron_geg)

    return (w, b, neuron, funktion)

def perzeptron(data, values):

    w, b, neuron, funktion = values

    if funktion == "relu":
        act = relu
    elif funktion == "softplus":
        act = softplus
    elif funktion == "leaky":
        act = leaky_relu
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

if (False):
    datensatz = [((0.2928810235639485, 0.2928810235639485), (np.float64(0.2887117577277164), np.float64(0.2887117577277164))), ((1.2911361982345166, 1.2911361982345166), (np.float64(0.9611493081940838), np.float64(0.9611493081940838))), ((0.616580256429863, 0.616580256429863), (np.float64(0.5782485128461503), np.float64(0.5782485128461503))), ((0.2692990979813814, 0.2692990979813814), (np.float64(0.2660558622596657), np.float64(0.2660558622596657))), ((-0.45807120396657197, -0.45807120396657197), (np.float64(-0.4422189797345347), np.float64(-0.4422189797345347))), ((0.8753646783999365, 0.8753646783999365), (np.float64(0.7677772089015118), np.float64(0.7677772089015118))), ((-0.3744767324238447, -0.3744767324238447), (np.float64(-0.36578557449600696), np.float64(-0.36578557449600696))), ((2.3506380046924784, 2.3506380046924784), (np.float64(0.7110248737782079), np.float64(0.7110248737782079))), ((2.7819765630061752, 2.7819765630061752), (np.float64(0.35191490772032175), np.float64(0.35191490772032175))), ((-0.699350887045334, -0.699350887045334), (np.float64(-0.6437210825807215), np.float64(-0.6437210825807215)))]

datensatz = [((-0.09960730650821059, -1.116585220802659), (np.float64(1.1473198780156248), np.float64(0.4486751598961371))), 
             ((-1.9726838675346254, -1.9841356261706178), (np.float64(3.0164698723682135), np.float64(3.4898120003759034))), 
             ((1.728975731475101, 0.8000785872816252), (np.float64(1.6276414469080815), np.float64(3.6860074121605266))), 
             ((1.5470855748512276, -0.19188915173904952), (np.float64(1.0365403598455418), np.float64(3.37511947579823))), 
             ((0.3146158897087714, -1.6490315648949698), (np.float64(3.028756339727261), np.float64(0.020827705290551682))), 
             ((-1.7323153168504248, 1.952639510128083), (np.float64(2.825816914745795), np.float64(2.628284819440867))), 
             ((-1.134425398286735, 0.9935344127078456), (np.float64(0.08081916249332821), np.float64(1.8326525630354218))), 
             ((1.8437097686559292, -1.4123913584875747), (np.float64(2.9578390501523986), np.float64(3.5570090568516126))), 
             ((-1.0509832509274362, 0.8775420472026374), (np.float64(-0.09783199879618076), np.float64(1.7436094511209261))),
               ((-0.7281253790765816, 1.28963631673891), (np.float64(0.9976902849137543), np.float64(0.8076368640070228)))]

datensatz = [((0.2928810235639485, 0.2928810235639485), (np.float64(0.2887117577277164), np.float64(0.2887117577277164))), ((1.2911361982345166, 1.2911361982345166), (np.float64(0.9611493081940838), np.float64(0.9611493081940838))), ((0.616580256429863, 0.616580256429863), (np.float64(0.5782485128461503), np.float64(0.5782485128461503))), ((0.2692990979813814, 0.2692990979813814), (np.float64(0.2660558622596657), np.float64(0.2660558622596657))), ((-0.45807120396657197, -0.45807120396657197), (np.float64(-0.4422189797345347), np.float64(-0.4422189797345347))), ((0.8753646783999365, 0.8753646783999365), (np.float64(0.7677772089015118), np.float64(0.7677772089015118))), ((-0.3744767324238447, -0.3744767324238447), (np.float64(-0.36578557449600696), np.float64(-0.36578557449600696))), ((2.3506380046924784, 2.3506380046924784), (np.float64(0.7110248737782079), np.float64(0.7110248737782079))), ((2.7819765630061752, 2.7819765630061752), (np.float64(0.35191490772032175), np.float64(0.35191490772032175))), ((-0.699350887045334, -0.699350887045334), (np.float64(-0.6437210825807215), np.float64(-0.6437210825807215)))]


values = training(0.01, 80_000, "leaky", generate_weights(((7, 7), (7, 7, 7, 7, 7, 7, 7), (7, 7, 7, 7, 7, 7, 7), (2, 2, 2, 2, 2, 2, 2)), 2), datensatz, 0.01, 0.005)

print(perzeptron(((0.2928810235639485, 0.2928810235639485), (np.float64(0.2887117577277164), np.float64(0.2887117577277164))), values))

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
