import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from ddgs import DDGS
from urllib.parse import urlparse

def get_session_with_retries():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.mount('http://', HTTPAdapter(max_retries=retries))
    return session

def clean_company_name(name):
    noise_words = [" LTD.", " LTD", " INC.", " INC", " CORP.", " CORP", " LLC"]
    clean = name.upper()
    for word in noise_words:
        clean = clean.replace(word, "")
    return clean.strip()

def resolve_domain(company_name, city="Lethbridge"):
    session = get_session_with_retries()
    clean_name = clean_company_name(company_name)
    
    # Phase 1: Clearbit
    try:
        url = f"https://autocomplete.clearbit.com/v1/companies/suggest?query={clean_name}"
        response = session.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0].get('domain')
    except Exception:
        pass
        
    # Phase 2: DDGS Fallback
    try:
        # Prevent rate-limiting
        time.sleep(1.5) 
        
        search_query = f'"{clean_name}" {city} official website'
        results = DDGS().text(search_query, max_results=1)
        
        # ddgs returns a generator, cast to list
        results_list = list(results)
        
        if results_list:
            raw_url = results_list[0].get("href")
            parsed_uri = urlparse(raw_url)
            domain = parsed_uri.netloc
            return domain.replace("www.", "")
            
    except Exception as e:
        pass

    return None