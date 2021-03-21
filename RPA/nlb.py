import rpa as t

def nlb_search(search_query):

    url = 'https://nlb.overdrive.com'
    search_query_prefix = '/search?query='

    try:
        t.init()
        t.url(f'{url}{search_query_prefix}{search_query}')
        t.wait(5)
        print('Search Query: ' + search_query)

        titles_on_page = t.count('(//div[@class="CoverImageContainer"])')
        print(f'Titles on page: {titles_on_page}')

        for i in range(1, titles_on_page + 1):
            t.hover(f'(//div[@class="CoverImageContainer"])[{i}]')
            search_results = t.read(f'(//div[@class="CoverImageContainer"])[{i}]/a/@href')
            t.url(f'{url}{search_results}')
            print(f'Going to: {url}{search_results}')

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

            t.url(f'{url}{search_query_prefix}{search_query}')

        t.close()

    finally:
        t.close()

#main
import sys
nlb_search(sys.argv[1])

