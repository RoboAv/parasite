from termcolor import colored


def check():
    file = open("input.txt", mode="r", encoding="utf-8")
    text = file.read()
    dictionary = ["как бы", "собственно", "таким образом", "буквально", "как говорится", "так далее", "скажем", "ведь",
                  "как его", "в натуре", "так вот", "короче", "как сказать", "видишь", "слышишь", "типа",  "итак",
                  "на самом деле", "вообще", "в общем-то", "в общем", "в некотором роде", "в принципе", "типа того"]
    counter = {}
    for i in range(len(dictionary)):
        help = dictionary[i]
        hell = text.lower().count(dictionary[i])
        if hell > 0:
            counter[help] = hell
    text = text.replace(" ", "_")
    text = text.split('_')
    flag = True
    for i in range(len(text)):
        for j in range(len(dictionary)):
            try:
                hell = counter[dictionary[j]]
            except KeyError:
                hell = -1
            try:
                help = text[i + 1]
            except IndexError:
                help = ""
            if (text[i] in (dictionary[j]) and hell > 0) or \
                    (text[i] + help in dictionary[j] and hell > 0):
                flag = False
        if flag:
            print(text[i], end=" ")
        else:
            print(colored(text[i], "red"), end=" ")
        flag = True
    txt = colored(text[3], "yellow")
    file.close()
    file = open("output.txt", "w")
    file.write(txt)
    print()
    print(counter)


if __name__ == '__main__':
    check()