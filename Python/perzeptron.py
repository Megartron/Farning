def lernen(a, x, y, y_wahr):
    return x * a * (y - y_wahr)


def alpha(w1, w2, y, y_wahr, x1, x2, b):
    werte_w_und_b = []
    
    for a in [0.01, 0.1, 1, 10]:
        w1_neu = w1 - lernen(a, x1, y, y_wahr)
        w2_neu = w2 - lernen(a, x2, y, y_wahr)
        b_neu = b - lernen(a, 1, y, y_wahr)
        
        werte_w_und_b.append((w1_neu, w2_neu, b_neu))

        

    #print(werte_w)

    werte_y = []
    y_neu = 0
    for w1_n, w2_n, b_n in werte_w_und_b:
        y_neu = w1_n * x1 + w2_n * x2 + b_n
        werte_y.append(y_neu)

    #print (werte_y)
    
    fehler = []
    for i in werte_y:
        fehler.append((i - y_wahr)**2)

    #print(fehler)

    return fehler.index(min(fehler))


def perzeptron(w1, w2, Testwerte, a, b):
    y = 0
    for i in range(500):
        for x1, x2, y_wahr in Testwerte:
            y = w1 * x1 + w2 * x2 + b
            
            # a finden
            a = 0.01 * 10**(alpha(w1, w2, y, y_wahr, x1, x2, b))
            #print(a)

            # lernen
            w1 = w1 - lernen(a, x1, y, y_wahr)
            w2 = w2 - lernen(a, x2, y, y_wahr)
            b = b - lernen(a, 1, y, y_wahr)
        
    
    return (w1, w2, b)


Test = [(1, 1, 1), (0, 0, -1)]

print(perzeptron(0, 0, Test, 0.1, 0))

"""
alpha(w1, w2, y, y_wahr, x1, x2, b)"""
#alpha(0,  0, -1, 1,      1,  1, -1)