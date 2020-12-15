from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.common.by import By
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

pos_count = 0
neg_count = 0
neutral_count = 0
def sentiment_scores(sentence):
    global pos_count
    global neg_count
    global neutral_count
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # oject gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)

    """print("Overall sentiment dictionary is : ", sentiment_dict)
    print("sentence was rated as ", sentiment_dict['neg'] * 100, "% Negative")
    print("sentence was rated as ", sentiment_dict['neu'] * 100, "% Neutral")
    print("sentence was rated as ", sentiment_dict['pos'] * 100, "% Positive")

    print("Sentence Overall Rated As", end=" ")"""

    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05:
        #print("Positive")
        pos_count+=1

    elif sentiment_dict['compound'] <= - 0.05:
        #print("Negative")
        neg_count+=1

    else:
       # print("Neutral")
        neutral_count+=1




def econonmics(stock,file):
    path = 'C:\chromedriver'
    buisness = webdriver.Chrome(path)
    buisness.maximize_window()
    buisness.get('https://economictimes.indiatimes.com/')
    sleep(10)
    search_economic = buisness.find_element_by_xpath('/html/body/main/div[5]/nav/div[18]/span')
    search_economic.click()
    search_news = buisness.find_element_by_xpath('/html/body/main/div[3]/div/div/input')
    search_news.send_keys(stock)
    sleep(3)
    search_news.send_keys(Keys.ENTER)
    sleep(8)
    news_button = buisness.find_element_by_xpath('//*[@id="stockNav"]/div/ul/li[2]')
    news_button.click()
    sleep(3)
    next_tab = buisness.find_element_by_xpath('//*[@id="newsAnalysis"]/div/div/a/span')
    next_tab.click()
    buisness._switch_to.window(buisness.window_handles[1])
    head_tags = buisness.find_elements(By.TAG_NAME,'h3')
    print("Processing........ datas from econnomic times news")
    q=0
    while q<len(head_tags)-3:
        sen = str(head_tags[q].text)
        file.write(sen)
        file.write('\n')
        q+=1
    buisness.quit()
    buisness.quit()

path='C:\chromedriver'
while True:
    choice=int(input("Press 1 to enter the name of the stock\npress 2 to exit\n"))
    if choice==2:
        break
    stock=input('Enter name of stock:')
    query=stock+' latest news'
    driver = webdriver.Chrome(path)
    driver.maximize_window()
    driver.get('https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN:en')
    search=driver.find_element_by_xpath('//*[@id="gb"]/div[2]/div[2]/div/form/div[1]/div/div/div/div/div[1]/input[2]')
    search.send_keys(query)
    sleep(3)
    search.send_keys(Keys.ENTER)
    url=driver.current_url
    sleep(5)
    driver.quit()
    print("Processing........ datas from google news")
    html = urlopen(url)
    bs = BeautifulSoup(html, "html.parser")
    titles = bs.find_all(['h3','span'])
    f_name=stock+'.txt'
    f=open(f_name,"w",encoding="utf-8")
    i=0
    while i<len(titles):
        sen=str(titles[i])
        if sen[1]=='h':
            l=len(sen)-10
            t=l
            while sen[l]!='>':
                l-=1
            n=str(sen[l+1:t])
            f.write(n)
            f.write(',')
            temp=str(titles[i+1])
            l1=len(temp)-10
            t1=l1
            while temp[l1]!='>':
                l1-=1
            n=str(temp[l1+1:t1])
            f.write(n)
            f.write('\n')
            i+=2
        i+=1
    econonmics(stock,f)
    print("Done :)")
    f.close()

    scan=0
    analyze = open(f_name,"r",encoding="utf-8")
    while True:
        line = analyze.readline()
        if line=='':
            break
        else:
            scan+=1
            sentiment_scores(line)
    analyze.close()
    print("positive count",pos_count,"negative count",neg_count,"neutral count",neutral_count,"total lines",scan)
    pos_count=neutral_count=neg_count=0
#print('List all the header tags :', *titles, sep='\n\n')