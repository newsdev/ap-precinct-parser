import os
from ftplib import FTP
import csv

# environment variables
ap_ftp_user = os.environ.get('AP_FTP_USER', None)
ap_ftp_pass = os.environ.get('AP_FTP_PASS', None)
ap_ftp_file_path = os.environ.get('AP_FTP_FILE_PATH', None),
ap_ftp_url = os.environ.get('AP_FTP_URL', None)
ap_ftp_results_filename = os.environ.get('AP_FTP_RESULTS_FILENAME', None)

# opens AP ftp, grabs results file, sticks it in local file called precinct_results.txt
with FTP(ap_ftp_url) as ftp:
    ftp.sendcmd('USER ' + ap_ftp_user)
    ftp.sendcmd('PASS ' + ap_ftp_pass)
    ftp.cwd(ap_ftp_file_path)
    print(ftp.nlst())
    
    localfile = 'precinct_results.txt'
    lf = open(localfile, 'wb')
    ftp.retrbinary('RETR ' + ap_ftp_results_filename, lf.write, 1024)
    
    ftp.quit()


# this is what ap gives us
ap_column_headers = ['TestFlag', 'ElectionDate', 'StatePostal', 'CountyNumber', 
					'FIPSCode', 'CountyName', 'RaceNumber', 'OfficeID',
					'RaceTypeID', 'SeatNumber', 'OfficeName', 'SeatName',
					'RaceTypeParty', 'RaceType', 'OfficeDescription',
					'NumberOfWinners', 'NumberInRunoff', 'PrecinctsReporting',
					'TotalPrecincts', 'CandidateNumber', 'Order', 'Party',
					'FirstName', 'MiddleName', 'LastName', 'Junior', 'UseJunior',
					'Incumbent', 'VoteCount', 'Winner', 'PoliticianID', 'CandidateNumber',
					'Order', 'Party', 'FirstName', 'MiddleName', 'LastName', 'Junior',
					'UseJunior', 'Incumbent', 'VoteCount', 'Winner', 'PoliticianID']

# these are the columns we have for precincts with nyt column names in the order ap gives us
nyt_column_headers_ap_order = ['test', 'electiondate', 'statepostal', '', 'fipscode', '',
                              'raceid', 'officecrid', 'racetypeid', 'seatnum', 'officename', 'seatname',
                              '', 'racetype', '', '', '', 'precinctsreporting', 'precinctstotal',
                              'candidateid', '', 'party', 'first','', 'last', '', '', 'incumbent', 
                              'votecount', 'winner', 'polid', 'candidateid', '', 'party', 'first', 
                              '', 'last', '', '', 'incumbent', 'votecount', 'winner', 'polid']

# these are all of the nyt column headers for ap files in the order they appear on regular races
nyt_column_headers_in_order = ['id', 'raceid', 'racetype', 'racetypeid', 'ballotorder',
                              'candidateid', 'electiondate', 'electtotal', 'electwon',
                              'fipscode', 'first', 'incumbent', 'initialization_data', 
                              'is_ballot_measure', 'last', 'lastupdated', 'level', 'national',
                              'officeid', 'officename', 'party', 'polid', 'polnum',
                              'precinctsreporting', 'precinctsreportingpct', 'precinctstotal',
                              'reportingunitid', 'reportingunitname', 'runoff', 'seatname',
                              'seatnum', 'statename', 'statepostal', 'test', 'uncontested',
                              'votecount', 'vot:dacepct', 'winner']

# input filename
ap_ftp_results_txt_file = 'precinct_results.txt'
# output filename
nyt_results_csv_file = 'precinct_results.csv'

# opens input file, reads it as a csv with semicolon delimiters 
ap_ftp_results_txt = csv.reader(open(ap_ftp_results_txt_file, 'r'), delimiter = ';')

# opens nyt csv file and writes contents of ap's txt file
with open(nyt_results_csv_file, 'w') as outfile:
    writer = csv.writer(outfile)
    # but first, headers
    writer.writerow(nyt_column_headers_ap_order)
    for row in ap_ftp_results_txt:
        writer.writerow(row)

