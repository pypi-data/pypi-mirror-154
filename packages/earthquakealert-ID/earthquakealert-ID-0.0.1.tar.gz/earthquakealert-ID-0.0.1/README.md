# indonesian-earthquake-alert
Package to retrieve latest Indonesia earthquake alert from https://www.bmkg.go.id/

## How it work?
Package will scrape the latest Indonesia earthquake alert from [BMKG](https://www.bmkg.go.id/) website.
The data will be shown with this format:
Latest Earthquake News in Indonesia
Date: ________
Time: ________ WIB
Magnitude: ________
Location: LS: ________ BT: ________
Center: ________
Impact Scale: ________

Package will use BeautifulSoup4 and requests to retrieve and parse the website data.