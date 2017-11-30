1. Download the LabCorp invoice pdf file from the LabCorp website.
2. Copy and paste the charges from the LabCorp invoice pdf into invtext.csv.
3. Number each row in invtext.csv.
4. Close the file and run cleanpdfhiv.py or cleanpdfstd.py, depending on the invoice that you’re getting the charges from.
5. Next, run the file pdfcsvparser.py to pull the charges from cleanedinvtxt.csv.
6. Create a pivot table using the data in patientcharges.csv which you can find in the output folder.
