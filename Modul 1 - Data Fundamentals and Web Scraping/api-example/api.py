import requests

def fetch_news(city):
    url = "https://indonesia-news.p.rapidapi.com/search/kompas"
    querystring = {"command": city, "page": "1", "limit": "10"}
    headers = {
        "X-RapidAPI-Key": "de85987dc7msha94ae4463722f1ep1b6118jsn8fa2737f13af",
        "X-RapidAPI-Host": "indonesia-news.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code == 200:
        response_news = response.json()
        return response_news
      
    else:
        return {"error": f"Failed to fetch news. Status code: {response.status_code}"}