


def myfun(stfd):
    import csv
    nid = []
    authorid = []
    type = []
    title = []
    content = []
    uid = []
    with open('/Users/rohithreddyv/Desktop/AW Final Project/Final_Project/notes/notecards.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            nid.append(row[0])
            authorid.append(row[1])
            type.append(row[2])
            title.append(row[3])
            content.append(row[4])
    for i in range(1, 676):
        notes.objects.create(noteid=int(nid[i]), authorid=int(authorid[i]), type=bool(type[i]), username=authorid[i],
                             points=0, title=title[i], content=content[i])

myfun("lol")
