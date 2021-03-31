from flask import Flask, request, make_response, jsonify
import requests
import json
import pandas as pd
import os
import time

app = Flask(__name__)
bookList = []
bookListLimit = 3

# **********************
# UTIL FUNCTIONS : START
# **********************


# **********************
# UTIL FUNCTIONS : END
# **********************

# *****************************
# Intent Handlers funcs : START
# *****************************


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
    if intent_name == "GetBookTitleIntent":
        bookTitle = req["queryResult"]["parameters"]["book-title"]
        bookList.append(bookTitle)

        if len(bookList) == bookListLimit:
        # Parse book title through to NLB/Amazon interface. Response will be set as default due to time out
            time.sleep(5)

        resp_text = "Would you like to enquire about another book?  \nCurrent book list:"
        for book in bookList:
            resp_text = resp_text + " " + book + ","
        resp_text = resp_text[:-1]
    elif intent_name == "GetBookTitleIntent - no":
        # Parse book title through to NLB/Amazon interface.Response will be set as default due to time out
        time.sleep(5)
    else:
        resp_text = "Unable to find a matching intent. Try again."

    # Clearing context and resetting the chat bot
    # respContext = []
    # for context in currentContext:
    #     context["lifespanCount"] = 0
    #     respContext.append(context)

    return make_response(jsonify({
        'fulfillmentText': resp_text,
        # 'outputContexts': respContext
        })
        )

# ***************************
# WEBHOOK MAIN ENDPOINT : END
# ***************************

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5000)
