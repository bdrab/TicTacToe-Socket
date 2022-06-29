import socket
from _thread import *
import pickle
from tictactoe import TicTacToe

server = "192.168.0.136"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error:
    pass

s.listen()
print("Server started... ")

games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    while True:
        try:
            data = conn.recv(4096).decode()
            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset()
                    elif data != "get_board":
                        game.play(p, data)
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Connection lost.")
    try:
        del games[gameId]
        print(f"Game {gameId} closed")
    except KeyError:
        print(f"Game {gameId} cannot be closed.")
    idCount -= 1
    conn.close()


while True:
    connector, address = s.accept()
    print("Connected to:", address)

    idCount += 1
    player = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = TicTacToe(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        player = 1

    start_new_thread(threaded_client, (connector, player, gameId))
