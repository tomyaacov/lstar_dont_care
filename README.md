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

4. Run our initial algorithms experiment on the magento toy example:
* find a 3DFA using a standard l star (moore machine):
  * membership queries - for w:
  if w not in M return ?, else check if it is a prefix of P or in F. if not run on system and see result.
  * Equivalence queries - for a 3DFA:
    * Check that the failing tests in the list are indeed accepted by the 3DFA.
    * Check that the passing tests are rejected by the 3DFA.
    * Sample tests from L(3DFA)\cap M and check that they fail.
    * Sample words from M, and check that they produce the “right” results: pass → rejected, fail → accepted.
* After the 3DFA is built run this 2  options to get the final DFA:
  * run RPNI on a data set created from the 3DFA (observation table).
  * run the minimization algorithm from [here](https://ieeexplore.ieee.org/document/5222697) to get the DFA. 
```shell
python test_suite_based_lstar.py
```

5. Run algorithms experiment on the coffee\magento examples:
```shell
python rc_lstar.py
```