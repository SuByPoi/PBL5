import time
import RPi.GPIO as GPIO
import io
import socket
import struct
import picamera
import signal
from _thread import *
import warnings

warnings.filterwarnings("ignore")

isDoorOpen = False

pir_pin = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_pin, GPIO.IN)

def detect(channel):
    print('co chuyen dong!')
    start_new_thread(send_to_server, (5, ))
    return


def signal_handler(sig, frame):
    print("Quit")
    GPIO.cleanup()


def send_to_server(num_of_image):
    count = 0
    print("2)")
    connection = client_socket.makefile('wb')
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (1024, 768)
            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg'):
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                stream.seek(0)
                count += 1
                connection.write(stream.read())
                if count == 5:
                    print('chup xong!')
                    camera.stop_preview()
                    camera.close()
                    return
                stream.seek(0)
                stream.truncate()
                print('Done!')

                time.sleep(1)
        connection.write(struct.pack('<L', 0))
        data = client_socket.recv(1024)
        print(data.decode("utf8"))
    except:
        print('Something is error')

server_ip = '192.168.2.102'
server_port = 9000
client_socket = socket.socket() # socket.AF_INET, socket.SOCK_STREAM
client_socket.connect((server_ip, server_port))
print('connected')

# GPIO.add_event_detect(pir_pin, GPIO.RISING, callback=detect, bouncetime=15000)
# signal.signal(signal.SIGINT, signal_handler)
# signal.pause()

input = int(input("Nhap so 1"))
if  input == 1:
    print("1")
    send_to_server(5)