# Sermon-Bingo
Pulls the latest sermon notes from a given website and outputs a Bingo Card in PDF for most commonly used words in the notes. Note that this currently only supports downloading from a website and not parsing from another PDF.

## Dependencies
This package requires python and poetry:
- [Python](https://www.python.org/)
- [Poetry](https://python-poetry.org/)


## Installation

The package and dependencies can be installed with the following:
```bash
git clone https://github.com/calebjcourtney/Sermon-Bingo.git
cd Sermon-Bingo
poetry install
```

## Running the program

The program can be run with the following command:
```bash
poetry run python -m sermon_bingo <insert link to sermon notes>
```

This will output a new pdf file to the destination `/data/example_output.pdf`


## Blank Spots
By default, the output of the Bingo Card will be a 5x5 grid	with three (3) random blank spaces. If you would like to change the number of blank spots, you can do so with the `--empty-boxes` flag. Example:

```bash
poetry run python -m sermon_bingo <insert link to sermon notes> --empty-boxes 1
```
