"""
This is a simple app that shows how we can control the leaflet map
from PyQt widgets. In this app we will explore how effective the
polio vaccine is, and how humanity can come together and trump all
other national, regional and cultural biases to truly achieve
something great
"""

import json
import math
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QSlider, QVBoxLayout, QWidget

from pyqtlet import L, MapWidget

DATA_PATH = 'data/polio_data.json'
MAX_SIZE = 50


class PolioEradiactor(QWidget):
    def __init__(self, data_path=DATA_PATH):
        super().__init__()
        self.data_path = data_path
        self.data = {}
        self._init_ui()
        self._init_map()
        self._load_data()
        self.show()

    def _init_ui(self):
        # Create the widgets and the layout
        self.layout = QVBoxLayout()
        self.mapWidget = MapWidget()
        self.yearLayout = QHBoxLayout()
        self.yearLabel = QLabel()
        self.yearSlider = QSlider(Qt.Horizontal)
        self.yearLayout.addWidget(self.yearLabel)
        self.yearLayout.addWidget(self.yearSlider)
        self.layout.addWidget(self.mapWidget)
        self.layout.addItem(self.yearLayout)
        self.setLayout(self.layout)
        self.yearSlider.valueChanged.connect(self._linkSlider)

    def _init_map(self):
        self.map = L.map(self.mapWidget)
        self.map.setView([0, 0], 1)
        L.tileLayer('http://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.png', {'noWrap': 'true'}).addTo(self.map)
        # Create empty layer group to hold the data
        self.layerGroup = L.layerGroup()
        self.map.addLayer(self.layerGroup)

    def _load_data(self):
        with open(self.data_path) as data_in:
            self.data = json.load(data_in)
        years = [int(year) for year in self.data['incidents']]
        self._getMaxIncidents()
        # We want to create markers for each country based on number
        # of incidents and save them for every year in the dataset
        self.yearLayers = {}
        for year in self.data['incidents']:
            self.yearLayers[year] = []
            for country in self.data['incidents'][year]:
                coords = self.data['countries'][country]['coordinates']
                number = self.data['incidents'][year][country]
                radius = self._getMarkerRadius(number)
                # While creating markers, options can also be passed
                yearMarker = L.circleMarker(coords, {'radius': radius, 'color': '#C62828', 'weight': 1})
                # A popup allows extra data to be shown on click of the marker
                yearMarker.bindPopup(
                    'In {year}, {country} has {number} incidents of polio reported'.format(year=year, country=country,
                                                                                           number=number))
                self.yearLayers[year].append(yearMarker)
        # Initialise the slider based on the data
        self.yearSlider.setMinimum(min(years))
        self.yearSlider.setMaximum(max(years))
        self.yearLabel.setText(str(min(years)))

    def _getMaxIncidents(self):
        incidents = []
        for year in self.data['incidents']:
            for country in self.data['incidents'][year]:
                incidents.append(self.data['incidents'][year][country])
        self.highIncidents = max(incidents)

    def _getMarkerRadius(self, value):
        # We want the marker size to be exponential to the number
        power = (1 / 3)
        return MAX_SIZE * (value ** power) / (self.highIncidents ** power)

    def _linkSlider(self, year):
        # Every time the slider changes, we want to change the label
        # showing the year, and the data shown on the map
        self.yearLabel.setText(str(year))
        # If any method has not been implemented in pyqtlet, we can
        # use the runJavaScript method to run the method
        self.layerGroup.clearLayers()
        for marker in self.yearLayers[str(year)]:
            self.layerGroup.addLayer(marker)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = PolioEradiactor()
    sys.exit(app.exec_())
