"""
Archive and organize collected Gemini grounding responses.

Creates a structured archive with:
- Organized folders by method
- Metadata index
- Extracted summaries
- Zip package for sharing

Usage:
    python archive_responses.py
"""

import os
import sys
import json
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from parse_gemini_response import parse_gemini_response

PROJECT_ROOT = Path(__file__).parent.parent
EXPERIMENTS_DIR = PROJECT_ROOT / "experiments"
RESPONSES_DIR = EXPERIMENTS_DIR / "responses"
ARCHIVE_DIR = PROJECT_ROOT / "archive"
OUTPUT_DIR = PROJECT_ROOT / "output"


def load_query_matrix():
    """Load query metadata."""
    queries = {}
    matrix_file = EXPERIMENTS_DIR / "query_matrix.tsv"
    
    if not matrix_file.exists():
        return queries
    
    with open(matrix_file, 'r', encoding='utf-8') as f:
        headers = f.readline().strip().split('\t')
        for line in f:
            values = line.strip().split('\t')
            row = dict(zip(headers, values))
            queries[row['query_id']] = row
    
    return queries


def create_archive():
    """Create organized archive of all responses."""
    
    print("="*60)
    print("  GEMINI GROUNDING RESPONSE ARCHIVE")
    print("="*60)
    
    # Create archive structure
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"gemini_grounding_archive_{timestamp}"
    archive_path = ARCHIVE_DIR / archive_name
    
    # Method folders
    method_dirs = {
        'method1_variations': archive_path / "01_Query_Variations",
        'method2_entities': archive_path / "02_Entity_Comparison", 
        'method3_attributes': archive_path / "03_Attribute_Probing",
        'other': archive_path / "04_Other"
    }
    
    for d in method_dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    
    # Load query metadata
    query_matrix = load_query_matrix()
    
    # Collect all response files
    response_files = list(RESPONSES_DIR.glob("*.txt")) if RESPONSES_DIR.exists() else []
    
    # Also check for responses on Desktop
    desktop = Path(os.path.expanduser("~")) / "OneDrive - Microsoft" / "Desktop"
    desktop_responses = list(desktop.glob("*Response*.txt")) + list(desktop.glob("*response*.txt"))
    
    all_responses = response_files + desktop_responses
    
    print(f"\nFound {len(all_responses)} response files")
    
    # Master index
    index = {
        'created': datetime.now().isoformat(),
        'total_responses': len(all_responses),
        'methods': {},
        'responses': []
    }
    
    # Process each response
    for resp_file in all_responses:
        print(f"\n  Processing: {resp_file.name}")
        
        # Determine query ID and method
        query_id = resp_file.stem.replace("_response", "").replace("Response", "")
        
        # Try to match to query matrix
        query_info = query_matrix.get(query_id, {})
        method = query_info.get('method', 'other')
        
        # If can't determine from ID, check filename
        if method == 'other':
            if 'M1_' in query_id or 'gemini' in resp_file.name.lower():
                method = 'method1_variations'
        
        # Parse the response
        try:
            parsed = parse_gemini_response(resp_file)
            
            # Create summary
            summary = {
                'query_id': query_id,
                'original_file': resp_file.name,
                'method': method,
                'query_text': query_info.get('query_text', '(unknown)'),
                'entity': query_info.get('entity', '(unknown)'),
                'parsed': {
                    'place_id': parsed['structured'].get('place_id'),
                    'phone': parsed['structured'].get('phone'),
                    'rating': parsed['structured'].get('rating'),
                    'price_range': parsed['structured'].get('price_range'),
                    'amenities': list(parsed['amenities'].keys()),
                    'has_review_summary': bool(parsed['semi_structured'].get('review_summary')),
                    'has_tips': bool(parsed['semi_structured'].get('tips')),
                    'has_most_ordered': bool(parsed['semi_structured'].get('most_ordered')),
                    'review_count': parsed['unstructured'].get('review_count', 0),
                    'photo_count': parsed['unstructured'].get('photo_count', 0)
                }
            }
            
        except Exception as e:
            print(f"    ⚠ Parse error: {e}")
            summary = {
                'query_id': query_id,
                'original_file': resp_file.name,
                'method': method,
                'error': str(e)
            }
        
        index['responses'].append(summary)
        
        # Copy to appropriate folder
        dest_dir = method_dirs.get(method, method_dirs['other'])
        dest_file = dest_dir / f"{query_id}.txt"
        shutil.copy(resp_file, dest_file)
        
        # Write individual summary
        summary_file = dest_dir / f"{query_id}_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        print(f"    → {dest_dir.name}/{query_id}.txt")
    
    # Count by method
    for method in method_dirs.keys():
        count = len([r for r in index['responses'] if r.get('method') == method])
        index['methods'][method] = count
    
    # Write master index
    index_file = archive_path / "INDEX.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)
    
    # Create README
    readme_content = f"""# Gemini Grounding Response Archive

Created: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Contents

| Folder | Description | Count |
|--------|-------------|-------|
| 01_Query_Variations | Same entity, different query intents | {index['methods'].get('method1_variations', 0)} |
| 02_Entity_Comparison | Same query, different entity types | {index['methods'].get('method2_entities', 0)} |
| 03_Attribute_Probing | Probing specific Google Maps attributes | {index['methods'].get('method3_attributes', 0)} |
| 04_Other | Uncategorized responses | {index['methods'].get('other', 0)} |

## Total Responses: {index['total_responses']}

## Files

- `INDEX.json` - Master index with all response metadata
- Each folder contains:
  - `<query_id>.txt` - Raw DevTools response
  - `<query_id>_summary.json` - Parsed attributes

## Amenities Discovered

"""
    
    # Collect all amenities
    all_amenities = set()
    for resp in index['responses']:
        if 'parsed' in resp:
            all_amenities.update(resp['parsed'].get('amenities', []))
    
    for amenity in sorted(all_amenities):
        readme_content += f"- {amenity}\n"
    
    readme_file = archive_path / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Create ZIP
    zip_path = ARCHIVE_DIR / f"{archive_name}.zip"
    print(f"\n  Creating ZIP archive...")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in archive_path.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(archive_path)
                zf.write(file_path, arcname)
    
    print(f"\n{'='*60}")
    print(f"  ARCHIVE COMPLETE")
    print(f"{'='*60}")
    print(f"\n  📁 Folder: {archive_path}")
    print(f"  📦 ZIP:    {zip_path}")
    print(f"  📊 Total:  {index['total_responses']} responses")
    
    return zip_path


def list_archive_contents(zip_path):
    """List contents of an archive."""
    
    print(f"\n  Contents of {zip_path.name}:")
    print("-"*50)
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for info in zf.infolist():
            size = info.file_size
            size_str = f"{size:,} bytes" if size < 1024 else f"{size/1024:.1f} KB"
            print(f"  {info.filename:<40} {size_str:>12}")


if __name__ == "__main__":
    # Create the archive
    zip_path = create_archive()
    
    # Show contents
    if zip_path.exists():
        list_archive_contents(zip_path)
        
        print(f"\n  To extract: Expand-Archive -Path \"{zip_path}\" -DestinationPath \"<folder>\"")
