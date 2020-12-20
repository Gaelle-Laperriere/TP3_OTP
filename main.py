#-*- coding: utf-8 -*-
import argparse
import os

def generate(directory):
    ''' '''
    create_subdirectory(directory)
    return

def send(directory, text):
    ''' '''
    return

def receive(directory):
    ''' '''
    return

def create_subdirectory(directory):
    ''' (String) -> NoneType '''
    if not(os.path.exists(directory)):
        os.mkdir(directory)
    for index in range(10000):
        subdirectory = directory + '/' + str(index).zfill(4)
        if not(os.path.exists(subdirectory)):
            os.mkdir(subdirectory)
            break

def is_interface_up():
    ''' (NoneType) -> NoneType '''
    path = '/sys/class/net/'
    interfaces = []
    for object in os.listdir(path):
        if os.path.isdir(path + object):
            interfaces.append(object)
    for interface in interfaces:
        f = open(path + interface + '/operstate', 'r')
        status = f.read()
        if 'up' in status:
            print("You can't run this script with a network interface up")
            exit()
        elif 'unknown' in status:
            user_confirmation = ''
            while True:
                user_confirmation = input("Your network interface " + interface + " has an unknown statut. Is it up ? [yes] or [no] ")
                if user_confirmation == 'no':
                    break
                elif user_confirmation == 'yes':
                    print("You can't run this script with a network interface up")
                    exit()
        f.close()

def read_txt(filename):
    ''' (String) -> String '''
    file = open(filename, 'r')
    text = file.read()
    file.close()
    return text

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Encrypt (write) or Decrypt (read) text in an image.')
    parser.add_argument('-g', '--generation_mode', action='store_true', help='Switch to generation mode.')
    parser.add_argument('-s', '--sending_mode', action='store_true', required=False, help='Switch to sending mode.')
    parser.add_argument('-r', '--receiving_mode', action='store_true', required=False, help='Switch to receiving mode.')
    parser.add_argument('directory', type=str, help='Set the directory name used to store the pads.')
    parser.add_argument('filename', type=str, help='Set the filename containing the encrypted message, if receiving mode.', nargs='?', default='')
    parser.add_argument('-f', '--filename_send', type=str, required=False, help='Set the filename of the message to encrypt, if sending mode.')
    parser.add_argument('-t', '--text', type=str, required=False, help='Write the quoted message to encrypt, if sending mode (please use simple quotes instead of double quotes or surround message with spaces)')
    args = parser.parse_args()

    g = args.generation_mode
    s = args.sending_mode
    r = args.receiving_mode
    directory = args.directory
    filename = args.filename
    filename_send = args.filename_send
    text = args.text

    # Check if sending mode and filename not referenced.
    if r and filename == '':
        print('usage: main.py [-h] [-g] [-s] [-r] [-f FILENAME_SEND] [-t TEXT_SEND] directory filename')
        print('main.py: error: the following arguments are required: filename')
        exit()

    if g or (not(s) and not(r)):
        generate(directory)
    elif s:
        if filename_send is not None:
            text = read_txt(filename_send)
        elif text is None:
            text = input('Please enter the message to encrypt: ')
        send(directory, text)
    elif r:
        receive(directory)
