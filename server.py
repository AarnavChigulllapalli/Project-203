import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
nicknames = []

questions=[
    "What is India's capital? \n a.Mumbai\n b.Delhi\n c.Pune",
    "What is the tallest mountain?\n a.Mount Everest\n b.Mount Kilimangaro\n c.None of the above"
    "Who won the 2022 FIFA World Cup? \n a.Argentina\n b.Portugal\n c.France"
]

answers=["b", "a", "a"]

print("Server has started...")

def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions) - 1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def clientthread(conn, addr):
    score = 0
    conn.send("Welcome to this chatroom!".encode('utf-8'))
    conn.send("You will recieve a question whose answer is either a, b or c!\n".encode('utf-8'))
    conn.send("Best of luck!\n".encode('utf-8'))
    index, question, answer = get_random_question_answer(conn)

    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answer:
                    score+=1
                    conn.send("That's the right answer\n".encode('utf-8'))

                else:
                    conn.send("Incorrect answer! Better luck next time!\n\n".encode('utf-8'))
                    remove_question(index)
                    index, question, answer = get_random_question_answer(conn)

            else:
                remove(conn)
                remove_nickname(nickname)
        except:
            continue

while True:
    conn, addr = server.accept()
    conn.send("NICKNAME".encode("utf-8"))
    nickname = conn.recv(2048).decode("utf-8")
    nicknames.append(nickname)
    list_of_clients.append(conn)
    message = "{} jOiNeD".format(nickname)
    print (addr[0] + " connected")
    new_thread = Thread(target= clientthread,args=(conn,addr))
    new_thread.start()
