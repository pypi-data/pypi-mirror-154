# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pycount_xilinx']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.2,<4.0.0']

setup_kwargs = {
    'name': 'pycount-xilinx',
    'version': '0.1.0',
    'description': 'Count words in a text file.',
    'long_description': '# pycount_xilinx\n\nCount words in a text file.\n\n## Installation\n\n```bash\n$ pip install pycount_xilinx\n```\n\n## Usage\n\n`pycount_xilinx` can be used to count words in a text file and plot results\nas follows:\n\n```python\nfrom pycount_xilinx.pycounts import count_words\nfrom pycount_xilinx.pycounts import plot_words\nimport matplotlib.pyplot as plot_words\n\nfile_path = "test.txt"  # path to your file\ncounts = count_words(file_path)\nfig = plot_words(counts, n=10)\nplt.show()\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`pycount_xilinx` was created by Xilinx. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`pycount_xilinx` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Xilinx',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
