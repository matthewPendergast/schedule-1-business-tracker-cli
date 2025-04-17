# Overview

This is a simple CLI business tracker developed in Python and designed for use with the game *Schedule 1*.

## Features

**Current**
- Enter and track daily sales data
- Calculate product profit margins
- Generate Excel business reports
- Export sales figures and other useful metrics

**Planned**
- Add support for different product types and distributors
- Develop a simple GUI for easier data entry

## Installation

This project uses Python 3.13. If you're using [pyenv](https://github.com/pyenv/pyenv), it will be automatically selected from the `.python-version` file.

You can then install the required dependencies with:

```bash
pip install -r requirements.txt
```

## How to Use

**Note:** This project is being developed using the terminal in VS Code on Windows. It has not been tested in other terminal environments and it may require additional setup to work as intended outside of VS Code.

1. Run `main.py` inside the VS Code terminal.
2. Use the numbered menu to add sales, set up product information, or export data.
3. After exporting, check the `business_report.xlsx` and `figures/` folder for generated reports and charts.

## Notes
- This is a work-in-progress as I continue my *Schedule 1* playthrough.
- Feel free to fork, modify, or adapt this for your own use.

## License

This project is licensed under the [MIT License](LICENSE.txt).