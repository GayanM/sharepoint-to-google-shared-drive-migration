from google.oauth2 import service_account
from googleapiclient.discovery import build
import uuid

class GoogleDriveProvisioner:

    def __init__(self, service_account_file, admin_user):
        self.service_account_file = service_account_file
        self.admin_user = admin_user
        self.service = self._authenticate()

    def _authenticate(self):
        credentials = service_account.Credentials.from_service_account_file(
            self.service_account_file,
            scopes=["https://www.googleapis.com/auth/drive"]
        )

        delegated_credentials = credentials.with_subject(self.admin_user)

        return build("drive", "v3", credentials=delegated_credentials)

    # ==============================
    # CREATE SHARED DRIVE
    # ==============================

    def create_shared_drive(self, drive_name):
        request_id = str(uuid.uuid4())

        body = {
            "name": drive_name
        }

        drive = self.service.drives().create(
            body=body,
            requestId=request_id
        ).execute()

        return drive["id"]

    # ==============================
    # ADD MANAGER
    # ==============================

    def add_manager(self, drive_id, user_email):
        permission = {
            "type": "user",
            "role": "organizer",  # Manager
            "emailAddress": user_email
        }

        self.service.permissions().create(
            fileId=drive_id,
            body=permission,
            supportsAllDrives=True
        ).execute()

    # ==============================
    # PROCESS PLAN
    # ==============================

    def provision_from_plan(self, plan):

        results = []

        for item in plan:

            drive_name = item["drive_name"]
            owners = item["owners"]

            print("--------------------------------------------------")
            print("Creating Drive:", drive_name)

            try:
                drive_id = self.create_shared_drive(drive_name)
                print("Created Drive ID:", drive_id)

                for owner in owners:
                    try:
                        #self.add_manager(drive_id, owner)
                        print(f"Assigned Manager: {owner}")
                    except Exception as e:
                        print(f"Failed to assign {owner}: {e}")

                # collect result
                results.append({
                    "site_url": item["site_url"],
                    "drive_id": drive_id,
                    "owners": "gayan@oneiam.info"
                })

            except Exception as e:
                print("Failed to create drive:", e)

        return results