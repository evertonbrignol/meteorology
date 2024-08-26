import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Carregar o arquivo GRIB e selecionar o nível de 500 hPa
ds = xr.open_dataset('geo_500hpa.grib', engine='cfgrib')

# Selecionar o geopotencial em 500 hPa
z500 = ds.sel(isobaricInhPa=500, method='nearest')['z']

# Converter a altura geopotencial de metros para decâmetros
z500_dam = z500 / 10.0

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

# Plotar a altura geopotencial a 500 hPa em decâmetros
contour = ax.contourf(z500_dam.longitude, z500_dam.latitude, z500_dam, cmap='viridis', transform=ccrs.PlateCarree())
cbar = plt.colorbar(contour, ax=ax, orientation='vertical', pad=0.05, aspect=40, shrink=0.8)
cbar.set_label('Geopotential Height (500 hPa)')

# Adicionar isolinhas
contour_lines = ax.contour(z500_dam.longitude, z500_dam.latitude, z500_dam, colors='black', transform=ccrs.PlateCarree(), linewidths=0.5)
ax.clabel(contour_lines, inline=True, fontsize=8, fmt='%1.0f ')

# Adicionar título e legendas aos eixos
plt.title('Geopotential Height at 500 hPa')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Exibir o gráfico
plt.show()
