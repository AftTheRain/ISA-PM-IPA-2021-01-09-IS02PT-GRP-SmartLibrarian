import json
import books
import email
import tagui as t

def main(bookList):
    bookInfoList = []

    t.init()

    for book in bookList:
        library = books.Library()
        amazon = books.Amazon()
        if(library.get_info(book)):
            amazon.get_info(f'{library.search_info["title"][0]} {library.search_info["sub_title"][0]}')

        bookInfoDict = {"NLB": library.search_info, "Amazon": amazon.search_info}
        bookInfoList.append(bookInfoDict)

    t.close()

    # print(bookInfoList)

if __name__ == "__main__":
    bookList = ["The Promised Land", "Becoming"]
    main(bookList)
