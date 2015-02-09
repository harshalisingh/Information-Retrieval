__author__ = 'Harshali'

import re
import mechanize
import urlparse
import sys
import time

# Function crawler starts with seed url
def crawler(seed, key, d):
    urls = [seed]
    visited = [seed]
    counter = 1
    print "Crawling......."
    while counter <= d:
        parsed, focused_list = crawl(urls, key)
        urls = []

        for u in parsed:
            if u not in visited:
                visited.append(u)
                urls.append(u)
        counter += 1

    if key != "":
        print "Focused Crawling:\n"
        for f in focused_list:
            print f
        print "No of pages in focused crawling:", len(focused_list)
    else:
        print "Unfocused Crawling:\n"
        for v in visited:
            print v
        print "No of pages in unfocused crawling:", len(visited)


#Function crawl checks if the page is relevant or not
def crawl(urls, key):
    result = []
    focused_urls = []
    br = mechanize.Browser()
    for url in urls:
        try:
            response = br.open(url)
            htmltext = response.read()
            ht = str(htmltext).lower()

            match = re.search(key, ht, re.IGNORECASE)

            # Checks if page has keyphrase "information retrieval" present
            if match:
                focused_urls.append(url)

                #Gets all the links from the page
                for link in br.links():
                    nu = urlparse.urljoin(link.base_url,link.url)
                    b1 = urlparse.urlparse(nu).hostname
                    b2 = urlparse.urlparse(nu).path

                    newurl = "http://"+b1+b2
                    pattern1 = re.findall(':|#|Main_Page',b2)
                    pattern2 = re.findall('en\.wikipedia\.org', b1)
                    pattern3 = re.findall('wiki', b2)

                    #Checks if the retrieved url is a valid url
                    if not pattern1:
                        if pattern2 and pattern3:
                            result.append(newurl)

        except:
            print "error"
            urls.pop(0)

        time.sleep(1)

    #Returns the extracted links and crawled pages
    return result, focused_urls

#main function
def main():
    if len(sys.argv) == 3:
        depth = 3
        seedurl, keyphrase = str(sys.argv[1]), str(sys.argv[2])
        print crawler(seedurl, keyphrase, depth)
    else:
        depth = 2
        seedurl = str(sys.argv[1])
        print crawler(seedurl, "", depth)

if __name__ == '__main__':
    main()
