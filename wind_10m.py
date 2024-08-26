import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import matplotlib.colors as mcolors

# Carregar o arquivo GRIB e selecionar as variáveis de vento (u10 e v10)
ds = xr.open_dataset('wind_10m.grib', engine='cfgrib')
u10 = ds['u10']  # Componente zonal do vento (m/s)
v10 = ds['v10']  # Componente meridional do vento (m/s)

# Calcular a magnitude do vento
wind_speed = np.sqrt(u10**2 + v10**2)

# Definir uma paleta de cores personalizada de azul escuro para vermelho escuro
cmap = mcolors.LinearSegmentedColormap.from_list('wind_cmap', ['darkblue', 'white', 'darkred'])

# Definir os níveis de contorno para a magnitude do vento
levels = np.linspace(0, np.nanmax(wind_speed), num=20)

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

# Plotar a magnitude do vento com as cores personalizadas
contourf = ax.contourf(u10.longitude, u10.latitude, wind_speed, levels=levels, cmap=cmap, transform=ccrs.PlateCarree())

# Adicionar os vetores de direção do vento
skip = (slice(None, None, 5), slice(None, None, 5))  # Pular alguns vetores para clareza
ax.quiver(u10.longitude.values[skip[1]], u10.latitude.values[skip[0]], u10.values[skip], v10.values[skip], transform=ccrs.PlateCarree(), color='black', scale=700)

# Adicionar uma barra de cores na lateral direita
cbar = plt.colorbar(contourf, orientation='vertical', pad=0.05, aspect=40, shrink=0.8)
cbar.set_label('Wind Speed (m/s)')
cbar.set_ticks(np.linspace(0, np.nanmax(wind_speed), num=10))

# Adicionar título e legendas aos eixos
plt.title('Wind Direction and Magnitude at 10m')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Exibir o gráfico
plt.show()
