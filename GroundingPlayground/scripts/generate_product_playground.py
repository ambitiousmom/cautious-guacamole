"""
RDQ Product Playground Generator

An interactive reference tool for PMs to understand:
1. Current state of grounding data and POCs
2. Side-by-side competitor comparisons
3. Interactive query playground
4. Gap analysis and experiment ideas

Usage:
    python generate_product_playground.py
"""

from pathlib import Path
from datetime import datetime
import json

PROJECT_ROOT = Path(__file__).parent.parent


def get_sample_queries():
    """Sample queries with competitor responses for demonstration."""
    return [
        {
            "id": "Q01",
            "query": "Does Din Tai Fung Bellevue have outdoor seating?",
            "category": "Amenity Lookup",
            "bing": {
                "answer": "Based on reviews, Din Tai Fung in Bellevue may have limited outdoor seating options...",
                "source": "Review inference",
                "has_structured": False,
                "confidence": "Low"
            },
            "gemini": {
                "answer": "Yes, Din Tai Fung Bellevue has outdoor seating available.",
                "source": "Google Maps (structured boolean)",
                "has_structured": True,
                "confidence": "High",
                "raw_data": '["Outdoor seating", true]'
            },
            "perplexity": {
                "answer": "Din Tai Fung Bellevue offers outdoor seating according to recent visitor reports.",
                "source": "Web aggregation",
                "has_structured": False,
                "confidence": "Medium"
            },
            "chatgpt": {
                "answer": "I don't have real-time information about Din Tai Fung Bellevue's outdoor seating.",
                "source": "Training data (stale)",
                "has_structured": False,
                "confidence": "Low"
            },
            "gap_analysis": "Gemini has structured boolean data directly from Google Maps. Bing must infer from reviews.",
            "rdq_layer": "L2 - Richness"
        },
        {
            "id": "Q02", 
            "query": "What are the hours for Starbucks Reserve Roastery Seattle?",
            "category": "Hours Lookup",
            "bing": {
                "answer": "Starbucks Reserve Roastery Seattle is open 7am-11pm daily.",
                "source": "Licensed feed",
                "has_structured": True,
                "confidence": "High"
            },
            "gemini": {
                "answer": "Open today: 7:00 AM – 11:00 PM. See full hours on Google Maps.",
                "source": "Google Maps (structured)",
                "has_structured": True,
                "confidence": "High"
            },
            "perplexity": {
                "answer": "The Roastery is typically open 7am to 11pm, but hours may vary.",
                "source": "Web search",
                "has_structured": False,
                "confidence": "Medium"
            },
            "chatgpt": {
                "answer": "Hours are generally 7am-11pm but I recommend checking their website for current hours.",
                "source": "Training data",
                "has_structured": False,
                "confidence": "Low"
            },
            "gap_analysis": "Both Bing and Gemini have structured hours data. This is a strength.",
            "rdq_layer": "L1 - Coverage"
        },
        {
            "id": "Q03",
            "query": "Is The Walrus and the Carpenter good for a romantic dinner?",
            "category": "Vibe/Occasion",
            "bing": {
                "answer": "The Walrus and the Carpenter is a popular oyster bar... reviews mention intimate atmosphere...",
                "source": "Review synthesis (unstructured)",
                "has_structured": False,
                "confidence": "Medium"
            },
            "gemini": {
                "answer": "Yes, The Walrus and the Carpenter is noted as romantic and good for special occasions.",
                "source": "Google Maps attributes + review synthesis",
                "has_structured": True,
                "confidence": "High",
                "raw_data": '["Romantic", true], Occasion: "Anniversary-worthy"'
            },
            "perplexity": {
                "answer": "Many diners describe it as romantic with dim lighting and intimate seating.",
                "source": "Review aggregation",
                "has_structured": False,
                "confidence": "Medium"
            },
            "chatgpt": {
                "answer": "It's known for its intimate atmosphere, often recommended for dates.",
                "source": "Training data",
                "has_structured": False,
                "confidence": "Medium"
            },
            "gap_analysis": "Gemini has structured 'Occasion' insights. Bing infers from reviews without structured flags.",
            "rdq_layer": "L2 - Richness"
        },
        {
            "id": "Q04",
            "query": "What should I order at Canlis Seattle?",
            "category": "Menu Recommendation",
            "bing": {
                "answer": "Canlis is known for its tasting menu and seasonal dishes...",
                "source": "General description",
                "has_structured": False,
                "confidence": "Low"
            },
            "gemini": {
                "answer": "Popular dishes: Canlis Salad, Wagyu Beef, Peter Canlis Prawns. Most ordered: Tasting Menu.",
                "source": "Google Maps 'Most Ordered' + Tips",
                "has_structured": True,
                "confidence": "High",
                "raw_data": 'MostOrdered: ["Tasting Menu", "Canlis Salad"]'
            },
            "perplexity": {
                "answer": "The Canlis Salad is iconic. The tasting menu is highly recommended.",
                "source": "Review synthesis",
                "has_structured": False,
                "confidence": "Medium"
            },
            "chatgpt": {
                "answer": "Their Canlis Salad is legendary. Consider the chef's tasting menu.",
                "source": "Training data",
                "has_structured": False,
                "confidence": "Medium"
            },
            "gap_analysis": "Gemini has structured 'Most Ordered' data. Others rely on general knowledge or reviews.",
            "rdq_layer": "L2 - Richness"
        },
        {
            "id": "Q05",
            "query": "Does Trader Joe's Capitol Hill have parking?",
            "category": "Amenity Lookup",
            "bing": {
                "answer": "Trader Joe's on Capitol Hill has a small parking lot...",
                "source": "Web content",
                "has_structured": False,
                "confidence": "Medium"
            },
            "gemini": {
                "answer": "Yes, free parking lot available.",
                "source": "Google Maps (structured)",
                "has_structured": True,
                "confidence": "High",
                "raw_data": '["Parking", true], ["Free parking lot", true]'
            },
            "perplexity": {
                "answer": "There's a parking lot but it fills up quickly during peak hours.",
                "source": "Review synthesis",
                "has_structured": False,
                "confidence": "Medium"
            },
            "chatgpt": {
                "answer": "Most Trader Joe's locations have parking. Check specific location details.",
                "source": "Generic training data",
                "has_structured": False,
                "confidence": "Low"
            },
            "gap_analysis": "Gemini has structured parking attributes. Bing lacks this structured data.",
            "rdq_layer": "L2 - Richness"
        }
    ]


def get_poc_inventory():
    """POC inventory with product-friendly descriptions and real sample outputs."""
    return [
        {
            "name": "AI Enrichment",
            "owner": "adric",
            "location": "dev/adric/AI_Enrichment/",
            "what_it_does": "Uses GPT-5 to generate rich descriptions, amenities, and highlights from web content. Processes entity HTML through LLM batch inference pipelines.",
            "how_it_works": "Web HTML → Prompt Injection → GPT-5 Batch → Parse Response → Structured Output",
            "sample_input": '''Raw HTML: "<div class='about'>Upscale farm-to-table restaurant featuring seasonal Pacific Northwest cuisine...</div>"''',
            "sample_output": '''{
  "description": "Upscale farm-to-table restaurant with seasonal tasting menus featuring local Pacific Northwest ingredients",
  "highlights": ["🍷 Award-winning wine list", "👨‍🍳 Chef's Table experience", "🌿 Farm partnerships"],
  "amenities": ["Outdoor patio", "Private dining", "Wheelchair accessible"]
}''',
            "key_files": ["Scope/FeatureGeneration/", "Scope/Evaluation/", "AML/*.yml"],
            "rdq_contribution": "L2 - Generates rich facets that could answer vibe/occasion queries",
            "status": "Active POC",
            "gap_addressed": "Could provide 'Tips' and 'Highlights' like Gemini",
            "blocker": "Encumbrance TBD - can AI-generated content be used for grounding?"
        },
        {
            "name": "Facet Extraction",
            "owner": "jkjolbro",
            "location": "dev/jkjolbro/QualityMeasurementLLM/",
            "what_it_does": "Extracts structured amenities and facets from review text using ML models. Converts unstructured text into confidence-scored boolean signals.",
            "how_it_works": "Reviews → Sentence Parsing → LLM Classification → Facet Scores → Threshold → Boolean Flags",
            "sample_input": '''"Great outdoor patio with nice views. Kid-friendly too! The wifi was fast."''',
            "sample_output": '''{
  "outdoor_seating": {"count": 5, "confidence": 0.92},
  "kid_friendly": {"count": 3, "confidence": 0.87},
  "wifi": {"count": 2, "confidence": 0.78}
}''',
            "key_files": ["Facet-Extraction/", "Richness-Analysis/"],
            "rdq_contribution": "L2 - Converts unstructured reviews into structured boolean signals",
            "status": "Active POC",
            "gap_addressed": "Could provide structured amenity flags like Google Maps",
            "blocker": "Confidence thresholds - when is 0.78 good enough to say 'true'?"
        },
        {
            "name": "Richness Model",
            "owner": "adrianaf",
            "location": "dev/adrianaf/RichnessModel/",
            "what_it_does": "Scores how 'rich' an entity's content is using XLM-RoBERTa trained on GPT-4o annotations. Helps prioritize which entities need enrichment.",
            "how_it_works": "Entity Content → XLM-RoBERTa → Probability Scores per Category → Aggregate Richness Score",
            "sample_input": '''Entity page with: name, description, 50 reviews, 10 photos, hours, menu''',
            "sample_output": '''{
  "prob_name": 0.92,
  "prob_description": 0.87,
  "prob_reviews": 0.75,
  "prob_menu": 0.68,
  "prob_amenities": 0.45,
  "richness_score": 0.78
}''',
            "key_files": ["ModelTraining/", "ModelInference/", "PrepareData/"],
            "rdq_contribution": "L1/L2 - Identifies entities that need enrichment based on content gaps",
            "status": "Active - Ready for Production",
            "gap_addressed": "Prioritization - which entities to enrich first",
            "blocker": "None - ready for production use"
        },
        {
            "name": "WrapStar / Schema.org",
            "owner": "N/A (Production System)",
            "location": "src/Features/StructuredData/",
            "what_it_does": "Extracts structured data from website Schema.org markup and WrapStar wrappers. Gets hours, ratings, price range, services directly from source.",
            "how_it_works": "Web Crawl → HTML Parsing → Schema.org/WrapStar Detection → Structured Extraction → Normalized Output",
            "sample_input": '''<script type="application/ld+json">{"@type": "LocalBusiness", "openingHours": "Mo-Fr 09:00-17:00"}</script>''',
            "sample_output": '''{
  "Type": "LocalBusiness",
  "Name": "Above10 Apparel LLC",
  "Hours": "Mon-Fri 9:00-17:00",
  "Rating": 4.5,
  "PriceRange": "$$",
  "Image": "https://..."
}''',
            "key_files": ["StructuredData.Providers.WrapStar/", "StructuredData.Filters/"],
            "rdq_contribution": "L1/L2 - Structured attributes directly from authoritative source",
            "status": "Production",
            "gap_addressed": "Hours, ratings, basic structured attributes",
            "blocker": "RequiresAttribution encumbrance - limits grounding use without citation"
        },
        {
            "name": "Entity Discovery",
            "owner": "adrianaf",
            "location": "dev/adrianaf/EntityDiscovery/",
            "what_it_does": "Discovers new business entities from web content using LLM to extract entity candidates from SLAPI logs and blog posts.",
            "how_it_works": "SLAPI Logs → Filter URLs → Content Extraction → LLM Prompt → Entity Candidate → Validation",
            "sample_input": '''Blog post: "Exciting news! Coastal Kitchen is opening at 123 Main St next month..."''',
            "sample_output": '''{
  "entity_candidate": {
    "name": "Coastal Kitchen",
    "address": "123 Main St",
    "type": "Restaurant",
    "confidence": 0.89
  }
}''',
            "key_files": ["001_FilterKURLs_SLAPILogs.script", "004_InjectPrompt.script"],
            "rdq_contribution": "L1 - Expands entity coverage for new/niche businesses",
            "status": "Active POC",
            "gap_addressed": "Coverage gaps for newly opened or niche businesses",
            "blocker": "Validation pipeline needed before adding to production index"
        },
        {
            "name": "AI Enrichment - SLM",
            "owner": "penglinhuang",
            "location": "dev/penglinhuang/AIEnrichment/",
            "what_it_does": "Same as AI Enrichment but uses Gemma-3 (Small Language Model) instead of GPT-5 for cost reduction while maintaining quality.",
            "how_it_works": "Web HTML → Prompt Injection → Gemma-3 (fine-tuned) → Parse Response → Structured Output (90% cost reduction)",
            "sample_input": '''Raw HTML: "<div class='info'>Cozy neighborhood café serving artisan coffee and fresh pastries...</div>"''',
            "sample_output": '''{
  "description": "Neighborhood café with artisan coffee and fresh-baked pastries",
  "highlights": ["☕ House-roasted beans", "🥐 Fresh pastries daily"],
  "amenities": ["WiFi", "Outdoor seating"]
}''',
            "key_files": ["SLM-Gemma3/FineTuning/", "SLM-Gemma3/Inference/"],
            "rdq_contribution": "L2 - Enables scaling AI Enrichment to more entities",
            "status": "In Progress",
            "gap_addressed": "Cost barrier to running AI Enrichment on all entities",
            "blocker": "Quality validation vs GPT-5 baseline in progress"
        }
    ]


def get_experiments():
    """Potential experiments based on gaps."""
    return [
        {
            "id": "EXP-01",
            "title": "Structured Boolean Extraction from Reviews",
            "hypothesis": "We can match Google's structured amenity flags by extracting booleans from review text with high confidence",
            "gap_addressed": "Gemini has 'Outdoor seating: true' - we infer from reviews",
            "approach": "Extend Facet Extraction POC to output boolean flags when confidence > 0.9",
            "success_metric": "90% precision on amenity flags vs. Google ground truth",
            "rdq_impact": "L2 - Direct facet parity",
            "effort": "Medium",
            "encumbrance_risk": "Low - derived from our review data"
        },
        {
            "id": "EXP-02",
            "title": "AI-Generated 'Tips' and 'Most Ordered'",
            "hypothesis": "LLM can synthesize review highlights into Gemini-style 'Tips' and 'Most Ordered' insights",
            "gap_addressed": "Gemini shows 'Most Ordered: Tasting Menu' - we don't surface this",
            "approach": "Add prompts to AI Enrichment for menu/tip extraction",
            "success_metric": "User preference for AI-tips vs. no tips in A/B test",
            "rdq_impact": "L2 - Rich insights",
            "effort": "Low - prompt engineering",
            "encumbrance_risk": "Medium - AI-generated content policy unclear"
        },
        {
            "id": "EXP-03",
            "title": "Review Summarization for Vibe/Occasion",
            "hypothesis": "We can answer 'Is this good for X?' queries by summarizing relevant reviews",
            "gap_addressed": "Gemini has 'Romantic: true', 'Good for groups: true'",
            "approach": "Cluster reviews by occasion/vibe, generate structured signals",
            "success_metric": "Match human labels for occasion suitability",
            "rdq_impact": "L2 - Occasion facets",
            "effort": "Medium",
            "encumbrance_risk": "Low - synthesis from multiple reviews"
        },
        {
            "id": "EXP-04",
            "title": "Grounding-Ready Encumbrance Classification",
            "hypothesis": "We can classify which content is safe for Copilot grounding",
            "gap_addressed": "We have rich data but unclear what's grounding-ready",
            "approach": "Audit top providers for encumbrance, create whitelist",
            "success_metric": "Clear grounding policy per data source",
            "rdq_impact": "L1/L2/L3 - Unlocks existing data for grounding",
            "effort": "High - legal/policy work",
            "encumbrance_risk": "N/A - this IS the encumbrance work"
        },
        {
            "id": "EXP-05",
            "title": "Competitive Facet Parity Tracking",
            "hypothesis": "Automated tracking of facet gaps vs. competitors enables prioritization",
            "gap_addressed": "Manual competitor analysis doesn't scale",
            "approach": "Build pipeline: sample queries → competitor responses → facet extraction → gap report",
            "success_metric": "Weekly facet parity dashboard",
            "rdq_impact": "L2 - Measurement",
            "effort": "Medium",
            "encumbrance_risk": "Low - competitive intelligence"
        },
        {
            "id": "EXP-06",
            "title": "SLM Cost Reduction for Enrichment",
            "hypothesis": "Gemma-3 can produce 80% of GPT-5 quality at 10% of cost",
            "gap_addressed": "AI Enrichment too expensive to scale to all entities",
            "approach": "A/B test SLM vs. GPT-5 outputs on quality metrics",
            "success_metric": "Quality parity at lower cost",
            "rdq_impact": "L2 - Scale",
            "effort": "In Progress (penglinhuang)",
            "encumbrance_risk": "Same as GPT-5"
        }
    ]


def generate_playground():
    """Generate the RDQ Product Playground HTML."""
    
    sample_queries = get_sample_queries()
    poc_inventory = get_poc_inventory()
    experiments = get_experiments()
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RDQ Product Playground</title>
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
            --success: #6b8e6b;
            --warning: #8e8a6b;
            --error: #8e6b6b;
        }}
        
        * {{ box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', -apple-system, sans-serif;
            margin: 0; padding: 0;
            background: var(--purple-wash);
            color: var(--text-primary);
            line-height: 1.6;
        }}
        
        /* Header */
        .header {{
            background: linear-gradient(135deg, var(--purple-dark), var(--purple-mid));
            color: var(--white);
            padding: 20px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .header h1 {{ margin: 0; font-size: 1.3em; font-weight: 500; }}
        .header .tagline {{ opacity: 0.8; font-size: 0.85em; font-weight: 300; }}
        
        /* Navigation */
        .nav {{
            background: var(--white);
            border-bottom: 1px solid var(--border);
            padding: 0 40px;
            display: flex;
            gap: 0;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .nav-item {{
            padding: 14px 24px;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            font-size: 0.88em;
            color: var(--text-secondary);
            transition: all 0.2s;
        }}
        .nav-item:hover {{ color: var(--purple-dark); }}
        .nav-item.active {{ color: var(--purple-dark); border-bottom-color: var(--purple-mid); font-weight: 500; }}
        
        /* Main content */
        .main {{ padding: 32px 40px; max-width: 1400px; margin: 0 auto; }}
        .section {{ display: none; }}
        .section.active {{ display: block; }}
        
        /* Cards */
        .card {{
            background: var(--white);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            border: 1px solid var(--border);
        }}
        .card h2 {{ margin: 0 0 8px 0; font-size: 1.1em; font-weight: 500; }}
        .card .subtitle {{ color: var(--text-secondary); font-size: 0.9em; margin-bottom: 20px; }}
        .card h3 {{ margin: 20px 0 12px 0; font-size: 1em; font-weight: 500; }}
        
        /* Index cards */
        .index-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }}
        .index-card {{
            background: var(--white);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 20px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .index-card:hover {{ border-color: var(--purple-mid); transform: translateY(-2px); }}
        .index-card .number {{ font-size: 2em; font-weight: 300; color: var(--purple-mid); }}
        .index-card .label {{ font-size: 0.85em; color: var(--text-secondary); margin-top: 4px; }}
        .index-card .detail {{ font-size: 0.8em; color: var(--text-muted); margin-top: 8px; }}
        
        /* Insights list */
        .insight-item {{
            display: flex;
            gap: 16px;
            padding: 16px 0;
            border-bottom: 1px solid var(--border);
        }}
        .insight-item:last-child {{ border-bottom: none; }}
        .insight-icon {{
            width: 40px; height: 40px;
            background: var(--purple-pale);
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.2em;
            flex-shrink: 0;
        }}
        .insight-content {{ flex: 1; }}
        .insight-title {{ font-weight: 500; margin-bottom: 4px; }}
        .insight-desc {{ font-size: 0.88em; color: var(--text-secondary); }}
        
        /* Flow diagram */
        .flow-container {{
            background: var(--purple-wash);
            border-radius: 12px;
            padding: 24px;
            margin: 20px 0;
        }}
        .flow-row {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin: 16px 0;
        }}
        .flow-box {{
            background: var(--white);
            border: 1px solid var(--purple-light);
            border-radius: 8px;
            padding: 12px 20px;
            font-size: 0.88em;
            text-align: center;
        }}
        .flow-box.highlight {{ background: var(--purple-pale); border-color: var(--purple-mid); }}
        .flow-arrow {{ color: var(--purple-light); font-size: 1.5em; }}
        .flow-label {{
            text-align: center;
            font-size: 0.75em;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }}
        
        /* POC Detail Cards */
        .poc-detail {{
            background: var(--white);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
        }}
        .poc-detail-header {{
            margin-bottom: 16px;
        }}
        .poc-name-large {{
            font-size: 1.1em;
            font-weight: 500;
            margin-right: 12px;
        }}
        .poc-owner {{
            font-size: 0.82em;
            color: var(--text-muted);
            margin-top: 6px;
        }}
        .poc-owner code {{
            background: var(--purple-wash);
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.9em;
        }}
        .poc-status {{
            font-size: 0.75em;
            padding: 3px 12px;
            border-radius: 12px;
            background: var(--purple-pale);
            color: var(--purple-dark);
        }}
        .poc-description {{
            font-size: 0.92em;
            color: var(--text-secondary);
            margin-bottom: 16px;
            line-height: 1.5;
        }}
        .poc-flow {{
            background: var(--purple-wash);
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 16px;
        }}
        .poc-flow-label {{
            font-size: 0.75em;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }}
        .poc-flow-steps {{
            font-size: 0.88em;
            color: var(--purple-dark);
            font-family: monospace;
        }}
        .poc-samples-row {{
            display: flex;
            gap: 16px;
            align-items: stretch;
            margin-bottom: 16px;
        }}
        .poc-sample-box {{
            flex: 1;
            background: var(--purple-wash);
            border-radius: 8px;
            padding: 12px;
            overflow-x: auto;
        }}
        .poc-sample-box.output {{
            background: #f0f8f0;
        }}
        .poc-sample-box pre {{
            margin: 0;
            font-size: 0.78em;
            white-space: pre-wrap;
            word-break: break-word;
            font-family: 'Consolas', 'Monaco', monospace;
        }}
        .poc-sample-arrow {{
            display: flex;
            align-items: center;
            font-size: 1.5em;
            color: var(--purple-light);
        }}
        .poc-sample-label {{
            font-size: 0.72em;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        .poc-footer {{
            display: flex;
            gap: 24px;
            font-size: 0.85em;
            color: var(--text-secondary);
            margin-bottom: 12px;
        }}
        .poc-contribution, .poc-gap {{
            flex: 1;
        }}
        .poc-blocker {{ 
            padding: 12px 16px; 
            background: #faf5f5; 
            border-radius: 8px; 
            font-size: 0.85em;
            border-left: 3px solid var(--error);
            color: var(--text-secondary);
        }}
        
        /* Legacy POC cards (keep for compatibility) */
        .poc-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }}
        .poc-card {{
            background: var(--white);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 20px;
        }}
        .poc-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }}
        .poc-name {{ font-weight: 500; }}
        .poc-desc {{ font-size: 0.88em; color: var(--text-secondary); margin-bottom: 12px; }}
        .poc-sample {{
            background: var(--purple-wash);
            border-radius: 8px;
            padding: 12px;
            font-size: 0.82em;
            margin-bottom: 12px;
        }}
        .poc-meta {{ display: flex; gap: 16px; font-size: 0.82em; color: var(--text-muted); }}
        .poc-blocker {{ 
            margin-top: 12px; 
            padding: 10px 12px; 
            background: #f8f4f4; 
            border-radius: 6px; 
            font-size: 0.82em;
            border-left: 3px solid var(--error);
        }}
        
        /* Competitor comparison */
        .query-selector {{
            background: var(--white);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 20px;
        }}
        .query-selector label {{ font-weight: 500; margin-right: 12px; }}
        .query-selector select {{
            padding: 8px 16px;
            border: 1px solid var(--border);
            border-radius: 6px;
            font-size: 0.9em;
            min-width: 400px;
        }}
        
        .comparison-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
        }}
        .competitor-card {{
            background: var(--white);
            border: 1px solid var(--border);
            border-radius: 10px;
            overflow: hidden;
        }}
        .competitor-header {{
            padding: 12px 16px;
            font-weight: 500;
            font-size: 0.9em;
            border-bottom: 1px solid var(--border);
        }}
        .competitor-header.bing {{ background: #e8f4e8; }}
        .competitor-header.gemini {{ background: #e8e8f4; }}
        .competitor-header.perplexity {{ background: #f4e8e8; }}
        .competitor-header.chatgpt {{ background: #f4f4e8; }}
        .competitor-body {{ padding: 16px; }}
        .competitor-answer {{ font-size: 0.9em; margin-bottom: 12px; line-height: 1.5; }}
        .competitor-meta {{ font-size: 0.8em; color: var(--text-muted); }}
        .competitor-meta-row {{ display: flex; justify-content: space-between; margin: 4px 0; }}
        .has-structured {{ color: var(--success); }}
        .no-structured {{ color: var(--error); }}
        .raw-data {{
            margin-top: 12px;
            padding: 10px;
            background: var(--purple-wash);
            border-radius: 6px;
            font-family: monospace;
            font-size: 0.8em;
            word-break: break-all;
        }}
        
        .gap-callout {{
            margin-top: 20px;
            padding: 16px 20px;
            background: linear-gradient(135deg, var(--purple-pale), var(--purple-wash));
            border-radius: 10px;
            border-left: 4px solid var(--purple-mid);
        }}
        .gap-callout-title {{ font-weight: 500; margin-bottom: 8px; }}
        .gap-callout-text {{ font-size: 0.9em; color: var(--text-secondary); }}
        .rdq-tag {{
            display: inline-block;
            padding: 2px 8px;
            background: var(--purple-mid);
            color: var(--white);
            border-radius: 10px;
            font-size: 0.75em;
            margin-left: 8px;
        }}
        
        /* Playground */
        .playground-input {{
            background: var(--white);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .playground-input input {{
            width: 100%;
            padding: 12px 16px;
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 1em;
            margin-bottom: 12px;
        }}
        .playground-input input:focus {{ outline: none; border-color: var(--purple-mid); }}
        .playground-btn {{
            background: var(--purple-mid);
            color: var(--white);
            border: none;
            padding: 10px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9em;
        }}
        .playground-btn:hover {{ background: var(--purple-dark); }}
        
        .playground-results {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
        }}
        .playground-card {{
            background: var(--white);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px;
            min-height: 200px;
        }}
        .playground-card-header {{
            font-weight: 500;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border);
        }}
        .playground-placeholder {{
            color: var(--text-muted);
            font-size: 0.9em;
            font-style: italic;
        }}
        
        /* Experiments */
        .experiment-card {{
            background: var(--white);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 16px;
        }}
        .experiment-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 12px;
        }}
        .experiment-id {{ 
            font-size: 0.75em; 
            color: var(--text-muted); 
            margin-bottom: 4px; 
        }}
        .experiment-title {{ font-weight: 500; }}
        .experiment-effort {{
            font-size: 0.75em;
            padding: 3px 10px;
            border-radius: 12px;
            background: var(--purple-pale);
            color: var(--purple-dark);
        }}
        .experiment-body {{ font-size: 0.9em; }}
        .experiment-row {{ margin: 8px 0; }}
        .experiment-label {{ font-weight: 500; color: var(--text-secondary); }}
        .experiment-tags {{ display: flex; gap: 8px; margin-top: 12px; }}
        .experiment-tag {{
            font-size: 0.75em;
            padding: 3px 10px;
            border-radius: 12px;
        }}
        .experiment-tag.rdq {{ background: var(--purple-pale); color: var(--purple-dark); }}
        .experiment-tag.risk-low {{ background: #e8f4e8; color: var(--success); }}
        .experiment-tag.risk-medium {{ background: #f4f4e8; color: var(--warning); }}
        .experiment-tag.risk-high {{ background: #f4e8e8; color: var(--error); }}
        
        /* Tables */
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px 16px; text-align: left; border-bottom: 1px solid var(--border); font-size: 0.88em; }}
        th {{ background: var(--purple-wash); font-weight: 500; }}
        
        /* Utilities */
        .text-muted {{ color: var(--text-muted); }}
        .text-small {{ font-size: 0.85em; }}
        .mt-20 {{ margin-top: 20px; }}
        .mb-20 {{ margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>RDQ Product Playground</h1>
            <div class="tagline">Rich Data Quorum - PM Reference for Rich Data for Grounding</div>
        </div>
        <div class="text-small" style="opacity: 0.7;">{datetime.now().strftime('%Y-%m-%d')}</div>
    </div>
    
    <!-- INTRO SECTION -->
    <div style="background: linear-gradient(135deg, var(--purple-pale), var(--purple-wash)); padding: 24px 40px; border-bottom: 1px solid var(--border);">
        <div style="max-width: 1000px;">
            <h2 style="margin: 0 0 12px 0; font-size: 1.1em; font-weight: 500; color: var(--purple-dark);">What is this?</h2>
            <p style="margin: 0 0 12px 0; font-size: 0.92em; color: var(--text-secondary); line-height: 1.6;">
                This is a <strong>PM reference tool</strong> for understanding current state of things and gaps from RDQ and Grounding Data point of view. 
                It documents what POCs have been built, where gaps exist vs. competitors, and what experiments could close those gaps.
            </p>
            <h2 style="margin: 16px 0 12px 0; font-size: 1.1em; font-weight: 500; color: var(--purple-dark);">What should you expect?</h2>
            <ul style="margin: 0; padding-left: 20px; font-size: 0.92em; color: var(--text-secondary); line-height: 1.8;">
                <li><strong>Current State</strong> — Overview of RDQ framework, POC inventory with sample inputs/outputs, and encumbrance constraints</li>
                <li><strong>Competitor Lab</strong> — Side-by-side comparisons showing exactly where Gemini/ChatGPT have structured data we lack</li>
                <li><strong>Playground</strong> — Test any query to see which competitor likely wins and why</li>
                <li><strong>Experiments</strong> — Prioritized list of experiments to close identified gaps</li>
            </ul>
        </div>
    </div>
    
    <div class="nav">
        <div class="nav-item active" onclick="showSection('current-state')">Current State</div>
        <div class="nav-item" onclick="showSection('competitor-lab')">Competitor Lab</div>
        <div class="nav-item" onclick="showSection('playground')">Playground</div>
        <div class="nav-item" onclick="showSection('experiments')">Experiments</div>
    </div>
    
    <div class="main">
        <!-- CURRENT STATE SECTION (includes Overview) -->
        <div id="current-state" class="section active">
            
            <!-- Overview subsection -->
            <div class="card">
                <h2>Overview</h2>
                <div class="subtitle">Quick index and key insights</div>
                
                <div class="index-grid">
                    <div class="index-card" onclick="scrollToElement('poc-section')">
                        <div class="number">{len(poc_inventory)}</div>
                        <div class="label">Active POCs</div>
                        <div class="detail">AI Enrichment, Facet Extraction, etc.</div>
                    </div>
                    <div class="index-card" onclick="showSection('competitor-lab')">
                        <div class="number">{len(sample_queries)}</div>
                        <div class="label">Sample Queries</div>
                        <div class="detail">Side-by-side competitor analysis</div>
                    </div>
                    <div class="index-card" onclick="showSection('experiments')">
                        <div class="number">{len(experiments)}</div>
                        <div class="label">Experiment Ideas</div>
                        <div class="detail">Prioritized by RDQ impact</div>
                    </div>
                    <div class="index-card" onclick="showSection('playground')">
                        <div class="number">4</div>
                        <div class="label">Competitors</div>
                        <div class="detail">Bing, Gemini, Perplexity, ChatGPT</div>
                    </div>
                </div>
                
                <h3>RDQ Perspective</h3>
                <p style="font-size: 0.88em; color: var(--text-secondary); margin-bottom: 16px;">RDQ (Rich Data Quorum) measures grounding data quality across 3 layers: Coverage, Richness, and Sufficiency. Here's where we stand:</p>
                
                <h3>Key Insights (State of Things)</h3>
                <div class="insight-item">
                    <div class="insight-icon">1</div>
                    <div class="insight-content">
                        <div class="insight-title">Layer 1 (Coverage) is strong — we have broad entity coverage</div>
                        <div class="insight-desc">Our index covers most entities with basic attributes: name, address, hours, ratings, photos, and reviews. This is foundational grounding data.</div>
                    </div>
                </div>
                <div class="insight-item">
                    <div class="insight-icon">2</div>
                    <div class="insight-content">
                        <div class="insight-title">Layer 2 (Richness) has gaps — structured amenities and facets are sparse</div>
                        <div class="insight-desc">We lack structured boolean flags for amenities (outdoor seating, parking, WiFi) and occasion signals (romantic, kid-friendly). This data exists in reviews but isn't extracted.</div>
                    </div>
                </div>
                <div class="insight-item">
                    <div class="insight-icon">3</div>
                    <div class="insight-content">
                        <div class="insight-title">6 POCs are actively working on Richness — but encumbrance blocks production</div>
                        <div class="insight-desc">AI Enrichment, Facet Extraction, and other POCs can generate rich content. However, legal/policy classification for grounding use hasn't been finalized.</div>
                    </div>
                </div>
                <div class="insight-item">
                    <div class="insight-icon">4</div>
                    <div class="insight-content">
                        <div class="insight-title">Layer 3 (Sufficiency) is unmeasured — unclear if Copilot uses available data</div>
                        <div class="insight-desc">Even where we have grounding-ready data, we don't yet measure whether Copilot retrieves and uses it effectively. This is a measurement gap.</div>
                    </div>
                </div>
            </div>
            
            <!-- RDQ Framework -->
            <div class="card">
                <h2>RDQ Framework</h2>
                <div class="subtitle">How we measure grounding data quality</div>
                
                <div class="flow-container">
                    <div class="flow-label">Priority Order</div>
                    <div class="flow-row">
                        <div class="flow-box highlight">Layer 1: Coverage</div>
                        <div class="flow-arrow">→</div>
                        <div class="flow-box">Layer 2: Richness</div>
                        <div class="flow-arrow">→</div>
                        <div class="flow-box">Layer 3: Sufficiency</div>
                    </div>
                    <div style="text-align: center; margin-top: 16px; font-size: 0.85em; color: var(--text-secondary);">
                        Do we have enough? → Can we answer rich queries? → Does Copilot use it well?
                    </div>
                </div>
                
                <table class="mt-20">
                    <tr>
                        <th>Layer</th>
                        <th>Question</th>
                        <th>Metrics</th>
                        <th>Status</th>
                    </tr>
                    <tr>
                        <td><strong>L1: Coverage</strong></td>
                        <td>Do we have content for entities?</td>
                        <td>Review count, photo count, URL coverage</td>
                        <td style="color: var(--success);">Good</td>
                    </tr>
                    <tr>
                        <td><strong>L2: Richness</strong></td>
                        <td>Can we answer faceted queries?</td>
                        <td>Amenity flags, occasion signals, tips</td>
                        <td style="color: var(--warning);">Gap</td>
                    </tr>
                    <tr>
                        <td><strong>L3: Sufficiency</strong></td>
                        <td>Does Copilot serve it well?</td>
                        <td>Grounding hit rate, answer quality</td>
                        <td style="color: var(--text-muted);">Unknown</td>
                    </tr>
                </table>
            </div>
            
            <!-- Data Flow -->
            <div class="card">
                <h2>Data Flow</h2>
                <div class="subtitle">How data moves from sources through POCs to grounding</div>
                
                <div class="flow-container">
                    <div class="flow-label">Sources</div>
                    <div class="flow-row">
                        <div class="flow-box">Web HTML</div>
                        <div class="flow-box">Licensed Feeds</div>
                        <div class="flow-box">Reviews</div>
                        <div class="flow-box">Schema.org</div>
                    </div>
                    
                    <div class="flow-row"><div class="flow-arrow">↓</div></div>
                    
                    <div class="flow-label">Processing (POCs)</div>
                    <div class="flow-row">
                        <div class="flow-box highlight">AI Enrichment</div>
                        <div class="flow-box highlight">Facet Extraction</div>
                        <div class="flow-box highlight">WrapStar</div>
                        <div class="flow-box highlight">Richness Model</div>
                    </div>
                    
                    <div class="flow-row"><div class="flow-arrow">↓</div></div>
                    
                    <div class="flow-label">Enriched Attributes</div>
                    <div class="flow-row">
                        <div class="flow-box">DescriptionAI</div>
                        <div class="flow-box">AmenitiesAI</div>
                        <div class="flow-box">FacetScores</div>
                        <div class="flow-box">Hours/Rating</div>
                    </div>
                    
                    <div class="flow-row"><div class="flow-arrow">↓</div></div>
                    
                    <div class="flow-label">Grounding Layer</div>
                    <div class="flow-row">
                        <div class="flow-box" style="border-color: var(--error);">Encumbrance Filter</div>
                        <div class="flow-arrow">→</div>
                        <div class="flow-box highlight">Copilot Grounding</div>
                    </div>
                </div>
            </div>
            
            <!-- POC Inventory -->
            <div id="poc-section" class="card">
                <h2>POC Inventory</h2>
                <div class="subtitle">What's been built, how it works, and sample outputs</div>
                
                {"".join(f'''
                <div class="poc-detail">
                    <div class="poc-detail-header">
                        <div>
                            <span class="poc-name-large">{poc['name']}</span>
                            <span class="poc-status">{poc['status']}</span>
                        </div>
                        <div class="poc-owner">Owner: {poc['owner']} &nbsp;|&nbsp; Location: <code>{poc['location']}</code></div>
                    </div>
                    
                    <div class="poc-description">{poc['what_it_does']}</div>
                    
                    <div class="poc-flow">
                        <div class="poc-flow-label">How it works</div>
                        <div class="poc-flow-steps">{poc['how_it_works']}</div>
                    </div>
                    
                    <div class="poc-samples-row">
                        <div class="poc-sample-box">
                            <div class="poc-sample-label">Sample Input</div>
                            <pre>{poc['sample_input']}</pre>
                        </div>
                        <div class="poc-sample-arrow">→</div>
                        <div class="poc-sample-box output">
                            <div class="poc-sample-label">Sample Output</div>
                            <pre>{poc['sample_output']}</pre>
                        </div>
                    </div>
                    
                    <div class="poc-footer">
                        <div class="poc-contribution"><strong>RDQ Contribution:</strong> {poc['rdq_contribution']}</div>
                        <div class="poc-gap"><strong>Gap Addressed:</strong> {poc['gap_addressed']}</div>
                    </div>
                    
                    <div class="poc-blocker">
                        <strong>Blocker:</strong> {poc['blocker']}
                    </div>
                </div>
                ''' for poc in poc_inventory)}
            </div>
            
            <!-- Encumbrance -->
            <div class="card">
                <h2>Encumbrance Reality</h2>
                <div class="subtitle">What data can actually be used for Copilot grounding?</div>
                
                <table>
                    <tr>
                        <th>Encumbrance Level</th>
                        <th>Can Ground?</th>
                        <th>Example Sources</th>
                        <th>Impact</th>
                    </tr>
                    <tr>
                        <td><span style="background: var(--purple-pale); padding: 2px 10px; border-radius: 10px;">Factual</span></td>
                        <td style="color: var(--success);">Yes</td>
                        <td>Basic facts, hours, address</td>
                        <td>Full RDQ contribution</td>
                    </tr>
                    <tr>
                        <td><span style="background: #f4f4e8; padding: 2px 10px; border-radius: 10px;">RequiresAttribution</span></td>
                        <td style="color: var(--warning);">With citation</td>
                        <td>WrapStar, Schema.org extracts</td>
                        <td>Partial — needs citation UX</td>
                    </tr>
                    <tr>
                        <td><span style="background: #f4e8e8; padding: 2px 10px; border-radius: 10px;">Restricted</span></td>
                        <td style="color: var(--error);">No</td>
                        <td>Licensed feeds with restrictions</td>
                        <td>Zero grounding value</td>
                    </tr>
                    <tr>
                        <td><span style="background: var(--border); padding: 2px 10px; border-radius: 10px;">AI-Generated (TBD)</span></td>
                        <td>?</td>
                        <td>AI Enrichment POC outputs</td>
                        <td>Blocked until policy decision</td>
                    </tr>
                </table>
                
                <div class="gap-callout mt-20">
                    <div class="gap-callout-title">Key Insight</div>
                    <div class="gap-callout-text">We may have high RDQ Layer 1 (coverage) but low "grounding-ready" coverage because much of our rich data has encumbrance restrictions. This is a critical blocker for competitive parity.</div>
                </div>
            </div>
        </div>
        
        <!-- COMPETITOR LAB SECTION -->
        <div id="competitor-lab" class="section">
            
            <!-- Competitor Insights Card -->
            <div class="card">
                <h2>Competitive Insights</h2>
                <div class="subtitle">Where competitors have an advantage and why</div>
                
                <div class="insight-item">
                    <div class="insight-icon">1</div>
                    <div class="insight-content">
                        <div class="insight-title">Gemini has structured boolean amenities — we infer from reviews</div>
                        <div class="insight-desc">Google Maps provides direct flags like "Outdoor seating: true". Bing must parse reviews to answer, leading to lower confidence and occasional errors.</div>
                    </div>
                </div>
                <div class="insight-item">
                    <div class="insight-icon">2</div>
                    <div class="insight-content">
                        <div class="insight-title">Gemini has "Most Ordered" and "Tips" — we don't surface menu insights</div>
                        <div class="insight-desc">Google shows crowd-sourced menu recommendations. For "What should I order at X?" queries, Gemini wins with specific dish suggestions.</div>
                    </div>
                </div>
                <div class="insight-item">
                    <div class="insight-icon">3</div>
                    <div class="insight-content">
                        <div class="insight-title">Gemini has Occasion signals (Romantic, Groups, etc.) — we have raw review text</div>
                        <div class="insight-desc">"Is this good for a romantic dinner?" — Gemini has structured occasion tags. We must synthesize from reviews, which is less reliable.</div>
                    </div>
                </div>
                <div class="insight-item">
                    <div class="insight-icon">4</div>
                    <div class="insight-content">
                        <div class="insight-title">Hours and basic info are at parity</div>
                        <div class="insight-desc">For hours, ratings, address, and phone — we match or exceed competitors. This is not a gap area.</div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2>Side-by-Side Comparison</h2>
                <div class="subtitle">See how competitors answer the same query</div>
                
                <div class="query-selector">
                    <label>Select Query:</label>
                    <select id="querySelect" onchange="showQuery(this.value)">
                        {"".join(f'<option value="{q["id"]}">{q["query"]}</option>' for q in sample_queries)}
                    </select>
                </div>
                
                {"".join(f'''
                <div id="query-{q['id']}" class="query-display" style="display: {'block' if i == 0 else 'none'};">
                    <div style="margin-bottom: 16px;">
                        <span style="background: var(--purple-wash); padding: 4px 12px; border-radius: 12px; font-size: 0.82em;">{q['category']}</span>
                    </div>
                    
                    <div class="comparison-grid">
                        <div class="competitor-card">
                            <div class="competitor-header bing">Bing / Copilot</div>
                            <div class="competitor-body">
                                <div class="competitor-answer">{q['bing']['answer']}</div>
                                <div class="competitor-meta">
                                    <div class="competitor-meta-row">
                                        <span>Source:</span>
                                        <span>{q['bing']['source']}</span>
                                    </div>
                                    <div class="competitor-meta-row">
                                        <span>Structured:</span>
                                        <span class="{'has-structured' if q['bing']['has_structured'] else 'no-structured'}">{'Yes' if q['bing']['has_structured'] else 'No'}</span>
                                    </div>
                                    <div class="competitor-meta-row">
                                        <span>Confidence:</span>
                                        <span>{q['bing']['confidence']}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="competitor-card">
                            <div class="competitor-header gemini">Gemini</div>
                            <div class="competitor-body">
                                <div class="competitor-answer">{q['gemini']['answer']}</div>
                                <div class="competitor-meta">
                                    <div class="competitor-meta-row">
                                        <span>Source:</span>
                                        <span>{q['gemini']['source']}</span>
                                    </div>
                                    <div class="competitor-meta-row">
                                        <span>Structured:</span>
                                        <span class="{'has-structured' if q['gemini']['has_structured'] else 'no-structured'}">{'Yes' if q['gemini']['has_structured'] else 'No'}</span>
                                    </div>
                                    <div class="competitor-meta-row">
                                        <span>Confidence:</span>
                                        <span>{q['gemini']['confidence']}</span>
                                    </div>
                                </div>
                                {f'<div class="raw-data">{q["gemini"].get("raw_data", "")}</div>' if q['gemini'].get('raw_data') else ''}
                            </div>
                        </div>
                        
                        <div class="competitor-card">
                            <div class="competitor-header perplexity">Perplexity</div>
                            <div class="competitor-body">
                                <div class="competitor-answer">{q['perplexity']['answer']}</div>
                                <div class="competitor-meta">
                                    <div class="competitor-meta-row">
                                        <span>Source:</span>
                                        <span>{q['perplexity']['source']}</span>
                                    </div>
                                    <div class="competitor-meta-row">
                                        <span>Structured:</span>
                                        <span class="{'has-structured' if q['perplexity']['has_structured'] else 'no-structured'}">{'Yes' if q['perplexity']['has_structured'] else 'No'}</span>
                                    </div>
                                    <div class="competitor-meta-row">
                                        <span>Confidence:</span>
                                        <span>{q['perplexity']['confidence']}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="competitor-card">
                            <div class="competitor-header chatgpt">ChatGPT</div>
                            <div class="competitor-body">
                                <div class="competitor-answer">{q['chatgpt']['answer']}</div>
                                <div class="competitor-meta">
                                    <div class="competitor-meta-row">
                                        <span>Source:</span>
                                        <span>{q['chatgpt']['source']}</span>
                                    </div>
                                    <div class="competitor-meta-row">
                                        <span>Structured:</span>
                                        <span class="{'has-structured' if q['chatgpt']['has_structured'] else 'no-structured'}">{'Yes' if q['chatgpt']['has_structured'] else 'No'}</span>
                                    </div>
                                    <div class="competitor-meta-row">
                                        <span>Confidence:</span>
                                        <span>{q['chatgpt']['confidence']}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="gap-callout">
                        <div class="gap-callout-title">Gap Analysis <span class="rdq-tag">{q['rdq_layer']}</span></div>
                        <div class="gap-callout-text">{q['gap_analysis']}</div>
                    </div>
                </div>
                ''' for i, q in enumerate(sample_queries))}
            </div>
            
            <div class="card">
                <h2>Summary by Query Type</h2>
                <div class="subtitle">Where do we win and where do we lose?</div>
                
                <table>
                    <tr>
                        <th>Query Type</th>
                        <th>Bing</th>
                        <th>Gemini</th>
                        <th>Gap</th>
                    </tr>
                    <tr>
                        <td>Hours / Basic Info</td>
                        <td style="color: var(--success);">✓ Structured</td>
                        <td style="color: var(--success);">✓ Structured</td>
                        <td>Parity</td>
                    </tr>
                    <tr>
                        <td>Amenity Lookup</td>
                        <td style="color: var(--warning);">⚠ Inferred</td>
                        <td style="color: var(--success);">✓ Structured Boolean</td>
                        <td style="color: var(--error);">Gemini wins</td>
                    </tr>
                    <tr>
                        <td>Vibe / Occasion</td>
                        <td style="color: var(--warning);">⚠ Review text</td>
                        <td style="color: var(--success);">✓ Occasion tags</td>
                        <td style="color: var(--error);">Gemini wins</td>
                    </tr>
                    <tr>
                        <td>Menu Recommendations</td>
                        <td style="color: var(--error);">✗ General only</td>
                        <td style="color: var(--success);">✓ "Most Ordered"</td>
                        <td style="color: var(--error);">Gemini wins</td>
                    </tr>
                </table>
            </div>
        </div>
        
        <!-- PLAYGROUND SECTION -->
        <div id="playground" class="section">
            <div class="card">
                <h2>Query Playground</h2>
                <div class="subtitle">Enter a query and compare how each competitor would respond</div>
                
                <div class="playground-input">
                    <input type="text" id="playgroundQuery" placeholder="Enter a local query, e.g., 'Does Cafe Allegro have wifi?'" />
                    <button class="playground-btn" onclick="runPlayground()">Analyze Query</button>
                </div>
                
                <div class="playground-results">
                    <div class="playground-card">
                        <div class="playground-card-header" style="background: #e8f4e8;">Bing / Copilot</div>
                        <div id="playground-bing" class="playground-placeholder">Enter a query above to see expected response...</div>
                    </div>
                    <div class="playground-card">
                        <div class="playground-card-header" style="background: #e8e8f4;">Gemini</div>
                        <div id="playground-gemini" class="playground-placeholder">Enter a query above to see expected response...</div>
                    </div>
                    <div class="playground-card">
                        <div class="playground-card-header" style="background: #f4e8e8;">Perplexity</div>
                        <div id="playground-perplexity" class="playground-placeholder">Enter a query above to see expected response...</div>
                    </div>
                    <div class="playground-card">
                        <div class="playground-card-header" style="background: #f4f4e8;">ChatGPT</div>
                        <div id="playground-chatgpt" class="playground-placeholder">Enter a query above to see expected response...</div>
                    </div>
                </div>
                
                <div id="playground-gap" class="gap-callout mt-20" style="display: none;">
                    <div class="gap-callout-title">RDQ Gap Analysis</div>
                    <div id="playground-gap-text" class="gap-callout-text"></div>
                </div>
            </div>
            
            <div class="card">
                <h2>How to Use This Playground</h2>
                <div class="subtitle">Instructions for collecting real competitor responses</div>
                
                <div style="font-size: 0.9em; color: var(--text-secondary);">
                    <p><strong>Step 1:</strong> Enter your query in the box above</p>
                    <p><strong>Step 2:</strong> Open each competitor in separate tabs:</p>
                    <ul>
                        <li><a href="https://www.bing.com/chat" target="_blank">Bing Copilot</a></li>
                        <li><a href="https://gemini.google.com" target="_blank">Gemini</a></li>
                        <li><a href="https://www.perplexity.ai" target="_blank">Perplexity</a></li>
                        <li><a href="https://chat.openai.com" target="_blank">ChatGPT</a></li>
                    </ul>
                    <p><strong>Step 3:</strong> Ask the same query in each and note the response</p>
                    <p><strong>Step 4:</strong> For Gemini, use DevTools (F12) → Network tab to capture structured data</p>
                    <p><strong>Step 5:</strong> Record findings and identify RDQ gaps</p>
                </div>
            </div>
        </div>
        
        <!-- EXPERIMENTS SECTION -->
        <div id="experiments" class="section">
            <div class="card">
                <h2>Potential Experiments</h2>
                <div class="subtitle">Prioritized ideas based on identified gaps</div>
                
                {"".join(f'''
                <div class="experiment-card">
                    <div class="experiment-header">
                        <div>
                            <div class="experiment-id">{exp['id']}</div>
                            <div class="experiment-title">{exp['title']}</div>
                        </div>
                        <span class="experiment-effort">{exp['effort']}</span>
                    </div>
                    <div class="experiment-body">
                        <div class="experiment-row">
                            <span class="experiment-label">Hypothesis:</span> {exp['hypothesis']}
                        </div>
                        <div class="experiment-row">
                            <span class="experiment-label">Gap Addressed:</span> {exp['gap_addressed']}
                        </div>
                        <div class="experiment-row">
                            <span class="experiment-label">Approach:</span> {exp['approach']}
                        </div>
                        <div class="experiment-row">
                            <span class="experiment-label">Success Metric:</span> {exp['success_metric']}
                        </div>
                    </div>
                    <div class="experiment-tags">
                        <span class="experiment-tag rdq">{exp['rdq_impact']}</span>
                        <span class="experiment-tag {'risk-low' if 'Low' in exp['encumbrance_risk'] else 'risk-medium' if 'Medium' in exp['encumbrance_risk'] else 'risk-high'}">Encumbrance: {exp['encumbrance_risk']}</span>
                    </div>
                </div>
                ''' for exp in experiments)}
            </div>
            
            <div class="card">
                <h2>What's Missing?</h2>
                <div class="subtitle">Areas not yet covered by experiments</div>
                
                <table>
                    <tr>
                        <th>Gap</th>
                        <th>Why It Matters</th>
                        <th>Potential Experiment</th>
                    </tr>
                    <tr>
                        <td>Real-time competitor monitoring</td>
                        <td>Gemini/Google can ship features faster than we can detect</td>
                        <td>Automated weekly facet comparison pipeline</td>
                    </tr>
                    <tr>
                        <td>User preference testing</td>
                        <td>We assume structured > inferred, but is that true?</td>
                        <td>A/B test structured vs. synthesized answers</td>
                    </tr>
                    <tr>
                        <td>International coverage</td>
                        <td>All examples are US — gaps may be larger globally</td>
                        <td>Run same experiments for EU/APAC entities</td>
                    </tr>
                    <tr>
                        <td>Freshness measurement</td>
                        <td>Stale data erodes trust even if coverage is high</td>
                        <td>Track data age vs. competitors</td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    
    <script>
        function showSection(sectionId) {{
            document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.getElementById(sectionId).classList.add('active');
            event.target.classList.add('active');
        }}
        
        function scrollToElement(id) {{
            const el = document.getElementById(id);
            if (el) {{
                el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }}
        }}
        
        function showQuery(queryId) {{
            document.querySelectorAll('.query-display').forEach(q => q.style.display = 'none');
            document.getElementById('query-' + queryId).style.display = 'block';
        }}
        
        function runPlayground() {{
            const query = document.getElementById('playgroundQuery').value;
            if (!query) return;
            
            // Simulate analysis (in real version, this would call APIs or show instructions)
            const queryLower = query.toLowerCase();
            let category = 'General';
            let gapText = '';
            
            if (queryLower.includes('outdoor') || queryLower.includes('parking') || queryLower.includes('wifi') || queryLower.includes('wheelchair')) {{
                category = 'Amenity Lookup';
                gapText = 'This is an AMENITY query. Gemini likely has structured boolean data from Google Maps. Bing would need to infer from reviews or web content, resulting in lower confidence.';
            }} else if (queryLower.includes('hour') || queryLower.includes('open') || queryLower.includes('close')) {{
                category = 'Hours Lookup';
                gapText = 'This is a HOURS query. Both Bing and Gemini likely have structured data for this. This is a parity area.';
            }} else if (queryLower.includes('romantic') || queryLower.includes('date') || queryLower.includes('kid') || queryLower.includes('group') || queryLower.includes('occasion')) {{
                category = 'Vibe/Occasion';
                gapText = 'This is a VIBE/OCCASION query. Gemini has structured "Occasion" signals. Bing would need to synthesize from reviews, which is less reliable.';
            }} else if (queryLower.includes('order') || queryLower.includes('menu') || queryLower.includes('recommend') || queryLower.includes('best dish')) {{
                category = 'Menu Recommendation';
                gapText = 'This is a MENU query. Gemini has "Most Ordered" and "Tips" data. Bing lacks this structured insight.';
            }} else {{
                gapText = 'Analyze this query manually to determine the RDQ gap. Check if it requires structured attributes that competitors have.';
            }}
            
            document.getElementById('playground-bing').innerHTML = '<div style="color: var(--text-muted); font-size: 0.9em;"><strong>Category:</strong> ' + category + '<br><br>Open <a href="https://www.bing.com/chat" target="_blank">Bing Copilot</a> and ask this query to see the actual response.</div>';
            document.getElementById('playground-gemini').innerHTML = '<div style="color: var(--text-muted); font-size: 0.9em;"><strong>Category:</strong> ' + category + '<br><br>Open <a href="https://gemini.google.com" target="_blank">Gemini</a> and ask this query. Use DevTools to capture structured data.</div>';
            document.getElementById('playground-perplexity').innerHTML = '<div style="color: var(--text-muted); font-size: 0.9em;"><strong>Category:</strong> ' + category + '<br><br>Open <a href="https://www.perplexity.ai" target="_blank">Perplexity</a> and ask this query.</div>';
            document.getElementById('playground-chatgpt').innerHTML = '<div style="color: var(--text-muted); font-size: 0.9em;"><strong>Category:</strong> ' + category + '<br><br>Open <a href="https://chat.openai.com" target="_blank">ChatGPT</a> and ask this query.</div>';
            
            document.getElementById('playground-gap').style.display = 'block';
            document.getElementById('playground-gap-text').innerText = gapText;
        }}
    </script>
</body>
</html>
"""
    
    output_dir = PROJECT_ROOT / "output"
    output_dir.mkdir(exist_ok=True)
    report_path = output_dir / "rdq_product_playground.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ RDQ Product Playground generated: {report_path}")
    return report_path


if __name__ == "__main__":
    generate_playground()
