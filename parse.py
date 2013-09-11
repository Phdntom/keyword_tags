
import json
import csv
import sys


count = 8047532 

#------

def get_lines(reader, chunk_size = 1024):
    '''
    '''
    lines = []
    eof = False
    for i in range(chunk_size):
        try:
            lines.append(reader.next())
        except StopIteration:
            eof = True
            break
    return lines, eof

def convert_csv_to_json(csv_name, json_name = None):
    '''
    '''
    if json_name is None:
        names = csv_name.split('.')
        if names[-1] == "csv":
            print("OK. Changing file extension to '.json'.")
        else:
            print("File {0} does not have a valid '.csv' extension.\n"\
                  "Attempting using given file.".format(csv_name) )
        json_name = names[0] + ".json"
        print json_name


    with open(csv_name,'rb') as csvfile, open(json_name, 'w') as jsonfile:

        reader = csv.DictReader(csvfile, delimiter = ',', quotechar = '"')
        chunk_size = 1024

        while True:
            lines, eof = get_lines(reader, chunk_size)
            data_list = [ json.dumps(line) for line in lines ]
            jsonfile.write( "\n".join(data_list) )
            if eof:
                break
            else:
                jsonfile.write('\n')


if __name__ == "__main__":
    convert_csv_to_json(sys.argv[1])


#    with open(csv_name,'rb') as csvfile, open(json_name, 'w') as jsonfile:
#        reader = csv.DictReader(csvfile, delimiter = ',', quotechar = '"')
#        for row in reader:
#            print(row)
#            data = json.dumps( [r for r in row] )
#            jsonfile.write(data)



