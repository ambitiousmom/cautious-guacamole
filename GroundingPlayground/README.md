# Grounding Playground

A flexible, source-agnostic tool for analyzing grounding quality across different query sets, response sources, and evaluation rubrics.

## Philosophy

**Bring Your Own Data** — This tool doesn't prescribe what queries, responses, or metrics you use. Plug in your own:

| Component | Your Use | Team Use | Other Use |
|-----------|----------|----------|-----------|
| **Queries** | Free-form competitive | Official TopicalityICG set | User session logs |
| **Responses** | Manual Gemini/Perplexity | Speedbird API | UHRS evaluations |
| **Rubric** | Answered? Rich? Source? | LDCG, Distance | User satisfaction |

## Quick Start

### 1. Add Your Queries
Place a TSV file in `data/queries/` with at least:
```
query_id	query_text
Q001	Is Joe's Diner dog-friendly?
```

### 2. Add Your Responses  
Place a TSV file in `data/responses/` with at least:
```
query_id	responder	response_text
Q001	gemini	Yes, per Yelp reviews
Q001	bing_copilot	Unable to confirm
```

### 3. Run Comparison
```bash
python scripts/compare_responses.py --queries data/queries/my_queries.tsv --responses data/responses/my_responses.tsv
```

### 4. View Results
Open `output/grounding_report.html` in a browser.

## Folder Structure

```
GroundingPlayground/
├── data/
│   ├── queries/           # Query sources (TSV files)
│   ├── responses/         # Response sources (TSV files)
│   ├── entities/          # Entity data for context
│   └── rubrics/           # Evaluation rubrics
├── scripts/
│   ├── compare_responses.py    # Join and score
│   ├── generate_report.py      # Create HTML dashboard
│   └── utils.py                # Helper functions
├── output/
│   └── (generated reports go here)
├── templates/
│   └── report_template.html    # Dashboard template
└── README.md
```

## Data Schemas

### queries.tsv

| Column | Required | Description |
|--------|----------|-------------|
| query_id | ✅ | Unique identifier |
| query_text | ✅ | The query string |
| query_type | | factual, amenity, vibe, comparison |
| segment | | restaurant, hotel, retail, medical |
| entity_ypid | | Entity identifier |
| entity_name | | Entity name |
| location | | City, State |

### responses.tsv

| Column | Required | Description |
|--------|----------|-------------|
| query_id | ✅ | Links to query |
| responder | ✅ | gemini, perplexity, bing_copilot, chatgpt |
| response_text | ✅ | The actual response |
| answered | | yes, no, partial |
| confidence | | high, medium, low |
| source_cited | | yelp, google_reviews, website, none |
| richness_score | | 1-5 rating |

### rubrics.tsv

| Column | Description |
|--------|-------------|
| metric_name | e.g., "answered", "richness" |
| weight | Importance weight (0-1) |
| description | What this measures |

## Extending for Team Use

The team can plug in their official data:
```
data/queries/official_topicality_queries.tsv
data/responses/speedbird_responses.tsv
data/rubrics/official_ldcg_rubric.tsv
```

Then run the same scripts to compare official metrics with competitive outcomes.

## Moving to Azure DevOps

When ready to share:
1. Create repo at `msasg.visualstudio.com/Bing_GlobalLocalSearch`
2. `git init` in this folder
3. `git remote add origin <repo-url>`
4. `git add . && git commit -m "Initial commit"`
5. `git push -u origin main`
