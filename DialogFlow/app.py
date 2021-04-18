from flask import Flask, request, make_response, jsonify
import requests
import json
import time
import threading
import os
import sys

dir_main = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(dir_main, "RPA"))
dir_main = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(dir_main, "IntelligentBookAnalytics"))

app = Flask(__name__)
bookList = []
bookListLimit = 3

# **********************
# UTIL FUNCTIONS : START
# **********************

def loadRPA():
    print("Loading models. This will take a few minutes...")
    import RPA

def startRPA(bList):
    print("Starting RPA...")
    RPA.main(bList)
    print("End of RPA...")

def clearContext(context):
    clearedContext = []
    for cntxt in context:
        cntxt["lifespanCount"] = 0
        clearedContext.append(cntxt)
    return clearedContext

def clearBookList():
    global bookList
    bookList = []

x = threading.Thread(target = startRPA, args = (bookList, ))

# **********************
# UTIL FUNCTIONS : END
# **********************

# *****************************
# Intent Handlers funcs : START
# *****************************

def welcomeIntentHandler(context):
    global x
    resp = ""
    if x.is_alive():
        clearContext(context)
        resp = "Hello! I am your friendly neighbourhood Librarian. I am still working on your previous enquiry. Please check back in again after a few minutes!"
    else:
        resp = "Hello! I am your friendly neighbourhood Librarian. What book would you like to borrow from NLB?"
    return(resp, context)

def bookTitleIntentHandler(title, context):
    global x
    bookList.append(title)
    resp = ""
    if len(bookList) == bookListLimit:
        x = threading.Thread(target = startRPA, args = (bookList, ))
        x.start()
        context = clearContext(context)
        clearBookList()
        resp = "Ok! I have a full list of the books that you have enquired. I will send you an email on the ratings and availability. Thank you and Goodbye!"
    else:
        resp = "Would you like to enquire about another book? Current book list:"
        for book in bookList:
            resp = resp + " " + book + ","
        resp = resp[:-1]
    return (resp, context)

def bookTitleIntentEndHandler(context):
    global x
    x = threading.Thread(target = startRPA, args = (bookList, ))
    x.start()
    context = clearContext(context)
    clearBookList()
    resp = "Ok! I will send you an email on the ratings and availability of the books that you have enquired. Thank you and Goodbye!"
    return (resp, context)

# ***************************
# Intent Handlers funcs : END
# ***************************


# *****************************
# WEBHOOK MAIN ENDPOINT : START
# *****************************
@app.route('/', methods=['POST'])
def webhook():

    req = request.get_json(silent=True, force=True)
    print(req)

    intent_name = req["queryResult"]["intent"]["displayName"]
    session = req["session"]
    currentContext = req["queryResult"]["outputContexts"]

    resp_text = "Unable to find a matching intent. Try again."

    if intent_name == "Welcome Intent":
        response = welcomeIntentHandler(currentContext)
        resp_text = response[0]
        respContext = response[1]

    elif intent_name == "GetBookTitleIntent":
        bookTitle = req["queryResult"]["parameters"]["book-title"]
        response = bookTitleIntentHandler(bookTitle, currentContext)
        resp_text = response[0]
        respContext = response[1]

    elif intent_name == "GetBookTitleIntent - no":
        response = bookTitleIntentEndHandler(currentContext)
        resp_text = response[0]
        respContext = response[1]

    else:
        resp_text = "Unable to find a matching intent. Try again."

    return make_response(jsonify({
        'fulfillmentText': resp_text,
        'outputContexts': respContext
        })
        )

# ***************************
# WEBHOOK MAIN ENDPOINT : END
# ***************************

if __name__ == '__main__':
    loadRPA()
    app.run(debug=True, host='0.0.0.0', port=5000)
