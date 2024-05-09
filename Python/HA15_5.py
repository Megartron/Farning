String = "'hello''by''bye''asdlkjqwer''qwertzuiopasdfghjklyxcvbnm''fakjsdhfaiuewhkjaffdgsdfgsdgdsfgdsfgfdshksjsdhfk''Qwert=uiopasdfghjkl#xcvbnm'"
def substring_suche(string: str) -> str: 
    for i in (sorted(string.split("'"), key=len, reverse=True)):
        if len(set(i)) == len(i):
            return i
print(substring_suche(String))