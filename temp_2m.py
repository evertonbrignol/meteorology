import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Carregar o arquivo GRIB e selecionar a variável de temperatura a 2 metros
ds = xr.open_dataset('temp_2m.grib', engine='cfgrib')
t2m = ds['t2m']  # Temperatura a 2 metros (em Kelvin)

# Converter a temperatura de Kelvin para Celsius
t2m_celsius = t2m - 273.15

# Definir os níveis de contorno de 2 em 2 graus Celsius
# Ajuste os níveis manualmente para garantir a cobertura da faixa de temperatura
min_temp = np.floor(t2m_celsius.min())
max_temp = np.ceil(t2m_celsius.max())
levels = np.arange(min_temp, max_temp + 2, 2)

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

# Plotar a temperatura a 2 metros com contornos de 2 em 2 graus
# Usar 'extend' para garantir que os valores fora do range também sejam coloridos
contourf = ax.contourf(t2m_celsius.longitude, t2m_celsius.latitude, t2m_celsius, levels=levels, cmap='coolwarm', transform=ccrs.PlateCarree(), extend='both')

# Adicionar uma barra de cores na lateral direita
cbar = plt.colorbar(contourf, orientation='vertical', pad=0.05, aspect=40, shrink=0.8)
cbar.set_label('Temperature (°C)')

# Adicionar título e legendas aos eixos
plt.title('2m Temperature')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Exibir o gráfico
plt.show()
