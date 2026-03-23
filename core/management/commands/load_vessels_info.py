from django.core.management.base import BaseCommand
from core.models import Vessel, VesselInfo
import pandas as pd
import numpy as np
from pathlib import Path

class Command(BaseCommand):
    help = "Load vessel info into database"

    def handle(self, *args, **kwargs):


        file_path = Path.cwd() / 'll_latest_full.csv'
        df = pd.read_csv(file_path, on_bad_lines='skip', dtype={'mmsi': str, 'imo':str})
        df = df.dropna(subset=['mmsi'])
        df['mmsi'] = df['mmsi'].astype(int).astype(str).str.strip()
        df['imo'] = df['imo'].apply(lambda x: str(int(x)) if pd.notna(x) else None)
        df['year_of_build'] = [int(x) if not np.isnan(x) else None for x in df['year_of_build']]


        records = df.to_dict('records')
        records = [
            {k: (None if isinstance(v, float) and np.isnan(v) else v) for k, v in row.items()}
            for row in records
        ]


        valid_mmsi = set(Vessel.objects.values_list('mmsi', flat=True))


        objs = []

        for row in records:
            if row['mmsi'] not in valid_mmsi:
                continue
            objs.append(VesselInfo(
                mmsi_id=row['mmsi'],
                imo=row['imo'],
                vessel_name=row['vessel_name'],
                year_of_build=row['year_of_build'],
                flag=row['flag'],
                dwt=row['dwt'],
                teu_capacity=row['teu_capacity'],
                draft=row['draft'],
                loa=row['loa'],
                lbp=row['lbp'],
                breadth_extreme=row['breadth_extreme'],
                breadth_moulded=row['breadth_moulded'],
                vessel_type=row['vessel_type'],
            ))

        VesselInfo.objects.bulk_create(objs, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"{len(objs)} vessel info records loaded"))