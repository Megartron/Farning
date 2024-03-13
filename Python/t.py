sf = [["","","O"],
      ["","O",""],
      ["O","",""]]


def MittelschlauerComputer(sf):
    EckenComp = [(0, 2), (2, 2), (2, 0), (0, 0), (0, 2), (2, 2)]
    Ecken = [(0, 2), (2, 2), (2, 0), (0, 0)]
    SeitenComp = [(1, 2), (0, 1), (1, 0), (2, 1), (1, 2), (0, 1)]
    Seiten = [(1, 2), (0, 1), (2, 1), (1, 0)]
    Mitte = (1, 1)
    x = 0
    y = 0
    buch = {}

    o = "O"

    print(sf)
    mw = False

    if sf[1][1] == "O":
        if ((sf[0][2] == "O" and sf[2][0] == "") or (sf[2][2] == "O" and sf[0][0] == "") or (sf[0][2] == "" and sf[2][0] == "O") or (sf[2][2] == "" and sf[0][0] == "O")):
            return True
        
        elif (sf[1][2] == o and sf[1][0] == "") or (sf[0][1] == o and sf[2][1] == "") or (sf[1][2] == "" and sf[1][0] == "O") or (sf[0][1] == "" and sf[2][1] == "O"):
            return True
        elif (((sf[0][2] and sf[1][2]) == "O") and sf[2][2] == "") or (((sf[0][2] and sf[2][2]) == "O") and sf[1][2]) or (((sf[2][2] and sf[1][2]) == "0") and sf[0][2] == ""):
            return True
        elif (((sf[0][0] and sf[2][0]) == "O") and sf[1][0] == "") or (((sf[1][0] and sf[0][0]) == "O") and sf[2][0] == "" ) or (((sf[1][0] and sf[2][0]) == "0") and sf[0][0] == ""):
            return True
        elif ((sf[0][2] and sf[0][1]) == "O") or ((sf[0][0] and sf[0][1]) == "O") or ((sf[0][0] and sf[0][2]) == "0"):
            return True
    
    return False



print(MittelschlauerComputer(sf))