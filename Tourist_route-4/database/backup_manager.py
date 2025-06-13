import os
import shutil
from pathlib import Path
import datetime

class BackupManager:
    def __init__(self, db_path, backup_dir='data/backups'):
        self.db_path = Path(db_path)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, db_path, backup_dir):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_name = f'backup_{timestamp}.db'
        backup_path = os.path.join(backup_dir, backup_name)

        shutil.copy2(db_path, backup_path)
        print(f"Utworzono kopię zapasową: {backup_path}")
        return backup_path

    def list_backups(self):
        return sorted(self.backup_dir.glob("backup_*.db"))

    def restore_backup(self, backup_file):
        shutil.copy(backup_file, self.db_path)
        print(f"Baza przywrócona z: {backup_file}")