"""
Helper script for manually collecting competitive responses.

This script:
1. Loads queries that don't have responses yet
2. Opens each query for you to test
3. Prompts you to enter responses from each competitor
4. Saves to responses TSV

Usage:
    python collect_responses.py
    python collect_responses.py --queries my_queries.tsv --output my_responses.tsv
"""

import argparse
import pandas as pd
from pathlib import Path
from datetime import datetime
from utils import load_queries, load_responses, save_tsv, PROJECT_ROOT


RESPONDERS = ['bing_copilot', 'gemini', 'perplexity']

ANSWER_OPTIONS = {
    'answered': ['yes', 'partial', 'no'],
    'confidence': ['high', 'medium', 'low'],
}


def collect_responses(queries_file: str, output_file: str):
    """Interactive response collection."""
    
    queries = load_queries(queries_file)
    output_path = PROJECT_ROOT / "data" / "responses" / output_file
    
    # Load existing responses if file exists
    if output_path.exists():
        existing = load_responses(output_file)
        collected_ids = set(existing['query_id'].unique())
        print(f"Found {len(collected_ids)} queries already collected.")
    else:
        existing = pd.DataFrame()
        collected_ids = set()
    
    # Filter to uncollected queries
    remaining = queries[~queries['query_id'].isin(collected_ids)]
    print(f"{len(remaining)} queries remaining to collect.\n")
    
    if len(remaining) == 0:
        print("All queries have responses collected!")
        return
    
    new_responses = []
    
    for idx, query in remaining.iterrows():
        print("=" * 60)
        print(f"Query {query['query_id']}: {query['query_text']}")
        if 'entity_name' in query and pd.notna(query['entity_name']):
            print(f"Entity: {query['entity_name']}")
        if 'location' in query and pd.notna(query['location']):
            print(f"Location: {query['location']}")
        print("=" * 60)
        
        for responder in RESPONDERS:
            print(f"\n--- {responder.upper()} ---")
            print("Test this query on the service, then enter the response.")
            
            response_text = input("Response text (or 'skip' to skip): ").strip()
            if response_text.lower() == 'skip':
                continue
            if response_text.lower() == 'quit':
                print("Saving and quitting...")
                break
            
            answered = input("Answered? (yes/partial/no): ").strip().lower()
            if answered not in ANSWER_OPTIONS['answered']:
                answered = 'partial'
            
            confidence = input("Confidence? (high/medium/low): ").strip().lower()
            if confidence not in ANSWER_OPTIONS['confidence']:
                confidence = 'medium'
            
            source_cited = input("Source cited? (e.g., yelp, google, none): ").strip().lower()
            if not source_cited:
                source_cited = 'none'
            
            richness = input("Richness score (1-5): ").strip()
            try:
                richness = int(richness)
                richness = max(1, min(5, richness))
            except:
                richness = 3
            
            new_responses.append({
                'query_id': query['query_id'],
                'responder': responder,
                'response_text': response_text,
                'answered': answered,
                'confidence': confidence,
                'source_cited': source_cited,
                'richness_score': richness,
                'collected_date': datetime.now().strftime('%Y-%m-%d')
            })
        
        # Check if user wants to continue
        cont = input("\nContinue to next query? (y/n): ").strip().lower()
        if cont != 'y':
            break
    
    # Save new responses
    if new_responses:
        new_df = pd.DataFrame(new_responses)
        combined = pd.concat([existing, new_df], ignore_index=True)
        save_tsv(combined, output_path)
        print(f"\n✅ Saved {len(new_responses)} new responses to {output_path}")
    else:
        print("\nNo new responses collected.")


def main():
    parser = argparse.ArgumentParser(description='Collect competitive responses')
    parser.add_argument('--queries', default='sample_competitive_queries.tsv',
                        help='Queries TSV filename')
    parser.add_argument('--output', default='collected_responses.tsv',
                        help='Output TSV filename')
    
    args = parser.parse_args()
    collect_responses(args.queries, args.output)


if __name__ == "__main__":
    main()
