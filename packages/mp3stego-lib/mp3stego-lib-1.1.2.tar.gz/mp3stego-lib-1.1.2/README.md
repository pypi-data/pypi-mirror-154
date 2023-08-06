# MP3-Steganography
[![travis-ci](https://app.travis-ci.com/tomershay100/mp3-steganography-lib.svg?branch=main)](https://app.travis-ci.com/github/tomershay100/mp3-steganography-lib)
[![doc](https://readthedocs.org/projects/mp3-steganography-lib/badge/?version=latest)](https://mp3-steganography-lib.readthedocs.io/en/latest/)
[![PyPI version](https://badge.fury.io/py/mp3stego-lib.svg)](https://badge.fury.io/py/mp3stego-lib)
[![GitHub version](https://badge.fury.io/gh/tomershay100%2Fmp3-steganography-lib.svg)](https://badge.fury.io/gh/tomershay100%2Fmp3-steganography-lib)

#### Contributes

* Aviad Seady ([aviadevelops@gmail.com](mailto:aviadevelops@gmail.com))
* Tomer Shay ([tomershay100@gmail.com](mailto:tomershay100@gmail.com))
* Lee Zaid ([lizizaid@gmail.com](mailto:lizizaid@gmail.com))

This is a steganography library in python for hiding strings in mp3 files.

1. [General](#General)
    - [Background](#background)
    - [Project Description](#project-description)
    - [Project Structure](#project-structure)
2. [Dependencies](#dependencies)
3. [Running Instructions](#running-instructions)
4. [Installation](#installation)

## General

### Background

This python library allows the user to hide strings inside ``MP3`` files, extract the hidden strings from ``MP3`` file,
clean a ``MP3`` file from hidden strings in it and generally allows to convert ``MP3`` files to ``WAV`` (decoding
process) files and vice versa (encoding process).

### Project Description

The steganography process uses and modifies huffman tables as presented in the research article "_High capacity
reversible data hiding in MP3 based on Huffman table
transformation_" (which can be found [here](https://www.aimspress.com/fileOther/PDF/MBE/mbe-16-04-158.pdf)). Quite
simply, the idea is to be able to hide bits by changing the huffman tables. Each frame in the ``MP3`` file uses several
huffman tables (one per granule, channel and regin - a total of 8-12 tables).

Unofficially, they found pairs of tables, according to their similarities and determined that each would be for the bit
0 or the bit 1. For the sake of demonstration let us assume that the huffman table x and the huffman y table are a pair,
and that x is for the bit 0 and y for the bit 1. Now to hide a bit, given that the huffman table x has been used, it
must be replaced with the huffman table y if the bit is 1 or to keep the huffman table x if the bit is 0. An inverted
case will happen for original use of table y. Thus, all 30 huffman tables that use (out of 32) ``MP3`` files, are
divided into pairs and each time you see a huffman table z - replace it with the huffman table that matches the next bit
you want to hide.

### Project Structure

The library is contains several packages and several classes built as follows:

1. `decoder` package:
    * **Frame class:** contains all the information about the current ``MP3`` frame that been decoded.
    * **FrameHeader class:** contains all the information about the current ``MP3`` frame header that been decoded.
    * **FrameSideInformation class:** contains all the information about the current ``MP3`` frame side-information that
      been decoded.
    * **MP3Parser class:** performs the actual decoding process while going through all the frames of the file.
    * **ID3Parser class:** performs the decoding process on the ``METADATA`` of the ``MP3``` file.
    * **tables file:** contains all the tables that been used in the decoding process.
    * **util file:** contains all the different functions and dataclasses that other classes use frequently like
      mathematical calculations and bit conversions.
    * **Decoder class:** consolidates the ``MP3`` decoding process. Receives paths to files and takes
      care of the decoding process while printing information, creating files and analyzing the ``METADATA``.
2. `encoder` package:
    * **WAVReader class:** contains all the information about the ``WAV`` file that been encoded.
    * **MP3Encoder class:** performs the actual encoding process.
    * **ID3Parser class:** performs the decoding process on the ``METADATA`` of the ``MP3``` file.
    * **tables file:** contains all the tables that been used in the encoding process.
    * **util file:** contains all the different functions and dataclasses that other classes use frequently like
      mathematical calculations and bit conversions.
    * **Encoder class:** consolidates the ``MP3`` encoding process. Receives paths to files and takes
      care of the encoding process while printing information, creating files.
3. **Steganography class:** serves as a kind of Façade and allow the user to perform operations on his ``MP3``
   and ``WAV`` files. The possible actions are:
    * decode ``MP3`` file to ``WAV`` file.
    * encode ``WAV`` file to ``MP3`` file.
    * hide string in ``MP3`` file.
    * reveal string in ``MP3`` file.
    * clean ``MP3`` file from any string.

You can see more information about the class hierarchy
in [UML](https://github.com/tomershay100/mp3-steganography-lib/blob/main/src/uml.png).

## Dependencies

1. [Python 3.9+](https://www.python.org/downloads/)
2. [NumPy](https://numpy.org/install/)
3. [SciPy](https://scipy.org/install/)
4. [TQDM](https://github.com/tqdm/tqdm)
5. [bitarray](https://pypi.org/project/bitarray/)
6. [numba](https://numba.readthedocs.io/en/stable/user/installing.html)

you can also see in `requirements.txt` file

## Running Instructions

Steganography Class API:

* Creating Steganography object by
    ```python 
  from mp3stego import Steganography
  
  stego = Steganography(quiet=True)
    ```
    * ``quiet: bool``: boolean value for the function to print information or not (default value ``True``).
* for encoding ``WAV`` file into ``MP3`` file you may use
    ```python 
    stego = Steganography(quiet=True)
    stego.encode_wav_to_mp3("input.wav", "output.mp3", 320)
    ```
    * ``wav_file_path: str``: file path for the ``WAV`` file.
    * ``output_file_path: str``: file path for the output ``MP3`` file.
    * ``bitrate: int``: the bitrate to be used in the encoding process (default value is ``320``). You may use bitrate
      from ``32Kb`` to ``420Kb`` in jumps of ``32Kb``.
* For decoding ``MP3`` file into ``WAV`` file you may use
    ```python 
    stego = Steganography(quiet=True)
    stego.decode_mp3_to_wav("input.mp3", "output.wav")
    ```
    * ``input_file_path: str``: file path for the ``MP3`` file.
    * ``wav_file_path: str``: file path for the output ``WAV`` file (default value=```input_file_path[:-4] + ".wav"```).
* For hiding string in ``MP3`` file you may use
    ```python 
    stego = Steganography(quiet=True)
    stego.hide_message("input.mp3", "output.mp3", "String to hide in the file")
    ```
    * ``input_file_path: str``: file path for the input ``MP3`` file.
    * ``output_file_path: str``: file path for the output ``MP3`` file.
    * ``message: str``: the message to hide in the file.
    * ``wav_file_path: str``: file path for the output ``WAV`` file (default value=```input_file_path[:-4] + ".wav"```).
    * ``delete_wav: bool``: boolean value for the decoding process to delete the wav file or not (default
      value ``True``).
* For revealing string from ``MP3`` file you may use
    ```python 
    stego = Steganography(quiet=True)
    stego.reveal_massage("input.mp3", "results.txt")
    ```
    * ``input_file_path: str``: file path for the input ``MP3`` file.
    * ``txt_file_path: str``: file path for the results to be written to.
* For cleaning ``MP3`` file you may use
    ```python 
    stego = Steganography(quiet=True)
    stego.clear_file("input.mp3", "output.mp3")
    ```
    * ``input_file_path: str``: file path for the input ``MP3`` file.
    * ``output_file_path: str``: file path for the output ``MP3`` file.

## Installation

Install the library using:

```shell
pip install mp3stego-lib
```
