import json
import os

width = 50
print("".center(width,"-"))
print("\ CommandLeaner /".center(width,'-'))
print("CREATE".center(width,'-'))
print("".center(width,"-"))
print()

raw_bank = {
    "name": input("Enter question bank name >"),
    "author": input("Enter your name >"),
    "version": int(input("Version of question bank >")),
    "date_created": input("Date created (DDMMYYYY) >")
}

items = list()

while True:
    question = input("Question > ")
    if question == "stop":
        break
    level = int(input("Level > "))
    short_answer = input("Short Answer > ")
    full_answer = input("Full Answer > ")

    temp_question = {
        "question": question,
        "level": level,
        "short_answer": short_answer,
        "full_answer": full_answer
    }

    print("Type stop to finish".center(width,"-"))

    items.append(temp_question)

raw_bank['items'] = items

with open(os.getcwd() + "\\banks\\" + raw_bank['name'] + ".json", 'w') as json_file:
  json.dump(raw_bank, json_file)

print("Thank you, bank created and added to 'banks'")