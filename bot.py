from mastodon import Mastodon
from datetime import datetime
from dateutil.tz import tzutc
import sys

mastodon = Mastodon(
    access_token = 'user.secret',
    api_base_url = 'https://machteburch.social'
)

f = open('users.txt', 'r')

toots = []
lastid = {}
for line in f:
    user, lsid = line.split(':', 1)
    lastid[user] = int(lsid)
    for rawtoot in reversed(mastodon.account_statuses(user, since_id=lsid)):
        lastid[user] = rawtoot['id']
        if rawtoot['reblog'] == None:
            for tag in rawtoot['tags']:
                if tag['name'] == 'mastoadmin': toots.append(rawtoot)

toots = sorted(toots, key=lambda toot: toot['created_at'].timestamp())

for toot in toots:
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        print(str(toot['id']) + ' by ' + toot['account']['username'])
    else:
        mastodon.status_reblog(toot['id'])

f.close()
f = open('users.txt', 'w')

print(lastid)
for user in lastid.keys():
    f.write(str(user) + ':' + str(lastid[user]) + '\r\n')

f.close()
