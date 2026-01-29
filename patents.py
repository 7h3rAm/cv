import requests
import json
import os

PATENTSVIEW_BASE_URL = "https://search.patentsview.org/api/v1/patent/"
PATENTSVIEW_CITATIONS_ENDPOINT = "https://search.patentsview.org/api/v1/patent/us_patent_citation/"
API_KEY = "k5vDwwwR.co60SRGhkwhWz9b28VXV7mVzlN7aQ0Aa"


def clean_patent_id(patent_id: str) -> str:
  """Removes 'US' prefix and any suffixes like 'B2' or 'A1' from a patent ID."""
  # Remove 'US' prefix
  if patent_id.startswith("US"):
    patent_id = patent_id[2:]

  # Remove common suffixes like B2, A1, etc.
  if len(patent_id) > 2 and (patent_id[-2].isalpha() and patent_id[-1].isdigit() or patent_id[-2].isdigit() and patent_id[-1].isalpha()):
    patent_id = patent_id[:-2]
  elif len(patent_id) > 1 and patent_id[-1].isalpha():
    patent_id = patent_id[:-1]

  return patent_id.strip()

def display_patent_as_csv(patent: dict):
  """Prints a single patent's summary in CSV format."""
  patent_id = patent.get("patent_id", "N/A")
  patent_title = patent.get("patent_title", "N/A")
  patent_date = patent.get("patent_date", "N/A")

  inventor_names = []
  if patent.get("inventors"):
    for inv in patent["inventors"]:
      first = inv.get("inventor_name_first", "")
      last = inv.get("inventor_name_last", "")
      if first and last:
        inventor_names.append(f"{first} {last}")
      elif first:
        inventor_names.append(first)
      elif last:
        inventor_names.append(last)
  inventors_str = "; ".join(inventor_names) if inventor_names else "N/A"

  assignee_orgs = []
  if patent.get("assignees"):
    for ass in patent["assignees"]:
      org = ass.get("assignee_organization")
      if org:
        assignee_orgs.append(org)
  assignees_str = "; ".join(assignee_orgs) if assignee_orgs else "N/A"

  csv_line = [
    f'"{patent_id}"',
    f'"{patent_title.replace('"', '""')}"',
    f'"{patent_date}"',
    f'"{inventors_str.replace('"', '""')}"',
    f'"{assignees_str.replace('"', '""')}"'
  ]
  print(",".join(csv_line))

def fetch_patent_citations(patent_id: str) -> dict:
  cleaned_patent_id = clean_patent_id(patent_id)

  endpoint = PATENTSVIEW_CITATIONS_ENDPOINT
  headers = {
    "X-Api-Key": API_KEY,
    "accept": "application/json"
  }

  query = {"citation_patent_id": cleaned_patent_id}

  params = {
    "q": json.dumps(query),
    "f": json.dumps(["patent_id", "patent", "citation_patent_id", "citation_patent", "citation_category", "citation_date", "citation_name", "citation_sequence", "citation_wipo_kind"])
  }

  try:
    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("us_patent_citations", [])
  except requests.exceptions.RequestException as e:
    print(f"An error occurred while fetching citations for patent {patent_id}: {e}")
  except json.JSONDecodeError:
    print(f"Error decoding JSON while fetching citations for patent {patent_id}: {response.text}")

def fetch_patents(patent_ids: list) -> dict:
  cleaned_patent_ids = [clean_patent_id(pid) for pid in patent_ids]

  endpoint = PATENTSVIEW_BASE_URL
  headers = {
    "X-Api-Key": API_KEY,
    "accept": "application/json"
  }

  # Query directly by patent_id
  query = {"patent_id": cleaned_patent_ids}

  all_patents = []
  page = 1
  per_page = 1000  # Max allowed per_page

  while True:
    params = {
      "q": json.dumps(query),
      "o": json.dumps({"page": page, "per_page": per_page}),
      "f": json.dumps(["assignees", "gov_interest_statement", "inventors", "patent_abstract", "patent_cpc_current_group_average_patent_processing_days", "patent_date", "patent_detail_desc_length", "patent_earliest_application_date", "patent_id", "patent_num_foreign_documents_cited", "patent_num_times_cited_by_us_patents", "patent_num_total_documents_cited", "patent_num_us_applications_cited", "patent_num_us_patents_cited", "patent_processing_days", "patent_term_extension", "patent_title", "patent_type", "patent_uspc_current_mainclass_average_patent_processing_days", "patent_year", "wipo_kind", "withdrawn"])
    }

    try:
      response = requests.get(endpoint, headers=headers, params=params)
      response.raise_for_status()
      data = response.json()

      if data.get("patents"):
        all_patents.extend(data["patents"])

      total_patents = data.get("total_patent_count", 0)
      if len(all_patents) >= total_patents:
        break

      page += 1
    except requests.exceptions.RequestException as e:
      print(f"An error occurred during initial API call for my patents: {e}")
      break
    except json.JSONDecodeError:
      print(f"Error decoding JSON during initial API call: {response.text}")
      break

  enriched_patents = []
  for patent in all_patents:
    print(f"Fetching citations for patent ID: {patent.get('patent_id', '')}")
    patent["us_patent_citations"] = fetch_patent_citations(patent.get("patent_id", ""))
    print(f"Found {len(patent['us_patent_citations'])} citations.")
    print("-----")
    enriched_patents.append(patent)

  return enriched_patents

def main():
  my_patent_ids = ["US10089464B2", "US10104101B1", "US10958686B2", "US11334666B2", "US11805147B2", "US11968225B2", "US12034743B2", "US12301625B2", "US12417292B2", "US12445466B2", "US20170346827A1"]
  all_patents = fetch_patents(my_patent_ids)
  if all_patents:
    with open("patents.json", "w") as f:
      json.dump(all_patents, f, indent=2)
    print('"Patent ID","Title","Date","Inventors","Assignees"')
    for patent in all_patents:
      display_patent_as_csv(patent)


if __name__ == "__main__":
  main()
