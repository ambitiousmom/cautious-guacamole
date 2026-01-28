"""
Generate RDQ-aligned dashboard for Grounding Data Quality.

Structure aligned to RDQ framework:
- Layer 1: Coverage & Freshness (counts, quorum)
- Layer 2: Richness (facet diversity vs competitors)
- Layer 3: Grounding Sufficiency (can we answer queries?)

Usage:
    python generate_rdq_dashboard.py
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent


def get_rdq_framework_content():
    """RDQ Framework explanation."""
    return """
    <h2>RDQ Framework</h2>
    <p class="subtitle">Rich Data Quorum — Measuring Data Richness for Grounding</p>
    
    <div class="framework-layers">
        <div class="layer layer-1">
            <div class="layer-header">
                <span class="layer-num">1</span>
                <span class="layer-title">Coverage & Freshness</span>
                <span class="layer-priority high">HIGH PRIORITY</span>
            </div>
            <div class="layer-body">
                <p><strong>Question:</strong> Do we have enough content?</p>
                <div class="metrics-list">
                    <div class="metric-item">
                        <span class="metric-name">Review Count</span>
                        <span class="metric-desc">Entities with ≥5 reviews</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-name">Image Count</span>
                        <span class="metric-desc">Entities with ≥3 images</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-name">URL Coverage</span>
                        <span class="metric-desc">Entities with linked URLs</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-name">Freshness</span>
                        <span class="metric-desc">Content &lt;3 months old</span>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="layer layer-2">
            <div class="layer-header">
                <span class="layer-num">2</span>
                <span class="layer-title">Richness / Facet Diversity</span>
                <span class="layer-priority medium">MEDIUM PRIORITY</span>
            </div>
            <div class="layer-body">
                <p><strong>Question:</strong> What topics can we answer about a place?</p>
                <div class="metrics-list">
                    <div class="metric-item">
                        <span class="metric-name">Facet Coverage</span>
                        <span class="metric-desc">Topics we have vs. competitors</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-name">Structured Attributes</span>
                        <span class="metric-desc">Hours, amenities, price, etc.</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-name">Semi-Structured Insights</span>
                        <span class="metric-desc">Tips, popular items, occasions</span>
                    </div>
                </div>
                <div class="your-work">
                    <strong>Your Grounding Experiments Feed Here</strong>
                </div>
            </div>
        </div>
        
        <div class="layer layer-3">
            <div class="layer-header">
                <span class="layer-num">3</span>
                <span class="layer-title">Grounding Sufficiency</span>
                <span class="layer-priority low">FUTURE</span>
            </div>
            <div class="layer-body">
                <p><strong>Question:</strong> Can Copilot answer queries with our data?</p>
                <div class="metrics-list">
                    <div class="metric-item">
                        <span class="metric-name">Serving Gap</span>
                        <span class="metric-desc">Data we have vs. what Copilot uses</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-name">Answer Quality</span>
                        <span class="metric-desc">Compared to competitors</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="sub-card">
        <h3>Priority Order</h3>
        <div class="priority-flow">
            <div class="priority-item active">Coverage</div>
            <span class="arrow">→</span>
            <div class="priority-item">Freshness</div>
            <span class="arrow">→</span>
            <div class="priority-item">Richness</div>
            <span class="arrow">→</span>
            <div class="priority-item">Sufficiency</div>
        </div>
        <p class="note">High coverage required first, then freshness for trust, then richness for advanced experiences.</p>
    </div>
    """


def get_facet_gap_content():
    """Layer 2: Facet Gap Analysis from Grounding Experiments."""
    return """
    <h2>Facet Gap Analysis</h2>
    <p class="subtitle">Layer 2 — What topics can we answer vs. competitors?</p>
    
    <div class="sub-card">
        <h3>Competitor Facet Inventory (Gemini/Google Maps)</h3>
        <p>From grounding response analysis:</p>
        
        <table class="facet-table">
            <tr>
                <th>Facet Category</th>
                <th>Specific Attributes</th>
                <th>Source</th>
                <th>Bing Has?</th>
            </tr>
            <tr>
                <td><strong>Structured Booleans</strong></td>
                <td>Outdoor seating, Wheelchair accessible, Dine-in, Takeout, Delivery, Reservations, Wi-Fi, Parking</td>
                <td>Google Maps</td>
                <td><span class="status tbd">TBD</span></td>
            </tr>
            <tr>
                <td><strong>Business Info</strong></td>
                <td>Hours (per day), Price range, Phone, Website, Address, Coordinates</td>
                <td>Google Maps</td>
                <td><span class="status partial">Partial</span></td>
            </tr>
            <tr>
                <td><strong>Crowd/Suitability</strong></td>
                <td>Good for kids, Good for groups, LGBTQ+ friendly, Casual, Romantic, Trendy</td>
                <td>Google Maps</td>
                <td><span class="status tbd">TBD</span></td>
            </tr>
            <tr>
                <td><strong>AI-Generated Insights</strong></td>
                <td>Review Summary, Tips, Most Ordered, Occasion</td>
                <td>Gemini synthesis</td>
                <td><span class="status no">No</span></td>
            </tr>
            <tr>
                <td><strong>Dietary</strong></td>
                <td>Vegetarian, Vegan, Halal, Kosher options</td>
                <td>Google Maps + Reviews</td>
                <td><span class="status tbd">TBD</span></td>
            </tr>
        </table>
    </div>
    
    <div class="sub-card">
        <h3>Experiment Status</h3>
        <table>
            <tr>
                <th>Query Type</th>
                <th>Tests For</th>
                <th>Collected</th>
                <th>Finding</th>
            </tr>
            <tr>
                <td>Amenity (outdoor seating)</td>
                <td>Structured boolean</td>
                <td><span class="status yes">✓</span></td>
                <td>Gemini has <code>Outdoor seating: true</code></td>
            </tr>
            <tr>
                <td>Hours lookup</td>
                <td>Structured data</td>
                <td><span class="status pending">○</span></td>
                <td>-</td>
            </tr>
            <tr>
                <td>Vibe/occasion</td>
                <td>Semi-structured insight</td>
                <td><span class="status pending">○</span></td>
                <td>-</td>
            </tr>
            <tr>
                <td>Menu recommendations</td>
                <td>Semi-structured insight</td>
                <td><span class="status pending">○</span></td>
                <td>-</td>
            </tr>
            <tr>
                <td>Negative review synthesis</td>
                <td>Unstructured inference</td>
                <td><span class="status pending">○</span></td>
                <td>-</td>
            </tr>
        </table>
        <p class="action">Run experiments to populate this table: <code>python scripts/run_experiment.py</code></p>
    </div>
    
    <div class="sub-card">
        <h3>Key Finding from Sample</h3>
        <div class="finding-card">
            <div class="finding-header">Query: "Does Din Tai Fung Bellevue have outdoor seating?"</div>
            <div class="finding-body">
                <div class="finding-row">
                    <span class="label">Gemini Source:</span>
                    <span class="value">Google Maps (google_map_tool_v2)</span>
                </div>
                <div class="finding-row">
                    <span class="label">Structured Answer:</span>
                    <span class="value"><code>["Outdoor seating", true]</code></span>
                </div>
                <div class="finding-row">
                    <span class="label">Also Retrieved:</span>
                    <span class="value">648 reviews, 540 photos, Tips, Most Ordered, Occasion insights</span>
                </div>
            </div>
            <div class="finding-insight">
                <strong>Insight:</strong> Gemini doesn't infer from reviews — it has structured boolean flags for amenities.
            </div>
        </div>
    </div>
    """


def get_gap_dimensions_content():
    """The 3 dimensions from manager's mission."""
    return """
    <h2>Three Dimensions of Gap Analysis</h2>
    <p class="subtitle">Aligned to Cycle Mission: local-data-grounding-sufficiency</p>
    
    <div class="dimensions-grid">
        <div class="dimension-card">
            <div class="dim-header">
                <span class="dim-num">1</span>
                <span class="dim-title">Counts & Quorum</span>
            </div>
            <div class="dim-body">
                <p><strong>Measures:</strong> Reviews, Photos, URLs</p>
                <p><strong>Status:</strong> Existing RDQ dashboard</p>
                <p><strong>Gap Metric:</strong> Coverage % vs. SERP API</p>
            </div>
            <div class="dim-owner">Owner: RDQ Team</div>
        </div>
        
        <div class="dimension-card highlight">
            <div class="dim-header">
                <span class="dim-num">2</span>
                <span class="dim-title">Facet Comparisons</span>
            </div>
            <div class="dim-body">
                <p><strong>Measures:</strong> Topics we can answer vs. competitors</p>
                <p><strong>Status:</strong> <span class="badge active">YOUR FOCUS</span></p>
                <p><strong>Gap Metric:</strong> Facet inventory comparison</p>
            </div>
            <div class="dim-owner">Owner: You (Grounding Experiments)</div>
        </div>
        
        <div class="dimension-card">
            <div class="dim-header">
                <span class="dim-num">3</span>
                <span class="dim-title">Serving/Summarization Loss</span>
            </div>
            <div class="dim-body">
                <p><strong>Measures:</strong> What we have vs. what Copilot serves</p>
                <p><strong>Status:</strong> Dependent on C6 experiments</p>
                <p><strong>Gap Metric:</strong> Answer quality gap</p>
            </div>
            <div class="dim-owner">Owner: Speedbird Team</div>
        </div>
    </div>
    
    <div class="sub-card">
        <h3>Your Contribution to the Mission</h3>
        <table>
            <tr>
                <th>Sprint</th>
                <th>Mission Milestone</th>
                <th>Your Input</th>
            </tr>
            <tr>
                <td>Sprint 1 (1/30)</td>
                <td>Short list of 5 prioritized providers for RDQ eval</td>
                <td>Facet analysis → Which providers have facets we lack?</td>
            </tr>
            <tr>
                <td>Sprint 2 (2/13)</td>
                <td>Local pages tested for presence in WDP</td>
                <td>-</td>
            </tr>
            <tr>
                <td>C2</td>
                <td>Wrapstar/Schema.org migration plan</td>
                <td>What rich content comes from these sources?</td>
            </tr>
        </table>
    </div>
    """


def get_current_state_content():
    """Current state aligned to RDQ - includes POCs, data sources, and gaps."""
    return """
    <h2>Current State</h2>
    <p class="subtitle">Data Systems, POCs, and Gap Analysis</p>
    
    <!-- POC Flow Diagram -->
    <div class="sub-card">
        <h3>POC → RDQ Layer Flow</h3>
        <div class="flow-diagram">
            <div class="flow-section">
                <div class="flow-header">DATA SOURCES</div>
                <div class="flow-boxes">
                    <div class="flow-box source">Web HTML</div>
                    <div class="flow-box source">Semantic Docs</div>
                    <div class="flow-box source">Reviews</div>
                    <div class="flow-box source">Bing Search</div>
                </div>
            </div>
            
            <div class="flow-arrow-down">↓</div>
            
            <div class="flow-section">
                <div class="flow-header">POC PROCESSING</div>
                <div class="flow-row">
                    <div class="poc-group">
                        <div class="poc-title">AI Enrichment (adric)</div>
                        <div class="poc-items">
                            <span class="poc-item active">FeatureGeneration</span>
                            <span class="poc-item active">SmartExtraction</span>
                            <span class="poc-item active">Evaluation</span>
                        </div>
                    </div>
                    <div class="poc-group">
                        <div class="poc-title">Entity/Quality (adrianaf)</div>
                        <div class="poc-items">
                            <span class="poc-item active">EntityDiscovery</span>
                            <span class="poc-item active">RichnessModel</span>
                            <span class="poc-item active">DomainReputation</span>
                        </div>
                    </div>
                    <div class="poc-group">
                        <div class="poc-title">SLM Experiments</div>
                        <div class="poc-items">
                            <span class="poc-item progress">SLM-Gemma3</span>
                            <span class="poc-item progress">EntityDiscoverySLM</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="flow-arrow-down">↓</div>
            
            <div class="flow-section">
                <div class="flow-header">ENRICHED OUTPUTS</div>
                <div class="flow-boxes">
                    <div class="flow-box output">DescriptionAI</div>
                    <div class="flow-box output">AmenitiesAI</div>
                    <div class="flow-box output">HighlightsAI</div>
                    <div class="flow-box output">RichnessScore</div>
                </div>
            </div>
            
            <div class="flow-arrow-down">↓</div>
            
            <div class="flow-section">
                <div class="flow-header">RDQ LAYERS ADDRESSED</div>
                <div class="flow-boxes rdq">
                    <div class="flow-box rdq-layer partial">Layer 1: Coverage ⚠️</div>
                    <div class="flow-box rdq-layer partial">Layer 2: Richness ⚠️</div>
                    <div class="flow-box rdq-layer gap">Layer 3: Sufficiency ❌</div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- POC Table -->
    <div class="sub-card">
        <h3>POC Inventory</h3>
        <table class="poc-table">
            <tr>
                <th>POC Name</th>
                <th>Owner</th>
                <th>What It Does</th>
                <th>Layer</th>
                <th>Status</th>
                <th>Gap Filled?</th>
            </tr>
            <tr>
                <td><strong>AI_Enrichment</strong></td>
                <td>adric</td>
                <td>LLM (GPT-5) generates descriptions, amenities, highlights</td>
                <td><span class="layer-badge l2">L2</span></td>
                <td><span class="status yes">Active</span></td>
                <td>⚠️ Encumbrance TBD</td>
            </tr>
            <tr>
                <td><strong>AI Enrichment Portal</strong></td>
                <td>adric</td>
                <td>Web UI for prompt engineering</td>
                <td><span class="layer-badge l2">L2</span></td>
                <td><span class="status yes">Deployed</span></td>
                <td>✅ Iteration tool</td>
            </tr>
            <tr>
                <td><strong>AIEnrichment-SLM</strong></td>
                <td>penglinhuang</td>
                <td>Gemma-3 based enrichment (cheaper)</td>
                <td><span class="layer-badge l2">L2</span></td>
                <td><span class="status progress">In Progress</span></td>
                <td>⏳ Cost path</td>
            </tr>
            <tr>
                <td><strong>RichnessModel</strong></td>
                <td>adrianaf</td>
                <td>XLM-RoBERTa scores content quality</td>
                <td><span class="layer-badge l1">L1</span><span class="layer-badge l2">L2</span></td>
                <td><span class="status yes">Active</span></td>
                <td>✅ Scoring</td>
            </tr>
            <tr>
                <td><strong>EntityDiscovery</strong></td>
                <td>adrianaf</td>
                <td>Discover entities from web via LLM</td>
                <td><span class="layer-badge l1">L1</span></td>
                <td><span class="status yes">Active</span></td>
                <td>✅ Coverage</td>
            </tr>
            <tr>
                <td><strong>Facet Extraction</strong></td>
                <td>jkjolbro</td>
                <td>Extract amenities from reviews</td>
                <td><span class="layer-badge l2">L2</span></td>
                <td><span class="status yes">Active</span></td>
                <td>⚠️ Partial facets</td>
            </tr>
            <tr>
                <td><strong>StructuredData/WrapStar</strong></td>
                <td>src</td>
                <td>Schema.org extraction</td>
                <td><span class="layer-badge l1">L1</span><span class="layer-badge l2">L2</span></td>
                <td><span class="status yes">Production</span></td>
                <td>⚠️ RequiresAttribution</td>
            </tr>
            <tr>
                <td><strong>URL-Address Propagation</strong></td>
                <td>ekt</td>
                <td>Propagate address across URL mappings</td>
                <td><span class="layer-badge l1">L1</span></td>
                <td><span class="status yes">Active</span></td>
                <td>✅ URL-YPID linking</td>
            </tr>
        </table>
    </div>
    
    <!-- Data Sources by Layer -->
    <div class="sub-card">
        <h3>Data Sources by RDQ Layer</h3>
        <table>
            <tr>
                <th>Source</th>
                <th>Layer 1 (Coverage)</th>
                <th>Layer 2 (Richness)</th>
                <th>Grounding Ready?</th>
            </tr>
            <tr>
                <td><strong>Licensed Feeds</strong></td>
                <td>✅ Reviews, Photos</td>
                <td>⚠️ Limited facets</td>
                <td>Varies by provider</td>
            </tr>
            <tr>
                <td><strong>Wrapstar</strong></td>
                <td>✅ URLs, Descriptions</td>
                <td>✅ Amenities, Images</td>
                <td>⚠️ RequiresAttribution</td>
            </tr>
            <tr>
                <td><strong>Schema.org</strong></td>
                <td>✅ Structured markup</td>
                <td>✅ Rich attributes</td>
                <td>⚠️ Varies</td>
            </tr>
            <tr>
                <td><strong>AI Enrichment (POC)</strong></td>
                <td>❌ Not in prod</td>
                <td>✅ Could add facets</td>
                <td>? (Encumbrance TBD)</td>
            </tr>
        </table>
    </div>
    
    <!-- Gap Analysis -->
    <div class="sub-card">
        <h3>Gap Analysis: Covered vs. Remaining</h3>
        <div class="gap-grid">
            <div class="gap-card covered">
                <div class="gap-header">✅ COVERED</div>
                <ul>
                    <li>AI-generated descriptions</li>
                    <li>Amenities extraction</li>
                    <li>Richness scoring</li>
                    <li>Review extraction</li>
                    <li>Entity discovery</li>
                    <li>Domain trust</li>
                </ul>
            </div>
            
            <div class="gap-card partial">
                <div class="gap-header">⚠️ PARTIAL</div>
                <ul>
                    <li>Structured booleans (outdoor seating) — not Google-parity</li>
                    <li>Hours/pricing — coverage unknown</li>
                    <li>Crowd suitability (kid-friendly)</li>
                    <li>Dietary options — from reviews only</li>
                </ul>
            </div>
            
            <div class="gap-card missing">
                <div class="gap-header">❌ GAPS</div>
                <ul>
                    <li>Google-parity structured flags</li>
                    <li>AI "Tips" / "Most Ordered" synthesis</li>
                    <li>Review summarization (not prod)</li>
                    <li>Grounding encumbrance</li>
                    <li>Serving integration</li>
                    <li>Competitive comparison automation</li>
                </ul>
            </div>
        </div>
    </div>
    
    <!-- Encumbrance -->
    <div class="sub-card">
        <h3>Grounding Encumbrance Impact</h3>
        <table>
            <tr>
                <th>Encumbrance</th>
                <th>Can Ground?</th>
                <th>Impact</th>
            </tr>
            <tr>
                <td><span class="encumbrance factual">Factual</span></td>
                <td>✅ Yes</td>
                <td>Full Layer 2 contribution</td>
            </tr>
            <tr>
                <td><span class="encumbrance attribution">RequiresAttribution</span></td>
                <td>⚠️ With citation</td>
                <td>Partial contribution</td>
            </tr>
            <tr>
                <td><span class="encumbrance restricted">Restricted</span></td>
                <td>❌ No</td>
                <td>Zero grounding value</td>
            </tr>
        </table>
        <div class="alert warning">
            <strong>Key Gap:</strong> High RDQ Layer 1 coverage ≠ high "grounding-ready" coverage due to encumbrance.
        </div>
    </div>
    
    <!-- Priority Actions -->
    <div class="sub-card">
        <h3>Priority Actions</h3>
        <table>
            <tr>
                <th>#</th>
                <th>Gap</th>
                <th>Action</th>
                <th>POC</th>
            </tr>
            <tr>
                <td>1</td>
                <td>No Google-parity booleans</td>
                <td>Extend Facet Extraction → structured output</td>
                <td>Facet Extraction</td>
            </tr>
            <tr>
                <td>2</td>
                <td>AI output encumbrance</td>
                <td>Define: Factual or RequiresAttribution?</td>
                <td>AI_Enrichment</td>
            </tr>
            <tr>
                <td>3</td>
                <td>No "Tips" synthesis</td>
                <td>Add review synthesis prompts</td>
                <td>AI Enrichment Portal</td>
            </tr>
            <tr>
                <td>4</td>
                <td>No competitor comparison</td>
                <td>Automate facet tracking</td>
                <td>NEW</td>
            </tr>
            <tr>
                <td>5</td>
                <td>POC → Prod gap</td>
                <td>Productize for Top 100K</td>
                <td>AI_Enrichment</td>
            </tr>
        </table>
    </div>
    
    <!-- Open Questions -->
    <div class="sub-card">
        <h3>Open Questions</h3>
        <table>
            <tr><th>#</th><th>Question</th><th>Impacts</th></tr>
            <tr>
                <td>1</td>
                <td>What % of rich content is grounding-ready?</td>
                <td>Layer 2 true coverage</td>
            </tr>
            <tr>
                <td>2</td>
                <td>Which providers have facets we lack?</td>
                <td>Sprint 1 prioritization</td>
            </tr>
            <tr>
                <td>3</td>
                <td>What encumbrance for AI content?</td>
                <td>AI Enrichment value</td>
            </tr>
        </table>
    </div>
    """


def generate_dashboard():
    """Generate the RDQ-aligned dashboard."""
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RDQ Grounding Dashboard</title>
    <style>
        :root {{
            --purple-dark: #5b4b8a;
            --purple-mid: #7c6bae;
            --purple-light: #a99fd4;
            --purple-pale: #e8e4f3;
            --purple-wash: #f5f3fa;
            --text-primary: #2d2d3a;
            --text-secondary: #6b6b7b;
            --text-muted: #9b9bab;
            --border: #e5e5eb;
            --white: #ffffff;
        }}
        
        * {{ box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', -apple-system, sans-serif;
            margin: 0; padding: 0;
            background: var(--purple-wash);
            color: var(--text-primary);
            line-height: 1.6;
        }}
        
        .header {{
            background: linear-gradient(135deg, var(--purple-dark), var(--purple-mid));
            color: var(--white);
            padding: 24px 48px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .header h1 {{ margin: 0; font-size: 1.4em; font-weight: 500; letter-spacing: -0.5px; }}
        .header .subtitle {{ opacity: 0.85; font-size: 0.85em; font-weight: 300; margin-top: 4px; }}
        .header .timestamp {{ opacity: 0.6; font-size: 0.8em; font-weight: 300; }}
        
        .tabs {{
            background: var(--white);
            border-bottom: 1px solid var(--border);
            padding: 0 48px;
            display: flex;
            gap: 0;
        }}
        .tab {{
            padding: 16px 28px;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            font-weight: 400;
            color: var(--text-secondary);
            font-size: 0.9em;
            transition: all 0.2s ease;
        }}
        .tab:hover {{ color: var(--purple-dark); }}
        .tab.active {{ color: var(--purple-dark); border-bottom-color: var(--purple-mid); font-weight: 500; }}
        
        .content {{ padding: 32px 48px; max-width: 1300px; margin: 0 auto; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        
        .why-section {{
            background: linear-gradient(135deg, var(--purple-pale), var(--purple-wash));
            border: 1px solid var(--purple-light);
            border-radius: 12px;
            padding: 24px 28px;
            margin-bottom: 28px;
        }}
        .why-section h2 {{ margin: 0 0 8px 0; color: var(--purple-dark); font-size: 1.1em; font-weight: 500; }}
        .why-section .placeholder {{ color: var(--text-secondary); font-style: italic; font-size: 0.9em; }}
        
        h2 {{ font-size: 1.2em; font-weight: 500; color: var(--text-primary); margin-bottom: 8px; }}
        .subtitle {{ color: var(--text-secondary); font-size: 0.9em; margin-top: -4px; margin-bottom: 24px; }}
        
        .sub-card {{
            background: var(--white);
            border-radius: 12px;
            padding: 24px;
            margin: 20px 0;
            border: 1px solid var(--border);
        }}
        .sub-card h3 {{ margin: 0 0 16px 0; color: var(--text-primary); font-size: 1em; font-weight: 500; }}
        
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px 16px; text-align: left; border-bottom: 1px solid var(--border); font-size: 0.88em; }}
        th {{ background: var(--purple-wash); font-weight: 500; color: var(--text-secondary); }}
        tr:last-child td {{ border-bottom: none; }}
        
        /* RDQ Layers */
        .framework-layers {{ display: flex; flex-direction: column; gap: 16px; }}
        .layer {{
            background: var(--white);
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border);
        }}
        .layer-header {{
            padding: 16px 20px;
            display: flex;
            align-items: center;
            gap: 14px;
            background: linear-gradient(135deg, var(--purple-pale), var(--purple-wash));
        }}
        .layer-1 .layer-header {{ background: linear-gradient(135deg, #e8e4f3, #f5f3fa); }}
        .layer-2 .layer-header {{ background: linear-gradient(135deg, #ede4f3, #f7f3fa); }}
        .layer-3 .layer-header {{ background: linear-gradient(135deg, #e9e9ed, #f3f3f5); }}
        .layer-num {{
            width: 28px; height: 28px;
            border-radius: 50%;
            background: var(--purple-mid);
            color: var(--white);
            display: flex; align-items: center; justify-content: center;
            font-weight: 500;
            font-size: 0.85em;
        }}
        .layer-title {{ font-weight: 500; font-size: 1em; flex: 1; color: var(--text-primary); }}
        .layer-priority {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.7em;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .layer-priority.high {{ background: var(--purple-mid); color: var(--white); }}
        .layer-priority.medium {{ background: var(--purple-light); color: var(--purple-dark); }}
        .layer-priority.low {{ background: var(--border); color: var(--text-secondary); }}
        .layer-body {{ padding: 20px; }}
        .layer-body p {{ margin: 0 0 12px 0; color: var(--text-secondary); font-size: 0.9em; }}
        .metrics-list {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }}
        .metric-item {{
            background: var(--purple-wash);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.82em;
            color: var(--text-primary);
        }}
        .metric-name {{ font-weight: 500; }}
        .metric-desc {{ color: var(--text-muted); margin-left: 4px; }}
        .your-work {{
            margin-top: 16px;
            padding: 12px;
            background: linear-gradient(135deg, var(--purple-pale), var(--purple-wash));
            border-radius: 8px;
            text-align: center;
            font-size: 0.88em;
            color: var(--purple-dark);
        }}
        
        /* Priority flow */
        .priority-flow {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            margin: 24px 0;
        }}
        .priority-item {{
            padding: 10px 20px;
            background: var(--purple-wash);
            border-radius: 24px;
            font-weight: 400;
            font-size: 0.9em;
            color: var(--text-secondary);
        }}
        .priority-item.active {{ background: var(--purple-mid); color: var(--white); }}
        .arrow {{ color: var(--purple-light); font-size: 1.2em; }}
        .note {{ color: var(--text-muted); font-size: 0.85em; text-align: center; margin-top: 8px; }}
        
        /* Dimensions */
        .dimensions-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin: 20px 0;
        }}
        .dimension-card {{
            background: var(--white);
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border);
        }}
        .dimension-card.highlight {{ border-color: var(--purple-mid); }}
        .dim-header {{
            background: var(--purple-wash);
            padding: 14px 16px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .dim-num {{
            width: 26px; height: 26px;
            background: var(--purple-mid);
            color: var(--white);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-weight: 500;
            font-size: 0.8em;
        }}
        .dim-title {{ font-weight: 500; font-size: 0.95em; }}
        .dim-body {{ padding: 16px; font-size: 0.88em; }}
        .dim-body p {{ margin: 6px 0; color: var(--text-secondary); }}
        .dim-owner {{ padding: 12px 16px; background: var(--purple-wash); font-size: 0.8em; color: var(--text-muted); }}
        
        /* Status badges */
        .status {{ padding: 3px 10px; border-radius: 12px; font-size: 0.75em; font-weight: 500; }}
        .status.yes {{ background: var(--purple-pale); color: var(--purple-dark); }}
        .status.no {{ background: #f3e8e8; color: #8a5b5b; }}
        .status.partial, .status.progress {{ background: #f0edf5; color: var(--purple-mid); }}
        .status.tbd, .status.pending {{ background: var(--purple-wash); color: var(--text-muted); }}
        
        .badge {{ padding: 3px 10px; border-radius: 12px; font-size: 0.72em; font-weight: 500; }}
        .badge.active {{ background: var(--purple-mid); color: var(--white); }}
        
        /* Finding card */
        .finding-card {{
            border: 1px solid var(--border);
            border-radius: 10px;
            overflow: hidden;
        }}
        .finding-header {{
            background: var(--purple-wash);
            padding: 12px 16px;
            font-weight: 500;
            font-size: 0.9em;
        }}
        .finding-body {{ padding: 16px; }}
        .finding-row {{ display: flex; margin: 6px 0; font-size: 0.88em; }}
        .finding-row .label {{ width: 140px; color: var(--text-muted); }}
        .finding-row .value {{ flex: 1; color: var(--text-primary); }}
        .finding-insight {{
            padding: 12px 16px;
            background: linear-gradient(135deg, var(--purple-pale), var(--purple-wash));
            border-top: 1px solid var(--border);
            font-size: 0.88em;
        }}
        
        /* Encumbrance */
        .encumbrance {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 0.8em; font-weight: 500; }}
        .encumbrance.factual {{ background: var(--purple-pale); color: var(--purple-dark); }}
        .encumbrance.attribution {{ background: #f0edf5; color: var(--purple-mid); }}
        .encumbrance.restricted {{ background: #f3e8e8; color: #8a5b5b; }}
        
        .alert {{ padding: 16px; border-radius: 8px; margin: 16px 0; font-size: 0.9em; }}
        .alert.warning {{ background: var(--purple-pale); border-left: 3px solid var(--purple-mid); }}
        
        .action {{ background: var(--purple-wash); padding: 12px; border-radius: 8px; font-size: 0.88em; color: var(--text-secondary); }}
        
        code {{ background: var(--purple-wash); padding: 2px 8px; border-radius: 4px; font-size: 0.85em; color: var(--purple-dark); }}
        
        .facet-table td:first-child {{ font-weight: 500; width: 180px; }}
        
        /* POC Flow Diagram */
        .flow-diagram {{ padding: 24px; background: var(--purple-wash); border-radius: 12px; }}
        .flow-section {{ margin: 12px 0; }}
        .flow-header {{ 
            text-align: center; font-weight: 500; color: var(--text-muted); 
            font-size: 0.75em; margin-bottom: 12px; letter-spacing: 1.5px; text-transform: uppercase;
        }}
        .flow-boxes {{ display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }}
        .flow-box {{
            padding: 8px 18px;
            border-radius: 20px;
            font-weight: 400;
            font-size: 0.85em;
            text-align: center;
            background: var(--white);
            border: 1px solid var(--purple-light);
            color: var(--text-primary);
        }}
        .flow-box.source {{ background: var(--purple-pale); border-color: var(--purple-light); }}
        .flow-box.output {{ background: var(--white); border-color: var(--purple-mid); color: var(--purple-dark); }}
        .flow-box.rdq-layer {{ padding: 10px 22px; }}
        .flow-box.rdq-layer.partial {{ background: #f0edf5; border-color: var(--purple-light); }}
        .flow-box.rdq-layer.gap {{ background: #f3e8e8; border-color: #d4b8b8; color: #8a5b5b; }}
        .flow-arrow-down {{ text-align: center; font-size: 1.2em; color: var(--purple-light); margin: 8px 0; }}
        .flow-row {{ display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; }}
        .poc-group {{ 
            background: var(--white); border: 1px solid var(--border); border-radius: 10px; 
            padding: 14px; min-width: 180px;
        }}
        .poc-title {{ font-weight: 500; margin-bottom: 10px; text-align: center; font-size: 0.88em; color: var(--text-primary); }}
        .poc-items {{ display: flex; flex-direction: column; gap: 4px; }}
        .poc-item {{
            padding: 4px 10px; border-radius: 12px; font-size: 0.8em; text-align: center;
        }}
        .poc-item.active {{ background: var(--purple-pale); color: var(--purple-dark); }}
        .poc-item.progress {{ background: #f0edf5; color: var(--purple-mid); }}
        
        /* Layer badges */
        .layer-badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.72em;
            font-weight: 500;
            margin-right: 3px;
        }}
        .layer-badge.l1 {{ background: var(--purple-pale); color: var(--purple-dark); }}
        .layer-badge.l2 {{ background: #f0edf5; color: var(--purple-mid); }}
        .layer-badge.l3 {{ background: var(--purple-wash); color: var(--text-muted); }}
        
        /* Gap cards */
        .gap-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }}
        .gap-card {{ border-radius: 10px; padding: 16px; }}
        .gap-card.covered {{ background: var(--purple-pale); }}
        .gap-card.partial {{ background: #f0edf5; }}
        .gap-card.missing {{ background: #f3e8e8; }}
        .gap-header {{ font-weight: 500; margin-bottom: 12px; font-size: 0.9em; }}
        .gap-card ul {{ margin: 0; padding-left: 18px; }}
        .gap-card li {{ margin: 4px 0; font-size: 0.85em; color: var(--text-secondary); }}
        
        .poc-table td:first-child {{ font-weight: 500; }}
        .poc-table td {{ font-size: 0.85em; vertical-align: top; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>RDQ Grounding Dashboard</h1>
            <div class="subtitle">Rich Data Quorum → Grounding Sufficiency</div>
        </div>
        <span class="timestamp">{datetime.now().strftime('%Y-%m-%d')}</span>
    </div>
    
    <div class="tabs">
        <div class="tab active" onclick="showTab('framework')">Framework</div>
        <div class="tab" onclick="showTab('dimensions')">3 Dimensions</div>
        <div class="tab" onclick="showTab('state')">Current State</div>
        <div class="tab" onclick="showTab('facets')">Facet Gap</div>
    </div>
    
    <div class="content">
        <div class="why-section">
            <h2>Why This Dashboard</h2>
            <p class="placeholder">Add positioning text — how competitor analysis informs RDQ Layer 2 and the Facet Comparison dimension of the grounding sufficiency mission.</p>
        </div>
        
        <div id="framework" class="tab-content active">
            {get_rdq_framework_content()}
        </div>
        
        <div id="dimensions" class="tab-content">
            {get_gap_dimensions_content()}
        </div>
        
        <div id="state" class="tab-content">
            {get_current_state_content()}
        </div>
        
        <div id="facets" class="tab-content">
            {get_facet_gap_content()}
        </div>
    </div>
    
    <script>
        function showTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }}
    </script>
</body>
</html>
"""
    
    output_dir = PROJECT_ROOT / "output"
    output_dir.mkdir(exist_ok=True)
    report_path = output_dir / "rdq_grounding_dashboard.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ RDQ Dashboard generated: {report_path}")
    return report_path


if __name__ == "__main__":
    generate_dashboard()
