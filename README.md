# Stegos
***
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

Stegos is a desktop application for cryptographic image steganography. 

Supports Linux. On Windows 11, DCT embedding is not supported, but other features are functional.
## Table of Contents
***
- [High-Level Overview](#high-level-overview)
- [Features](#features)
- [Installation](#installation)
- [Testing](#testing)
- [Contact Me](#contact-me)

## High-Level Overview
***
1. The payload (files/text) is compressed (Zip/LZMA).
2. An AES key is derived using Argon2 (salted using a CSPRNG).
3. The payload is encrypted using AES.
4. The encrypted payload is embedded randomly within the image.
   - Pixels (BMP, PNG, etc.)
   - DCT Coefficients (JPEG)
5. Extraction reverses the process, allowing the embedded payload to be retrieved.
## Features
***

### Crytographic Image Steganography
- Embedding files and text in lossless and lossy (JPEG) images. Data is embedded in the pixels of lossless images, and in the DCT coefficents of JPEGs. Embedding in DCT coefficients allows the payload to survive lossy compression.
- Embedding position randomisation.
- Diffie-Hellman Key Exchange for shared secret key establishment.
- Payload encryption with AES.
- Prevent time-memory tradeoffs with Argon2 key derivation.
- Payload compression with Zip and LZMA.

### Qt Desktop GUI
- Image preview, preventing unintentional overwritting of images.
- Dialogs for all primary operations (progress indicator, overwrite dialog, etc.).
- Drag-and-drop for all file/directory inputs.
- Support for changing OS themes (dark/light mode) during runtime.

## Installation
***
1. Clone the repository.
````commandline
git clone https://github.com/adamoregan/stegos.git
````
2. Download the dependencies.
````commandline
cd stegos
pip install -r requirements.txt
````

## Testing
***
````commandline
cd stegos
pytest .
````
## Contact Me
***
- Adam O'Regan 
  - Github: [adamoregan](https://github.com/adamoregan)  
  - Email: [adamoregan457@gmail.com](mailto:adamoregan457@gmail.com)
  - LinkedIn: [adamoregan457](https://www.linkedin.com/in/adamoregan457)