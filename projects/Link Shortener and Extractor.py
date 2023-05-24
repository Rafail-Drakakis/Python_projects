import pyshorteners, urllib.request

def link_shortener(link):
    shortener = pyshorteners.Shortener()
    short_link = shortener.tinyurl.short(link)
    print(f"Shortened Link: {short_link}")

def link_opener(link):
    shortened_url = urllib.request.urlopen(link)
    real_link = shortened_url.geturl()
    print(f"Real Link: {real_link}")

def main():
    choice = int(input("1. Type 1 for shortening link\n2. Type 2 for extracting real link from a shortened link: "))
    link = input("Enter the link: ")
    if choice == 1:
        link_shortener(link)
    elif choice == 2:
        link_opener(link)

main()        