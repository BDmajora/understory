import requests
import csv
import io

def get_lethbridge_businesses(limit=100):
    """
    Fetches business licenses from the Lethbridge Open Data CSV endpoint
    and filters out generic license categories.
    """
    url = "https://gis.lethbridge.ca/OpenData/DataSets/BusinessLicenses.csv"
    
    # Generic categories often listed as Trade Names in the registry
    BANNED_NAMES = [
        "HOME OCCUPATION", 
        "RESIDENTIAL-TENANT", 
        "NON-RESIDENT",
        "BED AND BREAKFAST",
        "DAY CARE"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64)"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        content = response.content.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(content))
        
        cleaned_results = []
        
        for row in csv_reader:
            if len(cleaned_results) >= limit:
                break
            
            # Normalize the name for comparison
            raw_name = row.get("TRADE_NAME") or ""
            name = raw_name.strip().upper()
            
            # Skip if the name is a generic category or empty
            if not name or name in BANNED_NAMES:
                continue
                
            # Only ingest approved/active businesses
            if row.get("LICENSE_STATUS") == "APPROVED":
                cleaned_results.append({
                    "tradename": raw_name.strip(), # Keep original casing for resolver
                    "address": row.get("ADDRESS"),
                    "status": row.get("LICENSE_STATUS")
                })
                
        return cleaned_results

    except Exception as e:
        print(f"Data Fetch Error: {e}")
        return []