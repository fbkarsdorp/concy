# Concy: Simple Concordance Tool

## Installing

- This script requires Python 3.6 or higher.
- Install the Silver Searcher from https://github.com/ggreer/the_silver_searcher and put it on your path. 
- Download the repository and run `pip install --editable .` inside the main folder.

## Examples

After installing, `concy` becomes available on your path. Run it with `concy PATTERN PATH`, e.g.:

```bash
concy '\w+ing of\b' corpus-directory
```

## Options

- `--window`: Size of left and right context to match in number of  characters.  [default: 50]
- `--case / --no-case`:  Employs Silver Searcher's 'smart case', i.e. matches case insensitively unless PATTERN contains  uppercase characters.
- `--sort / --no-sort`: Sort results by match and context.
- `--outfile`: Path to file for saving results. Use .csv for CSV output and .xslx for Excel output.
