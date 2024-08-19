from pathlib import Path

import click
import gpxpy

from .cli import cli


@cli.command(help="Show minimum and maximum elevation in .gpx file.")
@click.argument(
    "gpx_path",
    metavar="INPUT_FILE",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
def main(
    gpx_path: Path,
) -> None:
    with open(gpx_path) as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    elevations: list[float] = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                if point.elevation is not None:
                    elevations.append(point.elevation)
    if not elevations:
        print(f"{gpx_path} doesn't have any elevations")
        exit(1)

    print(f"File: {gpx_path}")
    print(
        f"    Minimum elevation: {round(min(elevations))} m\n"
        f"    Maximum elevation: {round(max(elevations))} m"
    )


if __name__ == "__main__":
    main()
