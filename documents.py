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


def opportunity_to_text(o):
    account = (o.get("Account") or {}).get("Name", "Unknown account")
    amount = o.get("Amount")
    amount_str = f"${amount:,.0f}" if amount is not None else "an unknown amount"
    status = "won" if o.get("IsWon") else ("closed, not won" if o.get("IsClosed") else "open")
    return (
        f"Deal (Opportunity): {o['Name']} for {account}, worth {amount_str}. "
        f"Stage: {o.get('StageName')}, status {status}, "
        f"{o.get('Probability')}% probability. Type: {o.get('Type') or 'unknown'}. "
        f"Expected close date: {o.get('CloseDate', '')[:10]}."
    )


def load_documents():
    """Returns (docs, metadatas) as parallel lists, same order.

    Metadata lets retrieval filter on structured fields (e.g. exact dollar
    amounts, open/closed status) that embeddings alone can't reliably match
    on - similarity search finds semantically related text, not numeric
    thresholds.
    """
    with open("sf_data.json") as f:
        data = json.load(f)

    docs, metadatas = [], []

    for c in data["cases"]:
        docs.append(case_to_text(c))
        metadatas.append({"type": "case"})

    for a in data["accounts"]:
        docs.append(account_to_text(a))
        metadatas.append({"type": "account"})

    for o in data["opportunities"]:
        docs.append(opportunity_to_text(o))
        metadatas.append({
            "type": "opportunity",
            "amount": o.get("Amount") or 0,
            "is_closed": bool(o.get("IsClosed")),
            "is_won": bool(o.get("IsWon")),
            "stage": o.get("StageName") or "",
        })

    return docs, metadatas


if __name__ == "__main__":
    docs, metadatas = load_documents()
    print(f"{len(docs)} documents. Sample:\n{docs[0]}\n{metadatas[0]}")
