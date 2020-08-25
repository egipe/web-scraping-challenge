# Import dependencies
import pandas as pd
from bs4 import BeautifulSoup 
from splinter import Browser
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():

    browser=init_browser()
    time.sleep(5)

    # NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    mars_soup = BeautifulSoup(html, 'html.parser')

    title=mars_soup.select_one('ul.item_list li.slide')
    news_title= title.find('div', class_='content_title').get_text()
    paragraph=mars_soup.find('div', class_='article_teaser_body').get_text()

    # JPL Mars Space Images - Featured Image
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url = 'https://www.jpl.nasa.gov'
    browser.visit(image_url)
    html = browser.html
    jpl_soup = BeautifulSoup(html, 'html.parser')

    image = jpl_soup.find_all('a', class_='button fancybox')[0].get('data-fancybox-href').strip()

    featured_image_url = url + image

    # Mars Facts
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
    facts_soup = BeautifulSoup(html, 'html.parser')

    table_df = pd.read_html(url)[0]
    updated_table = table_df.rename(columns={0:'Measurement',1:'Value'}).set_index('Measurement').copy()

    # Convert to HTML
    table_html = updated_table.to_html()

    # Mars Hemispheres
    hemi_url = 'https://astrogeology.usgs.gov'
    full_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(full_url)
    html = browser.html
    hemisphere_soup = BeautifulSoup(html, 'html.parser')

    images = hemisphere_soup.find_all('div', class_='item')
    hemispheres = []

    # Loop through images
    for img in images:
        title = img.find('h3').text
        specific_image_url = img.find('a', class_='itemLink product-item')['href']
        browser.visit(hemi_url+specific_image_url)
        img_route = browser.html
        image_soup = BeautifulSoup(img_route,'html.parser')
        img_url = hemi_url + image_soup.find('img', class_='wide-image')['src']
        hemispheres.append({'title':title, 'img_url': img_url})
    
    mars_items = {
        "mars_title": news_title,
        "mars_paragraph": paragraph, 
        "mars_main_image": featured_image_url,
        "mars_table": table_html,
        "mars_hemi_imgs": hemispheres
    }

    browser.quit()

    return mars_items

