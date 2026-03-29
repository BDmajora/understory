import requests
import csv
import io

def get_lethbridge_businesses(limit=100):
    """
    Fetches business licenses from the Lethbridge Open Data CSV endpoint
    and filters out generic license categories and noise.
    """
    # Direct link to the 2026 Business License CSV
    url = "https://gis.lethbridge.ca/OpenData/DataSets/BusinessLicenses.csv"
    
    # Generic categories and placeholders that cause false positives in the resolver
    BANNED_NAMES = [
        "HOME OCCUPATION", 
        "RESIDENTIAL-TENANT", 
        "NON-RESIDENT",
        "BED AND BREAKFAST",
        "DAY CARE",
        "REDACTED",
        "TAXI OPERATOR",
        "DIRECT SALES",
        "MOBILE BUSINESS"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64)"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        # Use io.StringIO to treat the text as a file for the CSV reader
        content = response.content.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(content))
        
        cleaned_results = []
        
        for row in csv_reader:
            if len(cleaned_results) >= limit:
                break
            
            # Normalize the name for filtering comparison
            raw_name = row.get("TRADE_NAME") or ""
            name_upper = raw_name.strip().upper()
            
            # 1. Skip if empty or matches our noise list
            if not name_upper or name_upper in BANNED_NAMES:
                continue
            
            # 2. Skip specific placeholder strings (like 'REDACTED - ADDRESS')
            if "REDACTED" in name_upper:
                continue
                
            # 3. Only ingest approved/active businesses
            if row.get("LICENSE_STATUS") == "APPROVED":
                cleaned_results.append({
                    "tradename": raw_name.strip(), # Keep original casing for the search engine
                    "address": row.get("ADDRESS"),
                    "status": row.get("LICENSE_STATUS")
                })
                
        return cleaned_results

    except Exception as e:
        print(f"Data Fetch Error: {e}")
        return []