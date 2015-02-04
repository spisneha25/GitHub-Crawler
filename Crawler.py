import json, csv, time, requests
token = #API token
user = #username
TotalCount = 5400
Count = 0
FCount = 0
users = []
username = {}
userdata = []
linkdata = []
olduserdata = []
oldlinkdata = []

try:
        with open('userdata.sv', 'rb') as csvr:
                csvread = csv.reader(csvr, delimiter=",", quotechar = '|')
                for r in csvread:
                        users.append(r[0])
                        username[r[0]] = 1
                        olduserdata.append(r)

        with open('linkdata.csv', 'rb') as csvr:
                csvread = csv.reader(csvr, delimiter=",", quotechar = '|')
                for r in csvread:
                        oldlinkdata.append(r)
                        
except:
        pass

if not len(users):
        users.append(#seed)
        username = {#seed:1}

iterno = len(users)-1

while Count < TotalCount or FCount < TotalCount:
    print iterno
    url = 'https://api.github.com/users/' + users[iterno]
    reads = requests.get(url,auth=(user,token));
    data = json.loads(reads.content)
    u = []
    u.append(data['login'].encode('utf-8'))
    u.append(data['followers'])
    u.append(data['following'])
    userdata.append(u)

    followers = data['followers']
    if followers > 210:
        pages = 7
    else:
        pages = followers/30
        if followers%30 != 0:
            pages = pages+1

    for p in range(pages):
        urlp = 'https://api.github.com/users/' + users[iterno] + '/followers?page=' + str(p)
        readsp = requests.get(urlp,auth=(user,token));
        datap = json.loads(readsp.content)
        time.sleep(1)

        for d in datap:
            if not (username.has_key(d['login'])):
                username[d['login'].encode('utf-8')] = 1
                users.append(d['login'].encode('utf-8'))
                Count = Count + 1
                             
                link = []
                link.append(data['login'].encode('utf-8'))
                link.append(d['login'].encode('utf-8'))
                linkdata.append(link)

    following = data['following']
    if following > 210:
        pagesf = 7
    else:
        pagesf = following/30
        if followers%30 != 0:
            pagesf = pagesf+1

    for p in range(pagesf):
        urlp = 'https://api.github.com/users/' + users[iterno] + '/following?page=' + str(p)
        readsp = requests.get(urlp,auth=(user,token));
        datap = json.loads(readsp.content)
        time.sleep(1)

        for d in datap:
            if not (username.has_key(d['login'])):
                username[d['login'].encode('utf-8')] = 1
                users.append(d['login'].encode('utf-8'))
                FCount = FCount + 1
                             
                link = []
                link.append(d['login'].encode('utf-8'))
                link.append(data['login'].encode('utf-8'))
                linkdata.append(link)
                
    iterno = iterno + 1
    
writeuser = []
writelink = []

for l in olduserdata:
        writeuser.append(l)

for l in userdata:
        writeuser.append(l)

for l in oldlinkdata:        
        writelink.append(l)

for l in linkdata:        
        writelink.append(l)

with open("userdatatoku.csv", "wb") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for line in writeuser:
        writer.writerow(line)
        
with open("linkdatatoku.csv", "wb") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for line in writelink:
        writer.writerow(line)
