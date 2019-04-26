from mastodon import Mastodon
from datetime import datetime
from dateutil.tz import tzutc
import sys
import pickle

mastodon = Mastodon(
    access_token = 'user.secret',
    api_base_url = 'https://machteburch.social'
)

stored = pickle.load(open('users.pickle', 'rb'))

print("Getting new toots... ", end='')

toots = []
for user, lsid in stored.items():
    for rawtoot in reversed(mastodon.account_statuses(user, since_id=lsid)):
        stored[user] = int(rawtoot['id'])
        if rawtoot['reblog'] == None:
            for tag in rawtoot['tags']:
                if tag['name'] == 'mastoadmin': toots.append(rawtoot)

toots = sorted(toots, key=lambda toot: toot['created_at'].timestamp())

print('Found: ' + str(len(toots)))
print('Retooting... ', end='')

for toot in toots:
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        print(str(toot['id']) + ' by ' + toot['account']['username'])
    else:
        print(str(toot['id']) + ' by ' + toot['account']['username'])
        mastodon.status_reblog(toot['id'])

print('Done')
print('Storing last toot id...', end='')

pickle.dump(stored, open('users.pickle', 'wb'))

print('Done')
print('Bye bye!')
