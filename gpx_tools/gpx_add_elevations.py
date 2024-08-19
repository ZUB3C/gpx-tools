from pathlib import Path

import click
import gpxpy
import srtm  # type: ignore[import-untyped]

from .cli import cli


@cli.command(help="Add elevations to .gpx file using SRTM data.")
@click.argument(
    "gpx_path",
    metavar="INPUT_FILE",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    "-o",
    "--output",
    "output_gpx_path",
    metavar="OUTPUT_FILE",
    type=click.Path(dir_okay=False, path_type=Path),
    default=None,
)
@click.option(
    "-f",
    "--force",
    "replace_file",
    is_flag=True,
    default=False,
    help="Override the output file if it exists.",
)
@click.option(
    "-m",
    "--only-missing",
    "only_missing",
    is_flag=True,
    default=False,
    help="Only points without elevation will get a SRTM value.",
)
@click.option(
    "-s", "--smooth", "smooth", is_flag=True, default=False, help="Use smoothed elevation data."
)
def main(
    gpx_path: Path,
    output_gpx_path: Path | None = None,
    replace_file: bool = False,
    only_missing: bool = False,
    smooth: bool = False,
) -> None:
    if output_gpx_path is None:
        if not replace_file:
            print("Add -f option to overwrite .gpx input file.")
            exit(1)
        output_gpx_path = gpx_path
    elif output_gpx_path.is_file():
        if replace_file:
            Path.unlink(output_gpx_path)
        else:
            print(f"Output file {output_gpx_path} already exists. Add -f option for overwrite")
            exit(1)

    with open(gpx_path) as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    elevation_data = srtm.get_data()
    elevation_data.add_elevations(gpx, only_missing=only_missing, smooth=smooth)

    with open(output_gpx_path, "w") as output_gpx:
        output_gpx.write(gpx.to_xml())


if __name__ == "__main__":
    main()
