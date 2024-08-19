from pathlib import Path

import click
import gpxpy

from .cli import cli


@cli.command(help="Add elevations to .gpx file using SRTM data.")
@click.argument(
    "gpx_paths",
    nargs=-1,
    metavar="INPUT_FILE",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
def main(gpx_paths: Path | list[Path]):
    if isinstance(gpx_paths, Path):
        gpx_paths = [gpx_paths]
    for gpx_path in gpx_paths:
        with open(gpx_path) as gpx_file:
            gpx = gpxpy.parse(gpx_file)
        uphill, downhill = gpx.get_uphill_downhill()
        print(f"File: {gpx_path}")
        print(f"    Total uphill:   {round(uphill)} m")
        print(f"    Total downhill: {round(downhill)} m")
