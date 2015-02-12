#this is the std script the only difference between this script and the other script
#is the account number at the front of flagtext
import csv
import re
txtid={}


#this section looks for the rows that begin with flagtext
#when it finds one, it collects the next 25 and puts those numbers in an array called norow
#if you look in invtext.csv that should be the pattern - 26 lines including the line that is the same as flagtext
flagtext='32423340 PO BOX 12140 BURLINGTON, NC 27216-2140 (800) 343 - 4407 TAX ID: 13-3757370'
with open('../input/invtext.csv') as csvfile:
    reader=csv.DictReader(csvfile)
    norow=[]
    for row in reader:
        if row['TextRows']==flagtext:
            print('foundone')
            for i in range(int(row['Index']), int(row['Index'])+26):
                norow.append(i)
#all of the rows are placed in a dictionary called txtid - the key is the row number in the csv file and the value is the text of that row
        txtid[row['Index']]=row['TextRows']
    print('txtid has %d keys'%len(txtid.keys()))
#once norow has all of the numbers that need to be deleted, it removes those rows from txtid
for row in norow:
    txtid.pop(str(row), None)
print('txtid has %d keys'%len(txtid.keys()))

#this section makes a sorted list to get everything in its right place
sortlist=[]
for key in txtid.keys():
    sortlist.append(int(key))

sortlist.sort()

#this section writes all of the remaining rows in txtid to a csvfile called cleanedinvtxt.csv
with open('../output/cleanedinvtxt.csv', 'w', newline='') as csvfile:
    fieldnames=['Index', 'TextRows']
    writer=csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for number in sortlist:
        writer.writerow({'Index':sortlist.index(number)+1, 'TextRows':txtid[str(number)]})



