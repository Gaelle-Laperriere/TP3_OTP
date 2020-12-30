# TP3_OTP
This project is about producing a self-contained tool in Python that can be used for secure messaging. This tool apply a One-Time Pad cipher to a given message.

## Technologies and frameworks used
All the scripts are written in <i>Python 3.7.4</i>.
The libraries used for this project are as follow:
- [Python 3.7.4](https://www.python.org)

You can install Python through python's package manager or ``conda``. 

```
conda install python==3.7.4
```

## Execution
To run the software, you will have to pull all the deposit and activate your required environment. The program have three modes (generate, send and receive) specified through the ``-g``, ``-s`` and ``-r`` switches. If the switch is not provided, the generating mode will be assumed.
When the program starts, if it detects that a network interface is up, it exits immediately with an error message.

The convention is as follow:
```
main.py [-h] [-g] [-s] [-r] [-f FILENAME_SEND] [-t TEXT] directory [filename]
```

``directory`` is the name of a directory that will be used to store the pads. It is a mandatory argument for all modes. 
You can use the option ``-h`` alone, for help or more information. 

### Generating mode
To generate the One-Time-Pads that will be used later, please use the command:

```
python main.py [-g] directory
```

Then, you must duplicate the directory generated for the sender and receiver. To do so, you can use this kind of commands:

```
cp -r dir ./path_of_sender/
cp -r dir ./path_of_receiver/
```

The program will generate 100 pads. Each batch of 100 pads will reside in a subfolder of the directory specified through the positional argument ``directory``. For example, after two runs with ``dir`` as positional argument, you will have ``dir/0000`` and ``dir/0001`` each containing 100 pads.

Each individual pad is a set of three files: (``00p``, ``00c``, ``00s`` up to ``99p``, ``99c``, ``99s``):
- The files ``00p`` to ``99p`` are to be used as transmission prefix. They contain 48 bytes (384 bits) of random numbers.
- The files ``00s`` to ``99s`` are to be used as transmission suffix. They contain 48 bytes (384 bits) of random numbers.
- The files ``00c`` to ``99c`` are to be used as a pad on a given transmission. They contain 2000 bytes of random numbers.

The random numbers in all of the files are read from ``/dev/urandom``. The instructions specified to use ``/dev/random``. I did. It worked. Therefore, a generation would take at least 6 hours (I stopped it before it could be more). With ``urandom``, the generation takes seconds at most. If wanted, you can uncomment the code that use ``random`` and comment the one with ``urandom``.

### Sending mode
To use the One-Time-Pad and generate an encrypted message to send, please use the command:

```
python main.py -s directory [-f filename] [-t "text"]
```

The text to be encrypted should be specified by one of the three methods:
- if neither ``-f`` nor ``-t`` is specified, it will be read from standard input. You will be asked to write it in your console. 
- if ``-f filename`` is specified, it will be read from the file filename.
- If ``-t "text"`` is specified, it will be read from the command line.

Please be carefull with the text written in the command line. Use simple quotes if special characters are used, for more security. The same way, you can use double quotes by adding a space between them and the message (``" text "`` instead of ``"text"``). This problem is due to the Bash command line system, not the program nor the argparse module. If some specific characters are used without those securities, the command line might be badly interpreted by the system itself. 

To encrypt the message, the program will select the first available pad (first time would be the pad ``dir/0000/00c``) and apply the random numbers to the message. Then, it will create a file, named ``dir-0000-00t`` in your current directory, that will contain the entire transmission to give to your receiver. Finally, the program will shred the pad used for transmission (``dir/0000/00c`` of the sender, in this example).

Sanity checks are done before attempting to write. If the message is too long to fit in one pad, the program will exit with an error message.

### Receiving mode
To decrypt a transmission, please use the command:

```
python main.py -r directory filename
```

The transmission to decrypt must be specified by a second positional argument ``filename`` (``dir-0000-00t`` in the previous example). The program will than scan the directory (the one of the receiver, untouched), looking for the correct prefix. It will apply the corresponding pad to the transmission to recover the cleartext message, then shred the pad and the transmission. 

The cleartext message will be stored in a file with the “m” suffix and a name indicating which pad was used (``dir-0000-00m`` here).
