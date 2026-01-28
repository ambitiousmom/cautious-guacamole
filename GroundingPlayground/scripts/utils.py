"""
Utility functions for Grounding Playground
"""

import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict

# Project root
PROJECT_ROOT = Path(__file__).parent.parent


def load_tsv(filepath: str) -> pd.DataFrame:
    """Load a TSV file into a DataFrame."""
    return pd.read_csv(filepath, sep='\t')


def save_tsv(df: pd.DataFrame, filepath: str):
    """Save a DataFrame to TSV."""
    df.to_csv(filepath, sep='\t', index=False)


def load_queries(filename: str = "sample_competitive_queries.tsv") -> pd.DataFrame:
    """Load queries from data/queries/"""
    filepath = PROJECT_ROOT / "data" / "queries" / filename
    return load_tsv(filepath)


def load_responses(filename: str = "sample_responses.tsv") -> pd.DataFrame:
    """Load responses from data/responses/"""
    filepath = PROJECT_ROOT / "data" / "responses" / filename
    return load_tsv(filepath)


def load_entities(filename: str = "sample_entities.tsv") -> pd.DataFrame:
    """Load entities from data/entities/"""
    filepath = PROJECT_ROOT / "data" / "entities" / filename
    return load_tsv(filepath)


def load_rubric(filename: str = "competitive_rubric.tsv") -> pd.DataFrame:
    """Load rubric from data/rubrics/"""
    filepath = PROJECT_ROOT / "data" / "rubrics" / filename
    return load_tsv(filepath)


def score_response(row: pd.Series, rubric: pd.DataFrame) -> float:
    """
    Score a single response based on the rubric.
    
    Args:
        row: A response row with columns like 'answered', 'richness_score', etc.
        rubric: The scoring rubric DataFrame
    
    Returns:
        Weighted score (0-1)
    """
    total_score = 0.0
    total_weight = 0.0
    
    for _, metric in rubric.iterrows():
        metric_name = metric['metric_name']
        weight = metric['weight']
        
        if metric_name not in row.index:
            continue
            
        value = row[metric_name]
        
        # Handle different metric types
        if metric_name == 'answered':
            if value == 'yes':
                score = 1.0
            elif value == 'partial':
                score = 0.5
            else:
                score = 0.0
        elif metric_name == 'confidence':
            if value == 'high':
                score = 1.0
            elif value == 'medium':
                score = 0.5
            else:
                score = 0.0
        elif metric_name == 'source_cited':
            if pd.isna(value) or value == 'none':
                score = 0.0
            else:
                score = 0.75  # Any source cited
        elif metric_name == 'richness_score':
            score = float(value) / 5.0 if pd.notna(value) else 0.0
        else:
            score = 0.5  # Default for unknown metrics
        
        total_score += score * weight
        total_weight += weight
    
    return total_score / total_weight if total_weight > 0 else 0.0


def determine_winner(group: pd.DataFrame) -> str:
    """
    Determine winner for a query based on scores.
    
    Args:
        group: DataFrame grouped by query_id with 'score' column
    
    Returns:
        Name of winning responder
    """
    if len(group) == 0:
        return "none"
    
    max_score = group['score'].max()
    winners = group[group['score'] == max_score]['responder'].tolist()
    
    if len(winners) > 1:
        return "tie: " + ", ".join(winners)
    return winners[0]


def categorize_gap(bing_row: Optional[pd.Series], winner_row: pd.Series) -> str:
    """
    Categorize why Bing lost (if it did).
    
    Returns gap category:
    - 'missing_data': Bing couldn't answer, competitor did
    - 'less_rich': Both answered but competitor was richer
    - 'no_source': Bing didn't cite, competitor did
    - 'none': Bing won or tied
    """
    if bing_row is None:
        return 'no_bing_response'
    
    bing_answered = bing_row.get('answered', 'no')
    winner_answered = winner_row.get('answered', 'no')
    
    if bing_answered == 'no' and winner_answered in ['yes', 'partial']:
        return 'missing_data'
    
    bing_richness = bing_row.get('richness_score', 0)
    winner_richness = winner_row.get('richness_score', 0)
    
    if winner_richness > bing_richness:
        return 'less_rich'
    
    bing_source = bing_row.get('source_cited', 'none')
    winner_source = winner_row.get('source_cited', 'none')
    
    if (bing_source == 'none' or pd.isna(bing_source)) and winner_source not in ['none', None]:
        return 'no_source'
    
    return 'none'
