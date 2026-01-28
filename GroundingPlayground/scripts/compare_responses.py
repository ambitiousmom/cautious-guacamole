"""
Compare responses across different responders (Bing, Gemini, Perplexity, etc.)

Usage:
    python compare_responses.py
    python compare_responses.py --queries my_queries.tsv --responses my_responses.tsv
"""

import argparse
import pandas as pd
from pathlib import Path
from utils import (
    load_queries, load_responses, load_rubric, load_entities,
    score_response, determine_winner, categorize_gap, save_tsv,
    PROJECT_ROOT
)


def compare_responses(
    queries_file: str = "sample_competitive_queries.tsv",
    responses_file: str = "sample_responses.tsv",
    rubric_file: str = "competitive_rubric.tsv"
) -> pd.DataFrame:
    """
    Compare responses and generate comparison report.
    
    Returns:
        DataFrame with comparison results
    """
    # Load data
    queries = load_queries(queries_file)
    responses = load_responses(responses_file)
    rubric = load_rubric(rubric_file)
    
    print(f"Loaded {len(queries)} queries, {len(responses)} responses")
    
    # Score each response
    responses['score'] = responses.apply(lambda row: score_response(row, rubric), axis=1)
    
    # Merge with queries
    merged = responses.merge(queries, on='query_id', how='left')
    
    # Determine winner per query
    winners = []
    for query_id, group in merged.groupby('query_id'):
        winner = determine_winner(group)
        max_score = group['score'].max()
        
        # Get Bing's score
        bing_rows = group[group['responder'] == 'bing_copilot']
        bing_score = bing_rows['score'].iloc[0] if len(bing_rows) > 0 else None
        bing_gap = max_score - bing_score if bing_score is not None else None
        
        # Categorize gap
        bing_row = bing_rows.iloc[0] if len(bing_rows) > 0 else None
        winner_row = group[group['score'] == max_score].iloc[0]
        gap_reason = categorize_gap(bing_row, winner_row) if bing_row is not None else 'no_bing_response'
        
        winners.append({
            'query_id': query_id,
            'query_text': group['query_text'].iloc[0],
            'query_type': group.get('query_type', pd.Series(['unknown'])).iloc[0],
            'segment': group.get('segment', pd.Series(['unknown'])).iloc[0],
            'winner': winner,
            'winning_score': max_score,
            'bing_score': bing_score,
            'bing_gap': bing_gap,
            'gap_reason': gap_reason
        })
    
    results = pd.DataFrame(winners)
    
    # Print summary
    print("\n" + "="*60)
    print("COMPARISON SUMMARY")
    print("="*60)
    
    print("\n📊 Winner Distribution:")
    winner_counts = results['winner'].value_counts()
    for responder, count in winner_counts.items():
        pct = count / len(results) * 100
        print(f"  {responder}: {count} ({pct:.1f}%)")
    
    print("\n📉 Bing Gap Reasons (when Bing lost):")
    bing_losses = results[results['winner'] != 'bing_copilot']
    if len(bing_losses) > 0:
        gap_counts = bing_losses['gap_reason'].value_counts()
        for reason, count in gap_counts.items():
            print(f"  {reason}: {count}")
    
    print("\n📋 Results by Query Type:")
    for qtype, group in results.groupby('query_type'):
        bing_wins = (group['winner'] == 'bing_copilot').sum()
        total = len(group)
        print(f"  {qtype}: Bing wins {bing_wins}/{total} ({bing_wins/total*100:.0f}%)")
    
    return results, merged


def main():
    parser = argparse.ArgumentParser(description='Compare grounding responses')
    parser.add_argument('--queries', default='sample_competitive_queries.tsv',
                        help='Queries TSV filename (in data/queries/)')
    parser.add_argument('--responses', default='sample_responses.tsv',
                        help='Responses TSV filename (in data/responses/)')
    parser.add_argument('--rubric', default='competitive_rubric.tsv',
                        help='Rubric TSV filename (in data/rubrics/)')
    
    args = parser.parse_args()
    
    results, detailed = compare_responses(args.queries, args.responses, args.rubric)
    
    # Save results
    output_dir = PROJECT_ROOT / "output"
    output_dir.mkdir(exist_ok=True)
    
    save_tsv(results, output_dir / "comparison_summary.tsv")
    save_tsv(detailed, output_dir / "comparison_detailed.tsv")
    
    print(f"\n✅ Results saved to:")
    print(f"   {output_dir / 'comparison_summary.tsv'}")
    print(f"   {output_dir / 'comparison_detailed.tsv'}")


if __name__ == "__main__":
    main()
