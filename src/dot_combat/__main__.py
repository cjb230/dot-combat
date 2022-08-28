"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Dot Combat."""


if __name__ == "__main__":
    main(prog_name="dot-combat")  # pragma: no cover
