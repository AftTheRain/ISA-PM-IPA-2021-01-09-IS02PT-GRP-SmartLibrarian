import json
import books
import email_RPA
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
    if textField not '':
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
        for b in range(len(bookInfoList[i]["NLB"]["title"])):
            text += addInfoText('Subtitle', bookInfoList[i]["NLB"]["sub_title"][b])
            text += addInfoText('Author', bookInfoList[i]["NLB"]["author"][b])
            text += addInfoText('Book Type', bookInfoList[i]["NLB"]["book_type"][b])
            text += addInfoText('Ratings', bookInfoList[i]["NLB"]["ratings"][b])
            text += addInfoText('Punchline', bookInfoList[i]["NLB"]["abstract"][b])
            text += addInfoText('Availability', bookInfoList[i]["NLB"]["availability"][b])
            text += addInfoText('Link', bookInfoList[i]["NLB"]["link"][b])
            text += '[enter]'

        if not foundInAmazon:
            text += '[enter]'
            continue

        # Amazon information
        text += "Let's see what information Amazon has about a similar book![enter]"
        text += addInfoText('Title', bookInfoList[i]["Amazon"]["title"])
        text += addInfoText('Subtitle', bookInfoList[i]["Amazon"]["sub_title"])
        text += addInfoText('Author', bookInfoList[i]["Amazon"]["author"])
        text += addInfoText('Book Type', bookInfoList[i]["Amazon"]["book_type"])
        text += addInfoText('Ratings', bookInfoList[i]["Amazon"]["ratings"])
        text += addInfoText('Punchline', bookInfoList[i]["Amazon"]["abstract"])
        text += '[enter]'

        if not amazonRecList:
            text += '[enter]'
            continue

        # Amazon recommended book list
        text += "People who bought this book also bought these other books:[enter]"
        for b in range(len(bookInfoList[i]["Amazon"]["recommendation"][0]["title"])):
            text += f'{b+1}: '
            text += addInfoText('', bookInfoList[i]["Amazon"]["recommendation"][0]["title"][b])


        text += '[enter]'


    signOff =   'Yours Truly,[enter]'
    signOff +=  'SmartLibrarian'

    text += signOff

    return text

def main(bookList):
    email_recipient = ''
    try:
        with open('email_recipient.txt') as f:
            email_recipient = f.readlines()[0][:-1]
    except:
        pass

    emailAgent = email_RPA.Email()
    emailSub = '[SmartLibrarian] NLB Information for '

    for title in bookList:
        emailSub += (title+', ')
    emailSub = emailSub[:-2]

    t.init()
    emailBody = composeSendEmail(bookList, extractInfo(bookList))
    emailAgent.compose_email(subject=emailSub, body=emailBody, mail_to=email_recipient)
    t.close()

if __name__ == "__main__":
    bookList = ["The Promised Land", "Quidditch"]
    main(bookList)
