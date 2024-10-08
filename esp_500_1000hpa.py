import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Carregar o arquivo GRIB e selecionar os níveis de 1000 hPa e 500 hPa
ds = xr.open_dataset('esp_500_1000hpa.grib', engine='cfgrib')

# Selecionar o geopotencial em 1000 hPa e 500 hPa
z1000 = ds.sel(isobaricInhPa=1000, method='nearest')['z']
z500 = ds.sel(isobaricInhPa=500, method='nearest')['z']

# Converter o geopotencial para altura geopotencial em metros
g = 9.80665  # aceleração gravitacional em m/s²
h1000 = z1000 / g
h500 = z500 / g

# Calcular a espessura da camada em decâmetros (1 dam = 10 metros)
thickness_dam = (h500 - h1000) 

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

# Plotar a espessura da camada em decâmetros
contour = ax.contourf(thickness_dam.longitude, thickness_dam.latitude, thickness_dam, cmap='viridis', transform=ccrs.PlateCarree())
cbar = plt.colorbar(contour, ax=ax, orientation='vertical', pad=0.05, aspect=40, shrink=0.8)
cbar.set_label('Layer Thickness (1000 - 500 hPa)')

# Adicionar isolinhas nas bordas de troca de cor
contour_lines = ax.contour(thickness_dam.longitude, thickness_dam.latitude, thickness_dam, colors='black', transform=ccrs.PlateCarree(), linewidths=0.5)
ax.clabel(contour_lines, inline=True, fontsize=8, fmt='%1.0f ')

# Adicionar título e legendas aos eixos
plt.title('Layer Thickness (1000 - 500 hPa)')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Exibir o gráfico
plt.show()
