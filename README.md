# **Python Code Translator: Bytecode or JSON**

This script allows you to display Python code as bytecode or JSON using the `dis`, `json`, and `inspect` libraries.

## **Requirements**

- **Python Version**: Python 3.6 or higher is required.

## **Installation**

1. Ensure you have Python installed on your system:
   ```bash
   python --version
   ```
   If Python is not installed, download and install it from the official [Python website](https://www.python.org/downloads/).

2. Clone or download the repository containing the script.

## **Usage**

Run the script with the following command:

```bash
python translate.py <file_name> <command>
```

Where:
- `<file_name>` is the name of the Python file you want to translate.
- `<command>` specifies the output format: `bytecode` or `json`.

### **Available Commands**

- `bytecode`: Displays the code in bytecode format using the `dis` module.
- `json`: Displays the code as JSON using the `json` and `inspect` libraries.

### **Examples**

1. **View Bytecode**:
   ```bash
   python translate.py my_code.py bytecode
   ```

2. **View as JSON**:
   ```bash
   python translate.py my_code.py json
   ```

## **Contributors**

- Pavel Yakovlev - [paulcodeman@gmail.com](mailto:paulcodeman@gmail.com)
