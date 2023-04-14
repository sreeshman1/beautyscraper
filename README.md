# Ulta Beauty Web Scraper

This is a web scraper built using Python and Scrapy to scrape product information from Ulta Beauty's website.

## Installation

1. Make sure you have Python 3.6+ installed on your machine.

2. Clone this repository:

```bash

git clone https://github.com/yourusername/ulta-beauty-web-scraper.git

cd ulta-beauty-web-scraper

```

Install the required dependencies:

```bash

pip install -r requirements.txt

```

## Usage

To run the scraper and save the scraped data to a CSV file, execute the following command:

```bash

scrapy crawl ulta

```

This will generate a file named `ulta_products.csv` in the same directory, containing the scraped product data.

## Data Fields

The following data fields are scraped for each product:

- 'name': Product name

- 'brand': Brand name

- 'price': Product price

- 'ingredients': List of product ingredients

- 'images': List of product image URLs
