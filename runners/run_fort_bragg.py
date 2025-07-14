from civic_scraper.platforms import LegistarSite
url = 'https://cityfortbragg.legistar.com/Calendar.aspx'
site = LegistarSite(url)
assets_metadata = site.scrape()