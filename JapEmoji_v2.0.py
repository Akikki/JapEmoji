import sys
from random import random

import PySimpleGUI as sg
import pyperclip as pc
import itertools as it
import json
import keyboard

with open('config.json', "r+", encoding="utf8") as j:
    config = json.load(j)

# ------ GUI basics ----- #
sg.theme("DarkGrey2")

# favorite_column = [[sg.Button("1"), sg.Button("a")], [sg.Button("2")]]
# all_column = [[sg.Button("3")], [sg.Button("4")]]
# recent_column = [[sg.Button("5")], [sg.Button("6")]]
favorite_column = []
all_column = []
recent_column = []
f_mode = False
if config["expand"] == "True":
    expand_factor = True
else:
    expand_factor = False

# ----- General LISTS ----- #
favorites = []
buttons = []
all_list = config["emotes"]
# emotes = ["(* ^ ω ^)", "(´ ∀ ` *)", "(´｡• ω •｡`)", "(✧ω✧)", "(//ω//)", "(＃＞＜)", "(＞ｍ＜)"]
letters = ["g", "e", "f"]


# ----- BUTTON class ----- #
class Button:
    # num = it.count()
    d_num = {
        "all": it.count(),
        "favorite": it.count()
    }

    def __init__(self, name, lists=1):

        global special
        d_index = {
            "all": -1,
            "favorite": -1
        }
        match lists:
            case 1:
                list_name = all_column
                index = d_index["all"]
                self.num = next(self.d_num["all"])
                special = "-DEFAULT-"
            case 2:
                list_name = favorite_column
                index = d_index["favorite"]
                self.num = next(self.d_num["favorite"])
                special = "-FAV-"
            case _:
                list_name = all_column
                index = d_index["all"]
                self.num = next(self.d_num["all"])
                special = "-DEFAULT-"

        # self.num = next(num)
        self.name = name
        if self.num % 3 == 0:
            index += 1
            list_name.append([sg.Button(self.name, key=("-COPY-", self.name, self.num, special), expand_x=expand_factor,
                                        expand_y=expand_factor)])
        else:
            list_name[index].append(
                sg.Button(self.name, key=("-COPY-", self.name, self.num, special), expand_x=expand_factor,
                          expand_y=expand_factor))

    def getId(self):
        return self.num

    def getName(self):
        return self.name

    def addFavorite(self):
        favorites.append(self.name)
        # favorite_column.append([sg.Button(self.name, key=("-COPY-", self.name, self.num))])
        print("Favorite Added")


# ----- FUNCTIONS ----- #
def GenerateFromList(elist):
    c = 0
    for E in elist:
        b = Button(E)
        buttons.append(b)
        c += 1
    return f"Added {c} buttons"


def CreateWindow():
    layout = [[sg.Column(favorite_column, expand_x=expand_factor, expand_y=expand_factor),
               sg.VSeparator(),
               sg.Column(all_column, expand_x=expand_factor, expand_y=expand_factor)],
              [sg.Button("★", expand_x=expand_factor, expand_y=expand_factor),
               sg.Button("Add", expand_x=expand_factor, expand_y=expand_factor),
               sg.Button("Save", expand_x=expand_factor, expand_y=expand_factor),
               sg.Button("Expand", expand_x=expand_factor, expand_y=expand_factor),
               sg.Button("Help", button_color="LightYellow3", expand_x=expand_factor, expand_y=expand_factor)]]
    return sg.Window("Emoji", layout, resizable=True)


def CreatePopUpEmotes():
    layout = [[sg.Text('Emotes will be added after next restart')],
              [sg.Text('Enter Emote here'), sg.InputText(key="-EMOTE_INPUT-", do_not_clear=False)],
              [sg.Button('OK'), sg.Button('Close')]]
    return sg.Window("Emoji", layout)


def CheckFavorite(name):
    for k in favorites:
        if name == k:
            return True
        else:
            pass
    return False


def RemoveFavorite(name):
    favorites.remove(name)
    # favorite_column.remove(sg.Button(self.name, key=("-COPY-", self.name, self.num)))
    print(f"Favorite Removed {name}")


def GenerateFavorite():
    if len(config["favorites"]) != 0:
        c = 0
        for C in config["favorites"]:
            b = Button(C, 2)
            favorites.append(b.getName())
            c += 1
        return f"Added {c} buttons"
    else:
        return "List is empty"


def AddEmoji(emoji):
    all_list.append(emoji)


# ----- UTILS ----- #
def CreateVariable(name):
    globals()[f'{name}'] = []
    return name


def CleanList(slist):
    temp_list = set(slist)
    slist = list(temp_list)
    return slist


# ----- PRE loader ----- #
GenerateFromList(config["emotes"])
GenerateFavorite()


# ----- EVENT loop----- #
def StartGui(title="Emoji Paster"):
    window = CreateWindow()

    while True:
        # Dum code, but if not here the first Shift doesn't register, god know why
        if keyboard.is_pressed("shift"):
            pass

        event, values = window.read()
        global f_mode, expand_factor
        if event == sg.WIN_CLOSED:
            break
        if event[0] == "-COPY-":
            if keyboard.is_pressed("shift"):
                all_list.remove(event[1])
                sg.popup(f"The emote {event[1]} has been removed")
                # AskConfirm()
            else:
                if f_mode:
                    if event[3] == "-FAV-":
                        try:
                            RemoveFavorite(event[1])
                        except ValueError:
                            sg.popup("Favorite was already removed. Use the SAVE button to refresh !")
                    else:
                        if CheckFavorite(event[1]):
                            print("Favorite already exist")
                        else:
                            buttons[event[2]].addFavorite()
                else:
                    pc.copy(event[1])
        if event == "★":
            if f_mode:
                f_mode = False
                window[event].update(button_color=(sg.theme_button_color_text(), sg.theme_button_color_background()))
            else:
                f_mode = True
                window[event].update(button_color=("#2b2b28", "Greenyellow"))
        if event == "Save":
            window.close()
            sg.popup("Please restart program for changes to take effect")
            config["favorites"] = favorites
            config["emotes"] = all_list
            with open('config.json', "w", encoding="utf8") as f:
                json.dump(config, f, ensure_ascii=False)
            sys.exit()
        if event == "Add":
            emotes_window = CreatePopUpEmotes()
            while True:
                event, values = emotes_window.read()
                if event == sg.WIN_CLOSED or event == "Close":
                    break
                if event == "OK":
                    AddEmoji(values["-EMOTE_INPUT-"])
                    sg.popup("Your Emote has been Added")
            emotes_window.close()
        if event == "Help":
            if keyboard.is_pressed("shift"):
                sg.popup("HEY ! Dont remove me, I'm here to help you !")
            else:
                sg.popup("To ADD to FAVORITE, press ★ and click on the buttons you want to add, than press SAVE. \n"
                         "To REMOVE from FAVORITE, press FAV and click on the favorite buttons you want to remove, "
                         "then press SAVE.  \n "
                         "To REMOVE from ALL, press SHIFT and LEFT CLICK on the button you want to remove, than press "
                         "SAVE.\n"
                         "To TOGGLE the SCALING of elements, press EXPEND, than SAVE")
        if event == "Expand":
            if not expand_factor:
                expand_factor = True
                config["expand"] = "True"
                sg.popup("Expand has been Enabled, please SAVE and restart")
            else:
                expand_factor = False
                config["expand"] = "False"
                sg.popup("Expand has been Disabled, please SAVE and restart")

    window.close()


# ----- START GUI ----- #
StartGui()

"""
TO DO:
- Settings GUI:
    - Enable pop up on favorite add
    - Change expand
    - Change number of button per line
    - Change colors and theme and such
- Modern UI
- Scalable window
- Confirmation on Remove
"""
