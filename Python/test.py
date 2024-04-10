
x = 0
y = 0
sfechtpos = 0
def __transformation(pos_intern):
    return (pos_intern[0], pos_intern[1])

sfecht = [[(0,2),(1,2),(2,2)],
        [(0,1),(1,1),(2,1)],
        [(0,0),(1,0),(2,0)]]
sf = [["","",""],
    ["","O",""],
    ["O","",""]]
EckenEcht = [(0, 2), (2, 2), (2, 0), (0, 0), (0, 2), (2, 2)]
EckenSF = [sf[0][2],sf[0][0],sf[2][0],sf[2][2]]
if sf[1][1] == "O":
    if ((sf[0][2] == "O" and sf[2][0] == "") or (sf[2][2] == "O" and sf[0][0] == "") or (sf[0][2] == "" and sf[2][0] == "O") or (sf[2][2] == "" and sf[0][0] == "O")):
        for i in EckenSF:
            if i == "O":
                if EckenSF.index(i) <= 1:
                    x = 0
                else:
                    x = 2
                y = sf[x].index(i)
                sfechtpos = sfecht[x][y]
                print(EckenEcht[EckenEcht.index(sfechtpos)  + 2])
elif sf[1][1] == "":
         if(((sf[0][2] and sf[2][0]) or (sf[2][2] and sf[0][0])) == "O"):
              print(1,1)