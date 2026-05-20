"""
Management command to seed Prospect records from the MariaDB SQL backup file.
Extracts email addresses from the INSERT statement in dfi_students_backup.sql
and creates Prospect records (email-only, all other fields null).

Usage:
    python manage.py seed_prospects
"""

import re

from django.core.management.base import BaseCommand

from prospects.models import Prospect


class Command(BaseCommand):
    help = 'Seed Prospect records from dfi_students_backup.sql'

    def handle(self, *args, **options):
        from pathlib import Path
        from django.conf import settings

        sql_path = settings.BASE_DIR / 'dfi_students_backup.sql'
        if not sql_path.exists():
            self.stderr.write(self.style.ERROR(f'SQL file not found: {sql_path}'))
            return

        content = sql_path.read_text(encoding='utf-8')

        # Extract all email strings from INSERT VALUES tuples: (id, 'email', 'timestamp')
        emails = re.findall(r"\(\d+,'([^']+)','[^']+'\)", content)

        if not emails:
            self.stderr.write(self.style.WARNING('No email records found in the SQL file.'))
            return

        created = 0
        skipped = 0

        for email in emails:
            _, was_created = Prospect.objects.get_or_create(email=email)
            if was_created:
                created += 1
            else:
                skipped += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Seeding complete: {created} created, {skipped} skipped (already existed). '
                f'Total records: {Prospect.objects.count()}'
            )
        )
