import dataclasses
import json
import logging
from typing import Any
from typing import Dict
from typing import List

from .input_types import ComponentInfo
from .input_types import GreppoInputs

from .input_types import BarChart
from .input_types import LineChart
from .input_types import Multiselect
from .input_types import Number
from .input_types import Select
from .input_types import Text
from .input_types import Display
from .input_types import DrawFeature

from .layers.base_layer import BaseLayerComponent, BaseLayer
from .layers.tile_layer import TileLayer, TileLayerComponent
from .layers.wms_tile_layer import WMSTileLayer, WMSTileLayerComponent
from .layers.vector_layer import VectorLayer, VectorLayerComponent
from .layers.image_layer import ImageLayer, ImageLayerComponent
from .layers.raster_layer import RasterLayerComponent
from .layers.ee_layer import EarthEngineLayerComponent


class GreppoApp(object):
    """
    The main Greppo class that is the entry point for user scripts. User scripts will use this class via a module
    import variable `gpo`.

    This class provides an interface around available frontend component elements. The methods simply point to the
    backend representation of those frontend component elements (ie. `Number` is the backend class that a user script
    can access via `self.number`.
    """

    def __init__(self, name: str = "Untitled App"):
        self.name: str = name
        self.display = Display
        self.select = Select
        self.multiselect = Multiselect
        self.draw_feature = DrawFeature
        self.bar_chart = BarChart
        self.line_chart = LineChart

    # UX component proxy methods
    @staticmethod
    def number():
        """
        Interactive Number value rendered on the frontend.
        """
        return Number

    @staticmethod
    def text():
        """
        Interactive Text value rendered on the frontend.
        """
        return Text


class GreppoAppProxy(object):
    """
    Proxy object that mirrors the `GreppoApp` class. Adds additional methods that user scripts don't need to know about.
    These methods are used by a Greppo server to obtain an output from the user script that is then rendered by the
    frontend.
    """

    def __init__(self):
        # Map component data
        self.map_data: Dict = {'settings': {'zoom': 3,
                                            'center': [0, 0], 'maxZoom': 18, 'minZoom': 0}}
        self.base_layers: List[BaseLayer] = []
        self.tile_layers: List[TileLayer] = []
        self.wms_tile_layers: List[WMSTileLayer] = []
        self.vector_layers: List[VectorLayer] = []
        self.image_layers: List[ImageLayer] = []
        # TODO Cleanup raster temp
        # self.raster_image_reference: List[bytes] = []
        self.registered_inputs: List[ComponentInfo] = []

        # Input updates
        self.inputs = {}

    def display(self, **kwargs):
        display = Display(**kwargs)
        self.register_input(display)
        return display

    def number(self, **kwargs):
        number = Number(**kwargs)
        self.register_input(number)
        return number

    def text(self, **kwargs):
        text = Text(**kwargs)
        self.register_input(text)
        return text

    def select(self, **kwargs):
        select = Select(**kwargs)
        self.register_input(select)
        return select

    def multiselect(self, **kwargs):
        multiselect = Multiselect(**kwargs)
        self.register_input(multiselect)
        return multiselect

    def draw_feature(self, **kwargs):
        draw_feature = DrawFeature(**kwargs)
        self.register_input(draw_feature)
        return draw_feature

    def bar_chart(self, **kwargs):
        bar_chart = BarChart(**kwargs)
        self.register_input(bar_chart)
        return bar_chart

    def line_chart(self, **kwargs):
        line_chart = LineChart(**kwargs)
        self.register_input(line_chart)
        return line_chart

    def map(self, **kwargs):
        if 'zoom' in kwargs:
            self.map_data['settings']['zoom'] = kwargs.get('zoom')
        if 'center' in kwargs:
            self.map_data['settings']['center'] = kwargs.get('center')
        if 'max_zoom' in kwargs:
            self.map_data['settings']['maxZoom'] = kwargs.get('max_zoom')
        if 'min_zoom' in kwargs:
            self.map_data['settings']['minZoom'] = kwargs.get('min_zoom')

    def ee_layer(self, **kwargs):
        ee_layer_component = EarthEngineLayerComponent(**kwargs)
        ee_layer_dataclass = ee_layer_component.convert_to_dataclass()
        self.tile_layers.append(ee_layer_dataclass)

    def tile_layer(self, **kwargs):
        tile_layer_component = TileLayerComponent(**kwargs)
        tile_layer_dataclass = tile_layer_component.convert_to_dataclass()
        self.tile_layers.append(tile_layer_dataclass)

    def wms_tile_layer(self, **kwargs):
        wms_tile_layer_component = WMSTileLayerComponent(**kwargs)
        wms_tile_layer_dataclass = wms_tile_layer_component.convert_to_dataclass()
        self.wms_tile_layers.append(wms_tile_layer_dataclass)

    def base_layer(
        self,
        **kwargs
    ):
        base_layer_component = BaseLayerComponent(**kwargs)
        base_layer_dataclass = base_layer_component.convert_to_dataclass()
        self.base_layers.append(base_layer_dataclass)

    def vector_layer(self, **kwargs):
        vector_layer_component = VectorLayerComponent(**kwargs)
        vector_layer_dataclass = vector_layer_component.convert_to_dataclass()
        self.vector_layers.append(vector_layer_dataclass)

    def image_layer(self, **kwargs):
        image_layer_component = ImageLayerComponent(**kwargs)
        image_layer_dataclass = image_layer_component.convert_to_dataclass()
        self.image_layers.append(image_layer_dataclass)

    def raster_layer(self, **kwargs):
        raster_layer_component = RasterLayerComponent(**kwargs)
        image_layer_dataclass = raster_layer_component.convert_to_dataclass()
        self.image_layers.append(image_layer_dataclass)

    def overlay_layer(self, **kwargs):
        vector_layer_component = VectorLayerComponent(**kwargs)
        vector_layer_dataclass = vector_layer_component.convert_to_dataclass()
        self.vector_layers.append(vector_layer_dataclass)

    def update_inputs(self, inputs: Dict[str, Any]):
        self.inputs = inputs

    def register_input(self, discovered_input: GreppoInputs):
        """
        BarChart and LineChart are also registered with this `register_input` method. Maybe rename this method.
        """
        component_info = discovered_input.convert_to_component_info()
        self.registered_inputs.append(component_info)

        return discovered_input

    def gpo_prepare_data(self):
        """
        Take output of run script and setup the payload for the front-end to read.
        """

        app_output = {
            "base_layer_data": [],
            "tile_layer_data": [],
            "wms_tile_layer_data": [],
            "vector_layer_data": [],
            "image_layer_data": [],
            "component_info": [],
            "map": {},
        }
        app_output["map"] = self.map_data

        for _tile_layer in self.tile_layers:
            s = {}
            for k, v in _tile_layer.__dict__.items():
                _v = v
                s[k] = _v
            app_output["tile_layer_data"].append(s)

        for _wms_tile_layer in self.wms_tile_layers:
            s = {}
            for k, v in _wms_tile_layer.__dict__.items():
                _v = v
                s[k] = _v
            app_output["wms_tile_layer_data"].append(s)

        for _base_layer in self.base_layers:
            s = {}
            for k, v in _base_layer.__dict__.items():
                _v = v
                s[k] = _v
            app_output["base_layer_data"].append(s)

        for _vector_layer in self.vector_layers:
            s = {}
            for k, v in _vector_layer.__dict__.items():
                _v = v
                if k == "data":
                    _v = json.loads(v.to_json())
                s[k] = _v

            app_output["vector_layer_data"].append(s)

        for _image_layer in self.image_layers:
            s = {}
            for k, v in _image_layer.__dict__.items():
                _v = v
                s[k] = _v
            app_output["image_layer_data"].append(s)

        app_output["component_info"] = [
            dataclasses.asdict(i) for i in self.registered_inputs
        ]

        logging.info("Len component info: ", len(app_output["component_info"]))

        return app_output

    # def gpo_reference_data(self):
    #     """ Only return one reference image for testing. """
    #     if len(self.raster_image_reference) == 0:
    #         return None
    #     return self.raster_image_reference[0]


app = GreppoApp()
