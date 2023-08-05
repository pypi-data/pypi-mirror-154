import fiona
import gzip
import os
import io
import geopandas as gpd
import pandas as pd
from lodes_star.utils import get_latest_year, get_file_list, fetch_bytes
from lodes_star.state_codes import State


def fetch_lodes(state,
                zone_types=['od', 'rac', 'wac'],
                job_types=['JT00'],
                segments=['S000'],
                year=None,
                cache=True):

    zone_types = [zone_types] if isinstance(zone_types, str) else zone_types
    job_types = [job_types] if isinstance(job_types, str) else job_types
    segments = [segments] if isinstance(segments, str) else segments
    base_url = 'https://lehd.ces.census.gov/data/lodes/LODES7'

    if not year:
        year = get_latest_year(base_url, state)
        print('No year specified, defaulting to latest year ' + year)

    # Create file list
    flist = get_file_list(base_url, state, zone_types, job_types, segments, year)

    # Downloading files
    lodes = {}
    for fname, file_url in flist.items():
        # Fetch the file from URL or cache
        suffix = '{}/{}'.format(list(flist.keys()).index(fname) + 1, len(flist))
        bytes_data = fetch_bytes(file_url, suffix, cache)

        # Decompress the gzip bytes data and read into pandas dataframe
        string_io = io.StringIO(gzip.decompress(bytes_data).decode('utf-8'))
        df = pd.read_csv(string_io, dtype={'h_geocode': str, 'w_geocode': str, 'createdate': str})

        # Stash it
        key = fname.replace('.csv.gz', '')
        lodes[key] = df

    return lodes


# Fetch Census Blocks
def fetch_geo(state, geography, year='2021', cache=True):
    assert(len(year) == 4)
    year = str(year)

    if len(state) > 2:
        state = State.name2abb[state.capitalize()].lower()
    state_num = State.abb2code[state.upper()]

    altgeo = geography.lower()
    if geography == 'TABBLOCK':
        altgeo = geography.lower() + '10'

    # Format the file url
    url_template = 'https://www2.census.gov/geo/tiger/TIGER{year}/{geography}/tl_{year}_{fips}_{altgeo}.zip'
    # url_template = 'https://www2.census.gov/geo/tiger/TGRGDB{yy}/tlgdb_{yyyy}_a_{state_num}_{state}.gdb.zip'
    file_url = url_template.format(**{'year': year, 'geography': geography, 'fips': state_num, 'altgeo': altgeo})

    # Fetch the file from URL or cache
    bytes_data = fetch_bytes(file_url, cache=cache)

    if '.gdb' in os.path.basename(file_url):
        # Read geodatabase into geopandas
        with fiona.io.ZipMemoryFile(bytes_data) as zip_memory_file:
            with zip_memory_file.open(os.path.basename(file_url).rstrip('.zip')) as collection:
                geodf = gpd.GeoDataFrame.from_features(collection)
    else:
        geodf = gpd.read_file(io.BytesIO(bytes_data))

    return geodf
