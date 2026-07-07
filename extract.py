import json
from dotenv import load_dotenv
import os
from simple_salesforce import Salesforce

load_dotenv()

sf = Salesforce(
    username=os.getenv("SF_USERNAME"),
    consumer_key=os.getenv("SF_CONSUMER_KEY"),
    privatekey_file="certs/sf_jwt.key",
    domain="login",
)

# SOQL = Salesforce's SQL dialect
cases = sf.query_all(
    "SELECT CaseNumber, Subject, Description, Status, Priority, "
    "Account.Name, CreatedDate FROM Case"
)["records"]

accounts = sf.query_all(
    "SELECT Name, Industry, AnnualRevenue, NumberOfEmployees, "
    "BillingCity, Description FROM Account"
)["records"]

print(f"Pulled {len(cases)} cases, {len(accounts)} accounts")

with open("sf_data.json", "w") as f:
    json.dump({"cases": cases, "accounts": accounts}, f, indent=2, default=str)
