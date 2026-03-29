from src.discovery import get_lethbridge_businesses
from src.resolver import resolve_domain
from src.storage import save_to_jsonl

def main():
    print("Initializing Understory Discovery Engine...")
    
    # 1. Ingest from Lethbridge City Registry
    raw_businesses = get_lethbridge_businesses(100)
    print(f"Found {len(raw_businesses)} active licenses.")
    
    for bus in raw_businesses:
        name = bus.get("tradename")
        address = bus.get("address")
        
        print(f"Resolving: {name}...")
        
        # 2. Resolve Name -> Domain
        domain = resolve_domain(name)
        
        # 3. Structure
        result = {
            "name": name,
            "address": address,
            "domain": domain,
            "source": "Lethbridge Open Data"
        }
        
        # 4. Save locally
        save_to_jsonl(result)
        
        if domain:
            print(f"Found: {domain}")
        else:
            print(f"No domain found.")

if __name__ == "__main__":
    main()