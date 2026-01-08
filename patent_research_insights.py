import requests
import pandas as pd

API_KEY = "YOUR_PATENTSEARCH_API_KEY"
BASE_URL = "https://search.patentsview.org/api/v1/search"

HEADERS = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

def search_patents(inventor=None, assignee=None, size=100):
    # Build new PatentSearch API query
    qry = {"bool": {"must": []}}

    if inventor:
        parts = inventor.split()
        qry["bool"]["must"].append({
            "match": {"inventors.inventor_name": " ".join(parts)}
        })

    if assignee:
        qry["bool"]["must"].append({
            "match": {"assignees.assignee_organization": assignee}
        })

    payload = {
        "query": qry,
        "size": size,
        "fields": [
            "patent_number",
            "title",
            "abstract",
            "assignees.assignee_organization",
            "inventors.inventor_name",
            "citations.cited_patent_number",
            "citations.citing_patent_number"
        ]
    }

    r = requests.post(BASE_URL, headers=HEADERS, json=payload)
    r.raise_for_status()
    return r.json()

def parse_results(res):
    # Convert API JSON into DataFrame
    rows = []
    for hit in res.get("hits", []):
        rows.append({
            "patent": hit.get("patent_number"),
            "title": hit.get("title"),
            # Add other fields
        })
    return pd.DataFrame(rows)

# Example usage
res = search_patents(inventor="Geoffrey Hinton")
df = parse_results(res)
print(df.head())
