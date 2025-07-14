from civic_scraper.platforms import LegistarSite as BaseLegistarSite
import urllib3
import json
import pprint

# Optional: disable warnings about unverified HTTPS
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DebugLegistarSite(BaseLegistarSite):
    def scrape(self, start_year=None):
        """Override scrape to diagnose missing 'iCalendar' key"""
        import legistar

        webscraper = legistar.LegistarEventsScraper(self.url, verify=False)

        if start_year is None:
            start_year = 2015

        print(f"Fetching events from {start_year} onward...\n")
        events = list(webscraper.events(since=start_year))

        if not events:
            raise ValueError("No events returned from legistar scraper.")

        valid_events = []
        invalid_count = 0

        for idx, event in enumerate(events):
            event_data = event[0] if isinstance(event, list) else event

            if "iCalendar" not in event_data:
                print(f"[Warning] Event {idx + 1} missing 'iCalendar':")
                pprint.pprint(event_data)
                invalid_count += 1
                continue

            valid_events.append(event)

        if not valid_events:
            raise ValueError("All events missing 'iCalendar'. Check if Legistar page structure changed.")

        print(f"\nCollected {len(valid_events)} events with iCalendar links. Skipped {invalid_count}.\n")
        return valid_events

# Initialize and run
url = "https://cityfortbragg.legistar.com/Calendar.aspx"
site = DebugLegistarSite(url)
assets = site.scrape()

# Save results
with open("data/fort_bragg.json", "w") as f:
    json.dump(assets, f, indent=2)
