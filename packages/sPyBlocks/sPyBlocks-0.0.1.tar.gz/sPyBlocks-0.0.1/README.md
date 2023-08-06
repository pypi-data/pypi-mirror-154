# sPyBlocks

sPyBlocks is an open-source Python package that provides researchers with a new toolkit of Spiking Neural Networks (SNN)-based functional blocks that emulate the behavior of digital components. Therefore, these spiking functional blocks are useful for developing bio-inspired applications, for what can be especially useful for neuromorphic engineers. The toolkit has been developed using the sPyNNaker software package and the SpiNNaker hardware platform in conjunction with PyNN, and is compatible with all platforms supported by that package. More information in [Depencencies](#dependencies) and [Hardware platform](#hardware-platform).

The installation steps are explained in [Installing](#installing). The code has been documented to allow the user to fully understand it. In [Documentation](#documentation) it is explained how to access to the documentation. 

This package arises as a result of a series of works focused on the construction of these blocks. [Future works](#future-works) contains the most relevant pending tasks in this repository based on these works. Please go to [Cite this work](#cite-this-work) to learn how to properly reference the works cited here.

## Table of contents

- [Dependencies](#dependencies)
- [Hardware platform](#hardware-platform)
- [Installing](#installing)
- [Documentation](#documentation)
- [Future works](#future-works)
- [Cite this work](#cite-this-work)
- [License](#license)

## Dependencies

This section specifies the libraries that have been used to develop the code and their corresponding versions.

- PyNN 0.9.6
- sPyNNaker 6.0.0
- Numpy 1.22.1
- Matplotlib 3.5.1 (only for tests)
- XlsxWriter 3.0.2 (only for tests)

Higher versions can probably be used.

## Hardware platform

The code presented here has been developed and tested making use of two different versions of the SpiNNaker platform: the SpiNN-3 and the SpiNN-5. More information about these platforms can be found in the following work:

> A. G. Rowley, C. Brenninkmeijer, S. Davidson, D. Fellows, A. Gait, D. R. Lester, L. A. Plana, O. Rhodes, A. B. Stokes, S. B. Furber, Spinntools: the execution engine for the spinnaker platform, Frontiers in neuroscience 13 (2019) 231.

## Installing

Still working on this.

## Documentation

The documentation contains all the information about the code. It has been created to provide the user with useful information about how it was created and how he can use it. Although the code is fully visible, only the highest level functions, which are included in each of the spiking blocks, are relevant to the user.

This documentation can be found in https://spyblocks.readthedocs.io/en/latest/.

## Future works

Still working on this.

## Cite this work

> - Spike-based building blocks for performing logic operations using Spiking Neural Networks on SpiNNaker. International Joint Conference on Neural Networks. Padua, Italy, 2022.

> - Construction of a spike-based memory using neural-like logic gates based on Spiking Neural Networks on SpiNNaker. Preprint submitted to Neural Networks. June, 2022.

## License

<p align="justify">
This project is licensed under the GPL License - see the <a href="https://github.com/alvayus/Neural-Logic-Gates/blob/main/LICENSE">LICENSE.md</a> file for details.
</p>

<p align="justify">
Copyright © 2022 Alvaro Ayuso-Martinez<br>  
<a href="mailto:aayuso@us.es">aayuso@us.es</a>
</p>
