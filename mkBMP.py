from csv import reader
import math
import sys
import getopt
import struct

################################################################################
#                                   DNA Sequence to bitmap v2.0
#           
################################################################################




#Creates a bitmap header
def BmpHeader(dibHeaderSize, bitmapSize):
    dataArray = bytearray()
    dataArray += b'\x42\x4D' #BM id feild
    dataArray += intToByteString(14 + dibHeaderSize + bitmapSize, 4) #Size of the bitmap.
    dataArray += b'\x00\x00' #Reserved
    dataArray += b'\x00\x00' #Reserved
    dataArray += intToByteString(14 + dibHeaderSize, 4) #Offset till the pixle array begins

    return dataArray

#Create a pixel array representing a DIB header for a 24-bit image.
def winDibHeader24(width, height, bitmapSize):
    dataArray = bytearray()
    dataArray += b'\x28\x00\x00\x00' #Dib header size.
    dataArray += intToByteString(width, 4) #Width
    dataArray += intToByteString(height, 4) #Height
    dataArray += b'\x01\x00' #Planes, always 1
    dataArray += b'\x18\x00' #Bits per pixel
    dataArray += b'\x00\x00\x00\x00' #Pixel array compression. None in this case.
    dataArray += b'\x00\x00\x00\x00' #intToByteString(bitmapSize, 4) #Bitmap size. Not required for BI_RGB
    dataArray += b'\x13\x0B\x00\x00' #Print resolution (pixel/metter) horizontal
    dataArray += b'\x13\x0B\x00\x00' #Print resolution (pixel/metter) vertical
    dataArray += b'\x00\x00\x00\x00' #Colors in pallet. Does not apply in 24-bit images.
    dataArray += b'\x00\x00\x00\x00' #Important colors. All in this case.

    return dataArray

#BMP is encoded as BGR not RGB 
def encodeRGB(red, green, blue):
    rgbArray = [blue, green, red] #Little endian.
    return bytearray(rgbArray)

#Formats an integer to an unsigned little endian string
# Source: https://docs.python.org/2/library/struct.html

def intToByteString(int, size):
    if(size == 1):
        return struct.pack("<B", int) #unsigned char
    if(size == 2):
        return struct.pack("<H", int) #unsigned short
    if(size == 4):
        return struct.pack("<I", int) #unsigned int/long
    if(size == 8):
        return struct.pack("<Q", int) #unsigned long long

#Given a two dimentional array of DNA words (as GTAC), representing colors i.e r for G, create a bytearray

def genBitMap(array, guanine, thymine, adenine, cytosine):
    rowLen = len(array[0])  #How many rows this bitmap contains
    padding = 4 - ((rowLen * 3) % 4) #Each row must be a multiple of 4, if not padding must be appended.
    bitmap = bytearray()
    
    for i in reversed(range(len(array))): #Each Row 
        for j in range(len(array[i])): #Each Col
                
                bitmap += charToRGB(array[i][j], guanine, thymine, adenine, cytosine)
          
        if(padding != 4):
            for k in range(padding):
                bitmap += b'\x00'


    return bitmap

def genBitMap2(array, rowLen, rows, scale, guanine, thymine, adenine, cytosine):
    
   
    useThisManyBytes=int(rows*rowLen)  #fixes nasty half row endings.
    
    bitmap = bytearray()
    lineBitmap = bytearray()
    pixelCounter =0
    for i in reversed(range(useThisManyBytes)): #read it backwards!
                pixelCounter += 1
                for l in range(scale):
                    lineBitmap += charToRGB(array[i], guanine, thymine, adenine, cytosine) #add the pixel scale times
                if pixelCounter == rowLen:
                    pixelCounter =0
                    for m in range(scale):
                        bitmap += lineBitmap
                    lineBitmap = bytearray()    


    return bitmap

#Convert a character/string into an rgb byte array.
#This can read DNA letters (GTAC) and give each a colour
#Colour is 24 bit encoded RGB
def charToRGB(char, guanine, thymine, adenine, cytosine):
    # GTAC is passed in as string representing hex colour code
    
    

    if(char.lower() == "g"):
        return encodeRGB(guanine[0],guanine[1],guanine[2]) #G is Red
    if(char.lower() == "t"):
        return encodeRGB(thymine[0],thymine[1],thymine[2]) #T is Green
    if(char.lower() == "a"):
        return encodeRGB(adenine[0],adenine[1],adenine[2]) #A is Blue
    if(char.lower() == "c"):
        return encodeRGB(cytosine[0],cytosine[1],cytosine[2]) #C is Black

    return encodeRGB(255,255,255) #Default is white if not a DNA word


def hex2rgb(h):
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))



################################################################################
#                               Start
################################################################################

#see what args we have
 
def main(argv):

    #set up default colours
    cytosine = "ff0000"# [255,0,0] # red
    guanine = "00ff00"  #[0,255,0] green
    adenine = "0000ff"# [0,0,255] # blue
    thymine = "000000" #[0,0,0] # black  
    inputfile = ''
    outputfile = ''
    strScale = "1"
    try:
        opts, args = getopt.getopt(argv,"hi:o:s:c:a:t:g:",["inputfile=","outputfile=","help","scale","cytosine","adenine","thymine","guanine"])
    except getopt.GetoptError:
        print ("mkBMP.py -i <inputfile> -o <outputfile> -s <scalefactor>")
        print ("mkBMP.py --inputfile <inputfile> --outputfile <outputfile> --scalefactor <scalefactor>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ("mkBMP.py -i <inputfile> -o <outputfile> -s <scalefactor>")
            print ("mkBMP.py --inputfile <inputfile> --outputfile <outputfile> --scalefactor <scalefactor>\n")
            print ("input file is a txt file with genetic data in plain text GTAC etc\n")
            print ("output file is the destination of the bitmap")
            print ("NB if the file exists it will be clobbered\n")
            print ("scale factor is a factor to enlarge each pixel by")
            print ("scale factor must be a positive whole number\n")
            print ("default colour scheme can be overriden")
            print ("the switches are -g -t -a -c for guanine, thymine, adenine, and cytosine respectively")
            print ("the colour should be specified as a 24bit hex colour\n")
            print ("go to https://htmlcolorcodes.com for a colour picker which provides hexcodes\n\n")
            print ("NB limit input checking or error checking, be careful\n\n")
            print ("example:   python mkBMP.py -i dna.txt -o myDNA.bmp -s 16 -c 8B4232 -a 155995 -g DEA246 -t 462945")
          
            sys.exit()
        elif opt in ("-i", "--inputfile"):
            inputfile = arg
        elif opt in ("-o", "--outputfile"):
            outputfile = arg
        elif opt in ("-s", "--scalefactor"):
            strScale = arg
        elif opt in ("-c", "--cytosine"):
            cytosine = arg.lstrip('#')
        elif opt in ("-a", "--adenine"):
            adenine = arg.lstrip('#')
        elif opt in ("-t", "--thymine"):
            thymine = arg.lstrip('#')
        elif opt in ("-g", "--gaunine"):
            guanine = arg.lstrip('#')    

    if len(inputfile)==0:
        print ("No input file given")
        print ("mkBMP.py -h for help")
        sys.exit(2)
    if len(outputfile)==0:
        print ("No output file given")
        print ("mkBMP.py -h for help")
        sys.exit(2)    
    print ("Reading genetic data from: ", inputfile)
    print ("Writing bitmap to: ", outputfile)
    try :
        scale = int(strScale)
    except:
        print ("Cannot cast " + strScale +  " to int")
        print ("scalefactor must be >1 and a whole number")
        exit (2)
    if scale <1:
        scale = 1
        print ("Warning: scale was set to ", scale)
        print ("Shrinking is not implemented")
        print ("Resetting to scalefactor = 1")
        print ("") 
    print ("Scale factor: ", scale) 
    


#Create pixel array + get its properties dynamicaly

#Read as a string and make an array 
    with open (inputfile, 'r') as readObject:
        rawArray=readObject.read()

    stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)
    imageArray = stripped(rawArray)
    rowLen = 256  #How many rows this bitmap contains before scaling
    rows = math.floor(len(imageArray)/rowLen)  # BMP can't have incomplete rows, no padding so chop the incomplete row
    #change our hex colours string in to tuples
    
    tGuanine = hex2rgb(guanine)
    tThymine = hex2rgb(thymine)
    tAdenine = hex2rgb(adenine)
    tCytosine = hex2rgb(cytosine)
    
   

    pixelArray = genBitMap2(imageArray, rowLen, rows, scale, tGuanine, tThymine, tAdenine, tCytosine)
#size the bitmap according to the number of elements in the array 
    
    
    width = rowLen*scale #our scale factor
    height = rows*scale
    size = len(pixelArray)

#Create both the dib and bmp headers given the pixel array.
    dibHeader = winDibHeader24(width,height, size)
    bmpHeader = BmpHeader(len(dibHeader), len(pixelArray))



    f = open(outputfile, 'wb+') #Read/Write in binary format. **Overwrite** old file or create a new one.
    f.write(bmpHeader)
    f.write(dibHeader)
    f.write(pixelArray)
    f.close()

if __name__ == "__main__":
   main(sys.argv[1:])  

