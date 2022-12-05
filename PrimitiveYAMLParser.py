def correctText(text):
    for i in range(len(text)):
        if text[i] not in [" ", "\t", "\n"]:
            text = text[i : ]
            break 
        if i == len(text) - 1:
            text = ""     
            #return text
    for i in reversed(range(len(text))):
        if text[i] not in [" ", "\t", "\n"]:
            text = text[0 : i + 1]
            break
    if len(text) != 0 and text[0] =="\"" and text[len(text) - 1] == "\"":
        text = text[1 : len(text) - 1]
    return text

def serialize(p, tab = ""):
    text = ""
    if isinstance(p, str):
        for i in range(len(p)):
            if p[i] == ":":
                return "'" + p + "'\n"
        return p + "\n"
    if isinstance(p, dict):
        text = "\n"
        for i in p.keys():
            text += tab  + i +  ": " + serialize(p[i], tab + "  ")
    if isinstance(p, list):
        text += "\n"
        for i in p:
            text += tab + "- "
            if len(p) == 1 and i == "":
                text += "\n"
                break
            text += serialize(i, tab + "  ")
            #text += "\n" + tab + "  "
    return text