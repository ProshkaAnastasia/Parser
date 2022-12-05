import queue

class Tag:
    def __init__(self, i, name):
        self.end = i
        self.name = name

def dictFindKea(d, key):
    for i in d.keys():
        if i == key:
            return 1
    return 0

def correctText(text):
    for i in range(len(text)):
        if text[i] not in [" ", "\t", "\n"]:
            text = text[i : ]
            break      
    for i in reversed(range(len(text))):
        if text[i] not in [" ", "\t", "\n"]:
            text = text[0 : i + 1]
            break
    return text

def deserialize(text):
    text = correctText(text)
    id: int
    q = queue.LifoQueue()
    if len(text) == 0 or text[0] != "<":
        return text
    block = []
    for i in range(len(text)):
        if text[i] == "<":
            j = i + 1
            while text[j] != ">":
                j += 1
            tag = text[i : j + 1]
            if tag[ : 2] == "</":
                t = q.get()
                if q.empty():
                    if t.name == "<root>":
                        return deserialize(text[t.end + 1 : i])
                    #block[t.name[1 : len(t.name) - 1]] = deserialize(text[t.end + 1 : i])
                    block.append([t.name[1 : len(t.name) - 1], deserialize(text[t.end + 1 : i])])
            else:
                q.put(Tag(j, tag))
    answer = {}
    keys = {}
    for b in block:
        if dictFindKea(keys, b[0]):
            keys[b[0]] += 1
        else:
            keys[b[0]] = 1
    for b in block:
        if keys[b[0]] == 1:
            answer[b[0]] = b[1]
        else:
            a = []
            for b1 in block:
                if b1[0] == b[0]:
                    a.append([b1[1]])
            answer[b[0]] = a
    return answer
    
def serialize(p, tab = "", listTag = ""):
    text = ""
    if isinstance(p, str):
        return tab + "\t" + p + "\n"
    if tab == "":
        text = "<root>\n"
    if isinstance(p, dict):
        for i in p.keys():
            if isinstance(p[i], list):
                text += serialize(p[i], tab + "\t", i)
            else:
                text += tab + "\t" + "<" + i + ">\n" + serialize(p[i], tab + "\t") + tab + "\t" + "</" + i + ">\n"
    if isinstance(p, list):
        for i in p:
            text += tab + "<" + listTag + ">\n"
            text += serialize(i[0], tab)
            text += tab + "</" + listTag + ">\n"
    if tab == "":
        text += "</root>"
    return text

"""file = open("Schedule.xml", "r")
text = file.read()
file.close()
p = deserialize(text)
s = serialize(p)
print(s)"""

"""file = open("Schedule.xml", "r")
text = file.read()
file.close()
p = deserialize(text)
#print(p)
serialize(p)"""







def des(text):
    text = correctText(text)
    quoteCounter = 0
    id: int
    if text[0] != "<":
        return text
    q = queue.LifoQueue()
    for i in range(len(text)):
        if text[i] == ">":
            id = i + 1
            q.put(text[: i + 1])
    block = []
    for i in range(len(text)):
        if text[i] == "{" or text[i] == "[":
            q.put(text[i])
        if text[i] == "\"":
            quoteCounter += 1
        if text[i] == "</" and len(q.queue) == 1 and quoteCounter % 2 == 0:
            block.append(text[ind : i])
            ind = i + 1
        if text[i] == "}" or text[i] == "]":
            q.get()
    block.append(text[ind : len(text) - 2])
    interAnswer = []
    for b in block:
        interAnswer.append(b.split(": ", 1))
    answer = {}
    a = []
    if text[0] == "{":
        for ia in interAnswer:
            answer[correctText(ia[0])] = des(ia[1])
        return answer
    if text[0] == "[":
        for b in block:
            a.append([des(b)])
        return a