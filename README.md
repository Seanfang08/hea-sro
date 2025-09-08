# SROHEA Alloy ML Analysis

This project provides tools for analyzing and visualizing 3D atomic data from CSV files, focusing on Cr, Co, and Ni elements. It includes batch processing, data import, and 3D visualization.

## Features

- Import atomic data from CSV and convert to pickle format
- Batch process multiple datasets and Z ranges
- Visualize 3D atomic distributions and relationships
- Calculate ratios and distances between elements

## Requirements

- Python >= 3.13
- Jupyter >= 1.1.1
- matplotlib >= 3.10.0
- numpy >= 2.2.1

Install dependencies with:

```bash
pip install -r requirements.txt
```
or use the dependencies listed in [`pyproject.toml`](pyproject.toml:1).

## Usage

### 1. Import Data

Convert CSV data to pickle format:

```bash
python import_to_pickle.py
```

### 2. Batch Processing

Run batch analysis and generate plots:

```bash
python run_in_batch.py
```

### 3. Visualization

Visualize 3D atomic structures:

```bash
python visualize_3D_mini.py
```

## File Overview

- [`import_to_pickle.py`](import_to_pickle.py:1): Imports CSV data and saves as pickle.
- [`run_in_batch.py`](run_in_batch.py:1): Batch processes datasets and generates ratio/distance plots.
- [`visualize_3D_mini.py`](visualize_3D_mini.py:1): 3D visualization and analysis tools.
- [`pyproject.toml`](pyproject.toml:1): Project metadata and dependencies.

## Directories

- `data/`: Input and output data files. This directory is ignored by git except for a `.gitkeep` file, so it remains in version control even when empty.
- `images/`: Output images and plots. This directory is also ignored by git except for a `.gitkeep` file, so it remains in version control even when empty.

To keep these directories tracked by git, a placeholder file named `.gitkeep` is used in each directory.

## Data

Place your CSV files in the `data/` directory. Adjust file paths in [`run_in_batch.py`](run_in_batch.py:1) as needed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE:1) file for details.