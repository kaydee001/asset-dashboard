import os

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
