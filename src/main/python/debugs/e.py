import folium

m = folium.Map([40, -100], zoom_start=4)
url = 'http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi'
w = folium.raster_layers.WmsTileLayer(
    url=url,
    name='test',
    fmt='image/png',
    layers='nexrad-n0r-900913',
    attr=u'Weather data © 2012 IEM Nexrad',
    transparent=True
)
w.add_to(m)

m.save('asd.html')