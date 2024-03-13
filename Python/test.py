















def __transformation(pos_intern):
    return (pos_intern[0], pos_intern[1])

sfecht = [[(0,2),(1,2),(2,2)],
        [(0,1),(1,1),(2,1)],
        [(0,0),(1,0),(2,0)]]
sf = [["O","",""],
    ["","O",""],
    ["","",""]]
EckenEcht = [(0, 2), (2, 2), (2, 0), (0, 0), (0, 2), (2, 2)]
EckenSF = [sfecht[0][2],sfecht[2][0],sfecht[2][2],sf[0][0]]
if sf[1][1] == "O":
    if ((sf[0][2] == "O" and sf[2][0] == "") or (sf[2][2] == "O" and sf[0][0] == "") or (sf[0][2] == "" and sf[2][0] == "O") or (sf[2][2] == "" and sf[0][0] == "O")):
        for i in EckenSF:
            if i == "O":
                g = sfecht[0][2]
                h = EckenEcht.index(g)
                print(EckenEcht[EckenEcht.index(sfecht)  + 2])