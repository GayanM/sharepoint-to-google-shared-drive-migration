import requests
import msal

class SharePointExtractor:

    def __init__(self, tenant_id, client_id, client_secret):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = self._get_token()

    def _get_token(self):
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=f"https://login.microsoftonline.com/{self.tenant_id}",
            client_credential=self.client_secret
        )
        return app.acquire_token_for_client(
            scopes=["https://graph.microsoft.com/.default"]
        )["access_token"]

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }

    def get_all_sites_with_owners(self):
        results = []

        url = "https://graph.microsoft.com/v1.0/groups?$filter=groupTypes/any(c:c eq 'Unified')"

        while url:
            resp = requests.get(url, headers=self._headers()).json()
            groups = resp.get("value", [])

            for group in groups:
                group_id = group["id"]
                group_name = group["displayName"]

                site = self._get_site(group_id)
                if not site:
                    continue

                owners = self._get_owners(group_id)

                results.append({
                    "group_id": group_id,
                    "site_name": group_name,
                    "site_url": site,
                    "owners": owners
                })

            url = resp.get("@odata.nextLink")

        return results

    def _get_site(self, group_id):
        url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/sites/root"
        resp = requests.get(url, headers=self._headers())

        if resp.status_code == 200:
            return resp.json().get("webUrl")
        return None

    def _get_owners(self, group_id):
        url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/owners"
        resp = requests.get(url, headers=self._headers())

        owners = []
        if resp.status_code == 200:
            for user in resp.json().get("value", []):
                if "userPrincipalName" in user:
                    owners.append(user["userPrincipalName"])

        return owners