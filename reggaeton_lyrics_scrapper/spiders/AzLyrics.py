import scrapy
from scrapy.http.request import Request
from reggaeton_lyrics_scrapper.items import ReggaetonLyricsScrapperItem

class AZ(scrapy.Spider):
    name = 'azlyrics'
    base_url = 'http://www.azlyrics.com/'
    # This is to get any reggaeton artis from wikipedia and start look them in azlyrics
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_reggaeton_musicians',
    ]
    items = []
    def parse(self, response):
        artists_links = response.xpath('//div[@id="bodyContent"]/div[not(contains(div/@id, "catlinks"))]//ul//a[contains(@href,"/wiki/")]/text()').extract()
        artists = self.get_artists_names(artists_links)
        for artist in artists:
            reggaetonLyricsScrapperItem = ReggaetonLyricsScrapperItem()
            reggaetonLyricsScrapperItem['author'] = artist
            yield Request(url=self.get_artist_url(artist),meta={'item':reggaetonLyricsScrapperItem},
                callback=self.parse_songs)
        return

    def parse_songs(self,response):
        songs_links = response.xpath('//a[contains(@target,"blank")]/text()').extract()
        reggaetonLyricsScrapperItem = response.meta['item']
        if songs_links > 0:
            for song in songs_links:
                reggaetonLyricsScrapperItem = response.meta['item']
                reggaetonLyricsScrapperItem = reggaetonLyricsScrapperItem.copy()
                reggaetonLyricsScrapperItem['name'] = song
                print song
                yield Request(url=self.get_lyric_url(reggaetonLyricsScrapperItem['author'],song),meta={'item':reggaetonLyricsScrapperItem},
                    callback=self.parse_lyric)
        return
    def parse_lyric(self,response):
        lyric = response.xpath('//div[contains(@class,"col-xs-12 col-lg-8 text-center")]//div[5]/text()').extract()
        if lyric:
            print lyric
            reggaetonLyricsScrapperItem = response.meta['item']
            reggaetonLyricsScrapperItem = reggaetonLyricsScrapperItem.copy()
            reggaetonLyricsScrapperItem['lyric'] = lyric
            return reggaetonLyricsScrapperItem

    def get_artists_names(self,artists):
        import unicodedata
        result = []
        for artist in artists:
            author_name = unicodedata.normalize('NFD', artist.lower().replace(' ','')).encode('ascii', 'ignore')
            if '&' in author_name:
                '''
                Sometimes the artists are groups of 2 or more people.
                In Wikipedia, they are written like this:

                    `artist1&artist2`

                In azlyrics, some of the items are separated
                with "y" (not to all), this blocks put the artis name with y .
                '''
                result.append(author_name.replace('&','y'))
            result.append(author_name)
        return result

    def get_artist_url(self,artist):
        '''
        The url for AZlyrics is

            `aritst_first_letter/artist_name.html`
        '''
        return self.base_url + artist[0] + '/' + artist + '.html'

    def get_lyric_url(self,artist,song):
        return self.base_url + 'lyrics' + '/' + artist + '/' + song.lower().replace(' ','') + '.html'
