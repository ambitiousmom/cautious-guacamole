"""
Generate comprehensive HTML dashboard with tabs for all deliverables.

Tabs:
1. Competitive Analysis - Bing vs competitors
2. Current State - Systems overview (Deliverable 1)
3. Data Inventory - Sources and attributes (Deliverable 2)
4. Gap Analysis - Hypotheses and questions (Deliverable 3)

Usage:
    python generate_dashboard.py
"""

import pandas as pd
from pathlib import Path
from utils import PROJECT_ROOT, load_tsv
from datetime import datetime


def get_current_state_content():
    """Deliverable 1: Current State Summary"""
    return """
    <h2>📋 Current State Summary</h2>
    <p class="subtitle">Overview of Local Entity Data Enrichment & Grounding Systems</p>
    
    <div class="sub-card">
        <h3>1. Data Extraction Pipelines</h3>
        <table>
            <tr><th>System</th><th>Type</th><th>Status</th><th>Key Outputs</th><th>Maintenance</th></tr>
            <tr>
                <td><strong>Wrapstar</strong></td>
                <td>ML-based extraction</td>
                <td><span class="status-badge production">Production</span></td>
                <td>Descriptions, Reviews, Images, Amenities, ActionUrls, SocialProfiles</td>
                <td><span class="status-badge warning">High Cost</span></td>
            </tr>
            <tr>
                <td><strong>Schema.org</strong></td>
                <td>Structured markup parsing</td>
                <td><span class="status-badge production">Production</span></td>
                <td>Same + ServingArea, PaymentMethod, BusinessStartYear</td>
                <td><span class="status-badge success">Low Cost</span></td>
            </tr>
            <tr>
                <td><strong>Primary Website</strong></td>
                <td>Custom rules + basic ML</td>
                <td><span class="status-badge warning">Fragmented</span></td>
                <td>Hours, Contact info, Basic descriptions</td>
                <td><span class="status-badge warning">Medium</span></td>
            </tr>
        </table>
    </div>
    
    <div class="sub-card">
        <h3>2. AI-Based Enrichment (Experimental)</h3>
        <table>
            <tr><th>Project</th><th>Location</th><th>Outputs</th><th>Status</th></tr>
            <tr>
                <td><strong>LLM Feature Generation</strong></td>
                <td>dev/adric/AI_Enrichment/</td>
                <td>DescriptionAI, AmenitiesAI, HighlightsAI</td>
                <td><span class="status-badge experimental">POC</span></td>
            </tr>
            <tr>
                <td><strong>AI Enrichment Portal</strong></td>
                <td>dev/adric/ai-enrichment-portal-unified/</td>
                <td>Interactive prompt testing</td>
                <td><span class="status-badge experimental">POC</span></td>
            </tr>
            <tr>
                <td><strong>Address Propagation</strong></td>
                <td>dev/ekt/url-address-propagation-c1-2025/</td>
                <td>Address (graph-based propagation)</td>
                <td><span class="status-badge experimental">POC</span></td>
            </tr>
        </table>
    </div>
    
    <div class="sub-card">
        <h3>3. Grounding Governance</h3>
        <p>From <code>GovernanceConstants.cs</code>:</p>
        <table>
            <tr><th>Encumbrance Value</th><th>Meaning</th><th>Copilot Usage</th></tr>
            <tr>
                <td><span class="encumbrance factual">Factual</span></td>
                <td>Can be used freely</td>
                <td>✅ Full grounding</td>
            </tr>
            <tr>
                <td><span class="encumbrance attribution">RequiresAttribution</span></td>
                <td>Must cite the source</td>
                <td>⚠️ With citation</td>
            </tr>
            <tr>
                <td><span class="encumbrance quotation">RequiresQuotation</span></td>
                <td>Must quote exactly</td>
                <td>⚠️ With exact quote</td>
            </tr>
            <tr>
                <td><span class="encumbrance restricted">Restricted</span></td>
                <td>Cannot use for grounding</td>
                <td>❌ Blocked</td>
            </tr>
        </table>
        <div class="alert warning">
            <strong>⚠️ Key Finding:</strong> Default encumbrance is <code>Restricted</code>. 
            If flags aren't explicitly set, data is blocked from grounding.
        </div>
    </div>
    
    <div class="sub-card">
        <h3>4. Downstream Use Cases</h3>
        <div class="use-case-grid">
            <div class="use-case">
                <div class="use-case-icon">🔍</div>
                <div class="use-case-title">Relevance Enhancement</div>
                <div class="use-case-desc">Boost ranking with document + entity associations</div>
            </div>
            <div class="use-case">
                <div class="use-case-icon">🤖</div>
                <div class="use-case-title">Copilot Grounding</div>
                <div class="use-case-desc">Enrich AI answers with entity facts</div>
            </div>
            <div class="use-case">
                <div class="use-case-icon">✨</div>
                <div class="use-case-title">AI Enrichment</div>
                <div class="use-case-desc">Derive new attributes from source data</div>
            </div>
            <div class="use-case">
                <div class="use-case-icon">📱</div>
                <div class="use-case-title">UX Surfaces</div>
                <div class="use-case-desc">Display entity cards in search results</div>
            </div>
        </div>
    </div>
    """


def get_data_inventory_content():
    """Deliverable 2: Data & System Inventory"""
    return """
    <h2>📊 Data & System Inventory</h2>
    <p class="subtitle">Entity Enrichment Pipeline Mapping</p>
    
    <div class="sub-card">
        <h3>Data Flow Architecture</h3>
        <div class="architecture-diagram">
            <div class="arch-row sources">
                <div class="arch-box source">Web Crawl</div>
                <div class="arch-box source">Licensed Feeds</div>
                <div class="arch-box source">Primary Websites</div>
                <div class="arch-box source">AI Enrichment</div>
            </div>
            <div class="arch-arrow">↓</div>
            <div class="arch-row">
                <div class="arch-box extraction">Wrapstar</div>
                <div class="arch-box extraction">Schema.org</div>
            </div>
            <div class="arch-arrow">↓</div>
            <div class="arch-row">
                <div class="arch-box processing">URL-YPID Linking</div>
            </div>
            <div class="arch-arrow">↓</div>
            <div class="arch-row">
                <div class="arch-box processing">RAP (Rich Attribute Processing)</div>
            </div>
            <div class="arch-arrow">↓</div>
            <div class="arch-row">
                <div class="arch-box storage">UDS (Unified Data Store)</div>
            </div>
            <div class="arch-arrow">↓</div>
            <div class="arch-row consumers">
                <div class="arch-box consumer">Relevance</div>
                <div class="arch-box consumer">Copilot Grounding</div>
                <div class="arch-box consumer">UX Surfaces</div>
            </div>
        </div>
    </div>
    
    <div class="sub-card">
        <h3>Attribute Coverage by Source</h3>
        <table class="coverage-matrix">
            <tr>
                <th>Attribute</th>
                <th>Wrapstar</th>
                <th>Schema.org</th>
                <th>Licensed</th>
                <th>AI Enrichment</th>
            </tr>
            <tr><td>Name</td><td>❌</td><td>❌</td><td class="primary">✅ Primary</td><td>❌</td></tr>
            <tr><td>Address</td><td>❌</td><td>❌</td><td class="primary">✅ Primary</td><td>⚠️ POC</td></tr>
            <tr><td>Phone</td><td>❌</td><td>❌</td><td class="primary">✅ Primary</td><td>❌</td></tr>
            <tr><td>Hours</td><td>⚠️</td><td>⚠️</td><td class="primary">✅ Primary</td><td>❌</td></tr>
            <tr><td>Description</td><td>✅</td><td>✅</td><td>✅</td><td class="primary">✅ POC</td></tr>
            <tr><td>Reviews</td><td>❌</td><td>⚠️</td><td class="primary">✅ Primary</td><td>❌</td></tr>
            <tr><td>Images</td><td>✅</td><td>✅</td><td>✅</td><td>❌</td></tr>
            <tr><td>Amenities</td><td>✅</td><td>✅</td><td>⚠️</td><td class="primary">✅ POC</td></tr>
            <tr><td>Vibe/Atmosphere</td><td>❌</td><td>❌</td><td>❌</td><td>⚠️ Potential</td></tr>
        </table>
        <div class="legend">
            <span><span class="primary">✅ Primary</span> = Main source</span>
            <span>✅ = Available</span>
            <span>⚠️ = Limited/Partial</span>
            <span>❌ = Not available</span>
        </div>
    </div>
    
    <div class="sub-card">
        <h3>Provider → Encumbrance Mapping</h3>
        <table>
            <tr><th>Provider</th><th>Typical Encumbrance</th><th>Evidence</th></tr>
            <tr>
                <td>TripAdvisor Reviews</td>
                <td><span class="encumbrance attribution">RequiresAttribution</span></td>
                <td>From ReviewsTest.cs</td>
            </tr>
            <tr>
                <td>Facebook Reviews</td>
                <td><span class="encumbrance quotation">RequiresQuotation</span></td>
                <td>From ReviewsTest.cs</td>
            </tr>
            <tr>
                <td>Booking.com</td>
                <td><span class="encumbrance attribution">RequiresAttribution</span></td>
                <td>From ReviewsTest.cs</td>
            </tr>
            <tr>
                <td>Social Profiles</td>
                <td><span class="encumbrance factual">Factual</span></td>
                <td>From SocialProfileMergeProcessor.cs</td>
            </tr>
            <tr>
                <td>Web Scraped Images</td>
                <td><span class="encumbrance attribution">RequiresAttribution</span></td>
                <td>From AllPhotosWithMultiTagFeedGenerationReducer.cs</td>
            </tr>
            <tr>
                <td>AI Generated Content</td>
                <td><span class="encumbrance factual">Factual</span> (proposed)</td>
                <td>No external source to cite</td>
            </tr>
        </table>
    </div>
    
    <div class="sub-card">
        <h3>Key Cosmos Paths</h3>
        <table>
            <tr><th>Path</th><th>Content</th></tr>
            <tr>
                <td><code>.../Poi/UrlYpidLinking/Published/</code></td>
                <td>Production URL-YPID mappings</td>
            </tr>
            <tr>
                <td><code>.../Base/UrlYpidLinking/EntityMatching/</code></td>
                <td>Base entity matching feeds</td>
            </tr>
            <tr>
                <td><code>.../RebaseMetrics/</code></td>
                <td>Top entity rankings by impressions</td>
            </tr>
        </table>
    </div>
    """


def get_gap_analysis_content():
    """Deliverable 3: Gap Hypotheses & Open Questions"""
    return """
    <h2>🔍 Gap Analysis & Hypotheses</h2>
    <p class="subtitle">Why hasn't additional content improved grounding quality?</p>
    
    <div class="sub-card hypothesis">
        <h3>Hypothesis 1: Grounding Encumbrance Flags Are Not Set Correctly</h3>
        <div class="hypothesis-content">
            <div class="observation">
                <strong>Observation:</strong> Initial grounding encumbrance values showed 0-100 split, which "doesn't seem correct."
            </div>
            <div class="possible-causes">
                <strong>Possible Causes:</strong>
                <ul>
                    <li>Provider-level flagging, not attribute-level</li>
                    <li>Default to Restricted — if not set, everything blocked</li>
                    <li>Binary providers (100% Factual OR 100% Restricted)</li>
                    <li>Missing flags on web-scraped content</li>
                </ul>
            </div>
            <div class="validation">
                <strong>Validation Needed:</strong>
                <ul>
                    <li>☐ Query: What % of attributes have each encumbrance value?</li>
                    <li>☐ Query: Is encumbrance set per-entity, per-attribute, or per-provider?</li>
                </ul>
            </div>
        </div>
    </div>
    
    <div class="sub-card hypothesis">
        <h3>Hypothesis 2: Rich Attributes Exist But Aren't Grounding-Ready</h3>
        <div class="hypothesis-content">
            <div class="observation">
                <strong>Observation:</strong> RDQ metrics focus on coverage (quorum %, zero count %), not grounding readiness.
            </div>
            <div class="insight-box">
                <strong>Key Insight:</strong> Coverage ≠ Usability for Copilot<br>
                We may have 97% review coverage, but only 3% <em>grounding-ready</em> review coverage.
            </div>
            <div class="validation">
                <strong>Validation Needed:</strong>
                <ul>
                    <li>☐ Calculate: Coverage × Grounding-Ready % for each attribute</li>
                    <li>☐ Compare: Raw coverage vs. grounding-ready coverage</li>
                </ul>
            </div>
        </div>
    </div>
    
    <div class="sub-card hypothesis">
        <h3>Hypothesis 3: URL-YPID Linking Quality Is Unknown</h3>
        <div class="hypothesis-content">
            <div class="observation">
                <strong>Observation:</strong> No visibility into linking accuracy or mis-link rates by category.
            </div>
            <div class="impact">
                <strong>Impact on Grounding:</strong> Even with perfect encumbrance, wrong entity → wrong answer.
            </div>
            <div class="validation">
                <strong>Validation Needed:</strong>
                <ul>
                    <li>☐ Sample-based audit: Pull 500 URL-YPID pairs, manually verify</li>
                    <li>☐ Identify: Top verticals with highest suspected mis-link rates</li>
                </ul>
            </div>
        </div>
    </div>
    
    <div class="sub-card hypothesis">
        <h3>Hypothesis 4: AI Enrichment Not Connected to Grounding</h3>
        <div class="hypothesis-content">
            <div class="observation">
                <strong>Observation:</strong> AI Enrichment produces descriptions, amenities, highlights — but as POC outputs only.
            </div>
            <div class="opportunity">
                <strong>Opportunity:</strong> AI-generated content could be <span class="encumbrance factual">Factual</span> 
                (no external source to cite), significantly increasing grounding-ready coverage.
            </div>
            <div class="validation">
                <strong>Validation Needed:</strong>
                <ul>
                    <li>☐ Confirm: Is AI Enrichment output in UDS today?</li>
                    <li>☐ Define: What encumbrance should AI-generated content have?</li>
                </ul>
            </div>
        </div>
    </div>
    
    <div class="sub-card">
        <h3>Open Questions</h3>
        <table>
            <tr><th>#</th><th>Question</th><th>Owner</th><th>Status</th></tr>
            <tr>
                <td>1</td>
                <td>What attributes does Copilot actually retrieve for grounding?</td>
                <td>Grounding team</td>
                <td><span class="status-badge">Open</span></td>
            </tr>
            <tr>
                <td>2</td>
                <td>What is the retrieval mechanism? (RAG? Direct lookup?)</td>
                <td>Grounding team</td>
                <td><span class="status-badge">Open</span></td>
            </tr>
            <tr>
                <td>3</td>
                <td>Where is grounding encumbrance set in the pipeline?</td>
                <td>RAP team</td>
                <td><span class="status-badge">Open</span></td>
            </tr>
            <tr>
                <td>4</td>
                <td>Is there a YPID → Attribute → Source → Encumbrance table?</td>
                <td>Data Infra</td>
                <td><span class="status-badge">Open</span></td>
            </tr>
            <tr>
                <td>5</td>
                <td>What encumbrance should AI-generated content have?</td>
                <td>Legal / Governance</td>
                <td><span class="status-badge">Open</span></td>
            </tr>
        </table>
    </div>
    
    <div class="sub-card">
        <h3>The Core Gap</h3>
        <div class="alert danger">
            <strong>The gap between "data exists" and "data is useful for grounding" is likely large and unmeasured.</strong>
            <p>Current metrics focus on:</p>
            <ul>
                <li>✅ Coverage (do we have the attribute?)</li>
                <li>✅ Quality (is the value correct?)</li>
            </ul>
            <p>Missing metric:</p>
            <ul>
                <li>❌ <strong>Grounding readiness</strong> (can Copilot use it?)</li>
            </ul>
        </div>
    </div>
    """


def generate_dashboard():
    """Generate the comprehensive dashboard with all tabs."""
    
    output_dir = PROJECT_ROOT / "output"
    summary_file = output_dir / "comparison_summary.tsv"
    detailed_file = output_dir / "comparison_detailed.tsv"
    
    # Load comparison data if exists
    has_comparison_data = summary_file.exists()
    if has_comparison_data:
        summary = load_tsv(summary_file)
        detailed = load_tsv(detailed_file)
        
        total_queries = len(summary)
        bing_wins = (summary['winner'] == 'bing_copilot').sum()
        bing_win_pct = bing_wins / total_queries * 100 if total_queries > 0 else 0
        winner_dist = summary['winner'].value_counts().to_dict()
        
        losses = summary[summary['winner'] != 'bing_copilot']
        gap_reasons = losses['gap_reason'].value_counts().to_dict() if len(losses) > 0 else {}
        
        by_type = summary.groupby('query_type').apply(
            lambda g: (g['winner'] == 'bing_copilot').sum() / len(g) * 100
        ).to_dict()
        
        by_segment = summary.groupby('segment').apply(
            lambda g: (g['winner'] == 'bing_copilot').sum() / len(g) * 100
        ).to_dict()
        
        # Deep dive data
        deep_dive_rows = []
        for query_id in summary['query_id'].unique():
            query_responses = detailed[detailed['query_id'] == query_id]
            query_info = summary[summary['query_id'] == query_id].iloc[0]
            
            bing_resp = query_responses[query_responses['responder'] == 'bing_copilot']
            other_resp = query_responses[query_responses['responder'] != 'bing_copilot']
            
            if len(bing_resp) == 0 or len(other_resp) == 0:
                continue
                
            bing_row = bing_resp.iloc[0]
            best_other = other_resp.loc[other_resp['score'].idxmax()] if 'score' in other_resp.columns else other_resp.iloc[0]
            
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
            
            deep_dive_rows.append({
                'query_id': query_id,
                'query_text': query_info['query_text'],
                'query_type': query_info.get('query_type', 'N/A'),
                'winner': query_info['winner'],
                'bing_response': str(bing_row.get('response_text', ''))[:150] + '...' if len(str(bing_row.get('response_text', ''))) > 150 else str(bing_row.get('response_text', '')),
                'winner_response': str(best_other.get('response_text', ''))[:150] + '...' if len(str(best_other.get('response_text', ''))) > 150 else str(best_other.get('response_text', '')),
                'winner_source': comp_source,
                'advantages': advantages,
                'bing_score': bing_row.get('score', 0),
                'winner_score': best_other.get('score', 0)
            })
    else:
        total_queries = 0
        bing_win_pct = 0
        winner_dist = {}
        gap_reasons = {}
        by_type = {}
        by_segment = {}
        deep_dive_rows = []
    
    # Build competitive analysis content
    if has_comparison_data:
        competitive_content = f"""
        <h2>🏆 Competitive Analysis</h2>
        <p class="subtitle">Bing Copilot vs. Gemini, Perplexity, ChatGPT</p>
        
        <div class="metrics-row">
            <div class="metric">
                <div class="value">{total_queries}</div>
                <div class="label">Total Queries</div>
            </div>
            <div class="metric {'good' if bing_win_pct >= 50 else 'bad'}">
                <div class="value">{bing_win_pct:.0f}%</div>
                <div class="label">Bing Win Rate</div>
            </div>
        </div>
        
        <div class="sub-card">
            <h3>Winner Distribution</h3>
            {"".join(f'''
            <div class="bar-item">
                <span class="bar-label">{responder}</span>
                <div class="bar">
                    <div class="bar-fill {responder.split('_')[0] if '_' in responder else 'other'}" 
                         style="width: {count/total_queries*100}%">
                        {count} ({count/total_queries*100:.0f}%)
                    </div>
                </div>
            </div>
            ''' for responder, count in winner_dist.items())}
        </div>
        
        <div class="sub-card">
            <h3>Why Bing Lost</h3>
            <table>
                <tr><th>Gap Reason</th><th>Count</th><th>Description</th></tr>
                {"".join(f'''<tr>
                    <td><span class="gap-badge {reason}">{reason}</span></td>
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
        
        <div class="sub-card">
            <h3>Win Rate by Query Type</h3>
            <table>
                <tr><th>Query Type</th><th>Bing Win %</th><th></th></tr>
                {"".join(f'''<tr>
                    <td><span class="query-type-badge {qtype}">{qtype}</span></td>
                    <td class="{'good' if pct >= 50 else 'bad'}">{pct:.0f}%</td>
                    <td><div class="bar"><div class="bar-fill bing" style="width: {pct}%"></div></div></td>
                </tr>''' for qtype, pct in by_type.items())}
            </table>
        </div>
        
        <div class="sub-card deep-dive">
            <h3>🔬 Deep Dive: Why Competitors Win</h3>
            {"".join(f'''
            <div class="comparison-card">
                <div class="comparison-header">
                    <span class="query-type-badge {item['query_type']}">{item['query_type']}</span>
                    <strong>{item['query_text']}</strong>
                </div>
                <div class="comparison-body">
                    <div class="response-column bing-column">
                        <div class="column-header">
                            <span class="responder-name">🔷 Bing</span>
                            <span class="score">{f"{item['bing_score']:.2f}" if item['bing_score'] else 'N/A'}</span>
                        </div>
                        <div class="response-text">{item['bing_response']}</div>
                    </div>
                    <div class="response-column winner-column">
                        <div class="column-header">
                            <span class="responder-name">🏆 {item['winner'].split(':')[0] if ':' in str(item['winner']) else item['winner']}</span>
                            <span class="score">{f"{item['winner_score']:.2f}" if item['winner_score'] else 'N/A'}</span>
                        </div>
                        <div class="response-text">{item['winner_response']}</div>
                        <div class="source-badge">Source: {item['winner_source']}</div>
                    </div>
                </div>
                <div class="advantages">
                    <strong>Competitor advantages:</strong>
                    <ul>{"".join(f"<li>{adv}</li>" for adv in item['advantages']) if item['advantages'] else "<li>Higher overall quality</li>"}</ul>
                </div>
            </div>
            ''' for item in deep_dive_rows if item['winner'] != 'bing_copilot')}
        </div>
        """
    else:
        competitive_content = """
        <h2>🏆 Competitive Analysis</h2>
        <div class="alert info">
            <strong>No comparison data yet.</strong><br>
            Run <code>python scripts/compare_responses.py</code> after collecting competitive responses.
        </div>
        """
    
    # Generate full HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grounding Playground Dashboard</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, sans-serif;
            margin: 0; padding: 0;
            background: #f0f2f5;
        }}
        
        /* Header */
        .header {{
            background: linear-gradient(135deg, #0078d4, #00bcf2);
            color: white;
            padding: 20px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .header h1 {{ margin: 0; font-size: 1.5em; }}
        .header .timestamp {{ opacity: 0.8; font-size: 0.9em; }}
        
        /* Tabs */
        .tabs {{
            background: white;
            border-bottom: 1px solid #ddd;
            padding: 0 40px;
            display: flex;
            gap: 0;
        }}
        .tab {{
            padding: 15px 25px;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            font-weight: 500;
            color: #666;
            transition: all 0.2s;
        }}
        .tab:hover {{ color: #0078d4; background: #f5f5f5; }}
        .tab.active {{
            color: #0078d4;
            border-bottom-color: #0078d4;
        }}
        
        /* Content */
        .content {{
            padding: 30px 40px;
            max-width: 1400px;
            margin: 0 auto;
        }}
        .tab-content {{
            display: none;
        }}
        .tab-content.active {{
            display: block;
        }}
        
        /* Cards */
        .sub-card {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .sub-card h3 {{ margin-top: 0; color: #333; }}
        
        /* Metrics */
        .metrics-row {{
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
        }}
        .metric {{
            background: white;
            padding: 20px 30px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .metric .value {{ font-size: 2.5em; font-weight: bold; color: #0078d4; }}
        .metric.good .value {{ color: #107c10; }}
        .metric.bad .value {{ color: #d83b01; }}
        .metric .label {{ color: #666; margin-top: 5px; }}
        
        /* Tables */
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
        th {{ background: #f8f8f8; font-weight: 600; }}
        
        /* Bars */
        .bar-item {{ margin: 10px 0; }}
        .bar-label {{ display: inline-block; width: 200px; }}
        .bar {{ background: #e0e0e0; border-radius: 4px; height: 24px; flex: 1; display: inline-block; width: calc(100% - 210px); vertical-align: middle; }}
        .bar-fill {{ height: 100%; border-radius: 4px; color: white; padding: 0 10px; line-height: 24px; font-size: 0.85em; }}
        .bar-fill.bing {{ background: #0078d4; }}
        .bar-fill.gemini {{ background: #4285f4; }}
        .bar-fill.perplexity {{ background: #20b2aa; }}
        .bar-fill.tie {{ background: #888; }}
        .bar-fill.other {{ background: #666; }}
        
        /* Badges */
        .status-badge {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            background: #e0e0e0;
        }}
        .status-badge.production {{ background: #e8f5e9; color: #2e7d32; }}
        .status-badge.experimental {{ background: #e3f2fd; color: #1565c0; }}
        .status-badge.warning {{ background: #fff3e0; color: #e65100; }}
        .status-badge.success {{ background: #e8f5e9; color: #2e7d32; }}
        
        .encumbrance {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: 500;
        }}
        .encumbrance.factual {{ background: #e8f5e9; color: #2e7d32; }}
        .encumbrance.attribution {{ background: #fff3e0; color: #e65100; }}
        .encumbrance.quotation {{ background: #fce4ec; color: #c2185b; }}
        .encumbrance.restricted {{ background: #ffebee; color: #c62828; }}
        
        .query-type-badge {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.75em;
            margin-right: 10px;
        }}
        .query-type-badge.amenity {{ background: #e3f2fd; color: #1565c0; }}
        .query-type-badge.vibe {{ background: #fce4ec; color: #c2185b; }}
        .query-type-badge.factual {{ background: #e8f5e9; color: #2e7d32; }}
        .query-type-badge.reviews {{ background: #fff3e0; color: #e65100; }}
        .query-type-badge.comparison {{ background: #f3e5f5; color: #7b1fa2; }}
        
        .gap-badge {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 4px;
            font-size: 0.85em;
        }}
        .gap-badge.missing_data {{ background: #ffebee; color: #c62828; }}
        .gap-badge.less_rich {{ background: #fff3e0; color: #e65100; }}
        .gap-badge.no_source {{ background: #e3f2fd; color: #1565c0; }}
        
        /* Alerts */
        .alert {{
            padding: 15px 20px;
            border-radius: 8px;
            margin: 15px 0;
        }}
        .alert.warning {{ background: #fff3e0; border-left: 4px solid #ff9800; }}
        .alert.danger {{ background: #ffebee; border-left: 4px solid #f44336; }}
        .alert.info {{ background: #e3f2fd; border-left: 4px solid #2196f3; }}
        
        /* Use cases grid */
        .use-case-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
        }}
        .use-case {{
            background: #f8f8f8;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .use-case-icon {{ font-size: 2em; margin-bottom: 10px; }}
        .use-case-title {{ font-weight: 600; margin-bottom: 5px; }}
        .use-case-desc {{ font-size: 0.85em; color: #666; }}
        
        /* Architecture diagram */
        .architecture-diagram {{
            text-align: center;
            padding: 20px;
        }}
        .arch-row {{
            display: flex;
            justify-content: center;
            gap: 15px;
            margin: 10px 0;
        }}
        .arch-box {{
            padding: 12px 20px;
            border-radius: 6px;
            font-size: 0.9em;
        }}
        .arch-box.source {{ background: #e3f2fd; color: #1565c0; }}
        .arch-box.extraction {{ background: #fff3e0; color: #e65100; }}
        .arch-box.processing {{ background: #f3e5f5; color: #7b1fa2; }}
        .arch-box.storage {{ background: #e8f5e9; color: #2e7d32; }}
        .arch-box.consumer {{ background: #fce4ec; color: #c2185b; }}
        .arch-arrow {{ font-size: 1.5em; color: #888; }}
        
        /* Coverage matrix */
        .coverage-matrix td.primary {{ background: #e8f5e9; font-weight: 500; }}
        .legend {{ margin-top: 10px; font-size: 0.85em; color: #666; display: flex; gap: 20px; }}
        
        /* Hypothesis cards */
        .hypothesis .observation {{ background: #f5f5f5; padding: 10px; border-radius: 4px; margin: 10px 0; }}
        .hypothesis .possible-causes ul {{ margin: 5px 0; }}
        .hypothesis .validation {{ background: #e3f2fd; padding: 10px; border-radius: 4px; margin: 10px 0; }}
        .hypothesis .opportunity {{ background: #e8f5e9; padding: 10px; border-radius: 4px; margin: 10px 0; }}
        .insight-box {{ background: #fff3e0; padding: 15px; border-radius: 4px; margin: 10px 0; }}
        
        /* Deep dive */
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
        .comparison-body {{
            display: flex;
        }}
        .response-column {{
            flex: 1;
            padding: 15px;
        }}
        .bing-column {{ background: #fafafa; border-right: 1px solid #ddd; }}
        .winner-column {{ background: #f0fff0; }}
        .column-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            padding-bottom: 10px;
            border-bottom: 1px solid #eee;
        }}
        .responder-name {{ font-weight: bold; }}
        .score {{ color: #666; font-size: 0.9em; }}
        .response-text {{ font-size: 0.9em; line-height: 1.5; font-style: italic; color: #333; }}
        .source-badge {{ margin-top: 10px; padding: 5px 10px; background: #e8f5e9; border-radius: 4px; font-size: 0.8em; display: inline-block; }}
        .advantages {{ background: #fff8e1; padding: 15px; border-top: 1px solid #ddd; }}
        .advantages ul {{ margin: 5px 0 0 0; padding-left: 20px; }}
        
        .good {{ color: #107c10; }}
        .bad {{ color: #d83b01; }}
        
        .subtitle {{ color: #666; margin-top: -10px; margin-bottom: 20px; }}
        code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }}
        
        /* Why section */
        .why-section {{
            background: linear-gradient(135deg, #fff9e6, #fff3cc);
            border: 2px solid #ffc107;
            border-radius: 8px;
            padding: 20px 25px;
            margin-bottom: 25px;
        }}
        .why-section h2 {{ margin-top: 0; color: #856404; }}
        .why-section .placeholder {{
            color: #856404;
            font-style: italic;
            background: rgba(255,255,255,0.5);
            padding: 10px;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Grounding Playground Dashboard</h1>
        <span class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</span>
    </div>
    
    <div class="tabs">
        <div class="tab active" onclick="showTab('competitive')">🏆 Competitive Analysis</div>
        <div class="tab" onclick="showTab('current-state')">📋 Current State</div>
    </div>
    
    <div class="content">
        <div class="why-section">
            <h2>📌 Why This Dashboard</h2>
            <p class="placeholder">[Placeholder: Add positioning text here — why external perspective matters, what this reveals that internal metrics don't]</p>
        </div>
        
        <div id="competitive" class="tab-content active">
            {competitive_content}
        </div>
        
        <div id="current-state" class="tab-content">
            {get_current_state_content()}
            {get_data_inventory_content()}
            {get_gap_analysis_content()}
        </div>
    </div>
    
    <script>
        function showTab(tabId) {{
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
            
            // Show selected tab
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>
"""
    
    # Save
    output_dir.mkdir(exist_ok=True)
    report_path = output_dir / "grounding_dashboard.html"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Dashboard generated: {report_path}")


if __name__ == "__main__":
    generate_dashboard()
