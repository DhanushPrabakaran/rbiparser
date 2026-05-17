# rbiparser

A utility for downloading, parsing and sanitizing bank database (IFSC, MICR, address etc.) Excel sheets from the [RBI website](https://www.rbi.org.in/scripts/bs_viewcontent.aspx?Id=2009).

> **Note (2025):** The RBI website was redesigned. The download URL and Excel format have changed. This updated version handles `.xlsx` files using `openpyxl` instead of `xlrd`.

---

### Installation

```shell
pip install rbiparser
```

If installing from source (recommended for latest fixes):

```shell
pip install . --force-reinstall
```

---

### Dependencies

- `openpyxl` — required for `.xlsx` conversion (replaces legacy `xlrd`)
- `beautifulsoup4`, `lxml`, `requests`, `click`

Install manually if needed:

```shell
pip install openpyxl
```

---

### Usage

#### 1. Download Excel files from the RBI website

```shell
rbiparser download -d "./xls" -s "https://www.rbi.org.in/scripts/bs_viewcontent.aspx?Id=2009"
```

> The `-s` source URL must be specified explicitly as the RBI moved their data page.

#### 2. Convert downloaded `.xlsx` files to CSV

```shell
rbiparser convert -s "./xls" -d "./csv"
```

#### 3. Combine all CSVs into one master file

```shell
rbiparser combine -s "./csv" -d "data.csv"
```

#### Apply advanced clean filters

```shell
rbiparser combine -s "./csv" -d "data.csv" -f
```

#### Help for individual commands

```shell
rbiparser download --help
rbiparser convert --help
rbiparser combine --help
```

---

### Output

The final `data.csv` contains ~180,000 bank branch records with the following columns:

| Column | Description |
|---|---|
| BANK | Bank name |
| IFSC | IFSC code |
| MICR | MICR code |
| BRANCH | Branch name |
| ADDRESS | Branch address with pincode |
| CONTACT | Contact number |
| CITY | City |
| DISTRICT | District |
| STATE | State |
| ABBREVIATION | Bank abbreviation |

---

### Updating Data

Re-run all three steps. The etag system skips unchanged files on re-download:

```shell
rbiparser download -d "./xls" -s "https://www.rbi.org.in/scripts/bs_viewcontent.aspx?Id=2009"
rbiparser convert -s "./xls" -d "./csv"
rbiparser combine -s "./csv" -d "data.csv"
```

---

### License

MIT License — Kailash Nadh, http://nadh.in