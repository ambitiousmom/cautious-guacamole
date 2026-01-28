"""
Generate HTML dashboard report from comparison results.

Usage:
    python generate_report.py
"""

import pandas as pd
from pathlib import Path
from utils import PROJECT_ROOT, load_tsv
from datetime import datetime


def generate_html_report():
    """Generate an interactive HTML report from comparison results."""
    
    output_dir = PROJECT_ROOT / "output"
    summary_file = output_dir / "comparison_summary.tsv"
    detailed_file = output_dir / "comparison_detailed.tsv"
    
    if not summary_file.exists():
        print("❌ No comparison results found. Run compare_responses.py first.")
        return
    
    summary = load_tsv(summary_file)
    detailed = load_tsv(detailed_file)
    
    # Calculate stats
    total_queries = len(summary)
    bing_wins = (summary['winner'] == 'bing_copilot').sum()
    bing_win_pct = bing_wins / total_queries * 100 if total_queries > 0 else 0
    
    # Winner distribution
    winner_dist = summary['winner'].value_counts().to_dict()
    
    # Gap reasons
    losses = summary[summary['winner'] != 'bing_copilot']
    gap_reasons = losses['gap_reason'].value_counts().to_dict() if len(losses) > 0 else {}
    
    # By query type
    by_type = summary.groupby('query_type').apply(
        lambda g: (g['winner'] == 'bing_copilot').sum() / len(g) * 100
    ).to_dict()
    
    # By segment
    by_segment = summary.groupby('segment').apply(
        lambda g: (g['winner'] == 'bing_copilot').sum() / len(g) * 100
    ).to_dict()
    
    # Deep dive: What competitors have that Bing doesn't
    deep_dive_rows = []
    for query_id in summary['query_id'].unique():
        query_responses = detailed[detailed['query_id'] == query_id]
        query_info = summary[summary['query_id'] == query_id].iloc[0]
        
        bing_resp = query_responses[query_responses['responder'] == 'bing_copilot']
        other_resp = query_responses[query_responses['responder'] != 'bing_copilot']
        
        if len(bing_resp) == 0 or len(other_resp) == 0:
            continue
            
        bing_row = bing_resp.iloc[0]
        
        # Find best competitor
        best_other = other_resp.loc[other_resp['score'].idxmax()] if 'score' in other_resp.columns else other_resp.iloc[0]
        
        # Compare attributes
        bing_answered = bing_row.get('answered', 'no')
        comp_answered = best_other.get('answered', 'no')
        bing_source = bing_row.get('source_cited', 'none')
        comp_source = best_other.get('source_cited', 'none')
        bing_richness = bing_row.get('richness_score', 0)
        comp_richness = best_other.get('richness_score', 0)
        
        advantages = []
        if comp_answered in ['yes', 'partial'] and bing_answered == 'no':
            advantages.append('✅ Could answer the question')
        if str(comp_source) not in ['none', 'nan', ''] and str(bing_source) in ['none', 'nan', '']:
            advantages.append(f'📚 Cited source: {comp_source}')
        if pd.notna(comp_richness) and pd.notna(bing_richness) and float(comp_richness) > float(bing_richness):
            advantages.append(f'📝 Richer response ({int(comp_richness)} vs {int(bing_richness)})')
        
        if advantages or query_info['winner'] != 'bing_copilot':
            deep_dive_rows.append({
                'query_id': query_id,
                'query_text': query_info['query_text'],
                'query_type': query_info.get('query_type', 'N/A'),
                'winner': query_info['winner'],
                'bing_response': str(bing_row.get('response_text', ''))[:100] + '...' if len(str(bing_row.get('response_text', ''))) > 100 else str(bing_row.get('response_text', '')),
                'winner_response': str(best_other.get('response_text', ''))[:100] + '...' if len(str(best_other.get('response_text', ''))) > 100 else str(best_other.get('response_text', '')),
                'winner_source': comp_source,
                'advantages': advantages,
                'bing_score': bing_row.get('score', 0),
                'winner_score': best_other.get('score', 0)
            })
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grounding Playground Report</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0; padding: 20px;
            background: #f5f5f5;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #0078d4; }}
        .card {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .card h2 {{ margin-top: 0; color: #333; }}
        .metric {{
            display: inline-block;
            padding: 15px 25px;
            margin: 10px;
            background: #f0f0f0;
            border-radius: 8px;
            text-align: center;
        }}
        .metric .value {{ font-size: 2em; font-weight: bold; color: #0078d4; }}
        .metric .label {{ color: #666; font-size: 0.9em; }}
        .bar {{
            height: 24px;
            background: #e0e0e0;
            border-radius: 4px;
            margin: 8px 0;
            overflow: hidden;
        }}
        .bar-fill {{
            height: 100%;
            background: #0078d4;
            text-align: right;
            padding-right: 8px;
            color: white;
            font-size: 0.8em;
            line-height: 24px;
        }}
        .bar-fill.gemini {{ background: #4285f4; }}
        .bar-fill.perplexity {{ background: #20b2aa; }}
        .bar-fill.bing {{ background: #0078d4; }}
        .bar-fill.tie {{ background: #888; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{ background: #f5f5f5; }}
        .win {{ color: #107c10; font-weight: bold; }}
        .lose {{ color: #d83b01; }}
        .partial {{ color: #797673; }}
        .timestamp {{ color: #888; font-size: 0.8em; }}
        
        /* Deep Dive Styles */
        .deep-dive .subtitle {{ color: #666; margin-bottom: 20px; }}
        .comparison-card {{
            border: 1px solid #ddd;
            border-radius: 8px;
            margin: 20px 0;
            overflow: hidden;
        }}
        .comparison-header {{
            background: #f8f8f8;
            padding: 15px;
            border-bottom: 1px solid #ddd;
        }}
        .query-type-badge {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.75em;
            margin-right: 10px;
            background: #e0e0e0;
        }}
        .query-type-badge.amenity {{ background: #e3f2fd; color: #1565c0; }}
        .query-type-badge.vibe {{ background: #fce4ec; color: #c2185b; }}
        .query-type-badge.factual {{ background: #e8f5e9; color: #2e7d32; }}
        .query-type-badge.reviews {{ background: #fff3e0; color: #e65100; }}
        .query-type-badge.comparison {{ background: #f3e5f5; color: #7b1fa2; }}
        .comparison-body {{
            display: flex;
            gap: 0;
        }}
        .response-column {{
            flex: 1;
            padding: 15px;
        }}
        .bing-column {{
            background: #fafafa;
            border-right: 1px solid #ddd;
        }}
        .winner-column {{
            background: #f0fff0;
        }}
        .column-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            padding-bottom: 10px;
            border-bottom: 1px solid #eee;
        }}
        .responder-name {{
            font-weight: bold;
        }}
        .score {{
            color: #666;
            font-size: 0.9em;
        }}
        .response-text {{
            font-size: 0.9em;
            line-height: 1.5;
            color: #333;
            font-style: italic;
        }}
        .source-badge {{
            margin-top: 10px;
            padding: 5px 10px;
            background: #e8f5e9;
            border-radius: 4px;
            font-size: 0.8em;
            display: inline-block;
        }}
        .advantages {{
            background: #fff8e1;
            padding: 15px;
            border-top: 1px solid #ddd;
        }}
        .advantages ul {{
            margin: 5px 0 0 0;
            padding-left: 20px;
        }}
        .advantages li {{
            margin: 5px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Grounding Playground Report</h1>
        <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        
        <div class="card">
            <h2>📊 Overview</h2>
            <div class="metric">
                <div class="value">{total_queries}</div>
                <div class="label">Total Queries</div>
            </div>
            <div class="metric">
                <div class="value">{bing_wins}</div>
                <div class="label">Bing Wins</div>
            </div>
            <div class="metric">
                <div class="value">{bing_win_pct:.0f}%</div>
                <div class="label">Bing Win Rate</div>
            </div>
        </div>
        
        <div class="card">
            <h2>🏆 Winner Distribution</h2>
            {"".join(f'''
            <div>
                <strong>{responder}</strong>: {count} ({count/total_queries*100:.0f}%)
                <div class="bar">
                    <div class="bar-fill {responder.split('_')[0] if '_' in responder else responder}" 
                         style="width: {count/total_queries*100}%">
                        {count}
                    </div>
                </div>
            </div>
            ''' for responder, count in winner_dist.items())}
        </div>
        
        <div class="card">
            <h2>📉 Why Bing Lost</h2>
            <table>
                <tr><th>Gap Reason</th><th>Count</th><th>Description</th></tr>
                {"".join(f'''<tr>
                    <td>{reason}</td>
                    <td>{count}</td>
                    <td>{
                        'Bing could not answer, competitor did' if reason == 'missing_data'
                        else 'Both answered but competitor was richer' if reason == 'less_rich'
                        else 'Bing did not cite sources' if reason == 'no_source'
                        else reason
                    }</td>
                </tr>''' for reason, count in gap_reasons.items())}
            </table>
        </div>
        
        <div class="card">
            <h2>📋 Bing Win Rate by Query Type</h2>
            <table>
                <tr><th>Query Type</th><th>Bing Win %</th><th>Visual</th></tr>
                {"".join(f'''<tr>
                    <td>{qtype}</td>
                    <td class="{'win' if pct >= 50 else 'lose'}">{pct:.0f}%</td>
                    <td><div class="bar"><div class="bar-fill bing" style="width: {pct}%">{pct:.0f}%</div></div></td>
                </tr>''' for qtype, pct in by_type.items())}
            </table>
        </div>
        
        <div class="card">
            <h2>🏪 Bing Win Rate by Segment</h2>
            <table>
                <tr><th>Segment</th><th>Bing Win %</th><th>Visual</th></tr>
                {"".join(f'''<tr>
                    <td>{segment}</td>
                    <td class="{'win' if pct >= 50 else 'lose'}">{pct:.0f}%</td>
                    <td><div class="bar"><div class="bar-fill bing" style="width: {pct}%">{pct:.0f}%</div></div></td>
                </tr>''' for segment, pct in by_segment.items())}
            </table>
        </div>
        
        <div class="card">
            <h2>📝 Detailed Results</h2>
            <table>
                <tr>
                    <th>Query</th>
                    <th>Type</th>
                    <th>Winner</th>
                    <th>Bing Score</th>
                    <th>Gap Reason</th>
                </tr>
                {"".join(f'''<tr>
                    <td>{row['query_text'][:50]}{'...' if len(str(row['query_text'])) > 50 else ''}</td>
                    <td>{row.get('query_type', 'N/A')}</td>
                    <td class="{'win' if row['winner'] == 'bing_copilot' else 'lose'}">{row['winner']}</td>
                    <td>{f"{row['bing_score']:.2f}" if pd.notna(row['bing_score']) else 'N/A'}</td>
                    <td>{row['gap_reason']}</td>
                </tr>''' for _, row in summary.iterrows())}
            </table>
        </div>
        
        <div class="card deep-dive">
            <h2>🔬 Deep Dive: Why Competitors Win</h2>
            <p class="subtitle">Side-by-side comparison of Bing vs. winning competitor responses</p>
            
            {"".join(f'''
            <div class="comparison-card">
                <div class="comparison-header">
                    <span class="query-type-badge {item['query_type']}">{item['query_type']}</span>
                    <strong>{item['query_text']}</strong>
                </div>
                <div class="comparison-body">
                    <div class="response-column bing-column">
                        <div class="column-header">
                            <span class="responder-name">🔷 Bing Copilot</span>
                            <span class="score">Score: {f"{item['bing_score']:.2f}" if item['bing_score'] else 'N/A'}</span>
                        </div>
                        <div class="response-text">{item['bing_response']}</div>
                    </div>
                    <div class="response-column winner-column">
                        <div class="column-header">
                            <span class="responder-name">🏆 {item['winner']}</span>
                            <span class="score">Score: {f"{item['winner_score']:.2f}" if item['winner_score'] else 'N/A'}</span>
                        </div>
                        <div class="response-text">{item['winner_response']}</div>
                        <div class="source-badge">Source: {item['winner_source']}</div>
                    </div>
                </div>
                <div class="advantages">
                    <strong>Why competitor won:</strong>
                    <ul>
                        {"".join(f"<li>{adv}</li>" for adv in item['advantages']) if item['advantages'] else "<li>Higher overall quality score</li>"}
                    </ul>
                </div>
            </div>
            ''' for item in deep_dive_rows if item['winner'] != 'bing_copilot')}
        </div>
        
    </div>
</body>
</html>
"""
    
    # Save report
    report_path = output_dir / "grounding_report.html"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Report generated: {report_path}")
    print(f"   Open in browser to view.")


if __name__ == "__main__":
    generate_html_report()
