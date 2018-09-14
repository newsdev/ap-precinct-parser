import argparse
import csv
from ftplib import FTP
from itertools import chain
import os
import sys

import apftp

# this is what ap gives us
race_headers = ('test', 'racedate', 'statepostal', 'precinctid', 
                'fips', 'precinctname', 'raceid', 'officeid',
                'racetypeid', 'seatnum', 'officename', 'seatname',
                'racetypeparty', 'racetype', 'office',
                'numwinners', 'numrunoff', 'precinctsreporting',
                'totalprecincts')

candidate_headers = ('candidateid', 'order', 'party',
                    'first', 'middle', 'last', 'jr', 'usejr',
                    'incumbent', 'votecount', 'winner', 'polid')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-p', dest='ftp_path')
    args = parser.parse_args()

    ftp_path = None

    if not args.ftp_path:
        raise ValueError("Please pass in the path to the FTP file you'd like to process, e.g., /NY/ad/36376.txt.")
    else:
        ftp_path = args.ftp_path

    raceid = ftp_path.split('/')[-1].split('.')[0]

    result_path = '%s/%s-precinct_results.txt' % (apftp.TMP_DIR, raceid)

    get_ftp_file(raceid, ftp_path, result_path)
    produce_output(raceid, result_path)

def get_ftp_file(raceid, ftp_path, result_path):
    # opens AP ftp, grabs results file, sticks it in local file called precinct_results.txt
    with FTP(apftp.FTP_URL) as ftp:
        ftp.sendcmd('USER ' + apftp.FTP_USER)
        ftp.sendcmd('PASS ' + apftp.FTP_PASS)

        lf = open(result_path, 'wb')
        ftp.retrbinary('RETR ' + ftp_path, lf.write, 1024)
        
        ftp.quit()

def produce_output(raceid, result_path):

    # opens input file, reads it as a csv with semicolon delimiters
    with open(result_path, 'r') as readfile:

        # okay this is borderline unreadable but here's what's happening.
        # first, readfile.read().split('\n)[:-1] is what we're working with
        # this is splitting the ap's file on newline and dropping the last line.
        # second, we're doing a for loop over each row.
        # and we're applying the format_row() function against the row split on `;`
        # which is what the ap drunkenly uses as a delimiter.
        # third, this is wrapped in a list comprehension so it does this loop over the file
        # and row-processing rather quickly.
        # fourth, this produces a list of lists like this:
        # [[{candidate1,precinct1}, {candidate2,precinct1}], [{candidate1,precinct2}, {candidate2,precinct2}]]
        # in order to flatten this in to a single list of dictionaries
        # instead of a list of lists each containing two dictionaries
        # we use itertools.chain.from_iterable. it produces this shape:
        # [{candidate1,precinct1}, {candidate2,precinct1}, {candidate1,precinct2}, {candidate2,precinct2}]
        # which is what we ultimately want.
        results = list(chain.from_iterable([format_row(r.split(';')) for r in readfile.read().split('\n')[:-1]]))
        writer = csv.DictWriter(sys.stdout, fieldnames=list(results[0].keys()))
        writer.writeheader()
        for row in results:
            writer.writerow(row)

def clean_bools(race):
    race['test'] = False
    if race["test"] == 't':
        race['test'] = True
    return race

def format_row(row):
    """
    row is a list of cells.
    1. grab all the race fields
    2. detect number of candidates
    3. for each candidate, build a dict of race + candidate attributes
    4. return a list of all candidates
    """

    def _prepare(candidate_list):
        """
        * Totals votes for this race and gives the candidate pct.
        * Fixes usejr and incumbent.
        """
        total_votes = sum([int(candidate['votecount']) for candidate in candidate_list])
        for candidate in candidate_list:

            if candidate['incumbent'] == "1":
                candidate['incumbent'] = True
            else:
                candidate['incumbent'] = False
            
            if candidate['usejr'] == "1":
                candidate['usejr'] = True
            else:
                candidate['usejr'] = False

            candidate['votecount'] = int(candidate['votecount'])
            candidate['totalvotes'] = total_votes
            if candidate['votecount'] > 0:
                candidate['votepct'] = str(round((candidate['votecount'] / total_votes) * 100, 1))
            else:
                candidate['votepct'] = str(round(float(0), 1))
        return candidate_list


    payload = []

    race_data = clean_bools(dict(zip(race_headers, row[0:len(race_headers)-1])))
    candidate_fields = row[len(race_headers):]
    num_candidates = len(candidate_fields) // len(candidate_headers)

    for idx in range(num_candidates):
        """
        Here's the deal.
        The first n columns in this ap file are about the reporting unit.
        The second set of columns are for candidates. But they repeat.
        Every 12 columns are for one candidate, so if there are 3 candidates
        in the race, there will be 36 additional columns.
        I hate everything.
        """
        # we need to slice candidate fields by modulus len(candidate_headers)
        # e.g. when idx is 0, we want 0-11
        # when idx is 1, we want 12-23
        first_slice = idx*len(candidate_headers)
        second_slice = idx*len(candidate_headers) + len(candidate_headers) - 1
        candidate_data = dict(zip(candidate_headers, candidate_fields[first_slice:second_slice]))

        # this is apparently the fastest guido-approved way 
        candidate_data = {**candidate_data, **race_data}
        payload.append(candidate_data)

    return _prepare(payload)

if __name__ == "__main__":
    main()