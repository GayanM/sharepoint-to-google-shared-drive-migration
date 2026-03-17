def generate_shared_drive_plan(sites):
    plan = []
    seen_names = set()

    for site in sites:

        site_name = site["site_name"]
        site_url = site["site_url"]
        owners = site["owners"]

        suffix = site_url.rstrip("/").split("/")[-1]

        drive_name = f"{site_name}-{suffix}"

        original_name = drive_name
        counter = 1
        while drive_name in seen_names:
            drive_name = f"{original_name}-{counter}"
            counter += 1

        seen_names.add(drive_name)

        plan.append({
            "drive_name": drive_name,
            "site_name": site_name,
            "site_url": site_url,
            "owners": owners
        })

    return plan