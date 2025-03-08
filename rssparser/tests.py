import requests
import xml.etree.ElementTree as ET
from django.http import JsonResponse

def fetch_rss_feed(request):
    url = "https://api.io.canada.ca/io-server/gc/news/en/v2?dept=departmentofcitizenshipandimmigration&sort=publishedDate&orderBy=desc&publishedDate%3E=2021-07-23&pick=50&format=atom&atomtitle=Immigration,%20Refugees%20and%20Citizenship%20Canada"
    response = requests.get(url)
    root = ET.fromstring(response.content)
    
    items = []
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        item = {
            "title": entry.find("{http://www.w3.org/2005/Atom}title").text,
            "link": entry.find("{http://www.w3.org/2005/Atom}link").attrib['href'],
            "summary": entry.find("{http://www.w3.org/2005/Atom}summary").text,
            "published": entry.find("{http://www.w3.org/2005/Atom}updated").text,
            "author": entry.find("{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name").text,
            "category": entry.find("{http://www.w3.org/2005/Atom}category").attrib['term']
        }
        items.append(item)
    
    return JsonResponse(items, safe=False)
