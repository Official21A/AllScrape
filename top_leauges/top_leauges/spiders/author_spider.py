import scrapy


class AuthorSpider(scrapy.Spider): # an other class for example
    name = "author" # class name

    start_urls = ['http://quotes.toscrape.com/'] # web urls , defined directly

    def parse(self, response):
        # to follow all the a tags
        author_page_links = response.css('.author + a')
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = response.css('li.next a')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        # a method for getting the page and take the data we want from it
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }