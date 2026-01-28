"""
Interactive workflow for Gemini grounding analysis.

Guides you through the 3 methods and collects responses.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))
from parse_gemini_response import parse_gemini_response, print_results, save_to_tsv

EXPERIMENTS_DIR = Path(__file__).parent.parent / "experiments"
RESPONSES_DIR = EXPERIMENTS_DIR / "responses"
OUTPUT_DIR = Path(__file__).parent.parent / "output"

# Create directories
RESPONSES_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_query_matrix():
    """Load the query matrix from TSV."""
    queries = []
    matrix_file = EXPERIMENTS_DIR / "query_matrix.tsv"
    
    with open(matrix_file, 'r', encoding='utf-8') as f:
        headers = f.readline().strip().split('\t')
        for line in f:
            values = line.strip().split('\t')
            queries.append(dict(zip(headers, values)))
    
    return queries


def show_methods():
    """Show available methods."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║           GEMINI GROUNDING ANALYSIS EXPERIMENT               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Method 1: QUERY VARIATIONS                                  ║
║    Same entity (Din Tai Fung), different query intents       ║
║    Tests which attributes are retrieved per intent type      ║
║                                                              ║
║  Method 2: ENTITY COMPARISON                                 ║
║    Same query (outdoor seating), different entities          ║
║    Tests data richness across entity types                   ║
║                                                              ║
║  Method 3: ATTRIBUTE PROBING                                 ║
║    Systematically probe known Google Maps attributes         ║
║    Tests which attributes exist in Gemini's knowledge        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


def run_interactive():
    """Run interactive experiment session."""
    
    show_methods()
    queries = load_query_matrix()
    
    # Group by method
    method1 = [q for q in queries if q['method'] == 'method1_variations']
    method2 = [q for q in queries if q['method'] == 'method2_entities']
    method3 = [q for q in queries if q['method'] == 'method3_attributes']
    
    print(f"Loaded {len(queries)} queries:")
    print(f"  Method 1 (Query Variations): {len(method1)} queries")
    print(f"  Method 2 (Entity Comparison): {len(method2)} queries")
    print(f"  Method 3 (Attribute Probing): {len(method3)} queries")
    
    while True:
        print("\n" + "="*60)
        print("OPTIONS:")
        print("  1 - Run Method 1 queries")
        print("  2 - Run Method 2 queries")
        print("  3 - Run Method 3 queries")
        print("  a - Analyze collected responses")
        print("  s - Show summary statistics")
        print("  q - Quit")
        print("="*60)
        
        choice = input("\nEnter choice: ").strip().lower()
        
        if choice == '1':
            run_method_queries(method1, "Method 1: Query Variations")
        elif choice == '2':
            run_method_queries(method2, "Method 2: Entity Comparison")
        elif choice == '3':
            run_method_queries(method3, "Method 3: Attribute Probing")
        elif choice == 'a':
            analyze_responses()
        elif choice == 's':
            show_summary()
        elif choice == 'q':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


def run_method_queries(queries, method_name):
    """Guide through queries for a method."""
    
    print(f"\n{'='*60}")
    print(f"  {method_name}")
    print(f"{'='*60}")
    
    for i, query in enumerate(queries, 1):
        query_id = query['query_id']
        query_text = query['query_text']
        entity = query['entity']
        
        # Check if already collected
        response_file = RESPONSES_DIR / f"{query_id}.txt"
        status = "✓ collected" if response_file.exists() else "○ pending"
        
        print(f"\n[{i}/{len(queries)}] {status}")
        print(f"  ID: {query_id}")
        print(f"  Entity: {entity}")
        print(f"  Query: {query_text}")
        
        if response_file.exists():
            action = input("  (s)kip, (r)e-collect, (a)nalyze? [s]: ").strip().lower()
            if action == 'a':
                analyze_single_response(response_file)
                continue
            elif action != 'r':
                continue
        else:
            action = input("  (c)ollect, (s)kip? [c]: ").strip().lower()
            if action == 's':
                continue
        
        # Collection instructions
        print(f"\n  📋 INSTRUCTIONS:")
        print(f"  1. Open Gemini (gemini.google.com)")
        print(f"  2. Open DevTools (F12) → Network tab")
        print(f"  3. Clear the log, then ask:")
        print(f"     \"{query_text}\"")
        print(f"  4. Find the large response in Network tab")
        print(f"  5. Copy the Response content")
        print(f"  6. Save to: {response_file}")
        
        input("\n  Press Enter when saved (or 'x' to skip): ")
        
        if response_file.exists():
            print(f"  ✓ Response saved!")
            analyze_single_response(response_file)


def analyze_single_response(response_file):
    """Analyze a single response file."""
    try:
        results = parse_gemini_response(response_file)
        print_results(results)
        
        # Save to consolidated TSV
        output_file = OUTPUT_DIR / "gemini_grounding_analysis.tsv"
        save_to_tsv(results, output_file)
        
    except Exception as e:
        print(f"  ⚠ Error analyzing: {e}")


def analyze_responses():
    """Analyze all collected responses."""
    
    response_files = list(RESPONSES_DIR.glob("*.txt"))
    print(f"\nFound {len(response_files)} response files")
    
    if not response_files:
        print("No responses collected yet.")
        return
    
    for rf in response_files:
        print(f"\n--- {rf.name} ---")
        analyze_single_response(rf)


def show_summary():
    """Show summary of collected data."""
    
    output_file = OUTPUT_DIR / "gemini_grounding_analysis.tsv"
    
    if not output_file.exists():
        print("No analysis data yet. Run some queries first.")
        return
    
    with open(output_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"\n{'='*60}")
    print(f"  SUMMARY STATISTICS")
    print(f"{'='*60}")
    print(f"  Total responses analyzed: {len(lines) - 1}")  # minus header
    
    # Count amenities found
    all_amenities = set()
    for line in lines[1:]:
        parts = line.split('\t')
        if len(parts) > 10:
            amenities = parts[10].split('|')
            all_amenities.update(a for a in amenities if a)
    
    print(f"\n  Unique amenities discovered:")
    for a in sorted(all_amenities):
        print(f"    - {a}")


if __name__ == "__main__":
    run_interactive()
