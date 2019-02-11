import busio
import adafruit_mcp9808
import socket
import atexit

#################GRAB LOCAL IP ADDRESS##########################################
ipSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    ipSock.connect(('10.255.255.255', 1))
    localIP = ipSock.getsockname()[0]
except:
    localIP = '127.0.0.1'
ipSock.close()
socket.setdefaulttimeout(1)

########################CLEAN SHUTDOWN PROCEDURES###############################
def socketKill(sock):
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

############################TEMPERATURE FUNCTIONS###############################

def getTempLocal():
    return mcp.temperture * 9 / 5 + 32

def returnTemperature(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, 9001)
    sock.connect(server_address)
    message = json.dumps(getTempLocal())
    try:
        sock.sendall(message.encode())
    except Exception as e:
        print('Failed returning temperature\n' + e)
    finally:
        socketKill(sock)

def tempResponseServer():
    '''recieves a gimme command and sends temperature back to thermostat'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (localIP, 9000)
    print('Initiating socket on %s port %s' % server_address)
    sock.bind(server_address)
    sock.listen(20)
    sock.settimeout(None)
    atexit.register(socketKill, sock)
    while True:
        connection, client_address = sock.accept()
        request = ''
        while True:
            data = connection.recv(16).dedcode()
            request += data
            if data:
                pass
            else:
                request = json.loads(request)
                if request == 'gimme':
                    returnTemperature(client_address[0])
                else:
                    print('Invalid command type recieved')
                break
