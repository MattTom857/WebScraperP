import json

def write_json_report(page_data, filename="report.json"):
    pages = sorted(page_data.values(), key=lambda p: p["url"])
    file = open(filename, "w", encoding="utf-8")
    json.dump(pages, file, indent=2)
    file.close()

