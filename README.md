# top_100_spotify

Program that takes the top 100 songs from billboard from a certain date and makes a playlist.

I used the packages:
    bs4
    spotipy
    requests.

Program uses bs4 to scrape the Billboard website for a certain date and returns it into a list. The spotipy then uses the names of the songs and find data about them. It the creates a playlist and adds all the songs using the uri.

