#!/usr/bin/env python3

import socket


HOST = 'irc.thotcon.org'  # The server's hostname or IP address
#PORT = 10000     # The port used by the server


import sys

keyU = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
keyL = "abcdefghijklmnopqrstuvwxyz"

def rotthis(inputstring, rot):
    final = ''
    for char in inputstring:
        if not char.isalpha():
            final += char
            continue


        if char.isupper():
            array = keyU
        else:
            array = keyL

        
        index = array.index(char)
        index = (index + rot) % len(array)
        final += array[index]

    return final


def rotfinder(instr):
    instr = instr.decode('utf-8')
    print(instr)
    results = []
    for rot in range(26):
        final = rotthis(instr, rot)
        results.append(final)

    suggests = []
    for index, result in enumerate(results):
        if index < 10:
            print(' ', end='')

        print(index, '   ', result)

        if 'the' in result.lower() or 'who' in result.lower():
            suggests.append((index, result))

    for item in suggests:
        print('\nSUGGESTIONS: ', item[0], '   ', item[1])

    if len(suggests) > 0:
        index = suggests[0][1].rfind(' -')

        return suggests[0][1][index+2:].encode('utf-8')


    print('!!!!!!!!!!!!!!!DIDNOT FIND IT!!!!!!!!!!!!!!!!!!!!!')
    return '!!!!!!!!!!!!!!!DIDNOT FIND IT!!!!!!!!!!!!!!!!!!!!!'


while True:
    for port in range(10000,10010):
        
        try:

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, port))

                data = s.recv(1024)
                s.sendall(b'Yes')
                data = s.recv(1024)
                print('Received', repr(data))

                s.sendall(b'\n')

                while True:

                    print(port)
                    data = s.recv(1024)
                    print('Received', repr(data))

                    cleandata=rotfinder(data)
                    print(cleandata)

                    s.sendall(cleandata)
                    data = s.recv(1024)
                    print('Received', repr(data))

                    print('Received', repr(data))

        except ConnectionRefusedError as identifier:
            print("error. {}".format(identifier))

