from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.completion import Completer
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit import prompt
import os
import json
import random
from typing import List


class Welcome:
    def __init__(self, width=50, sep="-"):
        self._message = "\\  CommandLearner /"
        self._width = width
        self._seperator = sep

        self.printWelcome()
        self.displayBanks()

    def __str__(self):
        return self._selected

    # Print Initial Welcome Message
    def printWelcome(self) -> None:
        print("".center(self._width, self._seperator))
        print(self._message.center(self._width, self._seperator))
        print("LEARN".center(self._width, self._seperator))
        print("".center(self._width, self._seperator) + "\n")

    #Returns avaliable question banks
    #Question banks always located in folder "banks", respective of where learn.py is executed
    def displayBanks(self) -> None:
        local_contents = os.listdir(os.getcwd() +  "\\banks\\")
        for file in local_contents:
            if file.endswith(".json"):
                print_formatted_text(HTML("--> <green>" + file[:-5] + "</green>"))


    #_selected banks is a CSV variable. CSV variable is NOT split up in this function
    def setBank(self) -> None:
        selected_bank = prompt("Enter selected command banks: ")
        self._selected_bank = selected_bank


class Enviroment():
    _correct_answer = 0
    _total_answer = 0

    def __init__(self,
                 welcome: int) -> None:
        self._width = welcome._width
        self._seperator = welcome._seperator
        self.loadBank()


    def loadBank(self) -> None:
        bank_dir = os.getcwd() + "\\banks\\"
        question_bank = welcome._selected_bank

        self._bank = list()
        for bank in question_bank.split(","):
            with open(bank_dir + bank + ".json") as full_bank_path:
                bank_json = json.load(full_bank_path)
                self._bank += bank_json['items']


    def testBegin(self) -> None:
        random.shuffle(self._bank)
        print("\n" * 40)

        for question_info in self._bank:
            self.individualTest(question_info)
            input("Press Enter to continue")
            print("\n" * 40)

        print_formatted_text(HTML("<yellow>" + "You got " + str(Enviroment._correct_answer) + " out of " + str(Enviroment._total_answer) + " correct" + "</yellow>"))


    """
    Responsible for testing individual questions. Primarily gets "base" command (refer below) and checks to see if that is corrected.
    """
    def individualTest(self,
                       question_info: List) -> None:
        question = question_info['question']
        level_number = question_info['level']
        short_answer = question_info['short_answer']
        full_answer = question_info['full_answer']

        print_formatted_text(HTML("<blue>" + question + "</blue>"))
        user_answer, user_level = self.getBaseCommand()
        self.answerLogic(user_answer,user_level, full_answer, short_answer, level_number)


    """
    Responsible for breaking down what the user entered to return the "base" command and the level which that would be entered at.
    Base command is what answer is evaluated on
    Level0 = User
    Level1 = Privilege Executive
    Level2 = Global Configuration
    Level3 = Sub configuration mode. No distinction made between seperate sub-config modes made in this version
    """
    def getBaseCommand(self,
            prompt_icon: str=">",
            level: int=0) -> (str, int):

        level_prompt = {
            0: ">",
            1: "#",
            2: "Hostname(config)#",
            3: {
                "router": "Hostname(config-router)#",
                "line": "Hostname(config-line)#",
                "interface": "Hostname(config-interface)#",
                "vlan": "Hostname(config-vlan)#",
                "vrf": "Hostname(config-vrf)#",
                "access-list-std": "Hostname(config-std-nacl)#",
                "access-list-ext": "Hostname(config-ext-nacl)#",
            }
        }

        while True:
            answer = prompt(prompt_icon)

            #Exit Logic
            if answer == "exit":
                level -= 1
                if level >= 0:
                    prompt_icon = level_prompt[level]
                    continue
                else:
                    break


            #Support raw command usage
            if answer.split(" ")[0] == "cmd:":
                answer = answer.split(" ")[1]
                break


            #Hierarchy Logic - not particularly efficient or readable, hope to break down (seperate logic for each level) in future updates
            if answer == "enable":
                level = 1
                prompt_icon = level_prompt[level]
            elif answer == "config t":
                level = 2
                prompt_icon = level_prompt[level]
            else:
                answer_selector = answer.split(" ")[0]
                if answer_selector == "line":
                    level = 3
                    prompt_icon = level_prompt[level]['line']
                elif answer_selector == "router":
                    level = 3
                    prompt_icon = level_prompt[level]['router']
                elif answer_selector == "vrf":
                    level = 3
                    prompt_icon = level_prompt[level]['vrf']
                elif answer_selector == "vlan":
                    level = 3
                    prompt_icon = level_prompt[level]['vlan']
                elif answer_selector == "int" or answer_selector == "interface":
                    level = 3
                    prompt_icon = level_prompt[level]['interface']
                elif answer_selector == "ip":
                    level = 3

                    #Access-List sub-configuration related commands, eg ip access-list standard
                    answer_selector = answer.split(" ")[1]
                    if answer_selector == "access-list":
                        answer_selector = answer.split(" ")[2]
                        if answer_selector == "standard" or answer_selector == "std":
                            prompt_icon = level_prompt[level]['access-list-std']
                        elif answer_selector == "extended" or answer_selector == "ext":
                            prompt_icon = level_prompt[level]['access-list-ext']
                else:
                    break

        return answer, level


    def answerLogic(self, user_answer, user_level, answer_full, answer_short, answer_level):
        def levelToStr(level: int) -> str:
            level = int(level)
            if level == 0:
                level_str = "User Executive"
            elif level == 1:
                level_str = "Privileged Executive"
            elif level == 2:
                level_str = "Global Configuration"
            elif level == 3:
                level_str = "Sub Configuration mode"
            else:
                level_str = "Undetermined"

            return level_str

        user_answer = user_answer.split(" ")
        answer_short = answer_short.split(" ")

        correct = True

        for i in range(len(answer_short)):
            if answer_short[i] in user_answer[i]:
                continue
            else:
                correct = False
                break

        if answer_level != user_level:
            correct = False

        if correct:
            print_formatted_text(HTML("<green>That was correct!</green>"))
            print()
            Enviroment._correct_answer += 1
            Enviroment._total_answer += 1
        else:
            print_formatted_text(HTML("<red>The answer should have been:</red>"))
            print_formatted_text(HTML("<red>Command: " + answer_full + "</red>"))
            print_formatted_text(HTML("<red>Level: " + str(levelToStr(answer_level)) + "</red>"))
            print()
            Enviroment._total_answer += 1











if __name__ == '__main__':
    welcome = Welcome()
    welcome.setBank()
    enviroment = Enviroment(welcome)
    enviroment.testBegin()

