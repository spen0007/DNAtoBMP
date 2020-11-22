# DNAtoBMP
take GTAC DNA words in a text file and turn them in to a bitmap representing the DNA.   
text file must contain a single string with no control characters. String must contain only G,C,A,T and is not case dependent 


mkBMP.py -i <inputfile> -o <outputfile> -s <scalefactor>
mkBMP.py --inputfile <inputfile> --outputfile <outputfile> --scalefactor <scalefactor>

input file is a txt file with genetic data in plain text GTAC etc

output file is the destination of the bitmap
NB if the file exists it will be clobbered

scale factor is a factor to enlarge each pixel by
scale factor must be a positive whole number
scale factor 16 provides a 4096 pixel width

default colour scheme can be overriden
the switches are -g -t -a -c for guanine, thymine, adenine, and cytosine respectively.
the colour should be specified as a 24bit hex colour

go to https://htmlcolorcodes.com for a colour picker which provides hexcodes


NB limit input checking or error checking, be careful


example:   python mkBMP.py -i dna.txt -o myDNA.bmp -s 16 -c 8B4232 -a 155995 -g DEA246 -t 462945
