import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import matplotlib.colors as mcolors

# Carregar o arquivo GRIB e selecionar a variável de pressão ao nível do mar
ds = xr.open_dataset('msl.grib', engine='cfgrib')
msl = ds['msl']  # Pressão ao nível do mar (em Pa)

# Converter a pressão de Pa para hPa (1 hPa = 100 Pa)
msl_hpa = msl / 100.0

# Definir os níveis de contorno de 4 em 4 hPa, até 1032 hPa
levels = np.arange(np.floor(msl_hpa.min()), 1032, 4)

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

# Definir uma paleta de cores personalizada de azul escuro para vermelho escuro
cmap = mcolors.LinearSegmentedColormap.from_list('pressure_cmap', ['darkblue', 'white', 'darkred'])

# Plotar a pressão ao nível do mar com as cores personalizadas até 1028 hPa
contourf = ax.contourf(msl.longitude, msl.latitude, msl_hpa, levels=levels, cmap=cmap, transform=ccrs.PlateCarree())

# Adicionar as isolinhas (linhas de contorno) com 4 hPa de diferença em preto
contour = ax.contour(msl.longitude, msl.latitude, msl_hpa, levels=levels, colors='black', transform=ccrs.PlateCarree())
ax.clabel(contour, inline=True, fontsize=8, fmt='%1.0f hPa')  # Adicionar rótulos às isolinhas

# Adicionar uma barra de cores na lateral direita
cbar = plt.colorbar(contourf, orientation='vertical', pad=0.05, aspect=40, shrink=0.8)
cbar.set_label('Mean Sea Level Pressure (hPa)')
cbar.set_ticks(np.arange(np.floor(msl_hpa.min()), 1032, 4))

# Adicionar título e legendas aos eixos
plt.title('Mean Sea Level Pressure with 4 hPa Intervals (up to 1032 hPa)')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Exibir o gráfico
plt.show()
