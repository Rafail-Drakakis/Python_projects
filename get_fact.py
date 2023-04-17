#get_fact.py
import requests

def get_fact():
    number = int(input("Enter a number: "))
    url = "http://numbersapi.com/{}".format(number)
    r = requests.get(url)
    if r.status_code == 200:
        print(r.text)
    else:
        print("An error occurred, code={}".format(r.status_code))
        
get_fact()        
