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

5. Run our initial algorithm on magento toy example:
* membership queries - for w:
if w not in M return ?, else check if it is a prefix of P or in F. if not run on system and see result.
* Equivalence queries - for a 3DFA:
    - Check that the failing tests in the list are indeed accepted by the 3DFA.
    - Check that the passing tests are rejected by the 3DFA.
    - Sample tests from L(3DFA)\cap M and check that they fail.
    - Sample words from M, and check that they produce the “right” results: pass → rejected, fail → accepted.
* After the 3DFA is built run a minimization algorithm to get the final DFA
```shell
python test_suite_based_lstar.py
```