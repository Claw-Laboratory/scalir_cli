# SCALiR CLI

## 🧭 Overview

**SCALiR (Standard Curve ALgorithm for Isotope-labeled Regression)** is a command-line tool for predicting metabolite concentrations from LC-MS data using standard curves. It supports various input formats and models, and is designed for use in batch processing and reproducible workflows.

## 📚 Table of Contents

- [🗂 Project Structure](#project-structure)
- [📦 Installation & Environment Setup](#installation--environment-setup)
- [🚀 Running SCALiR CLI](#running-scalir-cli)
- [🔧 Required Arguments](#-required-arguments)
- [⚙️ Optional Arguments](#️-optional-arguments)
- [📂 Input Files](#-input-files)
  - [📘 Standard Concentration Files](#-standard-concentration-files)
  - [📗 Peaklist File Formats](#-peaklist-file-formats)
- [📤 Output Files](#-output-files)
- [📈 How to Interpret the Output](#-how-to-interpret-the-output)
- [ℹ️ Additional Notes](#-additional-notes)
- [🙏 Acknowledgments](#-acknowledgments)

---

## 🗂 Project Structure

A typical SCALiR CLI repository might include the following files:

```text
├── scalir_cli.py                # Main CLI entry point
├── ms_conc/                     # Core functionality modules
│   ├── calibration_curves.py   # Curve fitting logic
│   ├── ConcentrationEstimator.py
│   └── ...
├── example_data/               # Example peaklists and standard files
├── plots/                      # Output directory for standard curve plots
├── scalir_env.yaml             # Conda environment specification
└── README.md                   # Project documentation
```

---

## 📦 Installation & Environment Setup

To run SCALiR CLI, we recommend creating a Conda environment:

### `scalir_env.yaml`

```yaml
name: scalir-cli
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - pandas=1.5.*
  - numpy=1.23.*
  - matplotlib=3.6.*
  - seaborn=0.12.*
  - openpyxl  # for .xlsx support
  - pip
```

### Install environment:

```bash
conda env create -f scalir_env.yaml
conda activate scalir-cli
```

Ensure the SCALiR CLI tool and the `ms_conc` Python package are accessible in your `PYTHONPATH` or installed in the environment.

---

## 🚀 Running SCALiR CLI

```bash
python scalir_cli.py \
    --standards PATH_TO_STANDARDS \
    --peaklist PATH_TO_PEAKLIST \
    --program internal \
    --fit_mode interval \
    --output_prefix results/output \
    --plot_dir results/plots \
    --logfile scalir_run.log
```

---

## 🔧 Required Arguments

| Argument      | Description                                                            |
| ------------- | ---------------------------------------------------------------------- |
| `--standards` | Path to CSV/XLSX file containing standard concentrations and metadata. |
| `--peaklist`  | Path to CSV/XLSX file with peak intensity values.                      |
| `--program`   | One of: `Mint`, `Maven`, or `internal`.                                |

---

## ⚙️ Optional Arguments

| Argument          | Default         | Description                                                                                                                                                                                                                                    |
| ----------------- | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--mint_type`     | `dense`         | If `program` is Mint, choose between `full` or `dense` format.                                                                                                                                                                                 |
| `--intensity_col` | `peak_max`      | Name of the intensity column in the peaklist. For `Mint`, valid options include `peak_max`, `peak_area`, or `height`. For `Maven`, this is auto-set to `value`. For `internal` mode, `peak_max` is used by default.                            |
| `--fit_mode`      | `fixed`         | Curve fitting mode. `fixed` uses a slope of exactly 1.00 for the standard curve. `interval` constrains the slope within user-defined bounds (recommended: 0.85–1.15). `wide` allows an unconstrained best-fit line with no slope restrictions. |
| `--interval`      | `0.85 1.15`     | Used only with `interval` fit mode to set lower/upper range.                                                                                                                                                                                   |
| `--output_prefix` | `scalir_output` | Prefix for all output CSVs.                                                                                                                                                                                                                    |
| `--plot_dir`      | `plots`         | Output directory for standard curve plots.                                                                                                                                                                                                     |
| `--logfile`       | JSON log path   | File to write parameters and metadata to.                                                                                                                                                                                                      |

---

## 📂 Input Files

### 📘 Standard Concentration Files

#### SCALiR\_Standards\_Concentrations File (Wide Format)

| peak\_label                                            | Std\_1 | Std\_2 | Std\_3 | unit |
| ------------------------------------------------------ | ------ | ------ | ------ | ---- |
| L-Citrulline                                           | 500    | 125    | 31.25  | NaN  |
| Fumarate                                               | 250    | 62.5   | 15.63  | μM   |
| Guanine                                                | 25     | 6.25   | 1.56   | μM   |
| ➡️ [Download SCALiR\_Standards\_Concentrations.csv](#) |        |        |        |      |

#### SCALiR\_Standards\_Concentrations\_Internal File (Wide Format)

| peak\_label                                                      | Std\_1 | Std\_2 | Std\_3 | unit | internal\_standard\_injection\_concentration |
| ---------------------------------------------------------------- | ------ | ------ | ------ | ---- | -------------------------------------------- |
| Glycine                                                          | 0.05   | 0.199  | 1.021  | mM   | 3.5                                          |
| Serine                                                           | 0.052  | 0.2    | 0.979  | mM   | 3.5                                          |
| Leucine                                                          | 0.05   | 0.191  | 0.973  | mM   | 3.5                                          |
| ➡️ [Download SCALiR\_Standards\_Concentrations\_Internal.csv](#) |        |        |        |      |                                              |

### 📗 Peaklist File Formats

Accepted formats differ based on `--program`:

#### `Mint` (dense format)

| peak\_label                                                   | Sample\_1 | Sample\_2 | Sample\_3 | Std\_1   | Std\_2    | Std\_3     |
| ------------------------------------------------------------- | --------- | --------- | --------- | -------- | --------- | ---------- |
| D-Glucose 6-Phosphate                                         | 160173.27 | 134129.44 | 120652.06 | 21047736 | 4509362.5 | 988417     |
| Fumarate                                                      | 288052.16 | 419993.41 | 248160.64 | 18307764 | 6283951.5 | 1523609.75 |
| Guanine                                                       | 144809.55 | 397689.91 | 388854.38 | 13578100 | 7017882.5 | 2654957.75 |
| ➡️ [Download SCALiR\_MINT\_Peaklist\_Dense\_Peak\_Max.csv](#) |           |           |           |          |           |            |

#### `Mint` (full format)

➡️ [Download SCALiR\_MINT\_Peaklist\_Full\_Results.csv](#)

#### `Maven`

➡️ [Download SCALiR\_Maven\_Peaklist.csv](#)

#### `Internal` mode

| peak\_label                                               | Sample\_1  | Sample\_2  | Sample\_3  | Std\_1     | Std\_2     | Std\_3     |
| --------------------------------------------------------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- |
| Glycine                                                   | 9.08708217 | 5.90508369 | 19.9677963 | 0.01       | 0.182726   | 0.54167598 |
| Serine                                                    | 0.31574371 | 0.42099298 | 9.52674995 | 0.49641025 | 0.24204641 | 0.46519895 |
| Leucine                                                   | 1.62760775 | 1.42144225 | 3.33398873 | 0.0196519  | 0.17077021 | 1.00514853 |
| Aspartate                                                 | 1.37720198 | 1.82756797 | 3.64361837 | 0.21496096 | 0.12663311 | 0.47185553 |
| ➡️ [Download SCALiR\_Internal\_Standard\_Peaklist.csv](#) |            |            |            |            |            |            |

---

## 📤 Output Files

| Filename               | Description                                              |
| ---------------------- | -------------------------------------------------------- |
| `*_parameters.csv`     | Table of curve parameters per compound.                  |
| `*_concentrations.csv` | Predicted concentrations per sample and compound.        |
| `plots/*.png`          | Standard curve plots per compound (log-log).             |
| `scalir_run_log.json`  | Log file recording all input parameters and environment. |

---

## 📈 How to Interpret the Output

- `*_parameters.csv` includes slope/intercept values and flags for fit validity.
- `*_concentrations.csv` reports the predicted concentration (`pred_conc`) and whether each value is in the calibrated range (`in_range`).
- **Plots**:
  - **Black dots**: standard points used in the fit
  - **Gray dots**: standards excluded (out-of-range)
  - **Black line**: fitted curve (not included in legend)

---

## ℹ️ Additional Notes

### Recommended Use of Fit Modes

- **`fixed`**: Best for QC scenarios or highly standardized panels where response ratios are expected to scale linearly with concentration.

- **`interval`**: Recommended for most studies. Use when you want to enforce biological plausibility of the slope (e.g., 0.85–1.15). Helps reduce false fits due to outliers.

- **`wide`**: Use when the signal response may deviate significantly from linearity and you prefer a fully flexible model (e.g., exploratory datasets or unusual matrix effects).

- `internal` mode requires the standards file to include an `internal_standard_injection_concentration` column.

- Units (e.g., uM) can be specified per compound; defaults to `μM` if unspecified.

- Missing or invalid values are filtered out automatically.

---



## 🙏 Acknowledgments

This CLI was inspired by and adapted from the excellent work in the original [ms-conc & SCALiR Streamlit app](https://github.com/LewisResearchGroup/ms-conc/tree/main), developed by the Lewis Research Group.

Special thanks to the authors for making their code openly available and modular for community reuse and expansion.

---


