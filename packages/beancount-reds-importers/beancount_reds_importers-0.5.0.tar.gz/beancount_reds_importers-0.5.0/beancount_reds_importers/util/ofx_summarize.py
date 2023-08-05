#!/usr/bin/env python3
"""Quick and dirty way to summarize a .ofx file and peek inside it."""

import click
import itertools
import os
import sys
from collections import defaultdict
from ofxparse import OfxParser


def analyze(filename, ttype='dividends', pdb_explore=False):
    ts = defaultdict(list)
    ofx = OfxParser.parse(open(filename))
    for acc in ofx.accounts:
        for t in acc.statement.transactions:
            ts[t.type].append(t)
    import pdb
    pdb.set_trace()


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('-n', '--num-transactions', default=5, help='Number of transactions to show')
@click.option('-e', '--pdb-explore', is_flag=True, help='Open a pdb shell to explore')
@click.option('--stats-only', is_flag=True, help='Show stats and quit')
def summarize(filename, pdb_explore, num_transactions, stats_only):
    """Quick and dirty way to summarize a .ofx file and peek inside it."""
    if os.stat(filename).st_size == 0:
        if stats_only:
            print(0)
            sys.exit(0)
        else:
            print("Zero byte input file.", file=sys.stderr)
            sys.exit(1)

    ofx = OfxParser.parse(open(filename))
    if stats_only:
        total_txns = sum([len(acc.statement.transactions) for acc in ofx.accounts])
        # print("{{'num_accounts' : {}, 'total_transactions' : {}}}".format(len(ofx.accounts), total_txns))
        print(total_txns)
        sys.exit(0)
    print("Total number of accounts:", len(ofx.accounts))
    for acc in ofx.accounts:
        print('----------------')
        try:
            print("Account info: ", acc.account_type, acc.account_id, acc.institution.organization)
        except AttributeError:
            print("Account info: ", acc.account_type, acc.account_id)
            pass

        try:
            print("Statement info: {} -- {}. Bal: {}".format(acc.statement.start_date,
                  acc.statement.end_date, acc.statement.balance))
        except AttributeError:
            try:
                positions = [(p.units, p.security) for p in acc.statement.positions]
                print("Statement info: {} -- {}. Bal: {}".format(acc.statement.start_date,
                      acc.statement.end_date, positions))
            except AttributeError:
                print("Statement info: UNABLE to get start_date and end_date")

        print("Types: ", set([t.type for t in acc.statement.transactions]))

        print()
        for t in itertools.islice(acc.statement.transactions, 0, num_transactions):
            date = t.date if hasattr(t, 'date') else t.tradeDate
            description = t.payee + ' ' + t.memo if hasattr(t, 'payee') else t.memo
            amount = t.amount if hasattr(t, 'amount') else t.total
            print(date, t.type, description, amount)
        if pdb_explore:
            print("Hint: dir(acc), dir(acc.statement.transactions)")
            import pdb
            pdb.set_trace()
        print()
        print()


if __name__ == '__main__':
    summarize()
