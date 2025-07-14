import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

BASE_URL = "https://cityofukiah.com/meetings/"
CIVICCLERK_API = "https://ukiahca.api.civicclerk.com/v1/Meetings/GetMeetingFileStream"

def parse_datetime(text):
    try:
        # Example: "Tuesday Jul 1, 2025 at 6:00 PM PST"
        dt = datetime.strptime(text.strip(), "%A %b %d, %Y at %I:%M %p PST")
        return dt.isoformat()
    except ValueError:
        return None

def scrape_meetings():
    res = requests.get(BASE_URL)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    meetings = []

    for li in soup.select("li.clerk-simple-MuiListItem-container"):
        try:
            a_tag = li.find("a", href=True)
            meeting_id = a_tag["data-id"]
            raw_datetime = li.find("p").text.strip()
            iso_datetime = parse_datetime(raw_datetime)
            title = li.find("h3").text.strip()
            location = li.find("h6").text.strip()

            # Try fetching associated agenda file
            file_url = f"{CIVICCLERK_API}?fileId={meeting_id}&plainText=false"
            file_response = requests.get(file_url)

            agenda_files = []
            if file_response.status_code == 200 and "application/pdf" in file_response.headers.get("Content-Type", ""):
                agenda_files.append(file_url)

            meetings.append({
                "title": title,
                "datetime": iso_datetime,
                "location": location,
                "meeting_id": meeting_id,
                "agenda_files": agenda_files
            })

        except Exception as e:
            print(f"Failed to parse a meeting block: {e}")

    return meetings

if __name__ == "__main__":
    meeting_data = scrape_meetings()
    with open("ukiah_meetings.json", "w") as f:
        json.dump(meeting_data, f, indent=2)
    print("✅ Saved to ukiah_meetings.json")
