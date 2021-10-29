from scraper import ScraperIMDb

output_file = 'dataset.csv'

scraper = ScraperIMDb()
scraper.scrape()
scraper.write_csv(output_file)
