def Kann_gewinnen(reihe):
    gleich = 0
    leer = 0
    element = None
    for i in reihe:
        if i == "":
            leer += 1
        elif element == None:
        	element = "X" if i == "X" else "O"
        elif i == element:
            gleich += 1
    if gleich != 0 and leer != 0:
          return True
    else:
         return False

print(Kann_gewinnen(["","O","O"]))