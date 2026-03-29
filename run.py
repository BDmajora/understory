import os
import json
from src.discovery import get_lethbridge_businesses
from src.resolver import resolve_domain
from src.storage import save_to_jsonl

def load_existing_names(filename="discovery_log.jsonl"):
    """
    Reads the JSONL file and returns a set of company names already processed.
    """
    existing_names = set()
    if not os.path.exists(filename):
        return existing_names
    
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                name = data.get("name")
                if name:
                    existing_names.add(name.strip().upper())
            except json.JSONDecodeError:
                continue
    return existing_names

def main():
    print("Initializing Understory Discovery Engine...")
    
    # 1. Load cache to avoid duplicates
    processed_cache = load_existing_names()
    if processed_cache:
        print(f"Loaded {len(processed_cache)} companies from local cache.")

    # 2. Ingest from Lethbridge City Registry
    raw_businesses = get_lethbridge_businesses(150) # Pull extra to account for skips
    
    new_discoveries = 0
    target_new = 100
    
    for bus in raw_businesses:
        if new_discoveries >= target_new:
            break
            
        name = bus.get("tradename")
        address = bus.get("address")
        
        # Check Cache
        if name.strip().upper() in processed_cache:
            continue
            
        print(f"Resolving: {name}...")
        
        # 3. Resolve Name -> Domain
        domain = resolve_domain(name)
        
        # 4. Structure
        result = {
            "name": name,
            "address": address,
            "domain": domain,
            "source": "Lethbridge Open Data"
        }
        
        # 5. Save locally
        save_to_jsonl(result)
        new_discoveries += 1
        
        if domain:
            print(f"  ✅ Found: {domain}")
        else:
            print(f"  ❌ No domain found.")

    print(f"\nPipeline complete. Added {new_discoveries} new companies to discovery_log.jsonl")

if __name__ == "__main__":
    main()