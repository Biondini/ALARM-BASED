import csep
from csep.core import regions
from csep.utils import time_utils, comcat
# CSEP Imports
from csep.utils.time_utils import epoch_time_to_utc_datetime, datetime_to_utc_epoch, strptime_to_utc_datetime, \
    millis_to_days, parse_string_format, days_to_millis, strptime_to_utc_epoch, utc_now_datetime, create_utc_datetime
from csep.utils.stats import min_or_none, max_or_none
from csep.utils.calc import discretize
from csep.core.regions import CartesianGrid2D
from csep.utils.comcat import SummaryEvent
from csep.core.exceptions import CSEPSchedulerException, CSEPCatalogException, CSEPIOException
from csep.utils.calc import bin1d_vec
from csep.utils.constants import CSEP_MW_BINS
from csep.utils.log import LoggingMixin
from csep.utils.readers import csep_ascii
from csep.utils.file import get_file_extension
from csep.utils.plots import plot_catalog



import numpy as np

# start_time = csep.utils.time_utils.strptime_to_utc_datetime('2019-01-01 00:00:00.0') #DEFINISCE IL TEMPO DI INIZIO
# end_time = csep.utils.time_utils.strptime_to_utc_datetime('2021-06-21 00:00:00.0')# TEMPO DI FINE RICHIESTA
# catalog = csep.query_comcat(start_time, end_time)
# print(catalog)

# LOAD DEL CATALOGO:
# 1) il catalogo deve essere nel formato opportuno
# 2) la funzione "csep.load_catalog" serve a caricare il catalogo
# 3) "type" specifica la lettura del catalogo in uno dei formati definiti
# 4) "format" converte il catalogo o in formato "csep" o lo lascia nel formato "nativo"
cat = csep.load_catalog('ISIDE.csv', type='csep-csv', format='csep', loader=None, apply_filters=False)
cat.write_ascii('output_unfiltered_catalogue1.csv')
cat.write_json('provajson.csv')
cat1=cat.to_dataframe()
print(cat)
m_VEC=cat.get_magnitudes()

# FILTER OF THE CATALOGUE:
#Per filtrare il catalogo, considerando uno o più attributi
# 1) verificare il nome degli attributi utilizzando la console di python nella voce "dtype" di catalog

cat_fil = cat.filter(statements=(['magnitude >= 3.5','origin_time >= 1960', 'depth <= 30']))
print(cat_fil)
cat12=cat_fil.to_dataframe()

# FILTER OF THE CATALOGUE in a certain period of time:
# create epoch times from time-string formats
start_epoch = csep.utils.time_utils.strptime_to_utc_epoch('2010-07-06 03:19:54.040000')
end_epoch = csep.utils.time_utils.strptime_to_utc_epoch('2019-09-21 03:19:54.040000')
# csep.utils.time_utils.decimal_year(dt)
# A=csep.utils.time_utils.decimal_year_to_utc_datetime(2009.21551)


# dt = datetime.datetime(int(2009), 1, 1, 0, 0, 0, 0)
# filter catalog to magnitude ranges and times
filters = [f'origin_time >= {start_epoch}', f'origin_time < {end_epoch}']
cat_fil2 = cat.filter(filters)
italy_region = csep.regions.italy_csep_region()
cat_fil3= cat_fil2.filter_spatial(italy_region)
print(cat_fil3)
CCC=cat_fil3.update_stats()
cat_fil3.update_catalog_stats()
BBB=cat_fil3.to_dataframe()

#To save the filtered catalogue:
CCCC=cat_fil2.to_dataframe()
cat1=cat.to_dataframe()
AAAB=np.ndarray(cat_fil2.catalog)
AAABb=cat_fil2.get_csep_format()
AAAB.catalog.write_ascii('output_filtered_catalogue1.csv'), write_header=True, write_empty=False, append=True, id_col='id')
cat_fil_load = csep.load_catalog('output_filtered_catalogue1.csv', type='csep-csv', format='csep_ascii', loader=None, apply_filters=False)

loadCAT=csep.load_catalog('output_filtered_catalogue1.csv',loader=csep_ascii)
loadCAT=csep.load_catalog(cls, filename, loader=csep_ascii, **kwargs)

csep.load_catalog('output_filtered_catalogue1.csv', type='csep-csv', format='csep', loader=None, apply_filters=False)

#TO PLOT A CATALOG FOR A CERTAIN LONG LAT RANGE [10.941, 20.035, 39.875, 44.895]
# cat_fil.plot(ax=None, show=True, extent=[10.941, 20.035, 39.875, 44.895], set_global=False, plot_args=None)
cat_fil.plot(ax=None, show=True,  set_global=False, plot_args=None)
cat_fil.get_magnitudes()

import matplotlib.pyplot as plt

# lets assume we already loaded in some catalog

# quick and dirty plot
fig, ax = plt.subplots()
ax.plot(cat.get_epoch_times(), cat.get_cumulative_number_of_events())
plt.show()

# salvataghgio catalogo da dataframe come csv nel formato CSEP


magnitudes=cat.get_magnitudes()
longitudes=cat.get_longitudes()
latitudes=cat.get_latitudes()
depths=cat.get_depths()
ids=(cat.get_event_ids())#replace('b', '')
timest=cat.get_epoch_times()
datetime=cat.get_datetimes()


###
event_id=['']*len(ids)#np.zeros(len(ids))

for i in range(0,len(ids)):
    event_id[i]=str(ids[i].decode('utf-8'))

time_string=['']*len(timest)

for i in range(0,len(time_string)):
    time_string[i]=str(csep.utils.time_utils.epoch_time_to_utc_datetime(timest[i]).replace(tzinfo=None)).replace(' ', 'T')

import numpy as np
import pandas as pd
PANDAS_CAT = pd.DataFrame({'lon':longitudes, 'lat':latitudes, 'mag':magnitudes, 'time_string':time_string, 'depth':depths,'catalog_id':None ,'event_id':event_id })

PANDAS_CAT.to_csv('file_prova.csv', header=True, index=False)




cat_from_pandas = csep.load_catalog('file_prova.csv', type='csep-csv', format='csep', loader=None, apply_filters=False)




A0=cat.get_csep_format()
A=A0.to_dataframe()
PANDAS_CAT.time_string[:]=str(csep.utils.time_utils.epoch_time_to_utc_datetime(PANDAS_CAT.time_string[:]).replace(tzinfo=None)).replace(' ', 'T')
PANDAS_CAT.event_id.decode()

PANDAS_CAT.event_id[:]=str(PANDAS_CAT.event_id[:]).replace('b', '')
A=str(PANDAS_CAT.event_id[:]).replace('b', '')
cat.write_catalog_csep('catalogo_di_prova1.csv')
cat_uploaded = csep.load_catalog('catalogo_di_prova1.csv', type='csep-csv', format='csep', loader=None, apply_filters=False)
A=cat_uploaded.to_dataframe()

V=A.origin_time[3]-A.origin_time[2]


