import socket
import re
import logging

SERVER_ADDRESS = ('localhost', 8082)
MAX_CONNECTIONS = 10
logging.basicConfig(filename='logging.log', encoding='utf-8', level=logging.DEBUG)
pattern = re.compile("^\d\d\d\d\s(\d|\w)(\d|\w)\s((?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d)[.](\d\d\d)\s(\d\d)\[CR\]$")

server_socket = socket.socket()
server_socket.bind(SERVER_ADDRESS)
server_socket.listen(MAX_CONNECTIONS)

while True:
    client_socket, remote_address = server_socket.accept()
    client_socket.send(bytes("The server is running, please enter STOP to end the session.\n", 'utf-8'))
    while True:
        # delete the \r and \n characters
        data = client_socket.recv(1024).decode('utf-8')[:-2]
        if data == 'STOP':
            client_socket.close()
            break
        is_data_correct = bool(pattern.fullmatch(data))
        if is_data_correct:
            number, line, time, group = data[:4], data[5:7], data[8:18], data[21:23]
            data_is_correct = 'The data: {} was processed correctly\n'.format(data)
            output = "Cпортсмен, нагрудный номер {} прошёл отсечку {} в {}\n".format(number, line, time)
            if group == '00':
                with open("output.txt", 'a', encoding='utf-8') as f:
                    f.write(output)
                    b_output = bytes(data_is_correct + output, 'utf-8')
            else:
                b_output = bytes(data_is_correct, 'utf-8')
            logging.info(data_is_correct + output)
        else:
            output = "The data: {} is incorrect\n".format(data)
            logging.warning(output)
            b_output = bytes(output, 'utf-8')
        client_socket.send(b_output)
        print(output)
