import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Carregar o arquivo GRIB para 250 hPa
ds_250 = xr.open_dataset('wind_250hpa.grib', engine='cfgrib')

# Selecionar as componentes zonal (u) e meridional (v) do vento a 250 hPa
u250 = ds_250['u'].sel(isobaricInhPa=250)  # Seleciona o nível de 250 hPa
v250 = ds_250['v'].sel(isobaricInhPa=250)  # Seleciona o nível de 250 hPa

# Calcular a magnitude do vento
wind_speed_250 = np.sqrt(u250**2 + v250**2)

# Criar um mapa usando Cartopy
fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')

# Adicionar grade de coordenadas
gl = ax.gridlines(draw_labels=True, crs=ccrs.PlateCarree(), linestyle='--')
gl.top_labels = False
gl.right_labels = False

# Plotar a magnitude do vento no mapa com cores
magnitude_plot = ax.pcolormesh(u250.longitude, u250.latitude, wind_speed_250, cmap='coolwarm', transform=ccrs.PlateCarree(), shading='auto')

# Adicionar uma barra de cores
cbar = plt.colorbar(magnitude_plot, ax=ax, orientation='vertical', pad=0.05, aspect=40, shrink=0.8)
cbar.set_label('Wind Speed (m/s)')

# Adicionar vetores de vento usando quiver
skip = 10  # Reduzir a quantidade de vetores para melhorar a visualização
ax.quiver(u250.longitude[::skip], u250.latitude[::skip], u250[::skip, ::skip], v250[::skip, ::skip], 
          wind_speed_250[::skip, ::skip], transform=ccrs.PlateCarree(), scale=300, scale_units='inches')

# Adicionar título e legendas aos eixos
plt.title('Wind Vectors at 250 hPa')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Exibir o gráfico
plt.show()
