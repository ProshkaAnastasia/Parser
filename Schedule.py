import requests
import re
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

weekDays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

class Time:
    def __init__(self, time, week):
        if time == None:
            self.t = ""
        else:
            self.t = correctText(time.group())
        if week == None:
            self.week = ""
        else:
            self.week = correctText(week.group())

    def __str__(self):
        return self.t + "\n" + self.week

class Room:
    def __init__(self, room, location):
        if room == None:
            self.number = ""
        else:
            self.number = correctText(room.group())
        if location == None:
            self.location = ""
        else:
            self.location = correctText(location.group())

    def __str__(self):
        return self.number + "\n" + self.location

class Lesson:
    def __init__(self, name, teacher, format):
        if name == None:
            self.name = ""
        else:
            self.name = correctText(name.group())
        if teacher == None:
            self.teacher = ""
        else:
            t = teacher.group()
            t = re.sub(r'\n', "", t)
            t = re.sub(r'^\s+', "", t)
            t = re.sub(r'\s+$', "", t)
            self.teacher = t
        if format == None:
            self.format = ""
        else:
            self.format = correctText(format.group())

    def __str__(self):
        return self.name + "\n" + self.teacher + "\n" + self.format + "\n"

class TagInd:
    def __init__(self, tag, ind):
        self.tag = tag
        self.ind = ind

class LessonFormat:
    def __init__(self, code):
        q = queue.LifoQueue()
        i = 0
        while i < len(code):
            if code[i] == "<":
                j = i
                while code[j] != ">":
                    j += 1
                s = code[i : j + 1]
                if s[0:2] == "</":
                    tag = q.get()
                    if tag.tag == "<td class=\"time\">":
                        self.parseTime(code[tag.ind : j + 1])
                    if tag.tag == "<td class=\"room\">":
                        self.parseRoom(code[tag.ind : j + 1])
                    if tag.tag == "<td class=\"lesson\">":
                        self.parseLesson(code[tag.ind : j + 1])
                    if tag.tag == "<th class=\"day\">":
                        self.parseDay(code[tag.ind : j + 1])
                else:
                    q.put(TagInd(s, i))
                i += len(s)
            else:
                i += 1

    def print(self):
        print(self.day + "\n")
        print(self.time)
        print(self.room)
        print(self.lesson)

    def parseTime(self, text):
        pattern = r'(?<=<span>).+?(?=</span>)'
        time = re.search(pattern, text)
        pattern = r'(?<=<div>).+?(?=</div>)'
        week = re.search(pattern, text)
        self.time = Time(time, week)
        #print(self.time)


    def parseRoom(self, text):
        pattern = r'(?<=<dd>).+?(?=</dd>)'
        room = re.search(pattern, text)
        pattern = r'(?<=<span>).+?(?=</span>)'
        location = re.search(pattern, text)
        self.room = Room(room, location)
        #print(self.room)


    def parseLesson(self, text):
        pattern = r'(?<=<dd>).+?(?=</dd>)'
        lesson = re.search(pattern, text)
        pattern = r'(?<=<dt><b>)(?:.*\n)*?.+?(?=</b></dt>)'
        teacher = re.search(pattern, text)
        pattern = r'(?<=<td class=\"lesson-format\">).+?(?=</td>)'
        format = re.search(pattern, text)
        self.lesson = Lesson(lesson, teacher, format)
        #print(self.lesson)

    def parseDay(self, text):
        pattern = r'(?<=<span>).+?(?=</span>)'
        day = re.search(pattern, text)
        if (day != None):
            self.day = day.group()
        else:
            self.day = ""
        #print(self.day)



class DaySchedule:
    def __init__(self, dayCode, day):
        self.day = day
        self.classes = []
        self.parseHtml(dayCode)

    def parseHtml(self, dayCode):
        pattern = r"<tbody>(?!<tr>)"
        dayCode = re.sub(pattern, "<tbody><tr>", dayCode)
        pattern = r"<tr(?:.+\n+)*?.+\/tr>"
        match = re.findall(pattern, dayCode)
        for i in match:
            self.classes.append(LessonFormat(i))

    def print(self):
        for i in self.classes:
            i.print()
        

class Schedule:
    def __init__(self, group):
        reference = 'https://itmo.ru/ru/schedule/0/' + str(group) + '/raspisanie_zanyatiy_' + str(group) + '.htm'
        r = requests.get(reference)
        #file = open("code.txt", "w")
        #file.write(r.text)
        s = r.text
        pattern = r"<table(.+\n)*?.+\/table>"
        match = re.finditer(pattern, s)
        days = []
        self.days = {"Понедельник" : [], "Вторник" : [], "Среда" : [], "Четверг" : [], "Пятница" : [], "Суббота" : [], "Воскресенье" : []}
        for i in match:
            days.append(i.group())
        for i in days:
            match = re.search(r'<table id=..', i)
            if match != None:
                g = match.group()
                j = int(g[len(g) - 1: ])
                self.days[weekDays[j - 1]].append(DaySchedule(i, weekDays[j - 1]))

    def print(self, day):
        for i in self.days[day]:
            i.print()

def convertToJSON(fullSchedule, day):
    file = open("Schedule.json", 'w')
    text = "{\n\t"
    schedule = fullSchedule.days[day]
    text += "\"Day\": \"" + day + "\",\n\t"
    text += "\"Lesson\": [\n"
    for day in schedule:
        date = ""
        for lesson in day.classes:
            #text += "\"День\": \"" + lesson.day + "\",\n\t\t\t"
            text += "\t\t{\n\t\t\t"

            text += "\"Time_Week\": {\n\t\t\t\t"
            if len(lesson.day) > 3:
                date += "\"Date\": \"" + lesson.day + "\",\n\t\t\t\t"
            text += date
            text += "\"Time\": \"" + lesson.time.t + "\",\n\t\t\t\t"
            text += "\"Week\": \"" + lesson.time.week + "\"\n\t\t\t},\n\t\t\t"

            text += "\"Room_Building\": {\n\t\t\t\t"
            text += "\"Room\": \"" + lesson.room.number + "\",\n\t\t\t\t"
            text += "\"Building\": \"" + lesson.room.location + "\"\n\t\t\t},\n\t\t\t"

            text += "\"Class_Teacher\": {\n\t\t\t\t"
            text += "\"Class\": \"" + lesson.lesson.name + "\",\n\t\t\t\t"
            text += "\"Teacher\": \"" + lesson.lesson.teacher + "\",\n\t\t\t\t"
            text += "\"Format\": \"" + lesson.lesson.format + "\"\n\t\t\t}\n\t\t},\n"
        text = text[ : len(text) - 2]
        text += ",\n"
    text = text[ : len(text) - 2]
    text += "\n\t]\n}"
    file.write(text)
    file.close()

def convertToXML(fullSchedule, day):
    file = open("Schedule.xml", 'w')
    text = "<root>\n\t"
    text += "<Day>" + day + "</Day>\n\t"
    schedule = fullSchedule.days[day]
    for day in schedule:
        date = ""
        for lesson in day.classes:
            #text += "\"День\": \"" + lesson.day + "\",\n\t\t\t"
            text += "<Lesson>\n\t\t"

            if len(lesson.day) > 3:
                date += "<Date>" + lesson.day + "</Date>\n\t\t\t"

            text += "<Time_Week>\n\t\t\t"
            text += date
            text += "<Time>" + lesson.time.t + "</Time>\n\t\t\t"
            text += "<Week>" + lesson.time.week + "</Week>\n\t\t"
            text += "</Time_Week>\n\t\t"

            text += "<Room_Building>\n\t\t\t"
            text += "<Room>" + lesson.room.number + "</Room>\n\t\t\t"
            text += "<Building>" + lesson.room.location + "</Building>\n\t\t"
            text += "</Room_Building>\n\t\t"

            text += "<Class_Teacher>\n\t\t\t"
            text += "<Class>" + lesson.lesson.name + "</Class>\n\t\t\t"
            text += "<Teacher>" + lesson.lesson.teacher + "</Teacher>\n\t\t\t"
            text += "<Format>" + lesson.lesson.format + "</Format>\n\t\t"
            text += "</Class_Teacher>\n\t"

            text += "</Lesson>\n\t"
    text += "</root>"
    file.write(text)
    file.close()

"""def convertToJSON(fullSchedule, day):
    file = open("Schedule.json", 'w')
    text = "{\n\t"
    schedule = fullSchedule.days[day]
    text += "\"Day\": \"" + day + "\",\n\t"
    text += "\"Lesson\": [\n"
    for day in schedule:
        for lesson in day.classes:
            #text += "\"День\": \"" + lesson.day + "\",\n\t\t\t"
            text += "\t\t{\n\t\t\t"

            text += "\"Time_Week\": {\n\t\t\t\t"

            text += "\"Time\": \"" + lesson.time.t + "\",\n\t\t\t\t"
            text += "\"Week\": \"" + lesson.time.week + "\"\n\t\t\t},\n\t\t\t"

            text += "\"Room_Building\": {\n\t\t\t\t"
            text += "\"Room\": \"" + lesson.room.number + "\",\n\t\t\t\t"
            text += "\"Building\": \"" + lesson.room.location + "\"\n\t\t\t},\n\t\t\t"

            text += "\"Class_Teacher\": {\n\t\t\t\t"
            text += "\"Class\": \"" + lesson.lesson.name + "\",\n\t\t\t\t"
            text += "\"Teacher\": \"" + lesson.lesson.teacher + "\",\n\t\t\t\t"
            text += "\"Format\": \"" + lesson.lesson.format + "\"\n\t\t\t}\n\t\t},\n"
        text = text[ : len(text) - 2]
        text += ",\n"
    text = text[ : len(text) - 2]
    text += "\n\t]\n}"
    file.write(text)
    file.close()"""

def convertToYAML(fullSchedule, day):
    file = open("Schedule.yaml", 'w')
    text = ""
    schedule = fullSchedule.days[day]
    text += "Day: " + day + "\n"
    text += "Lesson:\n"
    for day in schedule:
        date = ""
        for lesson in day.classes:
            #text += "\"День\": \"" + lesson.day + "\",\n\t\t\t"
            text += "  - "

            if len(lesson.day) > 3:
                date += "      Date: " + lesson.day + "\n"

            text += "Time_Week:\n"
            text += date
            text += "      Time: " + lesson.time.t + "\n"
            text += "      Week: " + lesson.time.week + "\n"

            text += "    Room_Building:\n"
            text += "      Room: " + lesson.room.number + "\n"
            text += "      Building: " + lesson.room.location + "\n"

            text += "    Class_Teacher:\n"
            text += "      Class: " + lesson.lesson.name + "\n"
            text += "      Teacher: " + lesson.lesson.teacher + "\n"
            text += "      Format: " + lesson.lesson.format + "\n"
    file.write(text)
    file.close()