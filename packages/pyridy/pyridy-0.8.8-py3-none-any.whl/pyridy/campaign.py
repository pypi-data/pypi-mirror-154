import itertools
import json
import logging
import multiprocessing
import os
from functools import partial
from multiprocessing import Pool
from pathlib import Path
from typing import List, Union, Tuple, Optional, Type

import networkx as nx
import numpy as np
from ipyleaflet import Map, Polyline, Marker, Icon, FullScreenControl, ScaleControl
from ipywidgets import HTML
from networkx import connected_components
from tqdm.auto import tqdm

from . import config
from .file import RDYFile
from .osm import OSM, OSMRailwaySwitch, OSMRailwaySignal, OSMLevelCrossing
from .osm.utils import boxes_to_edges, iou
from .utils import GPSSeries, TimeSeries

logger = logging.getLogger(__name__)


class Campaign:
    def __init__(self, name="",
                 folder: Union[list, str] = None,
                 recursive=True,
                 exclude: Union[list, str] = None,
                 sync_method: str = "timestamp",
                 timedelta_unit: str = 'timedelta64[ns]',
                 strip_timezone: bool = True,
                 cutoff: bool = True,
                 lat_sw: float = None,
                 lon_sw: float = None,
                 lat_ne: float = None,
                 lon_ne: float = None,
                 download_osm_data: bool = False,
                 map_matching: bool = False,
                 osm_recurse_type: str = ">",
                 railway_types: Union[list, str] = None,
                 series: Union[List[Type[TimeSeries]], Type[TimeSeries]] = None):
        """

        Parameters
        ----------
        name: str
            Name of the campaign
        folder: str or list of str
            Folder or list of folders that should be imported
        recursive: bool, default: True
            Flag if folders should be searched recursively
        exclude: str or list of str
            Name(s) of file or folder that should be excluded
        sync_method: str
            Method to use to sync timestamps of individual files
        strip_timezone: bool, default: True
            Strips timezone from timestamps as np.datetime64 does not support timezones
        cutoff: bool, default: True
            If True, cutoffs the measurements precisely to the timestamp when the measurement was started, respectively
            stopped. By default, Ridy measurement files can contain several seconds of measurements from before/after
            the button press
        lat_sw: float
            South west Latitude of the campaign, if the geographic extent is not given via arguments, the library tries
            to determine the geographic extent based on the GPS tracks
        lon_sw: float
            South west longitude of the campaign
        lat_ne: float
            North east latitude of the campaign
        lon_ne: float
            North east longitude of the campaign
        download_osm_data: bool, default: False
            If True download OSM data via the Overpass API
        map_matching: bool, default: False
            If True removes tries to match GPS track of each file to most reasonable OSM nodes
        railway_types: list or list of str
            Railway type to be downloaded from OSM, e.g., "rail", "subway", "tram" or "light_rail"
        osm_recurse_type : str
            Recurse type to be used when querying OSM data using the overpass API
        series: list or TimeSeries
            Classes of TimeSeries to load, if None all TimeSeries of each file will be imported
        """
        self.folder = folder
        self.name = name
        self.files: List[RDYFile] = []

        # Geographic extent of campaign
        self.lat_sw, self.lon_sw = lat_sw, lon_sw
        self.lat_ne, self.lon_ne = lat_ne, lon_ne
        self.extent = [self.lon_sw, self.lat_sw, self.lon_ne, self.lat_ne]

        self.bboxs = []
        self.s_bboxs = []  # Simplified bounding boxes

        self.osm = None
        self.osm_recurse_type = osm_recurse_type
        self.railway_types = railway_types
        self.osm_mappings = {}  # Map Matching results for each file
        self.map_matching = map_matching

        # Sanity check if series is arg is valid
        if series:
            if type(series) is list:
                for s in series:
                    if not issubclass(s, TimeSeries):
                        raise ValueError("%s in %s is not a TimeSeries!" % (type(s), list(series)))
                self._series = series
            elif issubclass(series, TimeSeries):
                self._series = [series]
                pass
            else:
                raise ValueError("series argument must be list of TimeSeries or TimeSeries! not %s" % type(series))
        else:
            self._series = None

        if sync_method is not None and sync_method not in ["timestamp", "seconds", "device_time", "gps_time",
                                                           "ntp_time"]:
            raise ValueError(
                "synchronize argument must 'timestamp', 'seconds', 'device_time', 'gps_time' or 'ntp_time' not %s" %
                sync_method)

        self.sync_method = sync_method
        self.timedelta_unit = timedelta_unit # Only relevant for timestamp sync method
        self.strip_timezone = strip_timezone
        self.cutoff = cutoff

        self.results = {}  # Dictionary for Post Processing Results

        if folder:
            self.import_folder(self.folder, recursive, exclude,
                               cutoff=self.cutoff,
                               sync_method=self.sync_method,
                               timedelta_unit=self.timedelta_unit,
                               strip_timezone=self.strip_timezone)

        if not self.lat_sw or not self.lat_ne or not self.lon_sw or not self.lon_ne:
            self.determine_geographic_extent()

        if download_osm_data:
            self.download_osm_data()
        else:
            self.osm = None

    def __call__(self, name):
        results = list(filter(lambda file: file.filename == name, self.files))
        if len(results) == 1:
            return results[0]
        else:
            return results

    def __getitem__(self, index) -> RDYFile:
        return self.files[index]

    def __len__(self):
        return len(self.files)

    @property
    def osm(self):
        return self._osm

    @osm.setter
    def osm(self, value):
        for f in tqdm(self):
            f.osm = value
            if self.map_matching:
                f.do_map_matching()

        self._osm = value

    def add_tracks_to_map(self, m: Map) -> Map:
        """ Add all GPS tracks from the campaign files to a Map

        Parameters
        ----------
        m: Map
            ipyleaflet Map

        Returns
        -------
        Map

        """
        for file in self.files:
            m = self.add_track_to_map(m, file=file)

        return m

    def add_track_to_map(self, m: Map, name: str = "", file: RDYFile = None) -> Map:
        """ Adds a GPS track from a file to the Map

        Parameters
        ----------
        m: Map
            ipyleaflet map
        name: str
            Name of the file that should be drawn onto the map
        file: RDYFile
            Alternatively, provide RDYFile that should be drawn on the map

        Returns
        -------
        Map

        """
        if name != "":
            files = [self(name)]
        elif file is not None:
            files = [file]

        else:
            raise ValueError("You must provide either a filename or the file")

        for f in files:
            gps_series = f.measurements[GPSSeries]
            coords = gps_series.to_ipyleaflef()

            if coords != [[]]:
                file_polyline = Polyline(locations=coords, color=f.color, fill=False, weight=4,
                                         dash_array='10, 10')
                m.add_layer(file_polyline)

                # Add Start/End markers
                start_icon = Icon(
                    icon_url='https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
                    shadow_url='https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                    icon_size=[25, 41],
                    icon_anchor=[12, 41],
                    popup_anchor=[1, -34],
                    shadow_size=[41, 41])

                end_icon = Icon(
                    icon_url='https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
                    shadow_url='https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                    icon_size=[25, 41],
                    icon_anchor=[12, 41],
                    popup_anchor=[1, -34],
                    shadow_size=[41, 41])

                start_marker = Marker(location=tuple(coords[0]), draggable=False, icon=start_icon)
                end_marker = Marker(location=tuple(coords[-1]), draggable=False, icon=end_icon)

                start_message = HTML()
                end_message = HTML()
                start_message.value = "<p>Start:</p><p>" \
                                      + str(f.filename or '') + "</p><p>" \
                                      + str(getattr(f.device, "manufacturer", "")) + "; " \
                                      + str(getattr(f.device, "model", "")) + "</p>"
                end_message.value = "<p>End:</p><p>" \
                                    + str(f.filename or '') + "</p><p>" \
                                    + str(getattr(f.device, "manufacturer", "")) + "; " \
                                    + str(getattr(f.device, "model", "")) + "</p>"

                start_marker.popup = start_message
                end_marker.popup = end_message

                m.add_layer(start_marker)
                m.add_layer(end_marker)

        return m

    def add_osm_routes_to_map(self, m: Map) -> Map:
        """ Adds OSM Routes from the downloaded OSM Region

        Parameters
        ----------
        m: Map
            ipyleaflet Map

        Returns
        -------
        Map

        """
        if self.osm:
            for line in self.osm.railway_lines:
                for track in line.tracks:
                    coords = track.to_ipyleaflet()
                    file_polyline = Polyline(locations=coords, color=line.color, fill=False, weight=4)
                    m.add_layer(file_polyline)
        else:
            logger.warning("No OSM region downloaded!")

        return m

    def add_osm_railway_elements_to_map(self, m: Map) -> Map:
        """ Draws railway elements using markers on top of a map

        Parameters
        ----------
        m: Map
            Map where railway elements should be drawn onto

        Returns
        -------
        m: Map
            Map containing railway elements

        """
        if self.osm:
            for el in self.osm.railway_elements:
                if type(el) == OSMRailwaySwitch:
                    icon = Icon(
                        icon_url='https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-black.png',
                        shadow_url='https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                        icon_size=[25, 41],
                        icon_anchor=[12, 41],
                        popup_anchor=[1, -34],
                        shadow_size=[41, 41])
                    marker = Marker(location=(el.lat, el.lon), draggable=False, icon=icon)

                    m.add_layer(marker)
                elif type(el) == OSMRailwaySignal:
                    pass
                elif type(el) == OSMLevelCrossing:
                    pass
                else:
                    pass
        return m

    def clear_files(self):
        """
            Clear all files from the campaign
        """
        self.files = []

    def create_map(self, center: Tuple[float, float] = None,
                   show_gps_tracks=True,
                   show_railway_elements=False) -> Map:
        """ Creates a ipyleaflet map showing the GPS tracks of measurement files

        Parameters
        ----------
        show_gps_tracks
        center
        show_railway_elements

        Returns
        -------

        """
        if not center:
            if self.lat_sw and self.lat_ne and self.lon_sw and self.lon_ne:
                center = (
                    (self.lat_sw + self.lat_ne) / 2,
                    (self.lon_sw + self.lon_ne) / 2)
            else:
                raise ValueError("Cant determine geographic center of campaign, enter manually using 'center' argument")

        m = Map(center=center, zoom=12, scroll_wheel_zoom=True, basemap=config.OPEN_STREET_MAP_DE)
        m.add_control(ScaleControl(position='bottomleft'))
        m.add_control(FullScreenControl())

        # Add map
        m.add_layer(config.OPEN_RAILWAY_MAP)

        # Plot GPS point for each measurement and OSM Tracks
        m = self.add_osm_routes_to_map(m)

        if show_gps_tracks:
            m = self.add_tracks_to_map(m)

        if show_railway_elements:
            m = self.add_osm_railway_elements_to_map(m)

        return m

    def determine_geographic_extent(self):
        """ Determines the geographic extent of the campaign in terms of min/max lat/lon

        """
        min_lats = []
        max_lats = []
        min_lons = []
        max_lons = []

        for f in self.files:
            gps_series = f.measurements[GPSSeries]
            if gps_series.is_empty():
                continue
            else:
                min_lats.append(gps_series.lat.min())
                max_lats.append(gps_series.lat.max())
                min_lons.append(gps_series.lon.min())
                max_lons.append(gps_series.lon.max())

        self.lat_sw = min(min_lats) if min_lats else None
        self.lat_ne = max(max_lats) if max_lats else None
        self.lon_sw = min(min_lons) if min_lons else None
        self.lon_ne = max(max_lons) if max_lons else None

        self.extent = [self.lon_sw, self.lat_sw, self.lon_ne, self.lat_ne]

        logging.info("Geographic boundaries of measurement campaign: Lat SW: %s, Lon SW: %s, Lat NE: %s, Lon NE: %s"
                     % (str(self.lat_sw), str(self.lon_sw), str(self.lat_ne), str(self.lon_ne)))

    def do_map_matching(self, rematch=False, **kwargs):
        """ Performs map matching for all files in campaign

        Parameters
        ----------
        rematch: Bool, default: False
            If True performs map matching again, even when file already contains a map matching
        """
        if self.osm:
            for f in tqdm(self):
                if f.matched_ways and f.matched_nodes:
                    if rematch:
                        logger.info("(%s) File already has a map matching! Rematching..." % f.filename)
                        f.do_map_matching(**kwargs)
                    else:
                        logger.info("(%s) File already has a map matching! Skipping..." % f.filename)
                        continue
                else:
                    f.do_map_matching(**kwargs)
        else:
            raise RuntimeError("Can't do Map Matching, because no OSM data has been downloaded!")
        pass

    def download_osm_data(self):
        self.bboxs = [f.bbox for f in self.files if f.bbox]
        self.s_bboxs = []  # Filtered bounding boxes

        # Unify bounding boxes with a large overlap to reduce number of queries
        # Cluster boxes by overlap
        clusters = []
        for b1, b2 in itertools.combinations(self.bboxs, 2):
            if iou(b1, b2) > config.options["OSM_BOUNDING_BOX_SPLIT_IOU_THRES"]:
                clusters.append([str(b1), str(b2)])

        G = nx.Graph()
        for c in clusters:
            G.add_nodes_from(c)
            G.add_edges_from(boxes_to_edges(c))

        clusters = [list(c) for c in list(connected_components(G))]
        # Convert boxes back to float
        clusters = [[json.loads(b) for b in c] for c in clusters]

        # Add boxes not part of any cluster
        for b in self.bboxs:
            if b not in list(itertools.chain.from_iterable(clusters)):
                clusters.append([b])

        # Simplify boxes
        for c in clusters:
            arr = np.array(c)
            self.s_bboxs.append([arr[:, 0].min(), arr[:, 1].min(), arr[:, 2].max(), arr[:, 3].max()])

        # fig, ax = plt.subplots(1, figsize=(6, 6))
        # for b in self.bboxs:
        #     ax.add_patch(Rectangle((b[0], b[1]), b[2] - b[0], b[3] - b[1], alpha=1, edgecolor='r', facecolor='none'))
        #
        # for b in self.s_bboxs:
        #     ax.add_patch(Rectangle((b[0], b[1]), b[2] - b[0], b[3] - b[1], alpha=1, edgecolor='g', facecolor='none'))
        #
        # ax.grid()
        # ax.set_xlim([self.lon_sw, self.lon_ne])
        # ax.set_ylim([self.lat_sw, self.lat_ne])
        # plt.show()

        if config.options["OSM_SINGLE_BOUNDING_BOX"]:
            self.osm = OSM(bbox=self.extent, desired_railway_types=self.railway_types, recurse=self.osm_recurse_type)
        else:
            if config.options["OSM_BOUNDING_BOX_OPTIMIZATION"] and self.s_bboxs:
                self.osm = OSM(bbox=self.s_bboxs, desired_railway_types=self.railway_types,
                               recurse=self.osm_recurse_type)
            else:
                if self.bboxs:
                    self.osm = OSM(bbox=self.bboxs, desired_railway_types=self.railway_types, recurse=self.osm_recurse_type)
                else:
                    raise ValueError("Can't retrieve OSM Data because bounding boxes are empty!")

    def import_files(self, file_paths: Union[list, str] = None,
                     sync_method: str = "timestamp",
                     timedelta_unit: str = 'timedelta64[ns]',
                     cutoff: bool = True,
                     strip_timezone: bool = True,
                     det_geo_extent: bool = True,
                     use_multiprocessing: bool = False,
                     download_osm_region: bool = False,
                     railway_types: Union[list, str] = None,
                     osm_recurse_type: Optional[str] = None,
                     series: Union[List[Type[TimeSeries]], Type[TimeSeries]] = None):
        """ Import files into the campaign

        Parameters
        ----------
        series
        timedelta_unit: str , default: 'timedelta64[ns]'
            Timedelta unit for timestamp sync method
        strip_timezone: bool, default: True
            If True, strips timezone from timestamp arrays
        cutoff: bool, default: True
            If True, cutoffs measurement precisely to timestamp when the measurement was started respectively stopped
        file_paths: str or list of str
            Individual file paths of the files that should be imported
        sync_method: str
            Method to use for timestamp syncing
        det_geo_extent: bool, default: True
            If True, determine the geographic extent of the imported files
        download_osm_region: bool, default: False
            If True, download OSM Data via the Overpass API
        railway_types: str or list of str
            Railway types to be downloaded via the Overpass API
        osm_recurse_type : str
            Recurse type to be used when querying OSM data using the overpass API
        use_multiprocessing : bool, default: True
            If True, uses multiprocessing to import Ridy files
        """
        if osm_recurse_type:
            self.osm_recurse_type = osm_recurse_type

        if type(file_paths) == str:
            file_paths = [file_paths]
        elif type(file_paths) == list:
            pass
        else:
            raise TypeError("paths argument must be list of str or str")

        # Sanity check if series is arg is valid
        if series:
            if type(series) is list:
                for s in series:
                    if not issubclass(s, TimeSeries):
                        raise ValueError("%s in %s is not a TimeSeries!" % (type(s), list(series)))
                self._series = series
            elif issubclass(series, TimeSeries):
                self._series = [series]
                pass
            else:
                raise ValueError("series argument must be list of TimeSeries or TimeSeries! not %s" % type(series))

        if use_multiprocessing:
            with Pool(multiprocessing.cpu_count()) as p:
                files = list(tqdm(p.imap(partial(RDYFile,
                                                 sync_method=sync_method,
                                                 strip_timezone=strip_timezone,
                                                 cutoff=cutoff,
                                                 series=self._series), file_paths)))
                for f in files:
                    self.files.append(f)
        else:
            for p in tqdm(file_paths):
                self.files.append(RDYFile(path=p,
                                          sync_method=sync_method,
                                          timedelta_unit=timedelta_unit,
                                          strip_timezone=strip_timezone,
                                          cutoff=cutoff,
                                          series=self._series))

        self.railway_types = railway_types

        if osm_recurse_type:
            self.osm_recurse_type = osm_recurse_type

        if det_geo_extent:
            self.determine_geographic_extent()

        if download_osm_region:
            self.download_osm_data()

    def import_folder(self, folder: Union[list, str] = None,
                      recursive: bool = True,
                      exclude: Union[list, str] = None,
                      **kwargs):
        """ Imports folder(s) into the campaign

        Parameters
        ----------
        folder: str or list of str
            Folder(s) that should be imported
        recursive: bool, default: True
            Flag if folders should be imported recursively, i.e., whether subfolders should also be searched
        exclude: str or list of str
            Folder(s) or file(s) that should be excluded while importing
        """
        if exclude is None:
            exclude = []
        elif type(exclude) == str:
            exclude = [exclude]

        if type(folder) == str:
            folder = [folder]
        elif type(folder) == list:
            pass
        else:
            raise TypeError("folder argument must be list or str")

        file_paths = []

        for fdr in folder:
            if recursive:
                all_paths = list(Path(fdr).rglob("*"))

                # File paths without excluded files or folder names
                for p in all_paths:
                    inter = set(p.parts).intersection(set(exclude))
                    if len(inter) > 0:
                        continue
                    else:
                        if p.suffix in [".rdy", ".sqlite"]:
                            file_paths.append(p)
                        else:
                            continue
            else:
                _, _, files = next(os.walk(fdr))
                for f in files:
                    file_path = os.path.join(fdr, f)
                    _, ext = os.path.splitext(file_path)
                    if f not in exclude and ext in [".rdy", ".sqlite"]:
                        file_paths.append(file_path)

                pass

        self.import_files(file_paths, **kwargs)
