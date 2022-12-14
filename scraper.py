import json
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("site.html")
@app.route("/search", methods=['GET','POST'])
def getAdvertsData():
    output = request.form.to_dict()
    query = output["searchbar"]
    print(query)
    baseURL = "https://www.adverts.ie/for-sale/q_"+query
    ##initialising arrays of relevant data to scrape, for putting in JSON file for the site to read
    listingTitles=[]
    links = []
    images=[]
    prices=[]
    locations=[]
    ## Gets the HTML data from the URL specified
    advertsData = requests.get(baseURL)
    adverts = BeautifulSoup(advertsData.content, "html.parser")
    ## Finds all divs containing item information on the page
    adSearchResults = adverts.find("ul", class_ = "paging")
    pageNumResult = adSearchResults.find_all("a")
    pageNumbers = []
    for pageNumResult in pageNumResult:
        pageNumbers.append(pageNumResult.text)
    print(pageNumbers)
    i = 0
    while i < (int)(pageNumbers[-1]):
        newURL = baseURL + "/page-" + str(i+1)
        print(newURL)
        advertsData = requests.get(newURL)
        adSearchResults = adverts.find_all("div", class_="sr-grid-cell quick-peek-container")

        for adSearchResults in adSearchResults:
            ##For images, need to extract just the image "src" tag, so needed this extra "get" method to parse the data
            imgResult = adSearchResults.find("img", class_="main-ad-image")
            listingTitles.append(adSearchResults.find("div", class_ ="title").text.replace("\n","").strip())
            images.append(imgResult.get("src"))
            prices.append(adSearchResults.find("div", class_ ="price").text.replace("\n","").strip())
            locations.append(adSearchResults.find("div", class_ = "location").text.replace("\n","").strip())
            links.append("https://www.adverts.ie" + adSearchResults.find("a", class_ ="main-image").get("href"))
        i+=1
    print(listingTitles)

    file = open("scrapedInfo.json", "w")
    dumpedArray = json.dumps(listingTitles)
    file.write("[" + dumpedArray)
    dumpedArray = json.dumps(images)
    file.write(","+dumpedArray)
    dumpedArray = json.dumps(prices)
    file.write(","+dumpedArray)
    dumpedArray = json.dumps(locations)
    file.write(","+dumpedArray)
    dumpedArray = json.dumps(links)
    file.write(","+dumpedArray+"]")
    file.close()
    return render_template("search.html")

if __name__ =='__main__':
    app.run(debug=True, port =5000)
