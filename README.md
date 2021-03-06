# Data extractor

The script extracts column data from a file of CSVs generated by the accelerometer reader.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

1. Create virtual env first

```bash
python -m venv env
```

2. Activate virtual env

```bash
env\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Store any data in the mydata folder.

## Usage

```python
python main.py -d PathToFolderContainingCSV --ex RunToExcludeSepWSpaces
```

### Example usage

```python
python main.py -d raw_real_data\N0 -x 1 2 3
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
