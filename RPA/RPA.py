import json
import books
import email
import tagui as t

def extractInfo(bookList):
    bookInfoList = []

    for book in bookList:
        library = books.Library()
        amazon = books.Amazon()

        print(f'')
        print(f'------------------------------------------------------')
        print(f'Scrapping information for "{book}" from NLB...')
        print(f'------------------------------------------------------')
        print(f'')

        if(library.get_info(book)):

            print(f'')
            print(f'------------------------------------------------------')
            print(f'Scrapping information for "{book}" from Amazon...')
            print(f'------------------------------------------------------')
            print(f'')

            if not amazon.get_info(f'{library.search_info["title"][0]} {library.search_info["sub_title"][0]}'):
                print(f'{book} not found on Amazon...')
        else:
            print(f'{book} not found in NLB...')

        bookInfoDict = {"NLB": library.search_info, "Amazon": amazon.search_info}
        bookInfoList.append(bookInfoDict)

    # print(bookInfoList)

    print(f'')
    print(f'------------------------------------------------------')
    print(f'Completed scrapping information for "{book}"...')
    print(f'------------------------------------------------------')
    print(f'')

    return bookInfoList

def composeSendEmail(bookInfoList):
    return

def main(bookList):
    t.init()
    composeSendEmail(extractInfo(bookList))
    t.close()

if __name__ == "__main__":
    bookList = ["The Promised Land", "Becoming"]
    main(bookList)
