import requests
import feedparser
from bleach import clean
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import NewsItem
import datetime
from .serializers import NewsItemSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import NewsItem
from .serializers import NewsItemSerializer
import requests
import feedparser
from bleach import clean
import datetime

@api_view(['GET'])
def fetch_news(request):
    try:
        feed_url = "https://api.io.canada.ca/io-server/gc/news/en/v2?dept=departmentofcitizenshipandimmigration&sort=publishedDate&orderBy=desc&format=atom"
        news_items = fetch_and_parse_atom(feed_url)
        
        if news_items:
#            print("News items fetched from RSS feed:")
            for news_item in news_items:
                print(news_item)
                title = news_item['title'][:200]  # Truncate title to 200 characters
                link = news_item['link'][:200]  # Truncate link to 200 characters
                summary = news_item['summary'][:200]  # Truncate summary to 200 characters
                category = news_item['category'][:200]  # Truncate category to 200 characters
                source = news_item['source'][:100]  # Truncate source to 100 characters
                NewsItem.objects.update_or_create(
                    title=title,
                    link=link,
                    defaults={
                        'summary': summary,
                        'updated': news_item['updated'],
                        'category': category,
                        'source': source
                    }
                )
            response_source = "Fetched from RSS API, stored in DB"
        else:
            print("No news items fetched, falling back to database")
            news_items = NewsItem.objects.all().order_by('-updated')
            response_source = "API is down, fetched from database. Data might not be updated."

    except Exception as e:
        print(f"Error: {e}")
        news_items = NewsItem.objects.all().order_by('-updated')
        response_source = "API is down, fetched from database. Data might not be updated."

    serializer = NewsItemSerializer(news_items, many=True)
    return Response({'source': response_source, 'data': serializer.data})

def fetch_and_parse_atom(feed_url):
    try:
        response = requests.get(feed_url, timeout=10)
        response.raise_for_status()
        print(f"Fetched data: {response.content}")

        feed = feedparser.parse(response.content)
        news_items = [parse_entry(entry) for entry in feed.entries]

        print(f"Parsed news items: {news_items}")
        return news_items

    except requests.exceptions.RequestException as e:
        print(f"Error fetching RSS feed: {e}")
        return None

    except Exception as e:
        print(f"Error parsing RSS feed: {e}")
        return None

def parse_entry(entry):
    title = entry.title
    link = entry.link
    summary = clean(
        getattr(entry, 'summary', getattr(entry, 'description', '')),
        tags=['p', 'a', 'br', 'ul', 'ol', 'li', 'strong', 'em'],
        attributes={'a': ['href', 'rel']}
    )

    updated_date_str = getattr(entry, 'updated', None)
    published_date = parse_date(updated_date_str)
    categories = parse_categories(getattr(entry, 'category', []))

    return {
        'title': title,
        'link': link,
        'summary': summary,
        'updated': published_date.isoformat() if published_date else None,
        'category': ', '.join(categories),
        'source': 'IRCC'
    }

def parse_date(date_str):
    if date_str:
        try:
            return datetime.datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except ValueError:
            try:
                return datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                print(f"Warning: Could not parse date: {date_str}")
    return None

def parse_categories(categories):
    if isinstance(categories, list):
        return [extract_term(category) for category in categories if extract_term(category)]
    return [extract_term(categories)] if extract_term(categories) else []

def extract_term(category):
    if hasattr(category, 'term'):
        return decode_if_bytes(category.term)
    return decode_if_bytes(category) if isinstance(category, (str, bytes)) else None

def decode_if_bytes(value):
    if isinstance(value, bytes):
        try:
            return value.decode('utf-8')
        except UnicodeDecodeError:
            print(f"Warning: Could not decode value: {value}")
    elif isinstance(value, str):
        try:
            return value.encode('latin1').decode('utf-8')
        except UnicodeDecodeError:
            print(f"Warning: Could not decode value: {value}")
    return value


@api_view(['GET'])
def get_news_items(request):
    news_items = NewsItem.objects.all().order_by('-updated')
    data = [{
        'title': item.title,
        'link': item.link,
        'summary': item.summary,
        'updated': item.updated,
        'category': item.category,
        'source': item.source,
    } for item in news_items]

    response_message = "Data fetched may be outdated. Update using fetch-store endpoint if RSS API works; otherwise, stored data will be shown."
    if news_items.exists() and news_items.first().updated.date() == datetime.date.today():
        response_message = "Data is up-to-date."

    return Response({'source': response_message, 'data': data})

@api_view(['GET'])
def categories(request):
    try:
        categories = NewsItem.objects.values_list('category', flat=True).distinct()
        return Response({'categories': list(categories)})
    
    except Exception as e:
        return Response({'error': f"An error occurred: {str(e)}"})

@api_view(['GET'])
def news_releases(request):
    news_items = NewsItem.objects.filter(category__icontains='news releases').order_by('-updated')
    serializer = NewsItemSerializer(news_items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def readouts(request):
    news_items = NewsItem.objects.filter(category__icontains='readouts').order_by('-updated')
    serializer = NewsItemSerializer(news_items, many=True)
    return Response({'source': "Readouts f  etched successfully", 'data': serializer.data})

@api_view(['GET'])
def backgrounders(request):
    news_items = NewsItem.objects.filter(category__icontains='backgrounders').order_by('-updated')
    serializer = NewsItemSerializer(news_items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def media_advisories(request):
    news_items = NewsItem.objects.filter(category__icontains='media advisories').order_by('-updated')
    serializer = NewsItemSerializer(news_items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def statements(request):
    news_items = NewsItem.objects.filter(category__icontains='statements').order_by('-updated')
    serializer = NewsItemSerializer(news_items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def speeches(request):
    news_items = NewsItem.objects.filter(category__icontains='speeches').order_by('-updated')
    serializer = NewsItemSerializer(news_items, many=True)
    return Response(serializer.data)
