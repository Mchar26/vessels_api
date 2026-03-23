from django.core.management.base import BaseCommand
from core.models import Vessel
import pandas as pd
from pathlib import Path

class Command(BaseCommand):
    help = "Load vessels into database"

    def handle(self, *args, **kwargs):

        file_path = Path.cwd() / 'll_latest.csv'
        df = pd.read_csv(file_path, dtype=str)

        required_cols = ['mmsi']
        df = df[required_cols].dropna()

        objs = [Vessel(**row) for row in df.to_dict("records")]
        Vessel.objects.bulk_create(objs, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"{len(objs)} vessels loaded"))