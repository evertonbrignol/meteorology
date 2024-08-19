import cdsapi


# teste para saber se vai baixar os dados

dataset = "reanalysis-era5-pressure-levels"
request = {
    'product_type': ['reanalysis'],
    'variable': ['geopotential', 'temperature'],
    'year': ['2024'],
    'month': ['08'],
    'day': ['12'],
    'time': ['00:00'],
    'pressure_level': ['250', '500', '825', '1000'],
    'data_format': 'grib',
    'download_format': 'unarchived'
}

client = cdsapi.Client()
client.retrieve(dataset, request).download()