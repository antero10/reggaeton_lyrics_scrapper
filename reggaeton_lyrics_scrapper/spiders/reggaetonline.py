import scrapy
from scrapy.http.request import Request
from reggaeton_lyrics_scrapper.items import ReggaetonLyricsScrapperItem
import sys
reload(sys)
sys.setdefaultencoding('utf8')
class ReggaetonOnline(scrapy.Spider):
    name = 'ReggaetonOnline'
    base_url = 'http://www.reggaetonline.net/'
    start_urls = [
        'http://www.reggaetonline.net/es-artistas-reggaeton.php',
    ]
    items = []
    def parse(self, response):
        urls = response.xpath('//table[1]//tr//td/div//text()').extract()
        for url in urls:
            reggaetonLyricsScrapperItem = ReggaetonLyricsScrapperItem()
            author_name = url.lower().replace(' ', '-').replace(':','')
            reggaetonLyricsScrapperItem['author'] = author_name
            new_url = self.base_url + author_name + '_liricas-2'
            yield Request(url=new_url,meta={'item':reggaetonLyricsScrapperItem},
                callback=self.parse_songs)
        return

    def parse_songs(self,response):
        songs = response.xpath('//a[contains(@class,"NORM")][1]/text()').extract()
        if len(songs) > 1:
            for song in songs:
                song_name = song.lower().rstrip('\r\n').strip().replace(' ','-')
                if song_name:
                    reggaetonLyricsScrapperItem = response.meta['item']
                    reggaetonLyricsScrapperItem = reggaetonLyricsScrapperItem.copy()
                    reggaetonLyricsScrapperItem['name'] = song_name
                    new_url = self.base_url + song_name + '_liricas'
                    yield Request(url=new_url,meta={'item':reggaetonLyricsScrapperItem },
                    callback=self.parse_lyrics)
        return

    def parse_lyrics(self,response):
        text = response.xpath('//div[@id="artist_main"]//p[last()]/text()').extract()
        rating = response.xpath('//div[@id="artist_main"]/div[1]/div/small/span/text()').extract()
        try:
            lyric = ''.join([str(x) for x in text]).lower().rstrip('\r\n').strip()
            if lyric:
                reggaetonLyricsScrapperItem = response.meta['item']
                reggaetonLyricsScrapperItem = reggaetonLyricsScrapperItem.copy()
                reggaetonLyricsScrapperItem['lyric'] = lyric
                print '****' * 30
                print rating
                return reggaetonLyricsScrapperItem
        except Exception as e:
            print str(e)
            sys.exit()
        return None
