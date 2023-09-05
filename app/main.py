#!/usr/bin/python

import sys
import csv
import qrcode
import os
from textwrap import dedent

def main():

    # Loop with input csv file
    with open('input.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            # Skip column names row
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            
            # Set variables for easy usage
            id = row["id"].zfill(4)
            blood_type = row["bloodType"]
            email = row["email"]
            passport = row["passport"]
            ine = row["ine"]
            cell = row["cell"]
            position = row["position"].upper()

            # Get first and last name from email (first.last@aurom.net)
            temp_name = email.split("@")
            name = temp_name[0].split(".")
            firstname = name[0].title().upper()
            lastname = name[1].title().upper()

            # Create folder to store files
            folder = './people/' + id
            try:
                os.mkdir(folder)
            except:
                print ("Could not create folder " + folder)

            # Select photo id to print from ine / passport
            if passport != "NULL":
                print_id = passport
            elif ine != "NULL":
                print_id = ine
            else:
                print_id = "Missing Photo ID"

            # Create info text file
            info = open("people/"+id+"/"+id+"_info.txt", "x")
            info.write(
                       firstname + " " + lastname + "\n" +
                       position + "\n" +
                       id + "\n" +
                       blood_type + "\n" +
                       cell + "\n" +
                       email + "\n" +
                       print_id.upper() + "\n\n\n" +
                       "https://vcard.aurom.net/people/"+id+".vcf"
                       )
            info.close()

            # Create vcf card
            vcard = open("vcards/"+id+".vcf", "w")
            vcard.write(dedent('''\
                    BEGIN:VCARD
                    VERSION:3.0
                    N:'''+lastname+''';'''+firstname+''';;;
                    FN:'''+firstname+''' '''+lastname+'''
                    ORG:AUROM;
                    EMAIL;type=INTERNET;type=WORK;type=pref:'''+email+'''
                    TEL;type=CELL;type=VOICE;type=pref:'''+cell+'''
                    TEL;type=WORK;type=VOICE:+52 614 417 4040
                    TEL;type=WORK;type=VOICE:+52 614 410 3156
                    TEL;type=WORK;type=VOICE:+1 (915) 249-4582
                    item1.ADR;type=WORK;type=pref:;;Calle Mariano Jimenez 200\\nCol. Zona Centro;Chihuahua;Chihuahua;31000;Mexico
                    item1.X-ABADR:mx
                    item2.ADR;type=WORK:;;2417 E Yandell Dr.\\nSte B-127;El Paso;TX;79903;United States
                    item2.X-ABADR:us
                    URL;type=WORK;type=pref:https://www.aurom.net
                    END:VCARD'''))
            vcard.close()

            # Create QR code, less information to fit on the code
            # Data to be encoded
            data = (dedent('''\
                    BEGIN:VCARD
                    VERSION:3.0
                    N:'''+lastname+''';'''+firstname+''';;;
                    FN:'''+firstname+''' '''+lastname+'''
                    ORG:AUROM;
                    EMAIL;type=INTERNET;type=WORK;type=pref:'''+email+'''
                    TEL;type=CELL;type=VOICE;type=pref:'''+cell+'''
                    URL;type=WORK;type=pref:aurom.net
                    END:VCARD'''))
            # Encoding data using make() function
            img = qrcode.make(data)
            # Saving as an image file
            img.save("people/"+id+"/"+id+".png")

            # Count processed lines
            line_count += 1

            print ("Processed: " + email)


        print(f'Processed {line_count} lines.')


if __name__ == "__main__":
    main()
