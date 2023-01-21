

|Py-Versions| |Versions| |LICENCE| |DOI|

|Logo|

PyCircular
===========================

PyCircular is a specialized data analysis python library designed specifically for working with circular data.
Circular data, such as data that represents angles, directions or timestamps, can present unique challenges when it comes to analysis and modeling. The nature of the circular data can cause difficulties when trying to apply traditional linear and kernel-based methods, as these methods are not well suited to handle the periodic nature of circular data. Additionally, circular data can also raise issues when trying to compute mean and standard deviation, as these measures are not well-defined for circular data.

PyCircular addresses these challenges by providing a set of tools and functionality specifically tailored for working with circular data. The library includes a variety of circular statistical methods, including distributions, kernels, and confidence intervals. Additionally, it also includes visualization tools such as circular histograms and distribution plots, to help you better understand your data.


In particular, it provides:

1. A set of circular analysis algorithms
2. Different real-world datasets.

Installation
============
|Versions| |PyPI-Downloads| |Libraries-Dependents|

You can install ``pycircular`` with ``pip``::

    # pip install pycircular

Documentation
=============

Documentation is available at
http://albahnsen.github.io/pycircular

Tutorials are available at
http://albahnsen.github.io/pycircular/Tutorials.html


Contributions
=============

|GitHub-Commits| |GitHub-Issues| |GitHub-PRs| |GitHub-Contributions|

All source code is hosted on `GitHub <https://github.com/albahnsen/pycircular>`__.

Contributions are welcome. There are a number of `Issues <https://github.com/albahnsen/pycircular/issues>`__ that can be worked on. 

Developers who have made significant contributions,

.. list-table::
   :widths: 30 15 15
   :header-rows: 1

   * - Name
     - ID
     - Notes
   * - Alejandro Correa Bahnsen
     - `github <https://github.com/albahnsen>`__ `linkedin <https://www.linkedin.com/in/albahnsen/>`__
     - primary maintainer
   * - Jaime Acevedo
     - `github <https://github.com/jdacevedo3010>`__ `linkedin <https://www.linkedin.com/in/jd-acevedoviloria/>`__
     -
   * - Sergio Villegas
     - `github <https://github.com/serpiente>`__ `linkedin <https://www.linkedin.com/in/svpg/>`__
     -
   * - Juan Salcedo
     -
     -
   * - Jesus Solano
     -
     -

LICENCE
=======

Open Source (OSI approved): |LICENCE|

Citation information: |DOI|

.. |Logo| image:: https://raw.githubusercontent.com/albahnsen/pycircular/master/logo.png
.. |GitHub-Status| image:: https://img.shields.io/github/tag/albahnsen/pycircular.svg?maxAge=86400&logo=github&logoColor=white
   :target: https://github.com/albahnsen/pycircular/releases
.. |GitHub-Forks| image:: https://img.shields.io/github/forks/albahnsen/pycircular.svg?logo=github&logoColor=white
   :target: https://github.com/albahnsen/pycircular/network
.. |GitHub-Stars| image:: https://img.shields.io/github/stars/albahnsen/pycircular.svg?logo=github&logoColor=white
   :target: https://github.com/albahnsen/pycircular/stargazers
.. |GitHub-Commits| image:: https://img.shields.io/github/commit-activity/y/albahnsen/pycircular.svg?logo=git&logoColor=white
   :target: https://github.com/albahnsen/pycircular/graphs/commit-activity
.. |GitHub-Issues| image:: https://img.shields.io/github/issues-closed/albahnsen/pycircular.svg?logo=github&logoColor=white
   :target: https://github.com/albahnsen/pycircular/issues?q=
.. |GitHub-PRs| image:: https://img.shields.io/github/issues-pr-closed/albahnsen/pycircular.svg?logo=github&logoColor=white
   :target: https://github.com/albahnsen/pycircular/pulls
.. |GitHub-Contributions| image:: https://img.shields.io/github/contributors/albahnsen/pycircular.svg?logo=github&logoColor=white
   :target: https://github.com/albahnsen/pycircular/graphs/contributors
.. |GitHub-Updated| image:: https://img.shields.io/github/last-commit/albahnsen/pycircular/master.svg?logo=github&logoColor=white&label=pushed
   :target: https://github.com/albahnsen/pycircular/pulse
.. |Versions| image:: https://img.shields.io/pypi/v/pycircular.svg
.. |PyPI-Downloads| image:: https://img.shields.io/pypi/dm/pycircular.svg?label=pypi%20downloads&logo=PyPI&logoColor=white
   :target: https://pepy.tech/project/pycircular
.. |LICENCE| image:: https://img.shields.io/pypi/l/pycircular.svg
   :target: https://raw.githubusercontent.com/albahnsen/pycircular/master/LICENCE
.. |DOI| image:: https://img.shields.io/badge/DOI-10.5281/zenodo.7535828-blue.svg
   :target: https://doi.org/10.5281/zenodo.7535828
.. |Libraries-Dependents| image:: https://img.shields.io/librariesio/dependent-repos/pypi/pycircular.svg?logo=koding&logoColor=white
    :target: https://github.com/albahnsen/pycircular/network/dependents
.. |Py-Versions| image:: https://img.shields.io/pypi/pyversions/pycircular.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/pycircular
