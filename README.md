# lstar_dont_care


<b>Note: the project was implemented and tested on Python 3.7.8</b>

## Installation and Usage

1. Clone the project :

```shell
git clone https://github.com/tomyaacov/lstar_dont_care.git
```

2. Create a virtual environment and activate it:

```shell
cd lstar_dont_care
python -m venv env 
source env/bin/activate
```

3. Update pip and install all dependencies:

```shell
pip install --upgrade pip
pip install -r requirements.txt
```


4. Run the magento example on initial algorithm:
* find the 3dfa first (find a moor machine using aalpy)
* find the minimal consistent DFA (using the algorithm from https://ieeexplore.ieee.org/document/5222697)

```shell
python dc_lstar_2.py
```

