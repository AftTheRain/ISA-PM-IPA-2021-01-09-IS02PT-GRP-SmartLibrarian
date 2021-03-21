import rpa as t


class Library:

    def __init__(self):
        self.url = 'https://nlb.overdrive.com'
        self.search_query_prefix = '/search?query='
        self.search_query = ''
        self.search_info = {}

    def get_info(self, search_query):

        self.search_query = search_query

        try:
            t.init()
            t.url(f'{self.url}{self.search_query_prefix}{self.search_query}')
            t.wait(5)
            print('Search Query: ' + self.search_query)

            titles_on_page = t.count('(//div[@class="CoverImageContainer"])')
            print(f'Titles on page: {titles_on_page}')
            print(f'---------------------------')
            print(f'')

            if titles_on_page > 0:
                for i in range(1, titles_on_page + 1):
                    t.hover(f'(//div[@class="CoverImageContainer"])[{i}]')
                    search_results = t.read(f'(//div[@class="CoverImageContainer"])[{i}]/a/@href')
                    t.url(f'{self.url}{search_results}')
                    print(f'Going to: {self.url}{search_results}')

                    title = t.read('//h1')
                    sub_title = t.read('//h1/following-sibling::div[@class="TitleSeries"]')
                    author = t.read('//h1/following-sibling::div[@class="TitleDetailsHeading-creator"]')
                    book_type = t.read('//h1/following-sibling::span')
                    ratings = t.read('//h1/../following-sibling::div[@class="js-starRatingsContainer"]//@data-global-rating')
                    availablity = t.read('//h1/../following-sibling::div[@class="show-for-600-up js-copiesAvailableContainer"]//span')
                    
                    print(f'Title      : {title}')
                    print(f'Subtitle   : {sub_title}')
                    print(f'Author     : {author}')
                    print(f'Book Type  : {book_type}')
                    print(f'Ratings    : {ratings}')
                    print(f'Availablity: {availablity}')
                    print(f'---------------------------')
                    print(f'')

                    t.url(f'{self.url}{self.search_query_prefix}{self.search_query}')

                t.close()
                return True

            else:
                return False

        finally:
            t.close()

#main
if __name__ == "__main__":
    import sys

    library = Library()
    print(library.get_info(sys.argv[1]))

