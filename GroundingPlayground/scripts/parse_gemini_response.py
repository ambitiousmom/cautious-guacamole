"""
Parse Gemini grounding responses and extract structured data.

Usage:
    1. Copy Gemini DevTools response to a .txt file
    2. Run: python parse_gemini_response.py <response_file.txt>
    3. See extracted attributes in console and output TSV
"""

import sys
import re
import json
from pathlib import Path
from datetime import datetime

def extract_between_patterns(text, start_pattern, end_pattern):
    """Extract text between two patterns."""
    match = re.search(f'{start_pattern}(.*?){end_pattern}', text, re.DOTALL)
    return match.group(1) if match else None

def find_all_quoted_strings(text):
    """Find all quoted strings in the response."""
    return re.findall(r'"([^"]*)"', text)

def parse_gemini_response(file_path):
    """Parse a Gemini response file and extract grounding data."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        raw = f.read()
    
    results = {
        'file': str(file_path),
        'parsed_at': datetime.now().isoformat(),
        'structured': {},
        'semi_structured': {},
        'unstructured': {},
        'amenities': {},
        'raw_extracts': []
    }
    
    # --- STRUCTURED ATTRIBUTES ---
    
    # Place ID
    place_id_match = re.search(r'places/(ChIJ[a-zA-Z0-9_-]+)', raw)
    if place_id_match:
        results['structured']['place_id'] = place_id_match.group(1)
    
    # Phone
    phone_match = re.search(r'\(\d{3}\) \d{3}-\d{4}', raw)
    if phone_match:
        results['structured']['phone'] = phone_match.group(0)
    
    # Address
    address_match = re.search(r'"(\d+ [^"]+(?:St|Ave|Blvd|Dr|Rd|Way)[^"]*(?:WA|CA|OR|TX) \d{5})"', raw)
    if address_match:
        results['structured']['address'] = address_match.group(1)
    
    # Coordinates
    coord_match = re.search(r'\[(\d+\.\d+),(-?\d+\.\d+)\]', raw)
    if coord_match:
        results['structured']['lat'] = float(coord_match.group(1))
        results['structured']['lng'] = float(coord_match.group(2))
    
    # Rating
    rating_match = re.search(r',(\d\.\d),"https://maps\.google\.com', raw)
    if rating_match:
        results['structured']['rating'] = float(rating_match.group(1))
    
    # Website
    website_match = re.search(r'"(https?://(?!maps\.google|www\.google|lh3\.google|fonts\.gstatic)[^"]+)"', raw)
    if website_match:
        results['structured']['website'] = website_match.group(1)
    
    # Hours - look for day patterns
    hours_pattern = r'"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday): (\d{1,2}:\d{2} [AP]M) – (\d{1,2}:\d{2} [AP]M)"'
    hours_matches = re.findall(hours_pattern, raw)
    if hours_matches:
        results['structured']['hours'] = {day: f"{open_t} - {close_t}" for day, open_t, close_t in hours_matches}
    
    # Price range
    price_match = re.search(r'\["USD",(\d+)\],\["USD",(\d+)\]', raw)
    if price_match:
        results['structured']['price_range'] = f"${price_match.group(1)}-${price_match.group(2)}"
    
    # Category
    category_match = re.search(r'\["(Restaurant|Cafe|Hotel|Store|Hospital|Mall|Bar|Bakery)","en"\]', raw)
    if category_match:
        results['structured']['category'] = category_match.group(1)
    
    # Description/tagline
    desc_match = re.search(r'"([^"]{30,150})","en"\],\[\[', raw)
    if desc_match:
        results['structured']['description'] = desc_match.group(1)
    
    # --- AMENITIES (Boolean flags) ---
    
    # Pattern: [\"Outdoor seating\",true] (escaped JSON)
    amenity_pattern = r'\[\\"([^\\]+)\\",\s*(true|false)\]'
    amenity_matches = re.findall(amenity_pattern, raw)
    for amenity_name, value in amenity_matches:
        if len(amenity_name) < 50:
            results['amenities'][amenity_name] = value == 'true'
    
    # Also try unescaped pattern
    amenity_pattern2 = r'\["([^"]{3,40})",(true|false)\]'
    amenity_matches2 = re.findall(amenity_pattern2, raw)
    for amenity_name, value in amenity_matches2:
        # Filter to likely amenity names
        if amenity_name not in results['amenities']:
            results['amenities'][amenity_name] = value == 'true'
    
    # --- SEMI-STRUCTURED (Insights) ---
    
    # Tips
    tips_match = re.search(r'\["Tips"\],null,"([^"]+)"', raw)
    if tips_match:
        results['semi_structured']['tips'] = tips_match.group(1).replace('\\n', '\n')
    
    # Most Ordered
    ordered_match = re.search(r'\["Most Ordered"\],null,"([^"]+)"', raw)
    if ordered_match:
        results['semi_structured']['most_ordered'] = ordered_match.group(1).replace('\\n', '\n')
    
    # Occasion
    occasion_match = re.search(r'\["Occasion"\],null,"([^"]+)"', raw)
    if occasion_match:
        results['semi_structured']['occasion'] = occasion_match.group(1).replace('\\n', '\n')
    
    # AI Review Summary
    summary_match = re.search(r'"(People say [^"]+)"', raw)
    if summary_match:
        results['semi_structured']['review_summary'] = summary_match.group(1)
    
    # --- UNSTRUCTURED ---
    
    # Count reviews
    review_count = len(re.findall(r'/reviews/[A-Za-z0-9_-]+', raw))
    results['unstructured']['review_count'] = review_count
    
    # Count photos
    photo_count = len(re.findall(r'/photos/[A-Za-z0-9_-]+', raw))
    results['unstructured']['photo_count'] = photo_count
    
    # Extract review texts
    review_texts = re.findall(r'\["([^"]{100,}?)","en"\],null,null,\["', raw)
    results['unstructured']['reviews'] = review_texts[:5]  # First 5
    
    return results


def print_results(results):
    """Pretty print the parsed results."""
    
    print("\n" + "="*60)
    print("GEMINI GROUNDING ANALYSIS")
    print("="*60)
    
    print("\n📊 STRUCTURED ATTRIBUTES:")
    print("-"*40)
    for key, value in results['structured'].items():
        if key == 'hours':
            print(f"  {key}:")
            for day, time in value.items():
                print(f"    {day}: {time}")
        else:
            print(f"  {key}: {value}")
    
    print("\n✅ AMENITIES (Boolean Flags):")
    print("-"*40)
    if results['amenities']:
        for amenity, value in results['amenities'].items():
            icon = "✓" if value else "✗"
            print(f"  [{icon}] {amenity}")
    else:
        print("  (none found)")
    
    print("\n💡 SEMI-STRUCTURED (Insights):")
    print("-"*40)
    for key, value in results['semi_structured'].items():
        print(f"  {key}:")
        for line in str(value).split('\n'):
            print(f"    {line}")
    
    print("\n📝 UNSTRUCTURED DATA:")
    print("-"*40)
    print(f"  Reviews found: {results['unstructured'].get('review_count', 0)}")
    print(f"  Photos found: {results['unstructured'].get('photo_count', 0)}")
    
    if results['unstructured'].get('reviews'):
        print("\n  Sample review excerpts:")
        for i, review in enumerate(results['unstructured']['reviews'][:3], 1):
            excerpt = review[:150] + "..." if len(review) > 150 else review
            print(f"    [{i}] {excerpt}")
    
    print("\n" + "="*60)


def save_to_tsv(results, output_path):
    """Save results to TSV for aggregation."""
    
    # Flatten for TSV
    row = {
        'parsed_at': results['parsed_at'],
        'place_id': results['structured'].get('place_id', ''),
        'phone': results['structured'].get('phone', ''),
        'address': results['structured'].get('address', ''),
        'rating': results['structured'].get('rating', ''),
        'price_range': results['structured'].get('price_range', ''),
        'category': results['structured'].get('category', ''),
        'website': results['structured'].get('website', ''),
        'description': results['structured'].get('description', ''),
        'has_hours': bool(results['structured'].get('hours')),
        'amenities_found': '|'.join(results['amenities'].keys()),
        'tips': results['semi_structured'].get('tips', '').replace('\n', ' | '),
        'most_ordered': results['semi_structured'].get('most_ordered', '').replace('\n', ' | '),
        'occasion': results['semi_structured'].get('occasion', '').replace('\n', ' | '),
        'review_summary': results['semi_structured'].get('review_summary', ''),
        'review_count': results['unstructured'].get('review_count', 0),
        'photo_count': results['unstructured'].get('photo_count', 0),
    }
    
    # Write
    file_exists = output_path.exists()
    with open(output_path, 'a', encoding='utf-8') as f:
        if not file_exists:
            f.write('\t'.join(row.keys()) + '\n')
        f.write('\t'.join(str(v) for v in row.values()) + '\n')
    
    print(f"\n📁 Results appended to: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_gemini_response.py <response_file.txt>")
        print("\nOr run with the sample file:")
        print("  python parse_gemini_response.py ../geminiSampleReponse.txt")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    results = parse_gemini_response(file_path)
    print_results(results)
    
    # Save to TSV
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    save_to_tsv(results, output_dir / "gemini_grounding_analysis.tsv")
