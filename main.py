#-*- coding: utf-8 -*-
import argparse
import os
import sys

def generate(directory):
    ''' (String) -> NoneType '''
    subdirectory = create_subdirectory(directory)
    for index in range(100):
      file_c = open(subdirectory + '/' + str(index).zfill(2) + 'c', 'wb')
      file_c.write(get_randoms(2000))
      file_c.close()
      file_p = open(subdirectory + '/' + str(index).zfill(2) + 'p', 'wb')
      file_p.write(get_randoms(48))
      file_p.close()
      file_s = open(subdirectory + '/' + str(index).zfill(2) + 's', 'wb')
      file_s.write(get_randoms(48))
      file_s.close()
    return

def send(directory, text):
    ''' '''
    # Get all information needed
    path = get_first_available_pad(directory)
    if path == '':
        print('There is no available pad in the directory "' + directory + '"')
        exit()
    text_encrypted = encrypt_message(text,path + 'c')
    prefix = read_file(path + 'p')
    suffix = read_file(path + 's')
    # Write encrypted prefix + text_encrypted + suffix
    split = path.split('/')
    file_t = open(split[0] + '-' + split[1] + '-' + split[2] + 't', 'wb')
    file_t.write(prefix + text_encrypted + suffix)
    file_t.close()
    # Shred
    os.system("shred -vu " + path + 'c')
    return

def receive(directory):
    ''' '''
    return

def check_interface_up():
    ''' (NoneType) -> NoneType '''
    path = '/sys/class/net/'
    interfaces = []
    for object in os.listdir(path):
        if os.path.isdir(path + object):
            interfaces.append(object)
    for interface in interfaces:
        file = open(path + interface + '/operstate', 'r')
        status = file.read()
        if 'up' in status:
            print('You cannot run this script with a network interface up: ' + interface)
            exit()
        elif 'unknown' in status:
            user_response = ''
            while True:
                print('Your network interface ' + interface + ' has an unknown statut.')
                user_response = input('Is it up ? [yes] or [no] ')
                if user_response == 'no':
                    break
                elif user_response == 'yes':
                    print('You cannot run this script with a network interface up: ' + interface)
                    exit()
        file.close()

def is_encryption_possible(text):
    ''' (String) -> Boolean '''
    if len(text) > 2000:
        return False
    return True

def create_subdirectory(directory):
    ''' (String) -> String '''
    if not(os.path.exists(directory)):
        os.mkdir(directory)
    for index in range(10000):
        subdirectory = directory + '/' + str(index).zfill(4)
        if not(os.path.exists(subdirectory)):
            os.mkdir(subdirectory)
            break
    return subdirectory

def get_first_available_pad(directory):
    ''' (String) -> String '''
    for subdirectory in os.listdir(directory):
        for index_pad in range(100):
            path_pad = directory + '/' + subdirectory + '/' + str(index_pad).zfill(2)
            if os.path.isfile(path_pad + 'c'):
                return path_pad
    return ''

def get_randoms(bytes):
    ''' (int) -> String '''
    # The following wommented code is very slow
    """
    randoms = []
    file = open('/dev/random', 'rb')
    for x in file.read(bytes):
        randoms.append(bin(ord(x))[2:].zfill(8))
    file.close()
    """
    # urandom use dev/urandom instead of de/random but is much faster !
    randoms = [bin(ord(x))[2:].zfill(8) for x in os.urandom(bytes)]
    return ''.join(randoms)

def read_file(path):
    ''' (String) -> String '''
    file = open(path, 'r')
    text = file.read()
    file.close()
    return text

def read_pad(path):
    ''' (String) -> array of int '''
    pad = read_file(path)
    pad_array = [int(pad[index:index+8], 2) for index in range(0, 16000, 8)]  # Separate each pad value.
    return pad_array

def text_to_ASCII(text):
    ''' (String) -> array of int '''
    ascii = [ord(char) for char in text]  # Get binary ASCII for each character.
    return ascii

def bin_ASCII_to_text(ascii):
    ''' (array of String) -> String '''
    text = [chr(int(char, 2)) for char in ascii]  # Get integer values and decode from ASCII.
    return ''.join(text)

def encrypt_message(text,path):
    ''' (String, String) -> String '''
    pad = read_pad(path)
    ascii = text_to_ASCII(text)
    text_encrypted = []
    for index in range(len(ascii)):
        text_encrypted.append(bin(ascii[index]+pad[index])[2:].zfill(8))
    return ''.join(text_encrypted)

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
    else:
        #check_interface_up()  # TODO uncomment
        if s:
            if filename_send is not None:
                text = read_file(filename_send)
            elif text is None:
                text = input('Please enter the message to encrypt: ')
            if not(is_encryption_possible(text)):
                print('You cannot encrypt a message that long (>2 000 characters).')
                exit()
            send(directory, text)
        elif r:
            receive(directory)
