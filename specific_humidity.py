import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Carregar o arquivo GRIB e selecionar a variável de umidade específica
ds = xr.open_dataset('specific_humidity.grib', engine='cfgrib')

# Filtrar para a umidade específica a 1000 hPa (caso o dataset contenha múltiplos níveis de pressão)
q1000 = ds.sel(isobaricInhPa=1000)['q']  # Substitua 'isobaricInhPa' e 'q' pelos nomes corretos

# Converter de kg/kg para g/kg
q1000_gkg = q1000 * 1000

# Criar um mapa usando Cartopy
fig = plt.figure(figsize=(12, 8))
ax = plt.axes(projection=ccrs.PlateCarree())

# Adicionar linhas de costa e outros recursos de mapa
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')

# Adicionar grade de coordenadas
gl = ax.gridlines(draw_labels=True, crs=ccrs.PlateCarree(), linestyle='--')
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 10, 'color': 'black'}
gl.ylabel_style = {'size': 10, 'color': 'black'}

# Plotar a umidade específica em g/kg com um mapa de cores adequado (ex: 'Blues')
contourf = ax.contourf(q1000_gkg.longitude, q1000_gkg.latitude, q1000_gkg, cmap='Blues', transform=ccrs.PlateCarree())

# Adicionar uma barra de cores na lateral direita
cbar = plt.colorbar(contourf, orientation='vertical', pad=0.05, aspect=40, shrink=0.8)
cbar.set_label('Specific Humidity (g/kg)')

# Adicionar título e legendas aos eixos
plt.title('Specific Humidity at 1000 hPa (g/kg)')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Exibir o gráfico
plt.show()
