import json
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("site.html")
@app.route("/<query>/search<pageNum>", methods=['GET','POST'])

def getAdvertsData(query,pageNum):
    output = request.form.to_dict()
    ##query = output["searchbar"]
    
    print(query)
    baseURL = "https://www.adverts.ie/for-sale/q_"+query+"/page-"+pageNum
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
    getDoneDealData(query,pageNum)
    #getGumtreeData(query, pageNum)
    return render_template("search.html")
def getDoneDealData(query, pageNum):
    output = request.form.to_dict()
    ##query = output["searchbar"]
    print(query)
    pageNum = int(pageNum)
    pageNum = (pageNum-1)*30
    baseURL = "https://www.donedeal.ie/all?words="+query+"&start="+str(pageNum)
    ##initialising arrays of relevant data to scrape, for putting in JSON file for the site to read
    listingTitles=[]
    links = []
    images=[]
    prices=[]
    locations=[]
    ## Gets the HTML data from the URL specified
    advertsData = requests.get(baseURL)
    adverts = BeautifulSoup(advertsData.content, "html.parser")
    adverts = adverts.find("div", id = '__next').select_one("div[class *= 'DefaultLayout__Wrapper']").select_one("div[class *= 'styles__Container']").select_one("ul[class *= 'Listings__List']").select("li[class *= 'Listings__Desktop']")
    print(adverts)
    ## Finds all divs containing item information on the page
    #for adSearchResults in adverts:
     #  print(adSearchResults)
  #  print(adSearchResults)
    print("here be the results")
    #pageNumResult = adSearchResults.find_all("a")
   # pageNumbers = []
    #for pageNumResult in pageNumResult:
       # pageNumbers.append(pageNumResult.text)
    #print(pageNumbers)
    i = 0
    #adSearchResults = adverts.find_all("div", class_="sr-grid-cell quick-peek-container")

    for adSearchResults in adverts:
        ##For images, need to extract just the image "src" tag, so needed this extra "get" method to parse the data
        listingTitles.append(adSearchResults.select_one("div[class *='Card__Body']").select_one("p[class *= 'Card__Title']").get_text())
        images.append(adSearchResults.find("img").get("src"))
        prices.append(adSearchResults.select_one("p[class *='Card__InfoText']").get_text())
        keyInfo = adSearchResults.select("li[class *='Card__KeyInfoItem']")
        locations.append(keyInfo[1].getText())
        links.append(adSearchResults.select_one("a[class *= 'Link__SLinkButton']").get("href"))
    i+=1
    print(listingTitles)
    print(images)
    print(prices)
    print(locations)
    print(links)
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
def getGumtreeData(query, pageNum):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"
    REQUEST_HEADERS = {'User-agent': USER_AGENT,}
    baseURL = "https://www.gumtree.ie/stuff-for-sale/search-results.html?action=search&post_form_key=stuff_for_sale_quick&f[keyword_search]="+query+"&f[pg]="+pageNum
    ##initialising arrays of relevant data to scrape, for putting in JSON file for the site to read
    print(baseURL)
    listingTitles=[]
    links = []
    images=[]
    prices=[]
    locations=[]
    ## Gets the HTML data from the URL specified
    advertsData = requests.get(baseURL, headers=REQUEST_HEADERS,)
    print(advertsData.status_code)
    adverts = BeautifulSoup(advertsData.content, "html.parser")
    ## Finds all divs containing item information on the page
    #adSearchResults = adverts.find("a", class_ = "listings__article-wrapper ")
    #pageNumResult = adSearchResults.find_all("a")
    #pageNumbers = []
    #for pageNumResult in pageNumResult:
     #   pageNumbers.append(pageNumResult.text)
    #print(pageNumbers)
    i = 0
    #adverts = adverts.find("div", class_ = "main-wrapper d-flex flex-column")
    #adverts = adverts.find("div", id_ = "wrapper")
    print(adverts)
    adSearchResults = adverts.find_all("a", class_="listings__article-wrapper ")
    print(adSearchResults)
    for adSearchResults in adSearchResults:
        ##For images, need to extract just the image "src" tag, so needed this extra "get" method to parse the data
        imgResult = adSearchResults.find("div", class_="picture")
        listingTitles.append(imgResult.get("alt"))
        images.append(imgResult.get("src"))
        prices.append(adSearchResults.find("div", class_ ="price").text.replace("\n","").strip())
        locations.append(adSearchResults.find("div", class_ = "location").text.replace("\n","").strip())
        links.append("https://www.adverts.ie" + adSearchResults.find("a", class_ ="main-image").get("href"))
    i+=1
    print(listingTitles)

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
    print
if __name__ =='__main__':
    app.run(debug=True, port =5000)
