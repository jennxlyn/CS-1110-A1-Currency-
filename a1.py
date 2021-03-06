#a1.py
#Jennifer Lin
#September 18, 2016
#Ingrid Libman & Kristy Liao helped with some of these functions.
"""Module for implementing a1 functions.

This module is divided into several parts. Part A has 2 functions: before_space
and after_space that breaks up a JSON string.

Part B has 4 functions: first_inside_quotes, get_from, get_to, and has_error
that help process JSON responses, whether it's valid or invalid.
get_from gets the FROM value from the JSON response,while get_to gets the TO
value. first_inside_quotes serves as a helper function (for the prior 2
functions), while has_error verifies if there is an error in the JSON response.

Part C has the function: currency_response, which interacts with the currency
exchange web service to get a JSON string when given the FROM, TO, and AMOUNT
FROM values.

Part D has 2 functions: iscurrency, which verifies the 3 letter code for a
currency, and exchange, which provides the exchanged amount when given the
FROM, TO, and AMOUNT FROM values."""

#PART A: BREAKING UP JSON STRING

def before_space(s):
    """Returns: Substring of s; up to, but not including, the first space
    
    Parameter s: the string to slice
    Precondition: s has at least one space in it"""
    
    #Find the space
    start = s.index(' ')
    
    #Text before space
    first = s[:start]

    #return result
    return first


def after_space(s):
    """Returns: Substring of s after the first space
    
    Parameter s: the string to slice
    Precondition: s has at least one space in it"""

    #Find the space
    start = s.index(' ')
    
    #Text after space
    second = s[start+1:]

    #Return the result
    return second

#PART B: PROCESSING A JSON STRING

def first_inside_quotes(s):
    """Returns: The first substring of s between two (double) quote characters
    
    A quote character is one that is inside a string, not one that delimits it.
    We typically use single quotes (') to delimit
    a string if want to use a double quote character (") inside of it.
    Example: If s is 'A "B C" D', this function returns 'B C'
    Example: If s is 'A "B C" D "E F" G', this function still returns 'B C'
    because it only picks the first such substring.
    
    Parameter s: a string to search
    Precondition: s is a string with at least two (double) quote characters
    inside."""
    
    #Find first double quote
    begin = s.index('"')
   
    #Store part after the double quote
    tail = s[begin+1:]
   
    #Find second double quote
    end = tail.index('"')
  
    #Return the result
    return tail[:end]


def get_from(json):
    """Returns: The FROM value in the response to a currency query.
    
    Given a JSON response to a currency query, this returns the string inside
    double quotes (") immediately following
    the keyword "from". For example, if the JSON is
    '{"from":"2 United States Dollars","to":"1.825936 Euros","success":true,
    "error":""}'
    then this function returns '2 United States Dollars'
    (not '"2 United States Dollars"'). It returns the empty string if the
    JSON is the result of on invalid query.
    
    Parameter json: a json string to parse
    Precondition: json is the response to a currency query"""
    #Find colon
    colon = json.index(':')
    
    #Text after colon
    aftercol = json[colon+1:]

    #Finding USD
    query = first_inside_quotes(aftercol)
    
    return query


def get_to(json):
    """Returns: The TO value in the response to a currency query.
    
    Given a JSON response to a currency query, this returns the string
    inside double quotes (") immediately following
    the keyword "to". For example, if the JSON is
    '{"from":"2 United States Dollars","to":"1.825936 Euros","success":true,
    "error":""}'
    then this function returns '1.825936 Euros' (not '"1.825936 Euros"').
    It returns the empty string if the JSON is the result of on invalid query.
    
    Parameter json: a json string to parse
    Precondition: json is the response to a currency query"""
    #Find comma
    comma = json.index(',')
    
    #Find text after comma
    remain = json[comma+1:]
    
    #Find next colon
    col = remain.index(':')
    
    #Text after colon
    rightcol = remain[col+1:]
    
    #Find JSON response
    response = first_inside_quotes(rightcol)
    
    return response
    
    
def has_error(json):
    """Returns: True if the query has an error; False otherwise.
    
    Given a JSON response to a currency query, this returns the opposite
    of the value following the keyword "success".
    For example, if the JSON is'{"from":"","to":"","success":false,
    "error":"Source currency code is invalid."}'
    then the query is not valid, so this function returns True
    (It does NOT return the message 'Source currency code is invalid').
    
    Acknowledgements: Consultant Kristy Liao (kpl44) helped with this function.
    
    Parameter json: a json string to parse
    Precondition: json is the response to a currency query"""
    #Find word 'error'
    word = json.index('error')
    
    #Text after e in 'error'
    text = json[word:]
    
    #Find colon
    colon = text.index(':')
    
    #Text after colon
    phrase = text[colon:]
    
    #Isolate text in double quotes after colon
    message = first_inside_quotes(phrase)
    
    #Length of text inside double quotes
    quote = len(message)
    
    return quote>0
    
#PART C: CURRENCY QUERY
    
def currency_response(currency_from, currency_to, amount_from):
    """Returns: a JSON string that is a response to a currency query.
    
    A currency query converts amount_from money in currency currency_from 
    to the currency currency_to. The response should be a string of the form
    
        '{"from":"<old-amt>","to":"<new-amt>","success":true, "error":""}'
    
    where the values old-amount and new-amount contain the value and name 
    for the original and new currencies. If the query is invalid, both 
    old-amount and new-amount will be empty, while "valid" will be followed 
    by the value false.
    
    Acknowledgements: Consultant Ingrid Libman (iml29) helped with this function.
    
    Parameter currency_from: the currency on hand
    Precondition: currency_from is a string
    
    Parameter currency_to: the currency to convert to
    Precondition: currency_to is a string
    
    Parameter amount_from: amount of currency to convert
    Precondition: amount_from is a float"""
    import urllib2
    
    #Get basic url currency site
    u = 'http://cs1110.cs.cornell.edu/2016fa/a1server.php?' + 'from=' + \
        currency_from + '&to=' + currency_to + '&amt=' + str(amount_from)

    #Open new url
    site = urllib2.urlopen(u)

    #Open new url    
    json_string = site.read()
    
    return json_string

#PART D:CURRENCY EXCHANGE

def iscurrency(currency):
    """Returns: True if currency is a valid (3 letter code for a) currency. 
    It returns False otherwise.

    Acknowledgements: Consultant Kristy Liao (kpl44) helped with this function.
    
    Parameter currency: the currency code to verify
    Precondition: currency is a string."""
    #Use get json string
    code = currency_response(currency, currency, 1)
    
    #Find given currency
    giv_curr = get_from(code)

    #Length of given currency
    length = len(giv_curr)

    #True if string has text, false if string is empty
    return len(giv_curr) > 0


def exchange(currency_from, currency_to, amount_from):
    """Returns: amount of currency received in the given exchange.

    In this exchange, the user is changing amount_from money in 
    currency currency_from to the currency currency_to. The value 
    returned represents the amount in currency currency_to.

    The value returned has type float.
    
    Parameter currency_from: the currency on hand
    Precondition: currency_from is a string for a valid currency code
    
    Parameter currency_to: the currency to convert to
    Precondition: currency_to is a string for a valid currency code
    
    Parameter amount_from: amount of currency to convert
    Precondition: amount_from is a float"""
    #Get url with the 3 arguments
    url = currency_response(currency_from, currency_to, amount_from)
    
    #Find converted currency value in json string
    new_currency = get_to(url)
    
    #Find value in converted form
    new_value = before_space(new_currency)
    
    #Casting string to float
    converted = float(new_value)
    
    #Print amount of currency received in exchange
    return converted
