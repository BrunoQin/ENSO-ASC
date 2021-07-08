import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap
import cmaps


def plot_helper(data, save=False, file_name=None, title=None, llcrnrlon=150, urcrnrlon=230, llcrnrlat=-40, urcrnrlat=40):
    m = Basemap(projection="cyl", llcrnrlon=llcrnrlon, urcrnrlon=urcrnrlon,
                llcrnrlat=llcrnrlat, urcrnrlat=urcrnrlat, resolution='i')

    m.fillcontinents(color='grey')
    m.drawcoastlines(linewidth=0.1)

    m.drawparallels(np.arange(llcrnrlat, urcrnrlat+1, 30), labels=[True, False, True, False], linewidth=0.2, color='k', fontsize=6)
    m.drawmeridians(np.arange(llcrnrlon, urcrnrlon+1, 30), labels=[True, False, False, True], linewidth=0.2, color='k', fontsize=6)

    xx = np.linspace(162, 218, 56)
    yy = np.linspace(-28, 28, 56)
    Lon, Lat = np.meshgrid(xx, yy)
    x, y = m(Lon, Lat)
    cs = m.contourf(x, y, data, cmap=cmaps.GMT_no_green)
    if save:
        cbar = m.colorbar(cs)
        cbar.outline.set_linewidth(1)
        plt.title(title, fontsize=6, pad=20)
        plt.savefig(file_name)
        plt.close(0)
    return m


def plot_helper(data, llcrnrlon=150, urcrnrlon=230, llcrnrlat=-40, urcrnrlat=40, xgrid=0, ygrid=0):
    m = Basemap(projection="cyl", llcrnrlon=llcrnrlon, urcrnrlon=urcrnrlon,
                llcrnrlat=llcrnrlat, urcrnrlat=urcrnrlat, resolution='i')

    # m.fillcontinents(color='grey')
    m.drawcoastlines(linewidth=0.2)
    m.drawcountries()

    m.drawparallels(np.arange(llcrnrlat, urcrnrlat+1, 30), labels=[True, False, True, False], linewidth=0.2, color='k', fontsize=6)
    m.drawmeridians(np.arange(llcrnrlon, urcrnrlon+1, 30), labels=[True, False, False, True], linewidth=0.2, color='k', fontsize=6)
    # m.shadedrelief()

    xx = np.linspace(llcrnrlon, urcrnrlon, xgrid)
    yy = np.linspace(llcrnrlat, urcrnrlat, ygrid)
    Lon, Lat = np.meshgrid(xx, yy)
    x, y = m(Lon, Lat)
    cs = m.contourf(x, y, data, cmap=cmaps.GMT_no_green)
    cbar = m.colorbar(cs)
    cbar.outline.set_linewidth(1)
    return m
