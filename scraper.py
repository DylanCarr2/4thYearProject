import json
import requests
import re
import os
from bs4 import BeautifulSoup
from flask import Flask, request, render_template
app = Flask(__name__)
##initialising arrays of relevant data to scrape, for putting in JSON file for the site to read
listingTitles=[]
links = []
images=[]
prices=[]
locations=[]
@app.route("/")
def index():
    return render_template("site.html")
@app.route("/<query>/search/<pageNum>", methods=['GET','POST'])
def getAdvertsData(query,pageNum):
    listingTitles=[]
    links = []
    images=[]
    prices=[]
    locations=[]
    output = request.form.to_dict()
    print(query)
    baseURL = "https://www.adverts.ie/for-sale/q_"+query+"/page-"+pageNum
    
    
    ## Gets the HTML data from the URL specified
    advertsData = requests.get(baseURL)
    adverts = BeautifulSoup(advertsData.content, "html.parser")
    ## Finds all divs containing item information on the page
    adSearchResults = adverts.find("ul", class_ = "paging")
    
    adSearchResults = adverts.find_all("div", class_="sr-grid-cell quick-peek-container")

    for adSearchResults in adSearchResults:
        ##For images, need to extract just the image "src" tag, so needed this extra "get" method to parse the data
        imgResult = adSearchResults.find("img", class_="main-ad-image")
        listingTitles.append(adSearchResults.find("div", class_ ="title").text.replace("\n","").strip())
        images.append(imgResult.get("src"))
        parsedPrice = adSearchResults.find("div", class_ ="price").get_text()
        re.sub(r'[^0-9]', '', parsedPrice)
        if(parsedPrice == ""):
                parsedPrice = 0
        prices.append(parsedPrice)
        locations.append(adSearchResults.find("div", class_ = "location").text.replace("\n","").strip())
        links.append("https://www.adverts.ie" + adSearchResults.find("a", class_ ="main-image").get("href"))

    #below used to be getDoneDealData, combined functions together to fix a bug where the json file would multiply arrays.
    pageNum = int(pageNum)
    pageNum = (pageNum-1)*30
    baseURL = "https://www.donedeal.ie/all?words="+query+"&start="+str(pageNum)
    
   
    ## Gets the HTML data from the URL specified
    advertsData = requests.get(baseURL)
    adverts = BeautifulSoup(advertsData.content, "html.parser")
    adverts = adverts.find("div", id = '__next').select_one("div[class *= 'DefaultLayout__Wrapper']").select_one("div[class *= 'styles__Container']").select_one("ul[class *= 'Listings__List']").select("li[class *= 'Listings__Desktop']")
    

    for adSearchResults in adverts:
        if not(adSearchResults.select_one("a[class *= 'Link__SLinkButton']") is None):
            ##For images, need to extract just the image "src" tag, so needed this extra "get" method to parse the data
            listingTitles.append(adSearchResults.select_one("div[class *='Card__Body']").select_one("p[class *= 'Card__Title']").get_text())
            print(listingTitles)
            if not(adSearchResults.find("img") == None):
                images.append(adSearchResults.find("img").get("src"))
            else:
                images.append("No Image")
            parsedPrice = adSearchResults.select_one("p[class *='Card__InfoText']").get_text()
            re.sub(r'[^0-9]', '', parsedPrice)
            #float(adSearchResults.select_one("p[class *='Card__InfoText']").get_text().replace("€","").replace(",","").replace("FREE","0")))
            if(parsedPrice == ""):
                parsedPrice = 0
            prices.append(parsedPrice)
            keyInfo = adSearchResults.select("li[class *='Card__KeyInfoItem']")
            locations.append(keyInfo[1].getText())
            
            links.append(adSearchResults.select_one("a[class *= 'Link__SLinkButton']").get("href"))
    if(os.path.isfile("static/js/scrapedInfo.json")):
        os.remove("static/js/scrapedInfo.json") 
    file = open("static/js/scrapedInfo.json", "w")
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
