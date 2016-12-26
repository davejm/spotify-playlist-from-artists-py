#!/usr/bin/env python3
import spotipy
import sys


spotify = spotipy.Spotify()

if len(sys.argv) > 1:
    name = ' '.join(sys.argv[1:])
else:
    print("Usage: %s artist" % (sys.argv[0],))
    sys.exit()

results = spotify.search(q='artist:' + name, type='artist')
artists = results['artists']['items']
for artist in artists:
    print(artist['name'], artist['popularity'], artist['uri'])
