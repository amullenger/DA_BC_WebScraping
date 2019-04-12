def scrape():
    #imort dependencies
    from bs4 import BeautifulSoup as bs
    import requests
    from splinter import Browser
    import pandas as pd

    """
    NASA MARS NEWS
    """

    #store NASA website URL
    nasa_news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    #retreieve page
    nasa_news_response = requests.get(nasa_news_url)
    nasa_news_response

    #create soup object for nasa news page
    nasa_news_soup = bs(nasa_news_response.text, 'html.parser')
    print(nasa_news_soup.prettify())


    #search for all items where class = 'content_title', pull the text for the first
    #   entry and strip the new line characters
    title_results = nasa_news_soup.find_all('div', class_='content_title')
    news_title = title_results[0].text.strip()

    p_results = nasa_news_soup.find_all('div', class_='image_and_description_container')
    news_p = p_results[0].text.strip()

    print(f"{news_title}\n\n {news_p}")

    """
    JPL MARS IMAGE
    """

    #setting up path for chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #visiting url
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    #navigating to full image page
    browser.click_link_by_partial_text('FULL IMAGE')

    #navigating to more info page to get full size image link
    browser.click_link_by_partial_text('more info')

    #parsing html and combining image source to get full image url
    html = browser.html
    soup = bs(html, 'html.parser')

    img_box = soup.find('figure', class_='lede')
    jpl_img_source = img_box.find('a')['href']
    base_url = 'https://www.jpl.nasa.gov'
    jpl_img_url = base_url + jpl_img_source

    """
    MARS WEATHER
    """

    #get response from mars weather twitter page
    nasa_weather_twitter_url = 'https://twitter.com/marswxreport?lang=en'
    nasa_weather_response = requests.get(nasa_weather_twitter_url)

    #create soup object for mars weather twitter page
    nasa_weather_soup = bs(nasa_weather_response.text, 'html.parser')

    #pull out most recent tweet text and save
    weather_tweet = nasa_weather_soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    """
    MARS FACTS
    """

    mars_facts_url = 'https://space-facts.com/mars/'

    #store facts table as dataframe and convert to html
    mars_facts_table = pd.read_html(mars_facts_url)[0]
    mars_facts_table_html = mars_facts_table.to_html()

    """
    MARS HEMISPHERES
    """

    ##visit mars hemisphere web page
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    mars_hemispheres_url =    'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = 'https://astrogeology.usgs.gov'
    browser.visit(mars_hemispheres_url)

    #click on each link and store title and image in dictionary. append dictionary to 
    #   list of dictionaries
    hemisphere_image_urls = []

    #first hemisphere
    browser.click_link_by_partial_text('Cerberus Hemisphere Enhanced')
    html = browser.html
    h1_soup = bs(html, 'html.parser')
    h1_title = h1_soup.find('h2').text
    img_source = h1_soup.find('img', class_='wide-image')['src']
    img_link = base_url + img_source
    hemisphere_image_urls.append({'title': h1_title, 'img_url': img_link})

    #second hemisphere
    browser.click_link_by_partial_text('Back')
    browser.click_link_by_partial_text('Schiaparelli Hemisphere Enhanced')
    html = browser.html
    h1_soup = bs(html, 'html.parser')
    h1_title = h1_soup.find('h2').text
    img_source = h1_soup.find('img', class_='wide-image')['src']
    img_link = base_url + img_source
    hemisphere_image_urls.append({'title': h1_title, 'img_url': img_link})

    #third hemisphere
    browser.click_link_by_partial_text('Back')
    browser.click_link_by_partial_text('Syrtis Major Hemisphere Enhanced')
    html = browser.html
    h1_soup = bs(html, 'html.parser')
    h1_title = h1_soup.find('h2').text
    img_source = h1_soup.find('img', class_='wide-image')['src']
    img_link = base_url + img_source
    hemisphere_image_urls.append({'title': h1_title, 'img_url': img_link})

    #fourth hemisphere
    browser.click_link_by_partial_text('Back')
    browser.click_link_by_partial_text('Valles Marineris Hemisphere Enhanced')
    html = browser.html
    h1_soup = bs(html, 'html.parser')
    h1_title = h1_soup.find('h2').text
    img_source = h1_soup.find('img', class_='wide-image')['src']
    img_link = base_url + img_source
    hemisphere_image_urls.append({'title': h1_title, 'img_url': img_link})

    return {'News Title': news_title, 'News Paragraph': news_p, 'JPL Featured Image URL': jpl_img_url,\
         'NASA Weather': weather_tweet, 'Mars Facts HTML Table': mars_facts_table_html, 'Mars Hemispheres': hemisphere_image_urls}


scrape()

