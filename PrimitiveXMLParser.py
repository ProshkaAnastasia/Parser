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
                    a.append(b1[1])
            answer[b[0]] = a
    return answer
    
def serialize(p, tab = "", listTag = ""):
    text = ""
    isRoot = False
    if isinstance(p, str):
        return tab + p + "\n"
    if tab == "" and len(p) != 1:
        text = "<root>\n"
        tab += "\t"
        isRoot = True
    if isinstance(p, dict):
        for i in p.keys():
            if isinstance(p[i], list):
                text += serialize(p[i], tab + "\t", i)
            else:
                text += tab +  "<" + i + ">\n" + serialize(p[i], tab + "\t") + tab + "</" + i + ">\n"
    if isinstance(p, list):
        for i in p:
            text += tab[ : len(tab) - 1] + "<" + listTag + ">\n"
            text += serialize(i, tab)
            text += tab[ : len(tab) - 1] + "</" + listTag + ">\n"
    if isRoot:
        text += "</root>"
    return text

"""file = open("file.xml", "r")
text = file.read()
file.close()
p = deserialize(text)
text = serialize(p)
print(text)"""