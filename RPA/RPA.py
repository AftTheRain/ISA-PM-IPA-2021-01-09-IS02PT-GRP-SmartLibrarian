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

def addInfoText(textField, infoLst):
    text = textField + ': '

    if len(infoLst) == 0: return ""

    for info in infoLst:
        if isinstance(info, list):
            for item in info:
                text += (item+', ')
            text = text[:-2]
        else:
            text += info
    text += '[enter]'
    return text

def composeSendEmail(bookList, bookInfoList):

    text = 'Hello there,[enter][enter]'

    for i in range(len(bookList)):
        print(f'Composing email for {bookList[i]}')
        print(bookInfoList[i])

        foundInNLB = True
        foundInAmazon = True
        amazonRecList = True

        if len(bookInfoList[i]["NLB"]["title"]) == 0:
            foundInNLB = False
            foundInAmazon = False
            amazonRecList = False
        elif len(bookInfoList[i]["Amazon"]["title"]) == 0:
            foundInAmazon = False
            amazonRecList = False
        elif len(bookInfoList[i]["Amazon"]["recommendation"]) == 0:
            amazonRecList = False

        # Header
        text += '-------------------------------------------------------------------------[enter]'
        if foundInNLB:
            text += (f'BOOK {i+1}: "{bookInfoList[i]["NLB"]["title"][0]}"[enter]')
        else:
            text += (f'BOOK {i+1}: "{bookList[i]}" - Not found in NLB[enter]')
        text += ('-------------------------------------------------------------------------[enter]')
        if not foundInNLB:
            text += '[enter]'
            continue

        # NLB information
        text += addInfoText('Subtitle', bookInfoList[i]["NLB"]["sub_title"])
        text += addInfoText('Author', bookInfoList[i]["NLB"]["author"])
        text += addInfoText('Book Type', bookInfoList[i]["NLB"]["book_type"])
        text += addInfoText('Ratings', bookInfoList[i]["NLB"]["ratings"])
        text += addInfoText('Abstract', bookInfoList[i]["NLB"]["abstract"])
        text += addInfoText('Availability', bookInfoList[i]["NLB"]["availability"])
        # text += addInfoText('Link', bookInfoList[i]["NLB"]["URL"])



        text += '[enter]'


    signOff =   'Yours Truly,[enter]'
    signOff +=  'SmartLibrarian'

    text += signOff

    return text

def main(bookList):
    emailAgent = email.Email()
    emailSub = '[SmartLibrarian] NLB Information for '

    for title in bookList:
        emailSub += (title+', ')
    emailSub = emailSub[:-2]

    t.init()
    emailBody = composeSendEmail(bookList, extractInfo(bookList))
    emailAgent.compose_email(subject=emailSub, body=emailBody)
    t.close()

if __name__ == "__main__":
    bookList = ["The Promised Land", "Becoming"]
    main(bookList)
