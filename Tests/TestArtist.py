import unittest
from PRY2AYED20.src.artist import Artist

class TestArtist(unittest.TestCase):

    def test_artist_initialization(self):
        name = "John Doe"
        mood = "Happy"
        genre = "Rock"
        artist = Artist(name, mood, genre)

        self.assertEqual(artist.name, name)
        self.assertEqual(artist.mood, mood)
        self.assertEqual(artist.genre, genre)

if __name__ == '__main__':
    unittest.main()
