import json


def case_to_text(c):
    account = (c.get("Account") or {}).get("Name", "Unknown account")
    return (
        f"Support case {c['CaseNumber']} for {account}. "
        f"Subject: {c.get('Subject')}. Status: {c.get('Status')}, "
        f"priority {c.get('Priority')}. Opened {c.get('CreatedDate', '')[:10]}. "
        f"Details: {c.get('Description') or 'No description.'}"
    )


def account_to_text(a):
    return (
        f"Account: {a['Name']}, industry {a.get('Industry') or 'unknown'}, "
        f"{a.get('NumberOfEmployees') or '?'} employees, "
        f"annual revenue {a.get('AnnualRevenue') or 'unknown'}, "
        f"based in {a.get('BillingCity') or 'unknown'}. "
        f"{a.get('Description') or ''}"
    )


def load_documents():
    with open("sf_data.json") as f:
        data = json.load(f)
    docs = [case_to_text(c) for c in data["cases"]]
    docs += [account_to_text(a) for a in data["accounts"]]
    return docs


if __name__ == "__main__":
    docs = load_documents()
    print(f"{len(docs)} documents. Sample:\n{docs[0]}")
