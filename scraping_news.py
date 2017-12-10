<<<<<<< HEAD


from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import pandas as pd


# Get links for all business articles
import datetime
# Set the origin date
start_date = "10/28/15"
orig_date = datetime.datetime.strptime(start_date, "%m/%d/%y")
all_news_link = []

# Increment origin date by 1 and read the page
# do this for 730 iterations (2 years)
for i in range(1,84):

    # Increment date
    archive_date = orig_date + datetime.timedelta(days=i)
    yr = str(archive_date.year)
    mnt = str(archive_date.month)
    dy = str(archive_date.day)

    # Create the link for scraping
    # The archive page contains all the news links for that date
    news_link = "http://www.thehindu.com/archive/web/" + yr + "/" + mnt + "/" + dy

    # Read the link
    req = Request(news_link,
                  headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage)

    # Only extract links (href attribute from "a" tag)
    link_text = [a['href'] for a in soup.find_all('a', href=True) if a.text.strip()]

    # We are only interested in business links
    # also we are only interested in articles..
    # news articles have .ece extension at the end
    links_business = [x for x in link_text if re.search("/business/", x)]
    links_business = [x for x in links_business if re.search("\.ece$", x)]

    news_link_df = pd.DataFrame({"news_date" : archive_date,"links": links_business})
    all_news_link.append(news_link_df)
    if (i % 50) == 0:
        res_interim = pd.concat(all_news_link)
        res_interim.to_csv("res_interim.csv")
    print(i)

res = pd.concat(all_news_link)

# Read news link
# read link file
link_file = pd.read_csv("all_links.csv")
news_article = []
links = []
article_date = []
error_ids = []
for i in range(0,len(link_file)):
    try:
        link = link_file["links"].iloc[i]
        req = Request(link,
                  headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage)

        # News artcile is contained in a div tag
        # .. with id defined by "content-body"
        txt = soup.find_all("div", {"id":re.compile("content-body")})
        soup = BeautifulSoup(str(txt))
        news_article.append(soup.get_text())
        links.append(link_file["links"].iloc[i])
        article_date.append(link_file["news_date"].iloc[i])

        if (i % 50) == 0:
            res_interim = pd.DataFrame({"date": article_date,
                                        "link": links,
                                        "article_txt": news_article})
            file_name = "res_interim" + str(i) + ".csv"
            res_interim.to_csv(file_name)

        print(i)
    except BaseException as e:
        error_ids.append(i)


# Append results ......
final_res = pd.DataFrame({"date": link_file["news_date"],
                          "news_link": link_file["links"],
=======


from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import pandas as pd


# Get links for all business articles
import datetime
# Set the origin date
start_date = "11/28/15"
orig_date = datetime.datetime.strptime(start_date, "%m/%d/%y")
all_news_link = []

# Increment origin date by 1 and read the page
# do this for 730 iterations (2 years)
for i in range(46,730):

    # Increment date
    archive_date = orig_date + datetime.timedelta(days=i)
    yr = str(archive_date.year)
    mnt = str(archive_date.month)
    dy = str(archive_date.day)

    # Create the link for scraping
    # The archive page contains all the news links for that date
    news_link = "http://www.thehindu.com/archive/web/" + yr + "/" + mnt + "/" + dy

    # Read the link
    req = Request(news_link,
                  headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage)

    # Only extract links (href attribute from "a" tag)
    link_text = [a['href'] for a in soup.find_all('a', href=True) if a.text.strip()]

    # We are only interested in business links
    # also we are only interested in articles..
    # news articles have .ece extension at the end
    links_business = [x for x in link_text if re.search("/business/", x)]
    links_business = [x for x in links_business if re.search("\.ece$", x)]

    news_link_df = pd.DataFrame({"news_date" : archive_date,"links": links_business})
    all_news_link.append(news_link_df)
    if (i % 50) == 0:
        res_interim = pd.concat(all_news_link)
        res_interim.to_csv("res_interim.csv")
    print(i)

res = pd.concat(all_news_link)

# Read news link
# read link file
link_file = pd.read_csv("res_1_84.csv")
news_article = []
error_ids = []
for i in range(0,20):
    try:
        link = link_file["links"].iloc[i]
        req = Request(link,
                  headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage)

        # News artcile is contained in a div tag
        # .. with id defined by "content-body"
        txt = soup.find_all("div", {"id":re.compile("content-body")})
        soup = BeautifulSoup(str(txt))
        news_article.append(soup.get_text())
        print(i)
    except BaseException as e:
        news_article.append(str(e))
        error_ids.append(i)

# Append results
final_res = pd.DataFrame({"date": link_file["news_date"].iloc[0:20],
                          "news_link": link_file["links"].iloc[0:20],
>>>>>>> 36ed0435128be5eb0c14c9184a05f4c6ee17c8a3
                          "article_txt": news_article})