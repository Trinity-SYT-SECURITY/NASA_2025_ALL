# Kepler Object of Interest (KOI) Dataset: Exoplanet Candidates and Host Star Properties

## Description
This dataset contains data on exoplanet candidates observed by NASA's Kepler mission. It includes information about the candidates' properties (e.g., orbital period, radius, equilibrium temperature) and their host stars (e.g., temperature, radius, surface gravity). The data is sourced from the NASA Exoplanet Archive.

## Columns
- kepid: KepID
- kepoi_name: KOI Name
- kepler_name: Kepler Name
- koi_disposition: Exoplanet Archive Disposition
- koi_pdisposition: Disposition Using Kepler Data
- koi_score: Disposition Score
- koi_fpflag_nt: Not Transit-Like False Positive Flag
- koi_fpflag_ss: Stellar Eclipse False Positive Flag
- koi_fpflag_co: Centroid Offset False Positive Flag
- koi_fpflag_ec: Ephemeris Match Indicates Contamination False Positive Flag
- koi_period: Orbital Period [days]
- koi_period_err1: Orbital Period Upper Unc. [days]
- koi_period_err2: Orbital Period Lower Unc. [days]
- koi_time0bk: Transit Epoch [BKJD]
- koi_time0bk_err1: Transit Epoch Upper Unc. [BKJD]
- koi_time0bk_err2: Transit Epoch Lower Unc. [BKJD]
- koi_impact: Impact Parameter
- koi_impact_err1: Impact Parameter Upper Unc.
- koi_impact_err2: Impact Parameter Lower Unc.
- koi_duration: Transit Duration [hrs]
- koi_duration_err1: Transit Duration Upper Unc. [hrs]
- koi_duration_err2: Transit Duration Lower Unc. [hrs]
- koi_depth: Transit Depth [ppm]
- koi_depth_err1: Transit Depth Upper Unc. [ppm]
- koi_depth_err2: Transit Depth Lower Unc. [ppm]
- koi_prad: Planetary Radius [Earth radii]
- koi_prad_err1: Planetary Radius Upper Unc. [Earth radii]
- koi_prad_err2: Planetary Radius Lower Unc. [Earth radii]
- koi_teq: Equilibrium Temperature [K]
- koi_teq_err1: Equilibrium Temperature Upper Unc. [K]
- koi_teq_err2: Equilibrium Temperature Lower Unc. [K]
- koi_insol: Insolation Flux [Earth flux]
- koi_insol_err1: Insolation Flux Upper Unc. [Earth flux]
- koi_insol_err2: Insolation Flux Lower Unc. [Earth flux]
- koi_model_snr: Transit Signal-to-Noise
- koi_tce_plnt_num: TCE Planet Number
- koi_tce_delivname: TCE Delivery
- koi_steff: Stellar Effective Temperature [K]
- koi_steff_err1: Stellar Effective Temperature Upper Unc. [K]
- koi_steff_err2: Stellar Effective Temperature Lower Unc. [K]
- koi_slogg: Stellar Surface Gravity [log10(cm/s**2)]
- koi_slogg_err1: Stellar Surface Gravity Upper Unc. [log10(cm/s**2)]
- koi_slogg_err2: Stellar Surface Gravity Lower Unc. [log10(cm/s**2)]
- koi_srad: Stellar Radius [Solar radii]
- koi_srad_err1: Stellar Radius Upper Unc. [Solar radii]
- koi_srad_err2: Stellar Radius Lower Unc. [Solar radii]
- ra: RA [decimal degrees]
- dec: Dec [decimal degrees]
- koi_kepmag: Kepler-band [mag]

## Potential Uses
- Analyze trends in exoplanet discoveries.
- Study the relationship between exoplanet candidates and their host stars.
- Identify potentially habitable exoplanets.

## Source
This dataset is sourced from the NASA Exoplanet Archive (https://exoplanetarchive.ipac.caltech.edu/).  
You can explore the dataset interactively here: https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=cumulative.

## License
This dataset is released under the Public Domain.

## Acknowledgments
- NASA and the Kepler mission for providing the data.
- The NASA Exoplanet Archive team for maintaining the dataset.