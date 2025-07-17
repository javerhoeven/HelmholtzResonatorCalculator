# Helmholtz Resonator Calculator

A command-line tool for performing acoustic calculations related to Helmholtz resonators.

---

## 📦 Installation
To install and run the **Helmholtz Resonator Calculator**, follow these steps:

### Prerequisites
Make sure to have Python and pip installed on your system.

### 0. Easy install (skip to step 5):
```bash
git clone https://git.tu-berlin.de/tobiast/python-and-akustik-2025-helmholtz.git
cd python-and-akustik-2025-helmholtz
pip install poetry
poetry install
```

If this does not work, use steps 1. - 4. 


### 1. Download and Extract the Code

- [Download the ZIP](https://git.tu-berlin.de/tobiast/python-and-akustik-2025-helmholtz) of this repository.
- Extract the contents to any folder on your computer.


### 2. Open a Terminal in the Project Root

Navigate to the extracted folder in your terminal:

```bash
cd path/to/your/extracted/folder
```
To verify, you can type `ls` and should see folders like "src" and "docs". 

### 3. Install Poetry (if not already installed)

```bash
pip install poetry
```
Verify the install:
```bash
poetry --version
```

### 4. Install the Project Environment
```bash
poetry install
```
This creates the virtual environment and installs all dependencies. 

### 5. Run the Calculator
Running the calculator for the first time might take a few seconds. 
```bash
poetry run hrcalc
```

### 6. Help
To get an overview, you can use
```bash
poetry run hrcalc --help
```
or read the Usage section below. 



## Usage
This tool currently provides two major use cases:
### 1. GUI Mode
This mode will open up a graphical user interface, which allows the user to enter geometry and aperture information. 
The GUI provides a graph of the absorbtion area over frequency, as well as some characteristic values like resonance frequency and q-factor. 
There is also the possibility to save and load parameter sets as .json files. 
```bash
poetry run hrcalc gui
```
### 2. Optimizer Mode
This mode will provide a set of parameters for maximum absorbtion at the given frequency with a given Q-factor. 
Since this mode relies on non-deterministic methods, even with the same input values the results may vary. 
The positional arguments are target frequency and target Q-factor
example usage for an ideal Helmholtz Resonator with resonance at 200 Hz and a Q-Factor of 10:
```bash
poetry run hrcalc optimizer 200 10
```

The optional `--save` flag lets you save your simulation object, so you can further edit / oberserve / refine it in the GUI application:
```bash
poetry run hrcalc optimizer 300 5 --save 'example.json'
```
The optimizer currently does not support all parameters. The following assumptions are made:
- Cuboid shape
- Standard Conditions: 20° Celsius, 50 % humidity, c = 344  m/s
- tube-shaped aperture
- aperture is filled with porous material that is returned with xi parameter


### Reference
A detailed reference for the project is available [here](https://python-and-akustik-2025-helmholtz-4aufhübschung-pages.tu-berlin.de). 


## Authors and acknowledgment

This project was built for the seminar "Python and Acoustics" at Technical University Berlin during the summer term of 2025.  
Authors are  
Felix Rösch, Jessica Schön, Tobias van Dijk, Jannis Verhoeven