#!/usr/bin/env python3
import spotipy
import spotipy.util as util
import sys


class PlaylistFromArtists:
    def __init__(self, username, artist_uris_path):
        self.username = username
        self.artist_uris_path = artist_uris_path
        scope = 'playlist-modify-public'
        token = util.prompt_for_user_token(username, scope)

        if token:
            self.sp = spotipy.Spotify(auth=token)
            self.sp.trace = False
        else:
            raise("Can't get token for", username)

    def _read_uris_from_file(self):
        uris = []
        with open(self.artist_uris_path) as f:
            for line in f.read().splitlines():
                uris.append(line.split()[0])
        return uris

    def _top_tracks(self, artist_uris):
        track_uris = []
        for artist_uri in artist_uris:
            top_tracks = self.sp.artist_top_tracks(artist_uri)['tracks']
            for track in top_tracks:
                track_uris.append(track['uri'])
        return track_uris

    def _create_playlist(self, name):
        playlist = self.sp.user_playlist_create(self.username, name)
        return playlist['id']

    def _chunkify(self, list, n):
        """Converts a list into sublists of max size n"""
        chunks = [list[x:x+n] for x in range(0, len(list), n)]
        return chunks

    def _add_tracks_to_playlist(self, playlist_id, track_uris):
        # Can only add a maximum of 100 songs per request
        chunks = self._chunkify(track_uris, 100)
        for chunk in chunks:
            self.sp.user_playlist_add_tracks(self.username, playlist_id, chunk)

    def pl_from_artists(self, playlist_name):
        artist_uris = self._read_uris_from_file()
        top_tracks = self._top_tracks(artist_uris)
        playlist_id = self._create_playlist(playlist_name)
        self._add_tracks_to_playlist(playlist_id, top_tracks)


if __name__ == '__main__':
    if len(sys.argv) > 3:
        username = sys.argv[1]
        artists_file = sys.argv[2]
        playlist_name = sys.argv[3]

        pl_from_artists = PlaylistFromArtists(username, artists_file)
        pl_from_artists.pl_from_artists(playlist_name)
        print("Done!")
    else:
        print("Usage: %s username artists-file-path playlist-name" % (sys.argv[0],))
        sys.exit()
