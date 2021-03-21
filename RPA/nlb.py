import rpa as t


class Library:

    def __init__(self):
        self.url = 'https://nlb.overdrive.com'
        self.search_query_prefix = '/search?query='
        self.search_query = ''
        self.search_info = {    'title'         : '',
                                'sub_title'     : '',
                                'author'        : [],
                                'book_type'     : [],
                                'ratings'       : [],
                                'availablity'   : []
                            }

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

            i = 1
            if titles_on_page > 0:
                t.hover(f'(//div[@class="CoverImageContainer"])[{i}]')
                search_results = t.read(f'(//div[@class="CoverImageContainer"])[{i}]/a/@href')
                t.url(f'{self.url}{search_results}')
                print(f'Going to: {self.url}{search_results}')

                title          = t.read('//h1')
                sub_title      = t.read('//h1/following-sibling::div[@class="TitleSeries"]')
                author         = t.read('//h1/following-sibling::div[@class="TitleDetailsHeading-creator"]')
                book_type      = t.read('//h1/following-sibling::span')
                ratings        = t.read('//h1/../following-sibling::div[@class="js-starRatingsContainer"]//@data-global-rating')
                availablity    = t.read('//h1/../following-sibling::div[@class="show-for-600-up js-copiesAvailableContainer"]//span')

                self.search_info["title"] = title
                self.search_info["sub_title"] = sub_title
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

                t.url(f'{self.url}{self.search_query_prefix}{self.search_query}')                

                i = 2
                is_same_title = True
                while i <= titles_on_page and is_same_title:

                    t.hover(f'(//div[@class="CoverImageContainer"])[{i}]')
                    search_results = t.read(f'(//div[@class="CoverImageContainer"])[{i}]/a/@href')
                    t.url(f'{self.url}{search_results}')
                    print(f'Going to: {self.url}{search_results}')

                    title          = t.read('//h1')
                    sub_title      = t.read('//h1/following-sibling::div[@class="TitleSeries"]')
                    author         = t.read('//h1/following-sibling::div[@class="TitleDetailsHeading-creator"]')
                    book_type      = t.read('//h1/following-sibling::span')
                    ratings        = t.read('//h1/../following-sibling::div[@class="js-starRatingsContainer"]//@data-global-rating')
                    availablity    = t.read('//h1/../following-sibling::div[@class="show-for-600-up js-copiesAvailableContainer"]//span')
                    
                    if title == self.search_info["title"] and sub_title == self.search_info["sub_title"]:

                        self.search_info["author"].append(author)
                        self.search_info["book_type"].append(book_type)
                        self.search_info["ratings"].append(ratings)
                        self.search_info["availablity"].append(availablity)

                        print(f'Added Author     : {author}')
                        print(f'Added Book Type  : {book_type}')
                        print(f'Added Ratings    : {ratings}')
                        print(f'Added Availablity: {availablity}')
                        print(f'---------------------------')
                        print(f'')

                    else:
                        is_same_title = False
                        print(f'Search Stopped')
                        print(f'---------------------------')
                        print(f'')

                    t.url(f'{self.url}{self.search_query_prefix}{self.search_query}')     
                    i = i + 1

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
    if library.get_info(sys.argv[1]):
        print(f'Search Results')
        print(f'Title     : {library.search_info["title"]}')
        print(f'Subtitle  : {library.search_info["sub_title"]}')
        print(f'Author    : {library.search_info["author"]}')
        print(f'Book Type : {library.search_info["book_type"]}')
        print(f'Ratings   : {library.search_info["ratings"]}')

