from civic_scraper.platforms.civic_clerk.site import CivicClerkSite

site = CivicClerkSite("https://cityofukiah.com/meetings/", place="Ukiah", state_or_province="CA")
assets = site.scrape(download=False)

# Save output
import json
with open("data/ukiah.json", "w") as f:
    json.dump([a.to_dict() for a in assets], f, indent=2)