# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mmfutils',
 'mmfutils.math',
 'mmfutils.math.bases',
 'mmfutils.math.bases.tests',
 'mmfutils.math.integrate',
 'mmfutils.math.integrate.tests',
 'mmfutils.math.tests',
 'mmfutils.performance',
 'mmfutils.plot',
 'mmfutils.solve',
 'mmfutils.solve.tests',
 'mmfutils.tests']

package_data = \
{'': ['*']}

install_requires = \
['husl>=4.0.3,<4.1.0',
 'importlib-metadata>=3.6.0',
 'zope.interface>=5.4.0,<5.5.0']

extras_require = \
{'doc': ['Sphinx<5.0.0',
         'mmf-setup>=0.4.6,<0.5.0',
         'mock>=4.0.3,<4.1.0',
         'nbconvert>=6.5.0,<6.6.0',
         'sphinx-rtd-theme>=1.0.0,<1.1.0'],
 'doc:python_full_version >= "3.7.0" and python_full_version < "3.8.0"': ['numpy>=1.20.2,<1.21.0',
                                                                          'matplotlib>=3.4.1,<3.5.0'],
 'doc:python_version > "3.7"': ['numpy', 'matplotlib>=3.5.2,<3.6.0'],
 'fftw': ['pyFFTW>=0.13.0,<0.14.0'],
 'test': ['ipyparallel>=8.3.0,<8.4.0',
          'numexpr>=2.8.1,<2.9.0',
          'persist>=3.0,<4.0',
          'psutil>=5.9.1,<5.10.0',
          'pyFFTW>=0.13.0,<0.14.0',
          'pytest>=7.1.2,<7.2.0',
          'pytest-cov>=3.0.0,<3.1.0',
          'uncertainties>=3.1.5,<3.2.0'],
 'test:python_full_version >= "3.7.0" and python_full_version < "3.8.0"': ['matplotlib>=3.4.1,<3.5.0',
                                                                           'scipy>=1.7.3,<1.8.0'],
 'test:python_version < "3.10"': ['numba>=0.55.2,<0.56.0'],
 'test:python_version > "3.7"': ['matplotlib>=3.5.2,<3.6.0',
                                 'scipy>=1.8.1,<1.9.0']}

setup_kwargs = {
    'name': 'mmfutils',
    'version': '0.6.3',
    'description': 'Small set of utilities: containers and interfaces.',
    'long_description': 'Small set of utilities: containers and interfaces.\n\nThis package provides some utilities that I tend to rely on during development. Since I\nuse these in many different projects, I turned this into a repository so that I can\neasily sync and keep track of updates. Once the intreface and contents become stable, it\nwill probably make sense to include these directly along with the original project so\nthat an additional dependency is not introduced.\n',
    'author': 'Michael McNeil Forbes',
    'author_email': 'michael.forbes+python@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://alum.mit.edu/www/mforbes/hg/forbes-group/mmfutils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.13,<3.10',
}


setup(**setup_kwargs)
