import  socket
import string
from threading import Thread
from  random import randint
import json

SYMBOLTABLE = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&'()*+,-./:;<=>?@[\]^_`{|}~")


def move2front_encode(strng, symboltable):
    sequence, pad = [], symboltable[::]
    for char in strng:
        indx = pad.index(char)
        sequence.append(indx)
        pad = [pad.pop(indx)] + pad
    return sequence


def bwt(Input):
    assert "$" not in Input  # Input string cannot contain $
    Input = Input + "$"  # Add "$" to the end of the string

    table = [Input[i:] + Input[:i] for i in range(len(Input))]  # Table of rotations of string
    print('table = ', table)

    table = sorted(table)
    print('sorted table = ', table)

    last_column = [row[-1:] for row in table]  # Last characters of each row
    return ''.join(last_column)



def send_server():


    g = 3
    p = 17

    data = json.dumps({"g": g, "p": p})
    print("Шя отправлю")
    client.send(data.encode("utf-8"))
    print("Отпрвил")
    listen_thred = Thread(target=lissten_server)
    listen_thred.start()
    #A_private = randint(0, 100000)
    #Alica = DH_code.DH_Endpoint(g, p, A_private)
    A_secret = randint(0, 100000)
    A_public = (g ** A_secret) % p
    data_A = json.dumps({"Alica": A_public})
    client.send(data_A.encode("utf-8"))



    Bob = client.recv(1024)
    Bob1 = json.loads(Bob.decode())
    Bob_a = Bob1.get("Bob")
    print("Bob public", Bob_a)


    A_key=(Bob_a**A_secret)%p
    print("key = ",A_key)



    while True:
        message=input("Вы: ")
        ll=bwt(message)
        print(ll)
        lll=move2front_encode(ll,SYMBOLTABLE)

        #ll=move2front_encode(message,SYMBOLTABLE)
        #ll=encrypt_message(message,A_key)
        print(lll)

        client.send(bytes(lll))




def lissten_server():

    while True:
        data = client.recv(1024)
        print(data.decode("utf-8"))



client =socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)
client.connect(

    ("127.0.0.1",700)

)


if __name__=='__main__':

    send_server()
