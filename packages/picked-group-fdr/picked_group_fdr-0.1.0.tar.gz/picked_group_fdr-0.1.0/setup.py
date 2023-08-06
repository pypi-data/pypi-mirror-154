# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['picked_group_fdr',
 'picked_group_fdr.pipeline',
 'picked_group_fdr.quant',
 'picked_group_fdr.simulation']

package_data = \
{'': ['*']}

install_requires = \
['cython>=0.29.21,<0.30.0',
 'dataclasses>=0.8,<0.9',
 'llvmlite==0.31.0',
 'matplotlib>=3.3.1,<4.0.0',
 'mokapot>=0.3,<0.4',
 'networkx>=2.4,<3.0',
 'numpy>=1.18,<2.0',
 'triqler>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'picked-group-fdr',
    'version': '0.1.0',
    'description': 'Scalable, accurate and sensitive protein group FDRs for large-scale mass spectrometry experiments',
    'long_description': '# Picked Protein Group FDR\n\nScalable, accurate and sensitive protein group FDRs for large-scale mass spectrometry experiments\n\n## Running Picked Protein Group FDR using the GUI\n\nOn Windows, you can download the `PickedGroupFDR_GUI_windows.zip` from the latest release, unzip it and open `PickedGroupFDR.exe` to start the GUI (no installation necessary).\n\nAlternatively, on all platforms, first install Picked Protein Group FDR as explained below. Then install `PyQt5` (`pip install PyQt5`) and run:\n\n```shell\npython gui.py\n```\n\n## Running Picked Protein Group FDR from the command line\n\nFirst install Picked Protein Group FDR as explained below, then run:\n\n```shell\npython -m picked_group_fdr --mq_evidence </path/to/mq_evidence_txt> --fasta </path/to/fasta_file>\n```\n\n## Installation\n\nPicked Protein Group FDR is available on PyPI and can be installed with `pip`:\n\n```shell\npip install picked_group_fdr\n```\n\nAlternatively, you can install directly from this repository:\n\n```shell\ngit clone https://github.com/kusterlab/picked_group_fdr.git\npip install .\n```\n',
    'author': 'Matthew The',
    'author_email': 'matthew.the@tum.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kusterlab/picked_group_fdr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
