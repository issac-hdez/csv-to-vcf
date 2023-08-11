#!/usr/bin/python

import sys
import csv
import qrcode
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
            id = row["id"]
            firstname = row["firstname"]
            lastname = row["lastname"]
            email = row["email"]
            cell = row["cell"]

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
                    TEL;type=WORK;type=VOICE:+52 614 417 4040
                    URL;type=WORK;type=pref:https://www.aurom.net
                    END:VCARD'''))
            # Encoding data using make() function
            img = qrcode.make(data)
            # Saving as an image file
            img.save('qrcodes/'+id+'.png')

            # Count processed lines
            line_count += 1


        print(f'Processed {line_count} lines.')


if __name__ == "__main__":
    main()
