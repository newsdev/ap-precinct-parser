# ap-precinct-parser
A quick parser for AP's precinct-level data files.

## Installation
```
pip install -e git+git@github.com:newsdev/ap-precinct-parser.git#egg=ap-precinct-parser
```

## Usage
```bash
export AP_FTP_USER=ftpftpuser
export AP_FTP_PASS=password
apftp /NY/ad/36376.txt > results.csv
```

## Output
```
candidateid,order,party,first,middle,last,jr,usejr,incumbent,votecount,winner,test,racedate,statepostal,precinctid,fips,precinctname,raceid,officeid,racetypeid,seatnum,officename,seatname,racetypeparty,racetype,office,numwinners,numrunoff,precinctsreporting,totalvotes,votepct
81252,1,Dem,Cynthia,,Nixon,,True,True,1045450,,True,2018-09-13,NY,1,00000,New York,36376,G,D,0,Governor,,Dem,Primary,,1,0,15526,2323223,45.0
80742,2,Dem,Andrew,,Cuomo,,True,True,1277773,,True,2018-09-13,NY,1,00000,New York,36376,G,D,0,Governor,,Dem,Primary,,1,0,15526,2323223,55.0
81252,1,Dem,Cynthia,,Nixon,,True,True,87,,True,2018-09-13,NY,23101,00000,Queens AD23 ED1,36376,G,D,0,Governor,,Dem,Primary,,1,0,1,174,50.0
80742,2,Dem,Andrew,,Cuomo,,True,True,87,,True,2018-09-13,NY,23101,00000,Queens AD23 ED1,36376,G,D,0,Governor,,Dem,Primary,,1,0,1,174,50.0
81252,1,Dem,Cynthia,,Nixon,,True,True,21,,True,2018-09-13,NY,23102,00000,Queens AD23 ED2,36376,G,D,0,Governor,,Dem,Primary,,1,0,1,174,12.1
80742,2,Dem,Andrew,,Cuomo,,True,True,153,,True,2018-09-13,NY,23102,00000,Queens AD23 ED2,36376,G,D,0,Governor,,Dem,Primary,,1,0,1,174,87.9
81252,1,Dem,Cynthia,,Nixon,,True,True,43,,True,2018-09-13,NY,23103,00000,Queens AD23 ED3,36376,G,D,0,Governor,,Dem,Primary,,1,0,1,174,24.7
80742,2,Dem,Andrew,,Cuomo,,True,True,131,,True,2018-09-13,NY,23103,00000,Queens AD23 ED3,36376,G,D,0,Governor,,Dem,Primary,,1,0,1,174,75.3
81252,1,Dem,Cynthia,,Nixon,,True,True,173,,True,2018-09-13,NY,23104,00000,Queens AD23 ED4,36376,G,D,0,Governor,,Dem,Primary,,1,0,1,174,99.4
```