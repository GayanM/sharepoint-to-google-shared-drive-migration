import csv

def export_to_csv(results, filename="migration_map.csv"):

    import csv

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Source SharePoint URL",
            "Target Drive FolderID",
            "Target GUser"
        ])

        for item in results:

            owners = item["owners"]

            if isinstance(owners, list):
                owners = "".join(owners)   # FIX

            writer.writerow([
                item["site_url"],
                item["drive_id"],
                owners
            ])

    print(f"\nCSV exported successfully → {filename}")