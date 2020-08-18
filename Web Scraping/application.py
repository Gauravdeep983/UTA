from flask import Flask, render_template, url_for, request
from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen  # Web client
import requests

app = Flask(__name__)

# Home redirect
@app.route('/')
def index(): return render_template('index.html')

@app.route('/scrape', methods=["GET"])
def scrape():    
    # URL to scrape
    page_url = "https://dev.to/t/python"

    # opens the connection and downloads html page from url
    page = requests.get(page_url)

    # parses html into a soup data structure to traverse html as if it were a json data type.
    page_soup = soup(page.content, 'html.parser')
    #Get all article titles
    titles = page_soup.findAll("div", {"class": "crayons-story"})

    title = titles[0]

    # for title in titles:
    #     title




    return render_template("scraped.html", data=title)


if __name__ == '__main__':
    app.run(debug=True)