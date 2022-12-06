# Census Data Cleaner
A research tool made to parse a US Census csv file

VERY EARLY STAGE

[RIT Research Page](https://www.rit.edu/gccis/geoinfosciencecenter/nsf-civic)
## Usage
censusParser.py filename [-print_help] [-keep]

## Process

Tool will go through the file twice. First it will tokenize all the possible categories
in the columns. From there the user will be prompted to select which column attributes to remove.
Currently, as it stands each column contains "attributes" which are split by a 
"|" separator, which is then tokenized.
After selecting which attributes to remove it will start at the beginning of the
file and start to process and clean all the info. By default, it will remove all
columns that contain null, currently no way to not have this happen
(planned to add functionality to keep all null column). Finally, it will write 
all cleaned data to outputFile.csv