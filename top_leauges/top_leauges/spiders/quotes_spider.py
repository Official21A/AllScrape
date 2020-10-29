import scrapy


DIR = "./output/" # A dir to save the responses


class QuotesSpider(scrapy.Spider): # the spider class to scrape the url page
    name = "quotes" # each class should have its own unique name

    def start_requests(self):
        # this method creates a url list for class
        # we can just define a list like a normal var in class insted of this
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # this method gets the reponses and creates a file to save them
        page = response.url.split("/")[-2]
        filename = f'{DIR}quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

    def other_parse(self, response):
    	# this method will follow a link to the next page of url site
    	# if you want just change the name to parse and remove the parse method
    	for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

    	next_page = response.css('li.next a::attr(href)').get()
    	if next_page is not None:
            yield response.follow(next_page, callback=self.parse) # following

        # a shortcut for doing this is :
        # yield from response.follow_all(css='ul.pager a', callback=self.parse)

# a usefull way to scrape and get the data you want is to use
# >> scrapy shell 'url_domain_name'  
# this will open the scrapy shell for testing and getting the data.      