from sharepoint_extractor import SharePointExtractor
from drive_mapper import generate_shared_drive_plan
from google_drive_provisioner import GoogleDriveProvisioner
from csv_exporter import export_to_csv

TENANT_ID = "bbe6a94b-d23b-42c4-b138-c00c3d953765"
CLIENT_ID = "3e79800d-e88f-4dd5-99ec-9222bcd1ab52"
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Google config
SERVICE_ACCOUNT_FILE = "service_account.json"
ADMIN_USER = "gayan@oneiam.info"

# ==============================
# STEP 1 – Extract SharePoint
# ==============================

extractor = SharePointExtractor(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
sites = extractor.get_all_sites_with_owners()

# ==============================
# STEP 2 – Build Plan
# ==============================

plan = generate_shared_drive_plan(sites)
for item in plan:
    print(item)
# ==============================
# STEP 3 – Create Drives
# ==============================

provisioner = GoogleDriveProvisioner(SERVICE_ACCOUNT_FILE, ADMIN_USER)
results = provisioner.provision_from_plan(plan)

export_to_csv(results)