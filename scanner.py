import os
import json
import argparse

exclude = {"node_modules", ".git", "__pycache__"}


def scan_assets(folder, extensions):
    assets = []

    for root, dirs, files in os.walk(folder, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]
        for f in files:
            path = os.path.join(root, f)
            _, file_ext = os.path.splitext(f)

            if file_ext in extensions:
                assets.append(path)

    return assets


def count_assets(assets):
    asset_count = {}
    for asset in assets:
        _, file_ext = os.path.splitext(asset)
        asset_count[file_ext] = asset_count.get(file_ext, 0) + 1
    return asset_count


def name_checker(assets):
    err_name = []
    for asset in assets:
        file_name, file_ext = os.path.splitext(asset)
        if " " in os.path.basename(file_name) or any(c.isupper() for c in os.path.basename(file_name)):
            err_name.append(os.path.basename(file_name)+file_ext)
    return err_name


def find_duplicates(assets):
    total_assets = {}
    for asset in assets:
        file_name, file_ext = os.path.splitext(asset)
        asset_name = os.path.basename(file_name) + file_ext
        file_path = total_assets.setdefault(asset_name, [])
        file_path.append(asset)
    duplicate_assets = {k: v for k,
                        v in total_assets.items() if len(v) > 1}
    return duplicate_assets


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
    asset_count = count_assets(scanned_assets)
    check_name = name_checker(scanned_assets)
    dup_assets = find_duplicates(scanned_assets)

    generate_report(scanned_assets, asset_count, check_name, dup_assets)
    export_json_report(scanned_assets, asset_count, check_name, dup_assets)


def run_scan(folder, extensions):
    res = {}
    scanned_assets = scan_assets(folder, extensions)
    asset_count = count_assets(scanned_assets)
    check_name = name_checker(scanned_assets)
    dup_assets = find_duplicates(scanned_assets)

    res = {"scanned assets": scanned_assets,
           "total number of assets": asset_count,
           "errors": check_name,
           "duplicate assets": dup_assets}

    return res


if __name__ == "__main__":
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        print("config not found")
        exit(1)
    except json.JSONDecodeError:
        print("not a valid json file")
        exit(1)

    parser = argparse.ArgumentParser()

    parser.add_argument("--folder", help="path to scan")
    parser.add_argument("--ext", help="allowed extensions", nargs="+")
    parser.add_argument("--fix", help="auto fix naming issues",
                        action="store_true")

    args = parser.parse_args()

    ROOT_DIR = args.folder or config["root_dir"]
    ALLOWED_EXTENSIONS = args.ext or config["allowed_extensions"]

    scanned_assets = scan_assets(ROOT_DIR, ALLOWED_EXTENSIONS)
    if args.fix:
        fixed = fix_names(scanned_assets)
        for old, new in zip(scanned_assets, fixed):
            os.rename(old, new)
        scanned_assets = scan_assets(ROOT_DIR, ALLOWED_EXTENSIONS)
    run_pipeline(scanned_assets)
