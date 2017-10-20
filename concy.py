import click
import io
import os
import re
import subprocess
import pandas as pd


ACKMATE_RE = re.compile(br':(.*?):(\d+);((?:\d+ \d+,?)+):(.*)')


def iter_ag_output(output, window=50):
    for line in output:
        try:
            path, line_number, indexes, match = ACKMATE_RE.search(line).groups()
        except AttributeError:
            print(line)
        line_number = int(line_number)
        indexes = [map(int, pair.split()) for pair in indexes.split(b',')]
        for start, length in indexes:
            end = start + length
            left_context = match[max(start - window, 0): start]
            right_context = match[end: end + window]
            yield (path.decode(), line_number,
                   left_context.decode(errors='replace'),
                   match[start: end].decode(errors='replace'),
                   right_context.decode(errors='replace'))


def ag(pattern, path, ignore_case=False):
    case = '--smart-case' if ignore_case else ''
    cmd = f'ag --noheading --ackmate {case} "{pattern}" "{path}"'
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True) as process:
        for line in process.stdout:
            if line.strip():
                yield line
    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, process.args)


def to_dataframe(ag_output):
    columns = ['file-path', 'line-number', 'left-context', 'match', 'right-context']
    df = pd.DataFrame(ag_output, columns=columns)
    return df


def print_to_screen(df):
    with pd.option_context('display.max_rows', None, 'display.max_colwidth', -1):
        print(df.to_string(
            formatters={
                'file-path': '{:.30}...'.format,
                'left-context': '{{:>{}s}}'.format(df['left-context'].str.len().max()).format,
                'right-context': '{{:<{}s}}'.format(df['right-context'].str.len().max()).format}, 
            ))


@click.command()
@click.argument('pattern')
@click.argument('path')
@click.option('--window', default=50, show_default=True,
    help='Size of left and right context to match in number of characters.')
@click.option('--case/--no-case', default=True, 
    help='Match case insensitively unless PATTERN contains uppercase characters')
@click.option('--sort/--no-sort', default=False, help='Sort results by match and context.')
@click.option('--outfile', type=click.File(mode='w'), 
    help='Path to file for saving results. Use .csv for CSV output and .xslx for Excel output.')
def concordance(pattern, path, window, case, sort, outfile):
    ag_search = ag(pattern, path, ignore_case=case)
    df = to_dataframe(iter_ag_output(ag_search, window=window))
    if sort:
        df = df.sort_values(['match', 'left-context', 'right-context'])
    if outfile is None:
        print_to_screen(df)
    elif outfile.name.endswith('csv'):
        df.to_csv(outfile)
    elif outfile.name.endswith('xlsx'):
        writer = pd.ExcelWriter(outfile.name)
        df.to_excel(writer)
        writer.save()
