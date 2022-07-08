# Geodetic data used for replays of geodetic algorithms (GFAST)
From:  
Murray, J. R., B. W. Crowell, M. H. Murray, C. W. Ulberg, J. J. McGuire (in prep, 2022). Incorporation of real-time earthquake magnitudes estimated via peak ground displacement scaling in the ShakeAlert Earthquake Early Warning system

## Directory structure
events/event_name/
- event_name.geodetic.dat (channel file)
- event_name.geodetic.tnk (tankplayer file)
- event_name.geodetic.mseed.tar.gz (contains an mseed/ directory with miniseed files that correspond with the tankplayer file)

README.md (this file)

start_joint.py (example script for starting the seismic and geodetic tankfiles in separate threads. Based on code from Mike Hagerty ([link](https://github.com/mikehagerty/GFAST_playback_data)) and ShakeAlert STP testsuite ([link](https://code.usgs.gov/EEW/testsuite)) )

## Processing methods
Events fall under one of four processing regimes:
- Method 1: We processed raw 1 Hz GNSS data using methods for PPP with ambiguity
resolution in simulated real-time mode via the RTNet software
- Method 2: Processed positions obtained from UNAVCO Inc (Hodgkinson et al., 2020)
- Method 3: Position time series from Ruhl et al. (2019)
- Method 4: Archived real-time data streams from processing with Fastlane by Central
Washington University


## Summary table
| Event name | Processing method | Japanese name |
| --- | --- | --- |
| 20030925_japan_subduction2  | 1 | Tokachi |
| 20040928_parkfield          | 3 | |
| 20100404_El-MayorCucapah    | 3 | |
| 20110309_japan_subduction10 | 1 | Miyagi |
| 20110311_japan_subduction11 | 1 | Tohoku |
| 20121207_japan_subduction17 | 1 | North Honshu |
| 20140824_southnapa          | 1 | |
| 20160416_japan_shcrust43    | 1 | Kumamoto |
| 20181130_anchorage          | 2 | |
| 20190706_ridgecrest6        | 2 | |
| 20210507_truckee            | 4 | |
| 20210605_calipatria2        | 4 | |
| 20210708_antelope_valley    | 4 | |
| 20211220_petrolia15         | 4 | |

Note: All events have corresponding seismic files in the ShakeAlert testsuite.

## References
Hodgkinson, K. M., D. J. Mencin, K. Feaux, C. Sievers, and G. S. Mattioli (2020). Evaluation of Earthquake Magnitude Estimation and Event Detection Thresholds for Real-Time GNSS Networks: Examples from Recent Events Captured by the Network of the Americas, Seismol. Res. Lett. 91 1628–1645, doi: 10.1785/0220190269.

Ruhl, C. J., D. Melgar, J. Geng, D. E. Goldberg, B. W. Crowell, R. M. Allen, Y. Bock, S. Barrientos, S. Riquelme, J. C. Baez, E. Cabral‐Cano, X. Pérez‐Campos, E. M. Hill, M. Protti, A. Ganas, M. Ruiz, P. Mothes, P. Jarrín, J.‐M. Nocquet, J.‐P. Avouac, E. D'Anastasio (2019). A global database of strong‐motion displacement GNSS recordings and an example application to PGD scaling, Seismol. Res. Lett. 90 271–279, doi: 10.1785/0220180177.
