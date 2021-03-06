from __future__ import unicode_literals

from tests.frontends.mpd import protocol


class MusicDatabaseHandlerTest(protocol.BaseTestCase):
    def test_count(self):
        self.sendRequest('count "tag" "needle"')
        self.assertInResponse('songs: 0')
        self.assertInResponse('playtime: 0')
        self.assertInResponse('OK')

    def test_findadd(self):
        self.sendRequest('findadd "album" "what"')
        self.assertInResponse('OK')

    def test_listall(self):
        self.sendRequest('listall "file:///dev/urandom"')
        self.assertEqualResponse('ACK [0@0] {} Not implemented')

    def test_listallinfo(self):
        self.sendRequest('listallinfo "file:///dev/urandom"')
        self.assertEqualResponse('ACK [0@0] {} Not implemented')

    def test_lsinfo_without_path_returns_same_as_listplaylists(self):
        lsinfo_response = self.sendRequest('lsinfo')
        listplaylists_response = self.sendRequest('listplaylists')
        self.assertEqual(lsinfo_response, listplaylists_response)

    def test_lsinfo_with_empty_path_returns_same_as_listplaylists(self):
        lsinfo_response = self.sendRequest('lsinfo ""')
        listplaylists_response = self.sendRequest('listplaylists')
        self.assertEqual(lsinfo_response, listplaylists_response)

    def test_lsinfo_for_root_returns_same_as_listplaylists(self):
        lsinfo_response = self.sendRequest('lsinfo "/"')
        listplaylists_response = self.sendRequest('listplaylists')
        self.assertEqual(lsinfo_response, listplaylists_response)

    def test_update_without_uri(self):
        self.sendRequest('update')
        self.assertInResponse('updating_db: 0')
        self.assertInResponse('OK')

    def test_update_with_uri(self):
        self.sendRequest('update "file:///dev/urandom"')
        self.assertInResponse('updating_db: 0')
        self.assertInResponse('OK')

    def test_rescan_without_uri(self):
        self.sendRequest('rescan')
        self.assertInResponse('updating_db: 0')
        self.assertInResponse('OK')

    def test_rescan_with_uri(self):
        self.sendRequest('rescan "file:///dev/urandom"')
        self.assertInResponse('updating_db: 0')
        self.assertInResponse('OK')


class MusicDatabaseFindTest(protocol.BaseTestCase):
    def test_find_album(self):
        self.sendRequest('find "album" "what"')
        self.assertInResponse('OK')

    def test_find_album_without_quotes(self):
        self.sendRequest('find album "what"')
        self.assertInResponse('OK')

    def test_find_artist(self):
        self.sendRequest('find "artist" "what"')
        self.assertInResponse('OK')

    def test_find_artist_without_quotes(self):
        self.sendRequest('find artist "what"')
        self.assertInResponse('OK')

    def test_find_filename(self):
        self.sendRequest('find "filename" "afilename"')
        self.assertInResponse('OK')

    def test_find_filename_without_quotes(self):
        self.sendRequest('find filename "afilename"')
        self.assertInResponse('OK')

    def test_find_file(self):
        self.sendRequest('find "file" "afilename"')
        self.assertInResponse('OK')

    def test_find_file_without_quotes(self):
        self.sendRequest('find file "afilename"')
        self.assertInResponse('OK')

    def test_find_title(self):
        self.sendRequest('find "title" "what"')
        self.assertInResponse('OK')

    def test_find_title_without_quotes(self):
        self.sendRequest('find title "what"')
        self.assertInResponse('OK')

    def test_find_date(self):
        self.sendRequest('find "date" "2002-01-01"')
        self.assertInResponse('OK')

    def test_find_date_without_quotes(self):
        self.sendRequest('find date "2002-01-01"')
        self.assertInResponse('OK')

    def test_find_date_with_capital_d_and_incomplete_date(self):
        self.sendRequest('find Date "2005"')
        self.assertInResponse('OK')

    def test_find_else_should_fail(self):
        self.sendRequest('find "somethingelse" "what"')
        self.assertEqualResponse('ACK [2@0] {find} incorrect arguments')

    def test_find_album_and_artist(self):
        self.sendRequest('find album "album_what" artist "artist_what"')
        self.assertInResponse('OK')


class MusicDatabaseListTest(protocol.BaseTestCase):
    def test_list_foo_returns_ack(self):
        self.sendRequest('list "foo"')
        self.assertEqualResponse('ACK [2@0] {list} incorrect arguments')

    ### Artist

    def test_list_artist_with_quotes(self):
        self.sendRequest('list "artist"')
        self.assertInResponse('OK')

    def test_list_artist_without_quotes(self):
        self.sendRequest('list artist')
        self.assertInResponse('OK')

    def test_list_artist_without_quotes_and_capitalized(self):
        self.sendRequest('list Artist')
        self.assertInResponse('OK')

    def test_list_artist_with_query_of_one_token(self):
        self.sendRequest('list "artist" "anartist"')
        self.assertEqualResponse(
            'ACK [2@0] {list} should be "Album" for 3 arguments')

    def test_list_artist_with_unknown_field_in_query_returns_ack(self):
        self.sendRequest('list "artist" "foo" "bar"')
        self.assertEqualResponse('ACK [2@0] {list} not able to parse args')

    def test_list_artist_by_artist(self):
        self.sendRequest('list "artist" "artist" "anartist"')
        self.assertInResponse('OK')

    def test_list_artist_by_album(self):
        self.sendRequest('list "artist" "album" "analbum"')
        self.assertInResponse('OK')

    def test_list_artist_by_full_date(self):
        self.sendRequest('list "artist" "date" "2001-01-01"')
        self.assertInResponse('OK')

    def test_list_artist_by_year(self):
        self.sendRequest('list "artist" "date" "2001"')
        self.assertInResponse('OK')

    def test_list_artist_by_genre(self):
        self.sendRequest('list "artist" "genre" "agenre"')
        self.assertInResponse('OK')

    def test_list_artist_by_artist_and_album(self):
        self.sendRequest(
            'list "artist" "artist" "anartist" "album" "analbum"')
        self.assertInResponse('OK')

    ### Album

    def test_list_album_with_quotes(self):
        self.sendRequest('list "album"')
        self.assertInResponse('OK')

    def test_list_album_without_quotes(self):
        self.sendRequest('list album')
        self.assertInResponse('OK')

    def test_list_album_without_quotes_and_capitalized(self):
        self.sendRequest('list Album')
        self.assertInResponse('OK')

    def test_list_album_with_artist_name(self):
        self.sendRequest('list "album" "anartist"')
        self.assertInResponse('OK')

    def test_list_album_by_artist(self):
        self.sendRequest('list "album" "artist" "anartist"')
        self.assertInResponse('OK')

    def test_list_album_by_album(self):
        self.sendRequest('list "album" "album" "analbum"')
        self.assertInResponse('OK')

    def test_list_album_by_full_date(self):
        self.sendRequest('list "album" "date" "2001-01-01"')
        self.assertInResponse('OK')

    def test_list_album_by_year(self):
        self.sendRequest('list "album" "date" "2001"')
        self.assertInResponse('OK')

    def test_list_album_by_genre(self):
        self.sendRequest('list "album" "genre" "agenre"')
        self.assertInResponse('OK')

    def test_list_album_by_artist_and_album(self):
        self.sendRequest(
            'list "album" "artist" "anartist" "album" "analbum"')
        self.assertInResponse('OK')

    ### Date

    def test_list_date_with_quotes(self):
        self.sendRequest('list "date"')
        self.assertInResponse('OK')

    def test_list_date_without_quotes(self):
        self.sendRequest('list date')
        self.assertInResponse('OK')

    def test_list_date_without_quotes_and_capitalized(self):
        self.sendRequest('list Date')
        self.assertInResponse('OK')

    def test_list_date_with_query_of_one_token(self):
        self.sendRequest('list "date" "anartist"')
        self.assertEqualResponse(
            'ACK [2@0] {list} should be "Album" for 3 arguments')

    def test_list_date_by_artist(self):
        self.sendRequest('list "date" "artist" "anartist"')
        self.assertInResponse('OK')

    def test_list_date_by_album(self):
        self.sendRequest('list "date" "album" "analbum"')
        self.assertInResponse('OK')

    def test_list_date_by_full_date(self):
        self.sendRequest('list "date" "date" "2001-01-01"')
        self.assertInResponse('OK')

    def test_list_date_by_year(self):
        self.sendRequest('list "date" "date" "2001"')
        self.assertInResponse('OK')

    def test_list_date_by_genre(self):
        self.sendRequest('list "date" "genre" "agenre"')
        self.assertInResponse('OK')

    def test_list_date_by_artist_and_album(self):
        self.sendRequest('list "date" "artist" "anartist" "album" "analbum"')
        self.assertInResponse('OK')

    ### Genre

    def test_list_genre_with_quotes(self):
        self.sendRequest('list "genre"')
        self.assertInResponse('OK')

    def test_list_genre_without_quotes(self):
        self.sendRequest('list genre')
        self.assertInResponse('OK')

    def test_list_genre_without_quotes_and_capitalized(self):
        self.sendRequest('list Genre')
        self.assertInResponse('OK')

    def test_list_genre_with_query_of_one_token(self):
        self.sendRequest('list "genre" "anartist"')
        self.assertEqualResponse(
            'ACK [2@0] {list} should be "Album" for 3 arguments')

    def test_list_genre_by_artist(self):
        self.sendRequest('list "genre" "artist" "anartist"')
        self.assertInResponse('OK')

    def test_list_genre_by_album(self):
        self.sendRequest('list "genre" "album" "analbum"')
        self.assertInResponse('OK')

    def test_list_genre_by_full_date(self):
        self.sendRequest('list "genre" "date" "2001-01-01"')
        self.assertInResponse('OK')

    def test_list_genre_by_year(self):
        self.sendRequest('list "genre" "date" "2001"')
        self.assertInResponse('OK')

    def test_list_genre_by_genre(self):
        self.sendRequest('list "genre" "genre" "agenre"')
        self.assertInResponse('OK')

    def test_list_genre_by_artist_and_album(self):
        self.sendRequest(
            'list "genre" "artist" "anartist" "album" "analbum"')
        self.assertInResponse('OK')


class MusicDatabaseSearchTest(protocol.BaseTestCase):
    def test_search_album(self):
        self.sendRequest('search "album" "analbum"')
        self.assertInResponse('OK')

    def test_search_album_without_quotes(self):
        self.sendRequest('search album "analbum"')
        self.assertInResponse('OK')

    def test_search_artist(self):
        self.sendRequest('search "artist" "anartist"')
        self.assertInResponse('OK')

    def test_search_artist_without_quotes(self):
        self.sendRequest('search artist "anartist"')
        self.assertInResponse('OK')

    def test_search_filename(self):
        self.sendRequest('search "filename" "afilename"')
        self.assertInResponse('OK')

    def test_search_filename_without_quotes(self):
        self.sendRequest('search filename "afilename"')
        self.assertInResponse('OK')

    def test_search_file(self):
        self.sendRequest('search "file" "afilename"')
        self.assertInResponse('OK')

    def test_search_file_without_quotes(self):
        self.sendRequest('search file "afilename"')
        self.assertInResponse('OK')

    def test_search_title(self):
        self.sendRequest('search "title" "atitle"')
        self.assertInResponse('OK')

    def test_search_title_without_quotes(self):
        self.sendRequest('search title "atitle"')
        self.assertInResponse('OK')

    def test_search_any(self):
        self.sendRequest('search "any" "anything"')
        self.assertInResponse('OK')

    def test_search_any_without_quotes(self):
        self.sendRequest('search any "anything"')
        self.assertInResponse('OK')

    def test_search_date(self):
        self.sendRequest('search "date" "2002-01-01"')
        self.assertInResponse('OK')

    def test_search_date_without_quotes(self):
        self.sendRequest('search date "2002-01-01"')
        self.assertInResponse('OK')

    def test_search_date_with_capital_d_and_incomplete_date(self):
        self.sendRequest('search Date "2005"')
        self.assertInResponse('OK')

    def test_search_else_should_fail(self):
        self.sendRequest('search "sometype" "something"')
        self.assertEqualResponse('ACK [2@0] {search} incorrect arguments')
