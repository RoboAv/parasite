from termcolor import colored
import re

dictionary = ["как бы", "собственно", "таким образом", "буквально", "как говорится", "так далее", "скажем", "ведь",
              "как его", "в натуре", "так вот", "короче", "как сказать", "видишь", "слышишь", "типа", "итак",
              "на самом деле", "вообще", "в общем-то", "в общем", "в некотором роде", "в принципе", "типа того", "вот",
              "как-бы", "ну", "то есть"]


def get_len(coun, txt):
    try:
        result = coun[txt]
    except KeyError:
        result = -1
    return result


def choose(text, txt, color="white"):
    result = ""
    if "." in txt or "," in txt or "?" in txt or "!" in txt:
        result = colored(txt[:len(txt) - 1], color) + "."
    else:
        result = text
    return result


def checker():
    file = open("input.txt", mode="r", encoding="utf-8")
    text = file.read()
    file.close()
    counter = {}
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
    text = text.split('_')
    hel = result.replace(" ", "_")
    hel = hel.split('_')
    flag = True
    flagS = False
    file = open("output.txt", "w")
    for i in range(len(text)):
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
            yoohoo = text[i].lower() + " " + help
            if (re.fullmatch(text[i].lower(), (dictionary[j])) and hell > 0) or \
                    (re.fullmatch(yoohoo, dictionary[j]) and hell > 0):
                flag = False
                if re.fullmatch(yoohoo, dictionary[j]):
                    flagS = True
        if flag:
            if flagS:
                try:
                    print(choose(text[i] + " " + text[i + 1], hel[i]), end=" ")
                except IndexError:
                    pass
            else:
                print(choose(text[i], hel[i]), end=" ")
            file.write(hel[i])
        elif get_len(counter, text[i]) <= 5:
            if flagS:
                print(choose(colored(text[i] + " " + text[i + 1], "yellow"), hel[i], "yellow"), end=" ")
            else:
                print(choose(colored(text[i], "yellow"), hel[i], "yellow"), end=" ")
            file.write(f"{hel[i]}")
        else:
            if flagS:
                print(choose(colored(text[i] + " " + text[i + 1], "red"), hel[i], "red"), end=" ")
            else:
                print(choose(colored(text[i], "red"), hel[i], "red"), end=" ")
            file.write(hel[i])
        flag = True
        flagS = False
    for i in range(len(dictionary)):
        try:
            result = f"{dictionary[i]}: {counter[dictionary[i]]} \n"
            file.write(result)
        except KeyError:
            pass
    file.close()
    print()
    print(counter)


if __name__ == '__main__':
    checker()
