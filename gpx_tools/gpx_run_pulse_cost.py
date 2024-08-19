import re
from datetime import datetime
from pathlib import Path
from typing import cast

import click
import gpxpy

from .cli import cli

HR_POINT_EXTENSION_TAG_REGEX = re.compile(r"{.*\/TrackPointExtension\/.*}hr")


@cli.command(help="Add elevations to .gpx file using SRTM data.")
@click.argument(
    "gpx_paths",
    nargs=-1,
    metavar="INPUT_FILE",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
def main(gpx_paths: Path | list[Path]) -> None:
    if isinstance(gpx_paths, Path):
        gpx_paths = [gpx_paths]
    for gpx_path in gpx_paths:
        with open(gpx_path) as gpx_file:
            gpx = gpxpy.parse(gpx_file)

            heart_rates: list[int] = []

            for point in gpx.walk(only_points=True):
                for extension in point.extensions:
                    for child in extension:
                        if re.match(HR_POINT_EXTENSION_TAG_REGEX, child.tag, flags=re.IGNORECASE):
                            heart_rate = int(child.text)
                    if heart_rate:
                        heart_rates.append(heart_rate)

            total_distance_km = gpx.length_3d() / 1000

            time_bounds = gpx.get_time_bounds()
            average_pace_seconds_per_km = (
                cast(time_bounds.end_time, datetime) - cast(time_bounds.start_time, datetime)
            ).total_seconds() / total_distance_km
            average_pace_min_per_km, average_pace_sec_per_km = divmod(
                average_pace_seconds_per_km, 60
            )

            average_heart_rate = sum(heart_rates) / len(heart_rates) if heart_rates else None
            if average_heart_rate is None:
                pulse_cost = None
            else:
                pulse_cost = average_pace_seconds_per_km / 60 * average_heart_rate
            print(f"File: {gpx_path}")
            print(
                "    Average pace:       "
                f"{int(average_pace_min_per_km)}:{int(average_pace_sec_per_km)}"
            )
            print(
                "    Average heart rate: "
                f"{round(average_heart_rate) if average_heart_rate is not None else None}"
            )
            print(f"    Run pulse cost:     {round(pulse_cost)}")
