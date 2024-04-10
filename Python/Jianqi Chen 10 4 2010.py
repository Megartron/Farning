intern_spielfeld = [["","",""],
              ["","",""],
              ["","",""]]

spielffeld_x = None 
spielffeld_y = None

def lesen(spielfeld_x, spielfeld_y, spielfeld):
    return spielfeld[(spielfeld_y//200) * -1 + 2][spielfeld_x//200]
def schreiben(spielfeld_x, spielfeld_y):
    return(spielfeld_x//200, (spielfeld_y//200) * -1 + 2)