# Sentiment Analysis

### Summary ###
Using BeautifulSoup to scrape the news information from the given website, and the results (including the title, sub-title, and content of the 10 most recent articles) are written to one JSON file. After that, using TextBlob as the tool to compute the sentiment of each news article and finally draw the plot by plotly.

Other details are showed in the following parts.

### JSON File Fotmat ###
![Screen Shot 2022-06-07 at 3 41 54 PM](https://user-images.githubusercontent.com/46780987/172495210-02b12adc-9834-4841-85f5-9072ec20b09f.png)

### Sentiment Analysis Approach ###
Textblob is a simple python library that offers API access to different NLP tasks such as sentiment analysis, spelling correction, etc. It is more suitable for news sentiment analysis compared with VADER which is applied more to social media's sentiment analysis.

Textblob sentiment analyzer can return two properties for a given input sentence: polarity and subjectivity. For this task, we will use the value of polarity as our criteria, which is a float that lies between [-1,1], -1 indicates negative sentiment and +1 indicates positive sentiments. 

### Results Visualization ###
The first plot shows the polarity of each article.
![plot1](https://user-images.githubusercontent.com/46780987/172498692-fb68aeb5-067f-4c04-8100-fa0a44ffbc22.png)

The second plot shows the number of each class: positive, neutral and negative. If the polarity of the article lies between [-0.05,0.05], the article will be classified as a neutral article; if it is larger than 0.05, then it will be classified as a positive article; otherwise, it will be classified as a negative article.

![plot2](https://user-images.githubusercontent.com/46780987/172523780-a05ac43e-d0d6-4419-bc58-8fd3d237e6bd.png)

The plots indicate that most of the articles are neutral which is consistent with our perception that news should be neutral.

### How to Run ###
Install all the external packages listed in requirements.txt and run the main.py in Python 3.8+ environment.

### Operation Time ###
The total operation time is around 14 seconds.
