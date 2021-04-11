import os


def findUniqueHeadings(entriesDir):
    Headings = []
    for entry in entriesDir:
        if(entry.endswith('.json')):
            continue
        tokens = entry.split('_')
        heading = tokens[1]

        if(heading in Headings):
            continue

        Headings.append(heading)
    return Headings


def getEntries(entriesDir, heading):

    entries = []
    for entry in entriesDir:
        if(entry.endswith('.json')):
            continue
        elif(heading in entry):
            entries.append(entry)

    return entries

# def indexFilingDates(file, entries):
#     file.

def deleteFileContent(pfile):
    pfile.seek(0)
    pfile.truncate()