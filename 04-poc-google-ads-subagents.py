"""
POC: Google Ads Copy Sub-Agent Workflow
Mirrors Austin Lau's Anthropic architecture.

Input:  ads_input.csv  — columns: ad_group, keyword, landing_page_url, notes
Output: ads_output.csv — columns: ad_group, headline_1..15, description_1..4

Sub-agent architecture:
  Coordinator  →  HeadlineAgent  (15 headlines, max 30 chars each)
               →  DescriptionAgent (4 descriptions, max 90 chars each)

Usage:
  pip install anthropic pandas
  export ANTHROPIC_API_KEY=your_key
  python 04-poc-google-ads-subagents.py --input ads_input.csv --output ads_output.csv
"""

import anthropic
import pandas as pd
import json
import argparse
import sys


HEADLINE_SYSTEM = """You are a Google Ads headline writer.
Rules:
- Write exactly 15 unique headlines
- Each headline must be 30 characters or fewer (count carefully)
- Include the primary keyword naturally in at least 3 headlines
- Vary the angle: benefit, urgency, social proof, feature, question
- No punctuation at the end of headlines
- Return ONLY a JSON array of 15 strings, nothing else
"""

DESCRIPTION_SYSTEM = """You are a Google Ads description writer.
Rules:
- Write exactly 4 unique descriptions
- Each description must be 90 characters or fewer (count carefully)
- Each should end with a call to action
- Vary the angle across the 4: value prop, differentiator, offer, urgency
- Return ONLY a JSON array of 4 strings, nothing else
"""


def run_headline_agent(client: anthropic.Anthropic, ad_group: str, keyword: str, notes: str) -> list[str]:
    prompt = f"Ad group: {ad_group}\nPrimary keyword: {keyword}\nContext/notes: {notes}"
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=HEADLINE_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    headlines = json.loads(response.content[0].text)
    # Enforce character limit — truncate silently
    return [h[:30] for h in headlines[:15]]


def run_description_agent(client: anthropic.Anthropic, ad_group: str, keyword: str, notes: str) -> list[str]:
    prompt = f"Ad group: {ad_group}\nPrimary keyword: {keyword}\nContext/notes: {notes}"
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=DESCRIPTION_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    descriptions = json.loads(response.content[0].text)
    return [d[:90] for d in descriptions[:4]]


def process_row(client: anthropic.Anthropic, row: pd.Series) -> dict:
    ad_group = str(row.get("ad_group", ""))
    keyword = str(row.get("keyword", ""))
    notes = str(row.get("notes", ""))

    print(f"  Processing: {ad_group} / {keyword}")

    headlines = run_headline_agent(client, ad_group, keyword, notes)
    descriptions = run_description_agent(client, ad_group, keyword, notes)

    result = {"ad_group": ad_group, "keyword": keyword}
    for i, h in enumerate(headlines, 1):
        result[f"headline_{i}"] = h
    for i, d in enumerate(descriptions, 1):
        result[f"description_{i}"] = d

    return result


def main():
    parser = argparse.ArgumentParser(description="Google Ads copy sub-agent POC")
    parser.add_argument("--input", default="ads_input.csv", help="Input CSV path")
    parser.add_argument("--output", default="ads_output.csv", help="Output CSV path")
    args = parser.parse_args()

    try:
        df = pd.read_csv(args.input)
    except FileNotFoundError:
        # Generate sample input if no file provided
        print(f"No input file found at {args.input} — generating sample data")
        df = pd.DataFrame([
            {"ad_group": "Cloud Security", "keyword": "cloud security solutions", "notes": "B2B, IT buyers, emphasize compliance"},
            {"ad_group": "Endpoint Protection", "keyword": "endpoint security software", "notes": "Mid-market, 50-500 employees"},
        ])
        df.to_csv(args.input, index=False)
        print(f"Sample input written to {args.input} — re-run to process it")
        sys.exit(0)

    client = anthropic.Anthropic()
    results = []

    print(f"Processing {len(df)} ad groups...")
    for _, row in df.iterrows():
        results.append(process_row(client, row))

    out_df = pd.DataFrame(results)
    out_df.to_csv(args.output, index=False)
    print(f"\nDone. Output written to {args.output}")
    print(f"Total ads generated: {len(results)}")


if __name__ == "__main__":
    main()
