import csv
import re
txtid={}


def checkmissing(list1, list2):
    if len(list1)==len(list2):
        return "Everything is in order with these two."
    else:
        if len(list1)>len(list2):
            missing=[]
            for value in list1:
                if value not in list2:
                    missing.append(value)
        else:
            missing=[]
            for value in list2:
                if value not in list1:
                    missing.append(value)
        print("Missing Row[s]", missing)
        return missing
        
    return missing
        

#creating the dictionary txtid with the row numbers in the file as keys and the text of that row as value 
with open('../output/cleanedinvtxt.csv') as csvfile:
    reader=csv.DictReader(csvfile)
    for row in reader:
        txtid[int(row['Index'])]=row['TextRows']
      
#this section creates a dictionary called dateofservice with the row number as key and the date of service as values
#in re.search the pattern \d{1,2}\/\d{1,2}\/\d{2} means the following \d{1,2}=one or two digits, \/=/, \d{2}=two digits
#this pattern is used because the labcorp invoices set up the dates as 9/12/2014 10/2/2014, 1/1/2014, or 10/12/2014
#for each entry in the txtid dictionary, if there is a date in it, it will store that date in the dateofservice dictionary with the corresponding row number as the key
dateofservice={}
for key, value in txtid.items():
    try:
        found=re.search('\d{1,2}\/\d{1,2}\/\d{2}', value).group(0)
        indexval=key
        dateofservice[indexval]=found
    except AttributeError:
        found=''
##        print('Could not find what you are looking for.')

#this section pulls out the names and ids of the patients
#we collect the patient names by finding the date row again and collecting all of the characters
#starting from the date and ending at the first space non-space characters after a series of capital letters, commas, spaces, and apostrophes (i.e. the person's name)
#then we start at character 9 and stop at two characters toward the end to get rid of the space and non-space characters that don't belong to the name
#we add that to the name dictionary with the key of the row number in which it was found
mainrows=[]
name={}
for key, value in txtid.items():
    try:
        found=re.search('\d{1,2}\/\d{1,2}\/\d{2}\s[A-Z,\s,\,, \']+\s\S', value).group(0)
        indexval=key
        name[indexval]=found[9:len(found)-2]
        mainrows.append(indexval)
    except AttributeError:
        found=''
##        print('Could not find what you are looking for.')

#because the patientid rows are always the next one, we setup all id rows as the rows with names and dates plus one
idrows=[]
for row in mainrows:
    idrows.append(int(row)+1)

#not all patients have patient ids listed which is why we have the exception
patientid={}
for row in idrows:
    try:
        found=re.search('\d+', txtid[row]).group(0)
        patientid[row]=found[0:len(found)]
    except AttributeError:
        print("There doesn't seem to be a Patient ID for patient %s"%name[row-1])
        patientid[row]='No Pat ID'

#this section helps us make sure that the number of service dates that we have matches the number of names that we have
dateofservicelist=[]
for key in dateofservice.keys():
    dateofservicelist.append(key)

namelist=[]
for key in name.keys():
    namelist.append(key)

datename=checkmissing(dateofservicelist, namelist)


        

charge={}
i=0
j=0
k=0
#this section pulls all of the charges from the invoice rows by looking for a service of up to 3 digits followed by a decimal point and two more digits
#i, j, and k exist to check that no rows were not looked at i+j should equal k
for key, value in txtid.items():
    try:
        found=re.search('[0-9]{1,3}\.[0-9]{2}CR', value).group(0)
        indexval=key
        charge[key]="-"+found[:len(found)-2]
        j+=1
        k+=1
    except AttributeError:
        try:
            found=re.search('[0-9]{1,3}\.[0-9]{2}', value).group(0)
            indexval=key
            charge[key]=found
##        print(indexval, found)
            j+=1
            k+=1
        except AttributeError:
##        print('did not find', value)
            i+=1
            k+=1
            found=''
print('i is %d'%i)
print('j is %d'%j)
print('k is %d'%k)
##        print('Could not find what you are looking for.')
print('There are %d charges in this invoice' % len(charge.keys()))

#this section takes the row numbers of all of the charges in the list and sees if it's in the same row as a name
#if it is, it assigns it to that name
#if it isn't, it keeps looking in the previous rows until it finds the next name row and assigns it to that row
chargeassignment={}
for key in charge.keys():
    discovered=False
    lookupkey=key
##    print('key is %d'%lookupkey)
    while discovered==False:
        if lookupkey in name.keys():
            discovered=True
            chargeassignment[key]=lookupkey
##            print("it's here %d"%lookupkey)
            break
        else:            
            lookupkey-=1
##            print("it's not here %d"%lookupkey)
            continue
#this compiles all of the arrays that we made into a dictionary with the key as row number and the values as a list that contains the name, patientid, service date and charge amount
        
output={}
for key, value in chargeassignment.items():
    try:
        output[int(key)]=[name[int(value)], patientid[int(value)+1], dateofservice[int(value)], charge[int(key)]]
    except KeyError:
        print("There seems to have been a problem with %s"%name[int(value)])

#this area creates the csv file called patientcharges.csv and writes each item in output as a line       
with open('../output/patientcharges.csv', 'w', newline='') as csvfile:
    fieldnames=['ID', 'Name', 'PatID','Date of Service', 'Charge']
    writer=csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for k, v in output.items():
        writer.writerow({'ID':k, 'Name':v[0], 'PatID': v[1], 'Date of Service':v[2], 'Charge':v[3]})


