# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sentinel_toolkit',
 'sentinel_toolkit.colorimetry',
 'sentinel_toolkit.colorimetry.illuminants',
 'sentinel_toolkit.colorimetry.tests',
 'sentinel_toolkit.ecostress',
 'sentinel_toolkit.ecostress.tests',
 'sentinel_toolkit.srf',
 'sentinel_toolkit.srf.tests']

package_data = \
{'': ['*'], 'sentinel_toolkit.srf': ['tests/test_data/*']}

install_requires = \
['colour-science>=0.4.1,<0.5.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.4.2,<2.0.0',
 'spectral>=0.22.4,<0.23.0']

setup_kwargs = {
    'name': 'sentinel-toolkit',
    'version': '2.0.0',
    'description': 'Various sentinel tools',
    'long_description': '# Sentinel-Toolkit\n\n## Description\n\nThis repository provides various utility tools for working with Sentinel data like:\n\n1. Reading Sentinel-2 Spectral Response Functions\n2. Converting colour.SpectralDistribution to Sentinel Responses\n\n## Installation\n\nSentinel-Toolkit and its primary dependencies can be easily installed from the Python Package Index by issuing this\ncommand in a shell:\n\n```shell\n$ pip install --user sentinel-toolkit\n```\n\n## Examples\n\n### Reading Sentinel-2 Spectral Response Functions\n\nGiven an Excel file containing the Sentinel-2 Spectral Response Functions,\nread Band2, Band3 and Band4 data in the wavelength range of (360, 830)\ninto a corresponding colour.MultiSpectralDistributions object:\n\n```python\nfrom sentinel_toolkit import S2Srf\n\ns2a_srf = S2Srf("srf.xlsx", satellite="A")\nbn = ["S2A_SR_AV_B2", "S2A_SR_AV_B3", "S2A_SR_AV_B4"]\nwr = (360, 830)\n\nbands_responses_distribution = s2a_srf.get_bands_responses_distribution(band_names=bn, wavelength_range=wr)\n```\n\nGiven an Excel file containing the Sentinel-2 Spectral Response Functions,\nread all band data in the wavelength range of (360, 830)\ninto a corresponding ndarray:\n\n```python\nfrom sentinel_toolkit import S2Srf\n\ns2a_srf = S2Srf("srf.xlsx", satellite="A")\n\n# By default, band_names is all band names and wavelength_range is (360, 830)\nall_bands_responses = s2a_srf.get_bands_responses()\n```\n\n### Converting SpectralDistribution to Sentinel-2 Responses\n\nGiven a colour.SpectralDistribution, Illuminant and Spectral Response Functions,\ncalculate the Sentinel-2 Responses. (WIP)\n',
    'author': 'Georgi Genchev',
    'author_email': 'gdgenchev97@gmail.com',
    'maintainer': 'Georgi Genchev',
    'maintainer_email': 'gdgenchev97@gmail.com',
    'url': 'https://github.com/sentinel-toolkit/sentinel-toolkit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
