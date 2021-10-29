import re
import requests
import time
from bs4 import BeautifulSoup


class ScraperIMDb:
    def __init__(self):
        self.url = 'https://www.imdb.com'
        self.subdomain = '/search/title/?groups=top_1000&sort=user_rating,desc&count=100'
        self.data = [['Rank', 'Title', 'Release year', 'Runtime', 'Genre',
                     'Rating', 'Director(s)', 'Votes', 'Gross']]

    def scrape_one_page(self, html):
        content = BeautifulSoup(html.content, 'html.parser')
        movieList = content.findAll('div', attrs={'class': 'lister-item mode-advanced'})

        for movie in movieList:
            movieInfo = movie.find('div', attrs={'class': 'lister-item-content'})
            rank = int(movieInfo.h3.find('span', attrs={'class': 'lister-item-index unbold text-primary'})
                       .text.replace(',', '')[:-1])
            title = movieInfo.h3.a.text
            year = movieInfo.h3.find('span', attrs={'class': 'lister-item-year text-muted unbold'}).text.strip()
            year = str(re.sub('[^0-9]', '', year))

            runtime = movieInfo.p.find('span', class_='runtime').text
            genre = movieInfo.p.find('span', class_='genre').text.strip()

            rating = float(movieInfo.find('div', class_='ratings-bar').div.strong.text)

            # There could be more than one director
            directors = [x.strip() for x in movieInfo.find('p', class_='').text.split('\n')]
            if directors[1] == 'Director:':
                director = directors[2]
            else:
                director = ' '.join(directors[2:directors.index('|')])
            # director = movieInfo.find('p', class_='').text.split('\n')[2]

            votes_and_gross = movieInfo.find('p', class_='sort-num_votes-visible').text.split('\n')[::2]
            votes = int(votes_and_gross[1].replace(',', ''))
            if len(votes_and_gross) > 2:
                gross = votes_and_gross[2]
            else:
                gross = '?'

            self.data.append([rank, title, year, runtime, genre, rating, director, votes, gross])

    def get_all_links(self):
        links = []
        for i in range(10):
            link = self.url + self.subdomain + '&start=' + str(i) + '01'
            links.append(link)

        return links

    def scrape(self):
        print('Web scraping started!')
        start_time = time.time()

        links = self.get_all_links()
        for link in links:
            html = requests.get(link, headers={"Accept-Language": "en-US, en;q=0.5"})
            self.scrape_one_page(html)

        print('Web scraping finished!')
        end_time = time.time()
        print('\tElapsed time: ' + str(round((end_time-start_time), 2)) + ' seconds\n')

    def write_csv(self, filename):
        file = open('./csv/' + filename, 'w+')

        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                file.write(str(self.data[i][j]) + ';')
            file.write('\n')

        print('You will find the resulting dataset in /csv/'+filename)
