# DNAtoBMP
take GTAC DNA words in a text file and turn them in to a bitmap representing the DNA.   
text file must contain a single string with no control characters. String must contain only G,C,A,T and is not case dependent 


mkBMP.py -i inputfile -o outputfile -s scalefactor

OR

mkBMP.py --inputfile inputfile --outputfile outputfile --scalefactor scalefactor

example:

mkBMP.py -i dna.txt -o myShinybmp.bmp -s 2
         
input file is a txt file with genetic data
input file must only contain GTAC with no control codes such as line feed or carriage return

output file is the destination of the bitmap
NB if the file exists it will be clobbered
  
scale factor is a factor to enlarge each pixel by
scale factor must be an unsigned integer ie >1 and a whole number
we are not shrinking the bitmap and we are not having half pixels
factor 16 will give a bmp of width 4096 pixels  
