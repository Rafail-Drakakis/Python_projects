#get_fact.py
import requests

def get_fact(number):
    # create a URL string by formatting the input number into the URL
    url = "http://numbersapi.com/{}".format(number)
    
    # send an HTTP GET request to the URL
    r = requests.get(url)
    
    # if the request is successful (status code 200), print the response text, otherwise, print an error message with the status code
    if r.status_code == 200:
        print(r.text)
    else: 
        print("An error occurred, code={}".format(r.status_code))
