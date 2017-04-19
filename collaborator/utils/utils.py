import hashlib
import time


def getTime():
    return int(round(time.time() * 1000))


def clearFile(path):
    open(path, 'w').close()


def hashContent(content):
    hash_content_object = hashlib.md5(content.encode())
    hash_content = hash_content_object.hexdigest()
    return hash_content


def basicShape(record):
    well_formed_record = [el for el in record if el[0] != ' ']
    for r in well_formed_record:
        if r[0] == '-':
            for entry in well_formed_record:
                if entry == '+ ' + r[2:]:
                    well_formed_record.remove(r)
                    well_formed_record.remove(entry)
                    break
    return well_formed_record


def writeLine(path, line):
    with open(path, 'a') as records_file:
        records_file.write(line + '\n')


def saveRecords(path, records):
    with open(path, 'a') as records_file:
        for timestamp, record in records.items():
            for diff in record:
                records_file.write(str(timestamp) + ' ' + diff + '\n')
