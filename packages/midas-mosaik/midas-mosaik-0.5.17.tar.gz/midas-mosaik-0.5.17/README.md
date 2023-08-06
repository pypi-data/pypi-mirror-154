# MIDAS

The MultI-DomAin test Scenario (MIDAS) is a collection of mosaik simulators
(https://gitlab.com/mosaik) for smart grid co-simulation and contains a
semi-automatic scenario configuration tool.

Version: 0.5.14

License: LGPL

## Requirements

Most of the dependencies will be installed automatically. However, there are
some additional requirements which you have to setup up manually.

You will need a working C compiler if you're using plain python to get a
flawless installation. For Windows users this means that you have to install
the VisualC++ compiler that usually comes with VisualStudio. Because of some
issues on Windows, it is generally recommended to use the Windows Subsystem
for Linux and follow the Linux installation guide. All other users simply
install the gcc or similar packages via your distribution's package repository.  

Furthermore, you will need to have a working Git installation, which you can
find on https://git-scm.com/downloads (or via your package manager).

Midas is able to create an analysis report of the simulation results. If you
have a working pandoc (https://pandoc.org/) installation, this report will
automatically be converted to an .odt file. This is **purely optional**.

## Installation

MIDAS requires Python >= 3.8 and is available on https://pypi.org. It can be
installed, preferably into a virtualenv,  with

    >>> pip install midas-mosaik

Alternatively, you can clone this repository with

    >>> git clone https://gitlab.com/midas-mosaik/midas.git

then switch to the midas folder and type

    >>> pip install -e .

## Usage

MIDAS comes with a command line tool called `midasctl` that let's you
conveniently start your scenario and/or add minor modifications to it (e.g.
change the number of simulations steps, write to a different database, etc..
`midasctl` also helps doing the initial setup of MIDAS. Just type

    >>> midasctl configure

and you will be asked to specify where the runtime configuration of MIDAS
should be stored and where you want the datasets to be located. You can of
course let MIDAS decide this for you, just append `-a` to the command:

    >>> midasctl configure -a

Afterwards, you need to download the datasets that MIDAS will use. Type

    >>> midasctl download

and wait a moment until MIDAS is done. Finally, you can test your installation
with

    >>> midasctl run demo

This will run a demonstration scenario and should not take very long.

Pro tip: If you just run the last command, configuration and download will be
performed implicitly.


## Troubleshooting

(Not fully tested)
If you're a Windows user and encounter issues during the installation, then
maybe you don't have a working C++ compiler installed. Either install
VisualStudio (there should be a community edition) or you have to rely on
precombiled binaries, which can be found ,e.g., here:
https://www.lfd.uci.edu/~gohlke/pythonlibs/.


## Documentation

A more comprehensive documentation can be found here: https://midas-mosaik.gitlab.io/midas

To build the docs yourself, sphinx (*pip install sphinx*) is required. Simply navigate
into the docs folder and type

    >>> make html

Afterwards, navigate inside the docs/_build/html folder and double-click on the
index.html file.


## Datasets and License

The datasets are pulled from different locations.

The default load profiles are publicly available at
https://www.bdew.de/energie/standardlastprofile-strom/

The commercial dataset is retrieved from https://data.openei.org/submissions/153
and is released under the Creative Commons License:
https://creativecommons.org/licenses/by/4.0/
The energy values are converted from Kilowatt to Megawatt and slightly rearranged to be usable with MIDAS.

The simbench datasets are directly extracted from the simbench pypi package.

The smart nord dataset comes from the research project Smart Nord
(www.smartnord.de).

The Weather datasets are publicly available at https://opendata.dwd.de/ (see
the Copyright information:
https://www.dwd.de/EN/service/copyright/copyright_node.html)
Since sometimes values are missing, those values are filled with previous or
similar values.
