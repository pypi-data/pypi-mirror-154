# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dearpygui_map']

package_data = \
{'': ['*']}

install_requires = \
['dearpygui>=1.3.1,<2.0.0']

setup_kwargs = {
    'name': 'dearpygui-map',
    'version': '0.1.0',
    'description': 'Map widget for Dear PyGui',
    'long_description': '# dearpygui-map\nMap widget for Dear PyGui\n\n## Installation\n\n### Requirements\n\n- Python >= 3.7\n- Dear PyGui >= 1.3.1\n\n### Option 1 - pip\n\nYou can install this package from pip, with\n\n    pip install dearpygui-map\n\n### Option 2 - Local install from sources\n\nClone code repository from your local machine, install from there. [Poetry][poetry-install] is required.\n\n    git clone https://github.com/mkouhia/dearpygui-map.git\n    cd dearpygui-map\n    poetry build\n    # take note of the build step output, install package from the dist folder\n    pip install dist/PRODUCED_PACKAGE.whl\n\n\n## Usage\n\nThis basic example creates a map widget with defined size, initial center point (latitude, longitude) and initial zoom level. The zoom levels are same as on [tiled maps][tile-zoom-levels], for example 12 could represent a town-sized view. Larger is more zoomed in.\n\n```python\nimport dearpygui.dearpygui as dpg\nimport dearpygui_map as dpg_map\n\ndpg.create_context()\n\nwith dpg.window(label="Map demo"):\n    dpg_map.add_map_widget(\n        width=700,\n        height=500,\n        center=(60.1641, 24.9402),\n        zoom_level=12)\n\ndpg.create_viewport(title="Dear PyGui map widget demo", width=800, height=600)\ndpg.setup_dearpygui()\ndpg.show_viewport()\ndpg.start_dearpygui()\ndpg.destroy_context()\n```\n\nThe function `add_map_widget` places a Dear PyGui drawlist with map contents,\nreturn value is the drawlist tag.\n\nBy default, OpenStreetMap is used as the map tile source. This can be configured with `add_map_widget` argument `tile_source`, with similar source definition:\n\n```python\nOpenStreetMap = TileServer(\n    name="OpenStreetMap",\n    base_url="http://{subdomain}.tile.openstreetmap.org/{z}/{x}/{y}.png",\n    subdomains=["a", "b", "c"],\n    max_zoom_level=19,\n    license_text="© OpenStreetMap contributors",\n    thread_limit=2,\n)\n```\n\n## Technical details\n\nTiles are downloaded from the supplier on a background thread.\nWhenever map is zoomed or moved, more tiles are downloaded.\nThe tiles are cached to local storage path in user cache directory - for different platforms, cache directories are:\n\n    Windows:    C:\\Users\\<username>\\AppData\\Local\\dearpygui_map\\Cache\n    Mac OS X:   ~/Library/Caches/dearpygui_map\n    Other:      ~/.cache/dearpygui_map\n\n\n### Known issues\n\nAs for now, dearpygui-map is in its early design phase and contains some items that may not be acceptable in production environments.\nThese issues will be addressed later\n\n- Tile download threads are created every time `TileManager.draw_layer` is called.\n- Non-visible tiles are not removed from dearpygui\n- Zooming and panning leads to wait times before tiles are ready to be shown.\n\n## Development\n\n### Environment\n\nPoetry is required for development (see [installation instructions][poetry-install])\n\n1. Create development environment with `poetry install`\n2. Enter environment with `poetry shell`\n\n\n### Code quality and testing\n\nAll code is to be formatted with `black`:\n\n    black dearpygui_map\n\nand code quality checked with `pylint`:\n\n    pylint dearpygui_map\n\nTests should be written in `pytest`, targeting maximum practical code coverage. Tests are run with:\n\n    pytest\n\nand test coverage checked with\n\n    pytest --cov\n\nOptionally, html test coverage reports can be produced with\n\n    pytest --cov dearpygui_map --cov-report html\n\n\n### Contributions\n\nContributions are welcome. Please also see GitHub issues and milestones.\n\n\n[poetry-install]: https://python-poetry.org/docs/#installation "Poetry: Installation"\n[tile-zoom-levels]: https://wiki.openstreetmap.org/wiki/Zoom_levels "Open Street Map wiki: Zoom levels"\n',
    'author': 'Mikko Kouhia',
    'author_email': 'mikko.kouhia@iki.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mkouhia/dearpygui-map',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
