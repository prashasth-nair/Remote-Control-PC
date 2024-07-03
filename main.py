import socket
import json
import pyautogui

from threading import Thread
from socket import AF_INET, SOCK_STREAM
import ctypes
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from comtypes import CoInitialize
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import jpysocket
from webbrowser import get
import screen_brightness_control as sbc
import pythoncom
from sound import Sound
# from zeroconf import Zeroconf, ServiceInfo
import os
v = 0
w = 0
connection = True
device_ip = ""

import subprocess

def Server():
    # Specify the Java file to compile and run
    java_file = "PCServer.java"

    # Compile the Java code
    compile_command = ["javac", java_file]
    compile_process = subprocess.run(compile_command)

    # Check if compilation was successful
    if compile_process.returncode == 0:
        print("Java compilation successful")

        # Run the compiled Java code
        run_command = ["java", "PCServer"]
        run_process = subprocess.run(run_command)

        # Check if execution was successful
        if run_process.returncode == 0:
            print("Java execution successful")
        else:
            print("Java execution failed with exit code:", run_process.returncode)
    else:
        print("Java compilation failed with exit code:", compile_process.returncode)

def get_ip():
    IPAddr = socket.gethostbyname(socket.gethostname())
    # print("Your Computer IP Address is:" + IPAddr)
    return IPAddr  


def onStart(ip):
    pythoncom.CoInitialize()
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    scalar = 0
    for i in range(volume.GetChannelCount()):
        scalar = int(volume.GetChannelVolumeLevelScalar(i) * 100)
    if (scalar % 2) == 0:
        scalar = scalar
    else:
        scalar = scalar + 1
    is_mute = str(volume.GetMute())
    brightness = sbc.get_brightness()

    s = socket.socket(AF_INET, SOCK_STREAM)  # Create a socket object
    port = 5012
    host = ip
    s.connect((host, port))  # Bind to the port

    m = {"is_mute": is_mute, "Current volume": str(
        scalar), "Current brightness": str(brightness)}
    msgsend = jpysocket.jpyencode(str(m))  # Encript The Msg
    s.send(msgsend)  # Send Msg
    s.close()  # Close connection
    

def send_data(host,data):
    # print("Sending Data to: ",host)
    try:
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
        s.settimeout(3)

        port = 5001 
        s.connect((host, port))  # Bind to the port
        str = data
        s.send(str.encode())
        # print("SuccessFully Sent")
        global device_ip
        device_ip = host
        global searching
        searching = False
        return
    except Exception as e:
        print(e)

def receive_data():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    host = get_ip()  # Get local machine name
    port = 6000  # Reserve a port for your service.
    s.bind((host, port))  # Bind to the port
    s.listen(5)  # Now wait for client connection.

    # timeout = 5
    s.settimeout(5) 
    # After 5 seconds, the socket will timeout and raise socket.timeout exception
    while True:
        try:
            c, addr = s.accept()  # Establish connection with client.
            # print('Got connection from', addr[0])
            # c.send(b'Thank you for connecting')
            data = c.recv(4096)
            data = data.decode("utf-8")
            # print(data)
            onStart(addr[0])
            c.close()  # Close the connection
            
            
        except Exception as e:
            print("Error: ",e)
            continue
    
def conn_start():
    is_locked = False
    pythoncom.CoInitialize()
    print("Listening for input...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object

    host = get_ip() # Get local machine name
    port = 5000  # Reserve a port for your service.
    s.bind((host, port))  # Bind to the port

    s.listen(5)  # Now wait for client connection.
    c = None
    
    while connection:
        try:
            s.settimeout(5)  # Set a timeout of 5 seconds for accept()
            c, addr = s.accept()  # Establish connection with client.

            # c.send(b'Thank you for connecting')
            data = c.recv(4096).decode("utf-8")
            if data:
                # print('Got connection from', addr[0])
                if 'Mouse:' not in data:
                    print("MESSAGE: ", data)

                # Volume Control
                if 'MUTE' in data:
                    pyautogui.press("volumemute")

                elif 'brightness' in data:
                    data = data.replace("brightness ", "").replace(".0", "")
                    brightness = int(data)
                    sbc.set_brightness(brightness)

                elif 'LOCK' in data:
                    ctypes.windll.user32.LockWorkStation()
                elif 'SHUTDOWN' in data:
                    os.system("shutdown /s /t 1")
                elif 'RESTART' in data:
                    os.system("shutdown /r /t 1")
                    

                elif 'key' in data:
                    keyboard_controls(data)

                elif 'volume' in data:
                    volume = data.replace('volume ', '')
                    volume = int(volume)
                    if (volume % 2) == 0:
                        volume = volume
                    else:
                        volume = volume + 1
                    Sound.volume_set(volume)

                elif 'Mouse:' in data:
                    # Get the current mouse cursor position
                    if 'Mouse: Left Click!' in data:
                        pyautogui.click()
                    elif 'Mouse: Right Click!' in data:
                        pyautogui.click(button='right')
                    elif 'Mouse: Middle Click!' in data:
                        pyautogui.click(button='middle')
                    else:
                        current_x, current_y = pyautogui.position()   
                        x = float(data.replace('Mouse: ', '').split(' ')[0])
                        y = float(data.replace('Mouse: ', '').split(' ')[1])
                        pyautogui.moveTo(current_x + (x), current_y + (y))


                elif 'PLAY' in data:
                    pyautogui.press("playpause")

                elif 'PREVIOUS' in data:
                    pyautogui.press("prevtrack")

                elif 'NEXT' in data:
                    pyautogui.press("nexttrack")

                elif 'DECREASE' in data:
                    pyautogui.press("volumedown")

                elif 'INCREASE' in data:
                    pyautogui.press("volumeup")

                elif 'FAST_FORWARD' in data:
                    pyautogui.press('right')

                elif 'REWIND' in data:
                    pyautogui.press('left')
        except socket.timeout:
            print("Socket Timeout")
            continue 
    s.close()
    if c:
        c.close()  # Close the connection

def keyboard_controls(data):
    try:
        d = json.loads(data)
        if d["key"] == "backspace":
            pyautogui.press('backspace')
        elif d["key"] == "EnterKey":
            pyautogui.press('enter')
        else:
            pyautogui.press(d["key"])

    except json.decoder.JSONDecodeError as e:
        print("Error")


if __name__ == "__main__":


        
    p2 = Thread(target=receive_data)
    # p2.daemon = True
    p2.start()

    p1 = Thread(target=conn_start)
    # p1.daemon = True
    p1.start()

    t1 = Thread(target=Server)
    # t1.daemon = True
    t1.start()
    print("Server Started")