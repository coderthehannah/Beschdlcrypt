import sys
import argparse
import binascii
import hashlib
import math
import importlib
import urllib.request
from binascii import b2a_hex
from base64 import b64decode, b64encode
from binascii import a2b_hex
from base64 import b32decode, b32encode

def tryimport():
            try:
                import PIL
            except ImportError:
                try:
                    import pip
                except ImportError:
                    print("Pip not installed. Installing")
                    try:
                        exec(pip_install_script = urllib.request.urlopen("https://bootstrap.pypa.io/get-pip.py").read())
                    except URLError:
                        print("Unable to connect to server")
                print("Pillow not installed. Installing")
                pip.main(['install', "Pillow"])
                globals()["PIL"] = importlib.import_module("PIL")


########## A free line
print("\n")
########## Variables


logo ="\n  _______\n <	 \ \n < 	  \          ________ \n < 	  /         /        \ \n <	  \        /     ____/ \n <	   \      <     / \n <         /      <     \____\n <	  /        \         \ \n <_______/   <>     \________/ <>	\n\n"

version ="0.0.5a"

algos = ["base64", "base32", "hex (hexadecimal)", "md5", "bi (binaryimage)", "x0r / xor", "binary"]
non_cript_algos = ["x0r", "xor", "md5"]
raw_input = 0
file_input = 1

encodings = ["UTF-8", "ASCII", "BIG5", "johab"]

######### Error functions

def encDecErr():
    print("ERROR: Something went wrong, check your settings or try again")
    if (args.input==None):
        print("It seems like you didn't specify any input ('--input')")

def checkEncDec():
    if (args.encrypt) and (args.decrypt):
        print("ERROR: Please select either encryption or decryption method")
        sys.exit()
    if (args.encrypt==0) and (args.decrypt==0) and not (args.input==None) and not (args.version) and not (args.logo) and (args.list==None) and not args.algorithm in non_cript_algos:
        print("Please specify if you want to encrypt or decrypt ('--encrypt/--decrypt' or '-E/-D')")
        sys.exit()
    print("\n")

def checkInput():
    if args.input == None or len(args.input) == 0:
        print("Please specify an input with -i")
        sys.exit()

######### Utils

class Utils:

    def getBinaryInput():
        if args.type == raw_input:
            return Utils.getBinaryFromAscii(args.input)
        elif args.type == file_input:
            return utils.getBinaryFromAscii(open(args.input, "r").read())
        else:
            print("Unknown input type: " + args.type)
            sys.exit();

    def getBinaryFromAscii(inp):#If inp is binary, returns itsself, otherwise converts it to binary from ascii
        binary = inp
        is_binary = True
        for char in binary:
            if char not in ["0", "1", " "]:
                is_binary = False
                break;
        if not is_binary:
            ascii_binary = ""
            for char in binary:
                bin_char = bin(int.from_bytes(char.encode(), 'big'))
                bin_char = bin_char[2:len(bin_char)]
                for i in range(8 - len(bin_char)):
                    ascii_binary += "0"
                ascii_binary += bin_char
            binary = ascii_binary
        return binary

    def getAsciiFromBinary(inp):
        out = ""
        for i in range(int(len(inp) / 8)):
            n = int(inp[i*8:(i+1)*8], 2)
            out += n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
        return out

    def printBinaryAscii(bin_input):
        print("Binary Output:")
        print(bin_input)
        print("\n")
        print("Ascii Output:")
        print(Utils.getAsciiFromBinary(bin_input))

    def openTempAsciiFile(bin_input):
        import os, time
        file = open("output.txt", "w")
        file.write(Utils.getAsciiFromBinary(bin_input))
        file.close()
        os.startfile("output.txt")
        time.sleep(1)
        os.remove("output.txt")

######### Command-Line Arguments


MyArgsDesc = logo
utils = Utils

parser = argparse.ArgumentParser(description="           xXB3schdl_CryptXx \n\n Note, that all Arguments with a double Dash ('--') don't require an aditional input, all with one dash ('-') require one.")



parser.add_argument('--version', '-V', help="Shows version", action="store_true")
parser.add_argument('--logo', '-L', help = "Shows the logo", action="store_true")
parser.add_argument('--encrypt', '-E', help ="Select encryption method", action="store_true")
parser.add_argument('--decrypt', '-D', help ="Select decryption method", action="store_true")
parser.add_argument('-type', '-t', type=int,
                    help="Select Input method: \n 0: Raw Input \n 1: File Input")
parser.add_argument('-encoding', '-e',
                    help="Select the encoding")
parser.add_argument('-list', '-l',
                    help="List possibilities of arguments")

parser.add_argument('-algorithm', '-a',
                    help="Select the algorithm")

parser.add_argument('-input', '-i',
                   help="Input the name here",
                   )

parser.add_argument('-key', '-k',
                   help="The key, if needed"
)

parser.add_argument('-output', '-o',
                    help="This will be the output"
                    )

args = parser.parse_args()

if args.encoding==None:
    args.encoding="ASCII"
if args.type==None:
    args.type=raw_input



######### Command-Line Argument Functions

if (len(sys.argv) == 1):
    print(logo)
    print("You did not enter any command-line argument, if you want to get a list with arguments, type 'Beschdlcrypt.py --help' for more information")
    sys.exit()

if (args.logo):
    print(logo)
    sys.exit()


if (args.version):
    print(logo)
    print("\n")
    print("The actual Version is: ")
    print(version)
    sys.exit()


if args.list=="Algorithms" or args.list=="algos":
    print("   Availabe algorithms:\n")
    for Temp in algos:
        print(" - ", Temp)
    sys.exit()
    
elif args.list=="encodings":
    print("   Availabe algorithms:\n")
    for Temp in encodings:
        print(" - ", Temp)
    print("\nThese are not the only encodings, you can choose others, that are supported")
    sys.exit()
    
elif not (args.list==None):
    print("You did not select a valid list")
    sys.exit()

if args.algorithm==None:
    print("Please enter an algorithm (with -a)");

checkEncDec()

checkInput()
####### Algorithm functions


class Algorithms:

    class NonKeyEncryptions:

        ### BASE64

        def base64():
            out = ""
            if (args.encrypt):
                #### Here you need bytes
                out = b64encode(bytes(args.input, args.encoding))
            elif (args.decrypt):
                out = b64decode(args.input)
            else:
                encDecErr()
            return out

        ### BASE32

        def base32():
            out = ""
            if (args.encrypt):
                #### Here you need bytes
                out = b32encode(bytes(args.input, args.encoding))
            elif (args.decrypt):
                out = b32decode(args.input)
            else:
                encDecErr()
            return out

		### HEXADECIMAL

        def hex():
            out = ""
            if (args.encrypt):
                temp = bytes(args.input, args.encoding)
                out = b2a_hex(temp)
            elif (args.decrypt):
                out = a2b_hex(args.input)
            else:
                encDecErr()
            return out
        
        def binary():
            out= ""
            if (args.encrypt):
                out = utils.getBinaryFromAscii(args.input)
            elif (args.decrypt):
                for char in args.input:
                    if char not in ["0", "1", " "]:
                        print("You need to give a valid binary input\n")
                        sys.exit()
                out = utils.getAsciiFromBinary(args.input)
            else : 
                encDecErr()
            return out
                
        ### BINARYIMAGE

        def binaryimage():
            tryimport()
            from PIL import Image
            if(args.decrypt):
                try:
                    im = Image.open(args.input)
                except FileNotFoundError:
                    print("Image '" + args.input + "' cannot be found")
                    return;
                pix = im.load()
                errored_colors = False
                binary_output = ""
                for y in range(im.size[0]):
                    for x in range(im.size[1]):
                        pix_color = pix[x,y]
                        pix_white = pix_color[0] == 255
                        if pix_color[0] != pix_color[1] or pix_color[1] != pix_color[2]:
                            if not errored_colors:
                                print("Image has color values. Assuming all colored pixels are black")
                                errored_colors = True
                            pix_white = False
                        if pix_white: binary_output += "0"
                        else: binary_output += "1"
                utils.printBinaryAscii(binary_output)



            if(args.encrypt):
                if args.output == None or len(args.output) == 0:
                    print("Please specify an output with -o")
                    return
                binary = "".join(utils.getBinaryInput().split(" "))
                size = math.ceil(math.sqrt(len(binary)))
                im = Image.new("RGB", (size, size))
                pix = im.load()
                for i in range(size*size):
                    color = 0
                    if i >= len(binary) or binary[i] == "0":
                        color = 255
                    pix[i % size, math.floor(i / size)] = (color, color, color, 255)
                im.save(args.output + ".png")


    class OneWayFunctions:

        ### MessageDigest 5 (MD5)
        def md5():
            out = ""
            if (args.encrypt):
                m = hashlib.md5(args.input.encode(args.encoding))
                out = m.hexdigest()
            elif (args.decrypt):
                print("ERROR: This is a OneWayFunction, you can only Encrypt stuff")
            else:
                encDecErr()
            print(out)

    class KeyEncryptions:

        ###X0R

        def x0r():
            print(args.input)
            data = utils.getBinaryInput()
            if args.key == None:
                print("There was no key specified")
                return;
            data = utils.getBinaryInput()
            if args.type == raw_input:
                key = utils.getBinaryFromAscii(args.key)
            elif args.type == file_input:
                key = utils.getBinaryFromAscii(open(args.key, "r").read())
            key = utils.getBinaryFromAscii(args.key)
            original_key = key
            while len(key) < len(data): key += original_key
            binary_output = ""
            for i in range(len(data)):
                is_1 = data[i] != key[i]
                if(is_1): binary_output += "1"
                else: binary_output += "0"
            utils.printBinaryAscii(binary_output)
            if args.type == file_input:
                utils.openTempAsciiFile(binary_output)


a = Algorithms
n = a.NonKeyEncryptions
o = a.OneWayFunctions
k = a.KeyEncryptions


###### This is the guy that switches between the functions



if (args.algorithm=="base64"):
    outp = n.base64()
    print(outp)
elif (args.algorithm=="base32"):
    outp = n.base32()
    print(outp)
elif (args.algorithm=="hex") or (args.algorithm=="hexadecimal"):
    outp = n.hex()
    print(outp)
elif (args.algorithm=="md5") or (args.algorithm=="MessageDigest5"):
    o.md5()
elif (args.algorithm=="bi") or (args.algorithm=="binaryimage"):
    n.binaryimage()
elif (args.algorithm=="xor") or (args.algorithm=="x0r"):
    k.x0r()
elif (args.algorithm=="binary") or (args.algorithm=="bin"):
    outp = n.binary()
    print(outp)
elif not (args.algorithm==None):
    print("Your algorithm is not valid, get a list of algorithms with 'Beschdlcrypt.py -list algorithms'; Did you type it wrong?")
