import re
import queue

floatPattern = re.compile(r"[-+]?[0-9]*[.,][0-9]+(?:[eE][-+]?[0-9]+)?")
intPattern = re.compile(r"[+-]?\d+")
#strPattern = re.compile(r"(\"(?:[^\\']|\\['\\/bfnrt]|\\u[0-9a-fA-F]{4})*?\")\s*(.*)")

def correctText(text):
    text = re.sub(r"(?<=\A)(?:\s|\n)*\"*", "", text)
    text = re.sub(r"\"*(?:\s|\n)*$", "", text)
    return text

def checkValid(text):
    qCounter = 0
    bCounter = 0
    eCounter = 0
    text = re.sub("\s+", "", text)
    if text[0] != "{" or text[len(text) - 1] != "}":
        return False
    id = 0
    for i in range(len(text)):
        if text[i] == "\"" and text[i - 1] != "\\":
            if qCounter % 2 == 0:
                if re.search(r"(?<=[,:\{]),", text[id: i]) != None:
                    #print(text[id, i])
                    return False
            else:
                id = i + 1
            qCounter += 1
        if text[i] == "{":
            bCounter += 1
        if text[i] == "}":
            eCounter += 1
        
    if bCounter != eCounter:
        return False
    if re.search(r"}{", text) != None:
        #print(".")
        return False
    if re.search(r"}{", text) != None:
        #print("?")
        return False
    if re.search(r"\]\[", text) != None:
        #print("!")
        return False
    if re.search(r"}\"", text) != None:
        return False
    if re.search(r"\"{", text) != None:
        return False
    if re.search(r",(?=\})", text) != None:
        return False
    
    #print(qCounter)

    return True


def deserialize(text):
    text = correctText(text)
    quoteCounter = 0
    if intPattern.fullmatch(text) != None:
        return int(text)
    if floatPattern.fullmatch(text) != None:
        return float(text)
    #if strPattern.match(text) != None:
        #return text[1 : len(text) - 1]
    if len(text) == 0 or text[0] not in ["{", "["]:
        return text

    q = queue.LifoQueue()
    ind = 1
    block = []
    for i in range(len(text)):
        if text[i] == "{" or text[i] == "[":
            q.put(text[i])
        if text[i] == "\"":
            quoteCounter += 1
        if text[i] == "," and len(q.queue) == 1 and quoteCounter % 2 == 0:
            block.append(text[ind : i])
            ind = i + 1
        if text[i] == "}" or text[i] == "]":
            q.get()
    block.append(correctText(text)[ind : len(text) - 1])
    interAnswer = []
    for b in block:
        interAnswer.append(b.split(":", 1))
    answer = {}
    a = []
    if text[0] == "{":
        for ia in interAnswer:
            answer[(correctText(ia[0]))] = deserialize(ia[1])
        return answer
    if text[0] == "[":
        for b in block:
            a.append(deserialize(b))
        return a

def serialize(p, tab = ""):
    text = ""
    if isinstance(p, str):
        return "\"" + p + "\""
    if isinstance(p, float):
        return str(p)
    if isinstance(p, int):
        return str(p)
    if isinstance(p, dict):
        text = "{\n"
        for i in p.keys():
            text += tab + "\t" + "\"" + i + "\"" + ": " + serialize(p[i], tab + "\t") + ",\n"
        text = text[ : len(text) - 2] + "\n"
        text += tab + "}"
    if isinstance(p, list):
        text = "[\n" + tab + "\t"
        for i in p:
            if len(p) == 1 and i == "":
                text += "\n"
                break
            text += serialize(i, tab + "\t")
            text += ",\n" + tab + "\t"
        if text[len(text) - 1] == "\t":
            text = text[ : len(text) - len(tab) - 3] + "\n"
        text += tab + "]" 
    return text

def Deserialize(text):
    if checkValid(text):
        return deserialize(text)
    else:
        print("Deserialization failed. File format is unacceptable.")
