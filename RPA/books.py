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
								'abstract'		: [],
								'reviews'		: [], # not used in NLB
								'availability'  : [],
								'recommendation': [], # not used in NLB
								'link'			: []
							}


	def read_info_from_page(self, dict_ref):
		title          = t.read('//h1')
		sub_title      = t.read('//h1/following-sibling::div[@class="TitleSeries"]')

		author = []
		author_string = t.read('//h1/following-sibling::div[@class="TitleDetailsHeading-creator"]')
		author_string = author_string[3:].split('\n')
		for i in range(len(author_string)):
			if author_string[i].strip() != '':
				author.append(author_string[i].strip())

		book_type      = t.read('//h1/following-sibling::span')
		ratings        = t.read('//h1/../following-sibling::div[@class="js-starRatingsContainer"]//@data-global-rating')

		abstract = ''
		if t.present('//article[contains(@class,"TitleDetailsDescription-description")]'):
			number_of_para = t.count('//div[@id="main"]//div[@id="title-description"]/child::*/descendant::text()[not(ancestor::b)]')
			for i in range(1, number_of_para+1):
				abstract = abstract + ' ' + t.read(f'(//div[@id="main"]//div[@id="title-description"]/child::*/descendant::text()[not(ancestor::b)])[{i}]')
			abstract = abstract.lstrip()

		availability    = t.read('//h1/../following-sibling::div[@class="show-for-600-up js-copiesAvailableContainer"]//span')
		link = t.url()

		dict_ref["title"].append(title)
		dict_ref["sub_title"].append(sub_title)
		dict_ref["author"].append(author)
		dict_ref["book_type"].append(book_type)
		dict_ref["ratings"].append(ratings)
		dict_ref["abstract"].append(abstract)
		dict_ref["availability"].append(availability)
		dict_ref["link"].append(link)

		print(f'Added Title      : {title}')
		print(f'Added Subtitle   : {sub_title}')
		print(f'Added Author     : {author}')
		print(f'Added Book Type  : {book_type}')
		print(f'Added Ratings    : {ratings}')
		if len(abstract) < 50:
			print(f'Added Abstract   : {abstract}')
		else:
			print(f'Added Abstract   : {abstract[:50]}...')
		print(f'Added Availability: {availability}')
		print(f'Added Link: {link}')
		print(f'---------------------------')
		print(f'')


	def get_info(self, search_query):

		self.search_query = search_query

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
									'abstract'		: [],
									'reviews'		: [],
									'availability'  : [],  #not used in amazon
									'recommendation': [],
									'link'			: []
							}

	def read_info_from_page(self, dict_ref, category):

		if t.read('(//a[@class="a-link-normal a-color-tertiary"])[1]') != category:
			print(f'Incorrect Category Found')
			print(f'---------------------------')
			print('')
			return False

		title = t.read('//span[@id="productTitle"]')

		author = []
		number_of_authors = t.count('//div[@id="bylineInfo"]//a[@class="a-link-normal"]')
		for i in range(1,number_of_authors+1):
			author.append(t.read(f'(//div[@id="bylineInfo"]//a[@class="a-link-normal"])[{i}]'))

		ratings = t.read('(//span[@class="a-declarative"]//span[@class="a-icon-alt"])[1]')
		if ratings != '':
			ratings = ratings.split(' ')[0]

		reviews	   = t.read('//div[@class="a-section a-spacing-small a-padding-base"]')

		abstract = ''
		if t.present('//iframe[@id="bookDesc_iframe"]'):
			t.frame('bookDesc_iframe')
			number_of_para = t.count('//div[@id="iframeContent"]/descendant::text()[not(ancestor::b)]')
			for i in range(1, number_of_para+1):
				abstract = abstract + ' ' + t.read(f'(//div[@id="iframeContent"]/descendant::text()[not(ancestor::b)])[{i}]')
			t.frame()
			abstract = abstract.lstrip()

		link = t.url()

		dict_ref["title"].append(title)
		dict_ref["author"].append(author)
		dict_ref["ratings"].append(ratings)
		dict_ref["abstract"].append(abstract)
		dict_ref["reviews"].append(reviews)
		dict_ref["link"].append(link)

		print(f'Added Title      : {title}')
		print(f'Added Author     : {author}')
		print(f'Added Ratings    : {ratings}')
		if len(abstract) < 50:
			print(f'Added Abstract   : {abstract}')
		else:
			print(f'Added Abstract   : {abstract[:50]}...')
		if len (reviews) < 50:
			print(f'Added Reviews    : {reviews}')
		else:
			print(f'Added Reviews    : {reviews[:50]}...')
		print(f'---------------------------')
		print(f'')

		return True


	def get_info(self, search_query, number_of_books_to_search = 1, number_of_recommendations = 2, category = "Books"):
		self.search_query = search_query

		t.url(f'{self.url}{self.search_query_prefix}{self.search_query}')
		print('Search Query: ' + self.search_query)
		print(f'Going to: {self.url}{self.search_query_prefix}{self.search_query}')
		wait_for_pageload('//input[@id="twotabsearchtextbox"]')

		items_on_page = t.count('(//h2/a[contains(@class, "a-text-normal")])')
		print(f'Items on page: {items_on_page}')
		print(f'---------------------------')
		print(f'')

		if items_on_page > 0:
			for i in range(1, min(number_of_books_to_search, items_on_page)+1):
				t.hover(f'(//h2/a[contains(@class, "a-text-normal")])[{i}]')
				search_results = t.read(f'(//h2/a[contains(@class, "a-text-normal")])[{i}]/@href')
				t.url(f'{self.url}{search_results}')
				print(f'Going to: {self.url}{search_results}')
				wait_for_pageload('//input[@id="twotabsearchtextbox"]')
				t.hover('//div[@class="a-divider a-divider-section"]')

				if self.read_info_from_page(self.search_info, category):

					recommended_items_on_page = t.count('//div[@id="anonCarousel2"]/ol[@class="a-carousel"]/li')
					print(f'Recommended items on page: {recommended_items_on_page}')
					print(f'---------------------------')
					print(f'')

					recommended_info = {	'title'         : [],
											'sub_title'     : [], #not used in amazon
											'author'        : [],
											'book_type'     : [],
											'ratings'       : [],
											'abstract'		: [],
											'reviews'		: [],
											'availability'  : [],  #not used in amazon
											'link'			: []
										}

					if recommended_items_on_page > 0:
						for j in range(1, min(recommended_items_on_page, number_of_recommendations)+1):
							t.hover(f'(//div[@id="anonCarousel1"]/ol[@class="a-carousel"]/li)[{j}]')
							recommended_results = t.read(f'(//div[@id="anonCarousel1"]/ol[@class="a-carousel"]/li)[{j}]/a/@href')
							t.url(f'{self.url}{recommended_results}')
							print(f'Going to: {self.url}{recommended_results}')
							wait_for_pageload('//input[@id="twotabsearchtextbox"]')
							self.read_info_from_page(recommended_info, category)
							t.url(f'{self.url}{search_results}')
							print(f'Going to: {self.url}{search_results}')
							wait_for_pageload('//input[@id="twotabsearchtextbox"]')
							t.hover('//div[@class="a-divider a-divider-section"]')

					self.search_info['recommendation'].append(recommended_info)
					t.url(f'{self.url}{self.search_query_prefix}{self.search_query}')
					print(f'Going to: {self.url}{self.search_query_prefix}{self.search_query}')
					wait_for_pageload('//input[@id="twotabsearchtextbox"]')

			return True
		else:
			return False

#main
if __name__ == "__main__":
	import sys

	library = Library()
	t.init()

	if library.get_info(sys.argv[1]):
		print(f'---------------------------')
		print(f'Search Results from NLB:')
		print(f'Title       : {library.search_info["title"]}')
		print(f'Subtitle    : {library.search_info["sub_title"]}')
		print(f'Author      : {library.search_info["author"]}')
		print(f'Book Type   : {library.search_info["book_type"]}')
		print(f'Ratings     : {library.search_info["ratings"]}')
		if len(library.search_info["abstract"][0]) < 50:
			print(f'Abstract    : {library.search_info["abstract"]}')
		else:
			print(f'Abstract    : [{library.search_info["abstract"][0][:50]}...]')
		print(f'Availability: {library.search_info["availability"]}')
		print(f'Link        : {library.search_info["link"]}')
		print(f'---------------------------')
		print(f'')

		amazon = Amazon()
		if amazon.get_info(f'{library.search_info["title"][0]} {library.search_info["sub_title"][0]}'):

			for i in range(len(amazon.search_info["title"])):
				print(f'---------------------------')
				print(f'Search Results from Amazon for {library.search_info["title"][0]} {library.search_info["sub_title"][0]} - {i+1}:')
				print(f'Title       : {amazon.search_info["title"][i]}')
				print(f'Author      : {amazon.search_info["author"][i]}')
				print(f'Ratings     : {amazon.search_info["ratings"][i]}')
				if len(amazon.search_info["abstract"][i]) < 50:
					print(f'Abstract   : {amazon.search_info["abstract"][i]}')
				else:
					print(f'Abstract   : [{amazon.search_info["abstract"][i][:50]}...]')
				if len (amazon.search_info["reviews"][i]) < 50:
					print(f'Reviews   : {amazon.search_info["reviews"][i]}')
				else:
					print(f'Reviews   : [{amazon.search_info["reviews"][i][:50]}...]')
				print(f'Link        : {amazon.search_info["link"][i]}')
				print(f'---------------------------')

				for j in range(len(amazon.search_info["recommendation"][i]["title"])):
					print(f'Recommended Results from Amazon for {amazon.search_info["title"][i]} - {j+1}:')
					print(f'Title       : {amazon.search_info["recommendation"][i]["title"][j]}')
					print(f'Author      : {amazon.search_info["recommendation"][i]["author"][j]}')
					print(f'Ratings     : {amazon.search_info["recommendation"][i]["ratings"][j]}')
					if len(amazon.search_info["recommendation"][i]["abstract"][j]) < 50:
						print(f'Abstract   : {amazon.search_info["recommendation"][i]["abstract"][j]}')
					else:
						print(f'Abstract   : {amazon.search_info["recommendation"][i]["abstract"][j][:50]}...')
					if len (amazon.search_info["recommendation"][i]["reviews"][j]) < 50:
						print(f'Reviews   : {amazon.search_info["recommendation"][i]["reviews"][j]}')
					else:
						print(f'Reviews   : {amazon.search_info["recommendation"][i]["reviews"][j][:50]}...')
					print(f'Link        : {amazon.search_info["recommendation"][i]["link"][j]}')
				print(f'')

	t.close()