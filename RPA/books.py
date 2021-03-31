from useful_lib import wait_for_pageload
import rpa as t


class Library:

	def __init__(self):
		self.url = 'https://nlb.overdrive.com'
		self.search_query_prefix = '/search?query='
		self.search_query = ''
		self.search_info = {    'title'         : [],
								'sub_title'     : [],
								'author'        : [],
								'book_type'     : [],
								'ratings'       : [],
								'availablity'   : []
							}


	def read_info_from_page(self, dict_ref):
		title          = t.read('//h1')
		sub_title      = t.read('//h1/following-sibling::div[@class="TitleSeries"]')
		author         = t.read('//h1/following-sibling::div[@class="TitleDetailsHeading-creator"]')
		book_type      = t.read('//h1/following-sibling::span')
		ratings        = t.read('//h1/../following-sibling::div[@class="js-starRatingsContainer"]//@data-global-rating')
		availablity    = t.read('//h1/../following-sibling::div[@class="show-for-600-up js-copiesAvailableContainer"]//span')

		self.search_info["title"].append(title)
		self.search_info["sub_title"].append(sub_title)
		self.search_info["author"].append(author)
		self.search_info["book_type"].append(book_type)
		self.search_info["ratings"].append(ratings)
		self.search_info["availablity"].append(availablity)
		
		print(f'Added Title      : {title}')
		print(f'Added Subtitle   : {sub_title}')
		print(f'Added Author     : {author}')
		print(f'Added Book Type  : {book_type}')
		print(f'Added Ratings    : {ratings}')
		print(f'Added Availablity: {availablity}')
		print(f'---------------------------')
		print(f'')


	def get_info(self, search_query):

		self.search_query = search_query

		try:
			t.init()
			t.url(f'{self.url}{self.search_query_prefix}{self.search_query}')
			print('Search Query: ' + self.search_query)
			print(f'{self.url}{self.search_query_prefix}{self.search_query}')
			wait_for_pageload('//div[@class="small-12 columns footer-mobile-element text-center"]')

			items_on_page = t.count('(//div[@class="CoverImageContainer"])')
			print(f'Items on page: {items_on_page}')
			print(f'---------------------------')
			print(f'')

			i = 1
			if items_on_page > 0:
				t.hover(f'(//div[@class="CoverImageContainer"])[{i}]')
				search_results = t.read(f'(//div[@class="CoverImageContainer"])[{i}]/a/@href')
				t.url(f'{self.url}{search_results}')
				print(f'Going to: {self.url}{search_results}')
				wait_for_pageload('//div[@class="small-12 columns footer-mobile-element text-center"]')
				self.read_info_from_page(self.search_info)

				t.url(f'{self.url}{self.search_query_prefix}{self.search_query}')                

				i = 2
				is_same_title = True
				while i <= items_on_page and is_same_title:

					t.hover(f'(//div[@class="CoverImageContainer"])[{i}]')
					search_results = t.read(f'(//div[@class="CoverImageContainer"])[{i}]/a/@href')
					t.url(f'{self.url}{search_results}')
					print(f'Going to: {self.url}{search_results}')
					wait_for_pageload('//div[@class="small-12 columns footer-mobile-element text-center"]')

					title          = t.read('//h1')
					sub_title      = t.read('//h1/following-sibling::div[@class="TitleSeries"]')
					
					if title == self.search_info["title"][0] and sub_title == self.search_info["sub_title"][0]:
						self.read_info_from_page(self.search_info)

					else:
						is_same_title = False
						print(f'Search Stopped')
						print(f'---------------------------')
						print(f'')

					t.url(f'{self.url}{self.search_query_prefix}{self.search_query}')     
					i = i + 1

				return True

			else:
				return False

		finally:
			t.close()



class Amazon:

	def __init__(self):
		self.url = 'https://www.amazon.sg'
		self.search_query_prefix = '/s?k='
		self.search_query = ''
		self.search_info = {    	'title'         : [],
									'sub_title'     : [], #not used in amazon
									'author'        : [],
									'book_type'     : [],
									'ratings'       : [],
									'availablity'   : []
							}
		self.recommended_info = {	'title'         : [],
									'sub_title'     : [], #not used in amazon
									'author'        : [],
									'book_type'     : [],
									'ratings'       : [],
									'availablity'   : []
								}
	def read_info_from_page(self, dict_ref, category):

		if t.read('(//a[@class="a-link-normal a-color-tertiary"])[1]') != category:
			return False

		title          = t.read('//span[@id="productTitle"]')
		author         = t.read('//div[@id="bylineInfo"]//a[@class="a-link-normal"]')
		ratings        = t.read('(//span[@class="a-declarative"]//span[@class="a-icon-alt"])[1]')

		dict_ref["title"].append(title)
		dict_ref["author"].append(author)
		dict_ref["ratings"].append(ratings)
		
		print(f'Added Title      : {title}')
		print(f'Added Author     : {author}')
		print(f'Added Ratings    : {ratings}')
		print(f'---------------------------')
		print(f'')

		return True


	def get_info(self, search_query, number_of_recommendations = 3, category = "Books"):
		self.search_query = search_query

		try:
			t.init()
			t.url(f'{self.url}{self.search_query_prefix}{self.search_query}')
			print('Search Query: ' + self.search_query)
			print(f'Going to: {self.url}{self.search_query_prefix}{self.search_query}')
			wait_for_pageload('//input[@id="twotabsearchtextbox"]')

			items_on_page = t.count('(//h2/a[contains(@class, "a-text-normal")])')
			print(f'Items on page: {items_on_page}')
			print(f'---------------------------')
			print(f'')

			i=1
			if items_on_page > 0:
				t.hover(f'(//h2/a[contains(@class, "a-text-normal")])[{i}]')
				search_results = t.read(f'(//h2/a[contains(@class, "a-text-normal")])[{i}]/@href')
				t.url(f'{self.url}{search_results}')
				print(f'Going to: {self.url}{search_results}')
				wait_for_pageload('//input[@id="twotabsearchtextbox"]')
				t.hover('//div[@id="sims-fbt"]')
				if not self.read_info_from_page(self.search_info, category):
					return False

				recommended_items_on_page = t.count('//div[@id="anonCarousel1"]/ol[@class="a-carousel"]/li')
				print(f'Recommended items on page: {recommended_items_on_page}')
				print(f'---------------------------')
				print(f'')

				if recommended_items_on_page > 0:
					for j in range(1, min(recommended_items_on_page, number_of_recommendations)+1):
						t.hover(f'(//div[@id="anonCarousel1"]/ol[@class="a-carousel"]/li)[{j}]')
						recommended_results = t.read(f'(//div[@id="anonCarousel1"]/ol[@class="a-carousel"]/li)[{j}]/a/@href')
						t.url(f'{self.url}{recommended_results}')
						print(f'Going to: {self.url}{recommended_results}')
						wait_for_pageload('//input[@id="twotabsearchtextbox"]')
						self.read_info_from_page(self.recommended_info, category)
						t.url(f'{self.url}{search_results}')
						print(f'Going to: {self.url}{search_results}')
						wait_for_pageload('//input[@id="twotabsearchtextbox"]')
						t.hover('//div[@id="sims-fbt"]')

				t.url(f'{self.url}{self.search_query_prefix}{self.search_query}')

				return True

			else:
				return False
		
		finally:

			t.close()


#main
if __name__ == "__main__":
	import sys

	library = Library()
	if library.get_info(sys.argv[1]):
		print(f'Search Results from NLB:')
		print(f'Title     : {library.search_info["title"]}')
		print(f'Subtitle  : {library.search_info["sub_title"]}')
		print(f'Author    : {library.search_info["author"]}')
		print(f'Book Type : {library.search_info["book_type"]}')
		print(f'Ratings   : {library.search_info["ratings"]}')
		print(f'---------------------------')
		print(f'')

		amazon = Amazon()
		if amazon.get_info((f'%27{library.search_info["title"][0]} {library.search_info["sub_title"][0]}%27').replace(' ', '+')):
			print(f'Search Results from Amazon:')
			print(f'Title     : {amazon.search_info["title"]}')
			print(f'Subtitle  : {amazon.search_info["sub_title"]}')
			print(f'Author    : {amazon.search_info["author"]}')
			print(f'Book Type : {amazon.search_info["book_type"]}')
			print(f'Ratings   : {amazon.search_info["ratings"]}')
			print(f'---------------------------')
			print(f'')

			print(f'Recommended Results from Amazon:')
			print(f'Title     : {amazon.recommended_info["title"]}')
			print(f'Subtitle  : {amazon.recommended_info["sub_title"]}')
			print(f'Author    : {amazon.recommended_info["author"]}')
			print(f'Book Type : {amazon.recommended_info["book_type"]}')
			print(f'Ratings   : {amazon.recommended_info["ratings"]}')
			print(f'---------------------------')
			print(f'')