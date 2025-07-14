from civic_scraper.platforms import LegistarSite

url = 'https://cityfortbragg.legistar.com/Calendar.aspx'
site = LegistarSite(url)

# Try scraping
try:
    assets_metadata = site.scrape()
except KeyError as e:
    if "'iCalendar'" in str(e):
        print("Some events were missing 'iCalendar'. Skipping them.")
        assets_metadata = []  # Proceed with empty list
    else:
        raise  # re-raise unexpected KeyErrors

# Optionally write to a JSON file
import json
with open("data/fort_bragg.json", "w") as f:
    json.dump([a.to_dict() for a in assets_metadata], f, indent=2)
