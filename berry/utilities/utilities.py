"""
Utility functions.
"""
import logging
import socket


# The port to listen on via UDP for registrations
REGISTRATION_PORT = 5555

# The default client port
CLIENT_PORT = 24601

# The port to run the server on
SERVER_PORT = 4444

# How much to log
LOG_LEVEL = logging.DEBUG


def get_my_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))

    ip_address = s.getsockname()[0]

    s.close()

    return ip_address


def send_with_tcp(message, recv_address, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((recv_address, port))

    s.send(message.encode('utf-8'))

    logging.info('sent: ' + message)
    logging.info('to  : ' + recv_address + ':' + port.__str__())

    s.close()


def blocking_receive_from_tcp(port):
    logging.info('waiting to receive on port ' + port.__str__())

    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.bind(('', port))
    tcpsock.listen(1)

    client, address = tcpsock.accept()
    client.settimeout(60)

    logging.info('someone is connecting')

    message = ''
    while True:
        try:
            data = client.recv(512)
            if data:
                # Set the response to echo back the recieved data
                message += data.decode('utf-8')
            else:
                logging.info('client at {} closed'.format(address))
                client.close()
                tcpsock.close()
                break
        except Exception as e:
            logging.error('Exception: {} ({})'.format(e, type(e)))
            client.close()
            return False

    logging.info('received: {}'.format(message))
    logging.info('from    : {}:{}'.format(address, port))

    return message