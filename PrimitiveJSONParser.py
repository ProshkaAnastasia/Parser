import queue


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

def deserialize(text):
    text = correctText(text)
    quoteCounter = 0
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
        if p.isdigit() or p == "true" or p == "false":
            return p
        else:
            return "\"" + p + "\""
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

