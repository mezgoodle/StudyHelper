from pandas import read_csv, read_excel

FILE_EXTENSIONS = {
    ".csv": read_csv,
    ".xlsx": read_excel,
    ".xls": read_excel,
}
