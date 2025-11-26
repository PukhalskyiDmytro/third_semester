import os, shutil
from datetime import datetime
from pathlib import Path
import json
import csv

def backup(src, dst):
    srcp = Path(src)
    dstp = Path(dst)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    backup_dir = dstp / f"backup_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    exts = {'.py', '.md', '.txt'}
    manifest = []
    for p in srcp.rglob('*'):
        if p.is_file() and p.suffix.lower() in exts:
            rel = p.relative_to(srcp)
            target = backup_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(p), str(target))
            size = target.stat().st_size
            manifest.append({"path": str(rel.as_posix()), "size": size})
    manifest_path = backup_dir / 'manifest.json'
    with manifest_path.open('w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    zip_path = shutil.make_archive(str(backup_dir), 'zip', root_dir=str(dstp), base_dir=backup_dir.name)
    return str(backup_dir), zip_path

def cleaner(folder, min_size_mb, older_than_days, dry_run=False):
    min_bytes = float(min_size_mb) * 1024 * 1024
    now = datetime.now().timestamp()
    log_path = Path(folder) / 'cleanup.log'
    for dirpath, dirnames, filenames in os.walk(folder):
        for fn in filenames:
            if fn.lower().endswith(('.log', '.tmp')):
                full = os.path.join(dirpath, fn)
                try:
                    st = os.stat(full)
                except FileNotFoundError:
                    continue
                size = st.st_size
                mtime = st.st_mtime
                age_days = (now - mtime) / 86400
                if size > min_bytes and age_days > older_than_days:
                    print(full, size)
                    action = 'DRY-RUN' if dry_run else 'DELETED'
                    with open(log_path, 'a', encoding='utf-8') as logf:
                        logf.write(f"{datetime.now().isoformat()}\t{action}\t{full}\n")
                    if not dry_run:
                        try:
                            os.remove(full)
                        except Exception:
                            with open(log_path, 'a', encoding='utf-8') as logf:
                                logf.write(f"{datetime.now().isoformat()}\tERROR_DELETE\t{full}\n")

def dirs_report(root):
    root = str(root)
    stats = {}
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        files_count = len(filenames)
        dirs_count = len(dirnames)
        total_bytes = 0
        latest_mtime = 0
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                st = os.stat(fp)
            except FileNotFoundError:
                continue
            total_bytes += st.st_size
            if st.st_mtime > latest_mtime:
                latest_mtime = st.st_mtime
        for dn in dirnames:
            child = os.path.join(dirpath, dn)
            if child in stats:
                cs = stats[child]
                files_count += cs['files_count']
                dirs_count += cs['dirs_count']
                total_bytes += cs['total_bytes']
                if cs['latest_mtime'] > latest_mtime:
                    latest_mtime = cs['latest_mtime']
        stats[dirpath] = {'path': dirpath, 'files_count': files_count, 'dirs_count': dirs_count, 'total_bytes': total_bytes, 'latest_mtime': latest_mtime}
    rows = list(stats.values())
    rows.sort(key=lambda x: x['total_bytes'], reverse=True)
    csv_path = os.path.join(root, 'dirs_report.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as cf:
        writer = csv.writer(cf)
        writer.writerow(['path', 'files_count', 'dirs_count', 'total_bytes', 'latest_mtime'])
        for r in rows:
            lm = datetime.fromtimestamp(r['latest_mtime']).isoformat() if r['latest_mtime'] else ''
            writer.writerow([r['path'], r['files_count'], r['dirs_count'], r['total_bytes'], lm])
    large_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                size = os.path.getsize(fp)
            except Exception:
                continue
            large_files.append((size, fp))
    large_files.sort(reverse=True)
    for size, fp in large_files[:5]:
        print(fp, size)

if __name__ == '__main__':
    print('1) Backup')
    print('2) Cleaner')
    print('3) Report')
    choice = input('Choose option (1/2/3): ').strip()
    if choice == '1':
        src = input('Source folder: ')
        dst = input('Destination folder: ')
        bdir, z = backup(src, dst)
        print('Backup dir:', bdir)
        print('Zip:', z)
    elif choice == '2':
        folder = input('Folder to clean: ')
        min_size = float(input('Min size MB: '))
        age = float(input('Older than days: '))
        dry = input('Dry run? (y/n): ').strip().lower() == 'y'
        cleaner(folder, min_size, age, dry_run=dry)
    elif choice == '3':
        root = input('Root folder: ')
        dirs_report(root)
    else:
        print('Invalid choice')
