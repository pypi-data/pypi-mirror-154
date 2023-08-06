import csv
import datetime as dt
from pathlib import Path

import click

from sco1_misc.prompts import prompt_for_file

TODAY_DATESTR = dt.date.today().isoformat()


def _date_convert(ctx: click.Context, param: click.Option, value: str) -> dt.date:
    return dt.date.fromisoformat(value)


def _build_output_filepath(
    log_filepath: Path, test_date: dt.date, out_filename: str | None
) -> Path:
    if not out_filename:
        out_filename = f"{log_filepath.stem}_{test_date.isoformat()}.csv"

    return log_filepath.parent / out_filename


@click.command()
@click.option("--log_filepath", type=Path, help="Path to log file to trim. Leave blank to prompt.")
@click.option(
    "--test_date",
    type=str,
    default=TODAY_DATESTR,
    help="Data date selection, as YYYY-MM-DD. Defaults to today's date.",
    callback=_date_convert,
)
@click.option(
    "--out-filename", type=str, help="Output filename. Defaults to <in_filename>_<test_date>.csv"
)
def trim_cli(
    log_filepath: Path | None,
    test_date: dt.date,
    out_filename: str | None,
) -> None:
    """
    Trim the provided log CSV to rows logged on the specified date.

    The trimmed log file is saved as a separate CSV file alongside the input log file. Any existing
    trimmed data matching `--out-filename` will be discarded. Attempting to overwrite the input CSV
    file will abort the process.

    It is assumed that the CSV file contains a column named `"Time"`, with timestamps
    formatted as `MM/DD/YYYY HH:MM:SS`. It is also assumed that the CSV file ends on the same date
    as the specified date filter.
    """
    if log_filepath is None:
        try:
            log_filepath = prompt_for_file(
                "Select Log File.",
                filetypes=[("Log CSV", ".csv"), ("All Files", "*.*")],
            )
        except ValueError as err:
            # Reraise as Click exception to gracefully exit
            raise click.ClickException("No file selected, aborting.") from err

    out_filepath = _build_output_filepath(log_filepath, test_date, out_filename)
    if out_filepath == log_filepath:
        raise click.ClickException("Cannot overwrite the input log file. Aborting.")

    with log_filepath.open("r") as in_log, out_filepath.open("w", newline="") as out_log:
        reader = csv.DictReader(in_log)
        if not reader.fieldnames:
            raise click.ClickException(
                "Could not identify a header row in the selected log file, aborting."
            )

        writer = csv.DictWriter(out_log, reader.fieldnames)
        writer.writeheader()
        for row in reader:
            row_date = dt.datetime.strptime(row["Time"], r"%m/%d/%Y %H:%M:%S").date()
            if row_date == test_date:
                # Assume that we're saving the logs right when we're done with testing, so once
                # we've hit the first correct date, we can just dump the rest of the rows
                writer.writerow(row)  # Write the current row since we've consumed it already
                writer.writerows(reader)


if __name__ == "__main__":
    trim_cli()
