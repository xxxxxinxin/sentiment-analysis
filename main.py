import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from textblob import TextBlob
import plotly.graph_objects as go
import timeit


# Return the sentimental polarity of the text
def polarity(text):
    return TextBlob(text).sentiment.polarity


if __name__ == '__main__':
    # Calculate running time
    start = timeit.default_timer()

    # Collect 10 most recent articles and pre-process the data by BeautifulSoup
    baseURL = "https://www.aljazeera.com"
    URL = "https://www.aljazeera.com/where/mozambique/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    link_list = []
    results_first = soup.find(id="featured-news-container")

    # Find <a> tag under element with id: featured-news-container
    # to get the links of news in first part of website
    news_elements_first = results_first.find_all("a",
                                                 class_="u-clickable-card__link")

    for news_elements in news_elements_first:
        link_url = news_elements["href"]
        link_list.append(baseURL + link_url)

    results_second = soup.find(id="news-feed-container")

    # Find <a> tag under element with id: news-feed-container
    # to get the links of news in second part of website
    news_elements_second = results_second.find_all("a",
                                                   class_="u-clickable-card__link")

    for news_elements in news_elements_second:
        link_url = news_elements["href"]
        link_list.append(baseURL + link_url)

    count = 10
    file = open('result.json', 'w')
    num = len(link_list)

    result_list = list()

    json_file = dict()

    for i in tqdm(range(num)):
        result_json = dict()

        news_page = requests.get(link_list[i])
        soup = BeautifulSoup(news_page.content, "html.parser")
        news_info = soup.find(id="main-content-area")
        header_info = news_info.find_all("header", class_="article-header")

        # Get the title of news
        title = header_info[0].find_all("h1")[0]
        result_json["title"] = title.text.strip()

        header_p = header_info[0].find_all("p")

        # Get the subtitle of news only when it is an article
        if len(header_p) != 0 and count > 0:
            subtitle = header_info[0].find_all("p")[0].find_all("em")[0]
            result_json["subTitle"] = subtitle.text.strip()

            content_info = news_info.find_all("div", class_="wysiwyg")[0]

            # Get the paragraph of news article and concatenate them as the content
            para = content_info.find_all("p")
            content = ""
            for c in para:
                c = c.text.strip().replace('\n', ' ').replace('\r', '')
                content = content + c

            result_json["content"] = content
            result_list.append(result_json)
            count -= 1

    json_file["data"] = result_list

    # Write result to json file
    file.write(json.dumps(json_file))
    file.close()

    # Opening JSON file
    with open('result.json') as json_file:
        data = json.load(json_file)

    polarity_list = list()
    for i in tqdm(range(10)):
        p = polarity(data['data'][i]['content'])
        polarity_list.append(p)

    # Visualize the results
    fig = go.Figure(
        data=[go.Bar(y=polarity_list)],
        layout_title_text="Polarity of each news article"
    )
    fig.show()

    # Calculate the number for each class and visualize the results
    pos = 0
    neg = 0
    neu = 0
    for p in polarity_list:
        if p > 0.05:
            pos += 1
        elif p < -0.05:
            neg += 1
        else:
            neu += 1

    fig = go.Figure(
        data=[go.Bar(y=[neg, neu, pos], x=["Negative", "Neutral", "Positive"])],
        layout_title_text="Articles per category(Threshold at 0.05)"
    )
    fig.show()

    stop = timeit.default_timer()
    print('Time: ', stop - start)
