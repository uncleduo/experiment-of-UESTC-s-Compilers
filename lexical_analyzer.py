#!/usr/bin/python
# -*- coding: UTF-8 -*-

#global temp
temp = ""
state = 0
ItemDict = {"begin": 1, "end": 2, "integer": 3, "if": 4, "then": 5, "else": 6, "function": 7, "read": 8, "write": 9, "=": 12, "<>": 13, "<=": 14, "<": 15, ">=": 16, ">": 17, "-": 18, "*": 19, ":=": 20, "(": 21, ")": 22, ";": 23}
Token = 10
Constants = 11
target = ""
file_name = "test.txt"
error_file_name = file_name.split('.')[0]+".err"
target_file_name = file_name.split('.')[0]+".dyd"

def print_binary_function(print_word, num):
    global target
    target += ((16-len(print_word))*' '+print_word+' '+str(num)+'\n')


def init_file():
    error_file = open(error_file_name, "w")
    error_file.close()
    target_file = open(target_file_name, "w")
    target_file.close()


def error_write(type):
    if type == 0:
        error_info = "出现了无法识别的字符"
    elif type == 1 :
        error_info = "请注意，:后必须跟="
    error_file = open(error_file_name, "w")
    error_file.write(error_info)
    error_file.close()


def end_word():
    global temp
    if temp != "":
        if state == 1:
            if ItemDict.get(temp):
                print_binary_function(temp, ItemDict.get(temp))
            else:
                print_binary_function(temp, Token)
        elif state == 3:
            print_binary_function(temp, Constants)
        else:
            if ItemDict.get(temp):
                print_binary_function(temp, ItemDict.get(temp))
            else:
                error_write(1)
        temp = ""


init_file()
with open(file_name, "r") as file:
    for line in file:
        for word in line:
            if word == ' ':
                if state != 0:
                    end_word()
                    state = 0
            elif 'z' >= word >= 'A':
                if state != 0 and state != 1:
                    end_word()
                temp += word
                state = 1
            elif '9' >= word >= '0':
                if state != 3:
                    end_word()
                temp += word
                state = 3
            elif word == '=':
                if state not in [0, 10, 14, 17]:
                    end_word()
                    temp += word
                    state = 5
                else:
                    temp += word
                    end_word()
                    state = 0
            elif word == '-':
                end_word()
                temp += word
                state = 6
            elif word == '*':
                end_word()
                temp += word
                state = 7
            elif word == '(':
                end_word()
                temp += word
                state = 8
            elif word == ')':
                end_word()
                temp += word
                state = 9
            elif word == '<':
                end_word()
                temp += word
                state = 10
            elif word == '>':
                if state != 10:
                    end_word()
                    state = 14
                else:
                    temp += word
                    state = 12
            elif word == ':':
                end_word()
                temp += word
                state = 17
            elif word == ';':
                end_word()
                temp += word
                state = 20
            elif word == '\n':
                end_word()
                state = 0
                print_binary_function("EOLN", 24)
            else:
                error_write(0)
    end_word()
    print_binary_function("EOF", 25)
    with open(target_file_name, "w") as target_file:
        target_file.write(target)



