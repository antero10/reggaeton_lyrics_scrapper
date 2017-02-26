from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from reggaeton_lyrics_scrapper.spiders.reggaetonline import ReggaetonOnline
from reggaeton_lyrics_scrapper.spiders.AzLyrics import AZ

configure_logging()
runner = CrawlerRunner()
runner.crawl(ReggaetonOnline)
runner.crawl(AZ)
d = runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run()
