from termcolor import colored
import re
import sys


dictionary = ["как бы", "собственно", "таким образом", "буквально", "как говорится", "так далее", "скажем", "ведь",
              "как его", "в натуре", "так вот", "короче", "как сказать", "видишь", "слышишь", "типа", "итак",
              "на самом деле", "вообще", "в общем-то", "в общем", "в некотором роде", "в принципе", "типа того", "вот",
              "как-бы", "ну", "то есть", "значит", "вроде"]

counter = {}


def updateDict():
    global dictionary
    file = open("dictionary.txt", "r", encoding="utf-8")
    dictionary = file.read().split(",")
    print(dictionary)


def getCounter():
    return counter


def get_len(coun, txt):
    try:
        result = coun[txt]
    except KeyError:
        result = -1
    return result


def choose(text, txt, color="white", int=0):
    if "." in txt or "," in txt or "?" in txt or "!" in txt:
        result = colored(txt[:len(txt) - 1], color) + txt[len(txt) - 1]
    else:
        result = text
    return int, result


def checker():
    updateDict()
    counter.clear()
    file = open("input.txt", mode="r", encoding="utf-8")
    text = file.read()
    file.close()
    result = text
    for i in range(len(dictionary)):
        help = dictionary[i]
        hell = text.lower().count(dictionary[i])
        if hell > 0:
            counter[help] = hell

    text = text.replace(".", "")
    text = text.replace(",", "")
    text = text.replace("?", "")
    text = text.replace("!", "")
    text = text.replace(" ", "_")
    text = text.lower()
    text = text.split('_')
    hel = result.replace(" ", "_")
    hel = hel.split('_')
    flag = True
    flagS = False
    flagPass = False
    file = open("output.txt", "w", encoding="utf-8")
    for i in range(len(text)):
        if flagPass:
            flagPass = False
            continue
        hell = 0
        for j in range(len(dictionary)):
            try:
                hell = counter[dictionary[j]]
            except KeyError:
                hell = -1

            try:
                help = text[i + 1].lower()
            except IndexError:
                help = ""

            youhoo = text[i].lower() + " " + help
            if (re.fullmatch(text[i].lower(), (dictionary[j])) and hell > 0) or \
                    (re.fullmatch(youhoo, dictionary[j]) and hell > 0):
                flag = False
                if re.fullmatch(youhoo, dictionary[j]):
                    flagS = True
        if flag:
            i, out = choose(text[i], hel[i], int=i)
            print(out, end=" ")
            file.write(hel[i] + " ")
        elif get_len(counter, text[i]) <= 5:
            if flagS:
                i, out = choose(colored(text[i] + " " + text[i + 1], "yellow"), hel[i], "yellow", int=i)
                print(out, end=" ")
                file.write(f"*{hel[i] + ' ' + hel[i + 1]}* ")
                flagPass = True
            else:
                i, out = choose(colored(text[i], "yellow"), hel[i], "yellow", int=i)
                print(out, end=" ")
                file.write(f"*{hel[i]}* ")
        elif get_len(counter, text[i]) > 5:
            if flagS:
                i, out = choose(colored(text[i] + " " + text[i + 1], "red"), hel[i], "red", int=i)
                print(out, end=" ")
                file.write(f"<{hel[i] + ' ' + hel[i + 1]}> ")
                flagPass = True
            else:
                i, out = choose(colored(text[i], "red"), hel[i], "red", int=i)
                print(out, end=" ")
                file.write(f"<{hel[i]}> ")

        flag = True
        flagS = False

    file.write("\n")
    for i in range(len(dictionary)):
        try:
            result = f"{dictionary[i]}: {counter[dictionary[i]]} \n"
            file.write(result)
        except KeyError:
            pass
    file.close()
    print()
    print(counter)
