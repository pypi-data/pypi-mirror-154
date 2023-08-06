[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]
<!--[![LinkedIn][linkedin-shield]][linkedin-url]-->



<br />
<p align="center">
  <a href="https://github.com/BizTecBritain/StegaSaurus">
    <img src="https://github.com/BizTecBritain/BizTecBritain/blob/main/BizTec.png?raw=true" alt="Logo" width="580" height="300">
  </a>

  <h3 align="center">StegaSaurus</h3>

  <p align="center">
    (Optionally) Dependency-free library for steganography (GUI and CLI included)
    <br />
    <a href="https://github.com/BizTecBritain/StegaSaurus"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/BizTecBritain/StegaSaurus">View Demo</a>
    ·
    <a href="https://github.com/BizTecBritain/StegaSaurus/issues">Report Bug</a>
    ·
    <a href="https://github.com/BizTecBritain/StegaSaurus/issues">Request Feature</a>
  </p>
</p>



<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



## About The Project

Once again, I was bored so I made this


### Built With

* Python version >= 3.8
* May work with earlier versions but it is untested feel free to try it by downloading from my github [https://github.com/BizTecBritain/StegaSaurus](https://github.com/BizTecBritain/StegaSaurus)



## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* Install git and python
  ```
   $ sudo apt-get update
   $ sudo apt-get install git
   $ sudo apt-get install python
  ```

* (Optional) Create virtual environment
  * #### Linux:
    ```
    $ python -m venv venv
    $ venv/bin/activate
    ```
  * #### Windows:
    ```
    > python -m venv venv
    > venv/Scripts/activate.bat
    ```

### Installation

* Clone the repo with ```$ git clone https://github.com/BizTecBritain/StegaSaurus.git```
(IF YOU USE THIS METHOD: In order for this project to run to its full capacity it is recommended that you install pillow and tqdm through pip but this isn't required)
* Or install with ```$ pip install KarnaughMap```


## Usage

This can be used as a library (see documentation) or run from the command line (you need to add to PATH)
```
$ StegaSaurus.exe [-h] [--read] [--write] [--audio] [--image] [--no-output] [--output OUTPUT] [--data DATA] [--depth DEPTH] [--raw RAW] input

positional arguments:
  input                 Input file path

optional arguments:
  -h, --help            show this help message and exit
  --read, -r            Decrypt Seganography file
  --write, -w           Encrypt Seganography file
  --audio, -a           Perform operation on audio file
  --image, -i           Perform operation on image file
  --no-output           No output file for decryption
  --output OUTPUT       Output file path
  --data DATA           Data file path (write only)
  --depth DEPTH, -d DEPTH
                        Bit depth (default is 2)
  --raw RAW             Raw data for if data file is not used

```

When using images it is not possible to write out to a gif as they can only include a limited amount of colours

_For more examples, please refer to the [Documentation](https://example.com)_



## Roadmap

See the [open issues](https://github.com/BizTecBritain/StegaSaurus/issues) for a list of proposed features (and known issues).



## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



## License

Distributed under the MIT License. See `LICENSE` for more information.



## Contact

Alexander Bisland - Twitter: [@BizTecBritain](https://twitter.com/BizTecBritain) - Email: BizTecBritain@gmail.com

Project Link: [https://github.com/BizTecBritain/StegaSaurus](https://github.com/BizTecBritain/StegaSaurus) 



## Acknowledgements

* Thanks to [othneildrew](https://github.com/othneildrew/Best-README-Template/blob/master/BLANK_README.md) for the blank README.md file

[contributors-shield]: https://img.shields.io/github/contributors/BizTecBritain/StegaSaurus.svg?style=for-the-badge
[contributors-url]: https://github.com/BizTecBritain/StegaSaurus/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/BizTecBritain/StegaSaurus.svg?style=for-the-badge
[forks-url]: https://github.com/BizTecBritain/StegaSaurus/network/members
[issues-shield]: https://img.shields.io/github/issues/BizTecBritain/StegaSaurus.svg?style=for-the-badge
[issues-url]: https://github.com/BizTecBritain/StegaSaurus/issues
<!--[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew-->