import os
import json
import scanner


def fix_names(assets):
    fixed_name = []
    for asset in assets:
        file_name, file_ext = os.path.splitext(asset)
        dir_name = os.path.dirname(file_name)
        file_name = os.path.basename(file_name)
        file_name = file_name.replace(" ", "").lower()
        new_name = os.path.join(dir_name, file_name+file_ext)
        fixed_name.append(new_name)
    return fixed_name


def generate_report(scanned_assets, asset_count, check_name, duplicate_assets):
    lines = []

    lines.append("Asset Pipeline Report")
    lines.append("="*20)
    lines.append(f"total assets found {len(scanned_assets)} : ")

    for key, value in asset_count.items():
        lines.append(f"-{key} : {value}")
    lines.append(f"naming issues : {len(check_name)}")

    for asset in check_name:
        lines.append(
            f"- {os.path.basename(asset)}")

    lines.append("duplicated assets found")
    if len(duplicate_assets) < 1:
        lines.append(" : none")
    else:
        for asset_name, asset_path in duplicate_assets.items():
            lines.append(f" - {asset_name} : {asset_path}")

    lines.append("="*20)

    with open("report.txt", "w") as file:
        file.write("\n".join(lines))


def export_json_report(scanned_assets, asset_count, check_name, duplicate_assets):
    data = {"total_assets": len(
        scanned_assets),
        "asset_count": asset_count,
        "naming_issues": check_name,
        "duplicated_assets": duplicate_assets}

    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)


def run_pipeline(scanned_assets):
    asset_count = scanner.count_assets(scanned_assets)
    check_name = scanner.name_checker(scanned_assets)
    dup_assets = scanner.find_duplicates(scanned_assets)

    generate_report(scanned_assets, asset_count, check_name, dup_assets)
    export_json_report(scanned_assets, asset_count, check_name, dup_assets)
