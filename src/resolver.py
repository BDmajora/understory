import requests

def resolve_domain(company_name):
    """
    Uses Clearbit's free autocomplete API to find a domain for a company name.
    """
    url = f"https://autocomplete.clearbit.com/v1/companies/suggest?query={company_name}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data:
                # Returns the most likely domain (e.g., "google.com")
                return data[0].get('domain')
    except Exception:
        return None
    return None