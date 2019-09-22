import csv 
import requests 
import xml.etree.ElementTree as ET 
import pandas as pd 

def loadRSS(url): 
  
    # url of rss feed 
    #url = 'http://www.hindustantimes.com/rss/topnews/rssfeed.xml'
    #url = "https://www.thehindu.com/news/national/karnataka/feeder/default.rss"
    #url = "https://www.thehindu.com/news/national/other-states/feeder/default.rss"
    #url = "https://www.bhaskar.com/rss-feed/3682/" #jharkhand
    #url = "https://feed.livehindustan.com/rss/5142" #ranchi
    # creating HTTP response object from given url 
    resp = requests.get(url) 
  
    # saving the xml file 
    with open('topnewsfeed.xml', 'wb') as f: 
        f.write(resp.content) 
          
  
def parseXML(xmlfile): 
  
    # create element tree object 
    tree = ET.parse(xmlfile) 
  
    # get root element 
    root = tree.getroot() 
  
    # create empty list for news items 
    newsitems = [] 
  
    # iterate news items 
    for item in root.findall('./channel/item'): 
  
        # empty news dictionary 
        news = {} 
  
        # iterate child elements of item 
        for child in item: 
  
            # special checking for namespace object content:media 
            if child.tag == '{http://search.yahoo.com/mrss/}content': 
                news['media'] = child.attrib['url'] 
            else: 
                news[child.tag] = child.text #.encode('utf8') 
  
        # append news dictionary to news items list 
        newsitems.append(news) 
      
    # return news items list 
    return newsitems 
  
  
def savetoCSV(newsitems, filename): 
  
    # specifying the fields for csv file 
    df = pd.DataFrame(newsitems)
    print(df.columns)
    return df
    #df.to_csv(filename,index=False)
    """
    fields = ['guid', 'title', 'pubDate', 'description', 'link', 'media'] 
  
    # writing to csv file 
    with open(filename, 'w') as csvfile: 
  
        # creating a csv dict writer object 
        writer = csv.DictWriter(csvfile, fieldnames = fields) 
  
        # writing headers (field names) 
        writer.writeheader() 
  
        # writing data rows 
        writer.writerows(newsitems) 
   """

def get_data_json(url):
    loadRSS(url) 
  
    # parse xml file 
    newsitems = parseXML('topnewsfeed.xml') 
  
    return newsitems

def get_data_csv():
    loadRSS() 
  
    # parse xml file 
    newsitems = parseXML('topnewsfeed.xml') 
  
    # store news items in a csv file 
    filename = 'topnews.csv'
    df = savetoCSV(newsitems, 'topnews.csv') 
    return df

def main(): 
    df = get_data()
    df.to_csv(filename,index=False)
      
if __name__ == "__main__": 
  
    # calling main function 
    main() 
