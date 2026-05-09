import time
import requests
from bs4 import BeautifulSoup
import urllib.parse
import random

def extract_amazon_reviews(url: str):
    """
    Scrapes reviews from an Amazon product URL using requests and BeautifulSoup.
    Includes rotating User-Agents and status checking to handle basic bot protection.
    """
    
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1'
    ]
    
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'en-US, en;q=0.5',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'https://www.google.com/'
    }
    
    start_time = time.time()
    domain = urllib.parse.urlparse(url).netloc or "amazon.com"
    is_simulated = False
    
    try:
        # Small delay to mimic human behavior
        time.sleep(random.uniform(0.5, 1.5))
        
        response = requests.get(url, headers=headers, timeout=15)
        
        # Amazon often returns 503 or 200 with a captcha page
        if response.status_code != 200 or "captcha" in response.text.lower() or "api-services-support@amazon.com" in response.text:
            is_simulated = True
            reviews = []
        else:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Amazon specific review blocks
            review_elements = soup.find_all('span', {'data-hook': 'review-body'})
            
            reviews = []
            for el in review_elements:
                text = el.get_text(separator=' ', strip=True)
                if text and len(text) > 10:
                    reviews.append(text)
            
            if not reviews:
                # Fallback to general paragraphs if specifically labeled reviews aren't found
                for p in soup.find_all('p')[:10]:
                    txt = p.get_text(strip=True)
                    if len(txt) > 40: reviews.append(txt)
                
            if not reviews: is_simulated = True

    except Exception:
        is_simulated = True
        reviews = []
            
    # If blocked or failed, use high-quality simulated data for the MVP demo
    if is_simulated:
        reviews = [
            "This product exceeded my expectations! The build quality is premium and it works exactly as described.",
            "Average experience. The shipping was delayed by 3 days and the packaging was slightly dented.",
            "Terrible. It stopped working after just two hours of use. I am requesting a full refund immediately.",
            "Great value for the price. I've been using it for a month now with no major issues.",
            "The instructions were hard to follow, but once set up, it performs quite well."
        ]
            
    extraction_time_ms = int((time.time() - start_time) * 1000)
    
    return {
        "reviews": reviews,
        "metadata": {
            "total_reviews_scraped": len(reviews),
            "source_domain": domain,
            "extraction_time_ms": extraction_time_ms,
            "is_simulated": is_simulated
        }
    }
