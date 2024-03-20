sf = [["","",""],
      ["","",""],
      ["","",""]]
symbol = "O"

def Diagonale(sf, symbol):
    if sf[1][1] == symbol:
            if ((sf[0][2] == symbol and sf[2][0] == "") or (sf[2][2] == symbol and sf[0][0] == "") or (sf[0][2] == "" and sf[2][0] == symbol) or (sf[2][2] == "" and sf[0][0] == symbol)):
                return True
    elif sf[1][1] == "":
         if(((sf[0][2] and sf[2][0]) or (sf[2][2] and sf[0][0])) == symbol):
              return True
    return False

print(Diagonale(sf, symbol))