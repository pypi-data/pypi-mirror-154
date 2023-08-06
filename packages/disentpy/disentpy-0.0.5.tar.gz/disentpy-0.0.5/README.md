# disentpy

Python client for Disent's API framework.

## Installation

Install using `pip`

```shell
pip install disentpy
```

## Usage

```python
import disent

# get AAPL vol surface (list of dicts)
model="DEMO_EQD_VOLS"
ticker = 'AAPL'
model_args = {'ticker':ticker}
df = disent.hub(model,model_args,env='disent-cloud')
print(df)

# get AAPL vol surface (pivoted on K)
df = disent.hub(model,model_args,env='disent-cloud')
model_args = {'ticker':ticker,'pivot':'T_DATE,K,IV'}
print(df)

# lambdify disent call for any ticker

f_vols = lambda i: disent.hub(model,{'ticker':i},env='disent-cloud')
print(f_vols('SPX'))
print(f_vols('RTY'))

```

## Documentation

Latest documentation is hosted on [read the docs](https://disentpy.readthedocs.io/en/latest/).

### Requirements

Using disentpy requires the following packages:

- pandas>=1.0
- requests>=2.19.0

### Install latest development version

```shell
pip install git+http://github.com/disentcorp/disent_pip.git
```

or

```shell
git clone pip install https://github.com/disentcorp/disent_pip.git
cd disentpy
python setup.py install
```
