# ReepiCheep: Multithreaded CSV Importer for PostgreSQL
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*yP7nQS9Y0nSrWFFiDWSPMQ.jpeg)
ReepiCheep is an open-source Python tool designed to efficiently import multiple CSV files in a directory into a PostgreSQL database. It dynamically creates database tables based on CSV file headers and uses multithreading to process large datasets concurrently.

## Features
- **Dynamic Table Creation**: Automatically generates database tables based on CSV structure.
- **Multithreaded Processing**: Processes multiple CSV files simultaneously for faster performance.
- **Easy Configuration**: Simple setup for database and directory paths.
- **Extensible Design**: Easily customizable to fit your needs.

## Requirements
- Python 3.8 or newer
- PostgreSQL
- Python libraries:
  - `pandas`
  - `sqlalchemy`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ReepiCheep.git
   cd ReepiCheep
   ```

2. Install the required dependencies:
   ```bash
   pip install pandas sqlalchemy
   ```

3. Ensure your PostgreSQL database is configured and running.

## Configuration

### Database Settings
Update the `db_config` dictionary in the script with your PostgreSQL credentials:
```python
 db_config = {
     'dbname': 'sample_csv',
     'user': 'postgres',
     'password': '123456',
     'host': 'localhost',
     'port': 5432
 }
```

### Directory
Set the `directory` variable to the folder containing your CSV files:
```python
directory = "/path/to/your/csv/files"
```

## Usage
Run the script using:
```bash
python reepicheep.py
```

### Workflow
1. Place your CSV files in the specified directory.
2. ReepiCheep dynamically creates tables in your PostgreSQL database for each CSV file.
3. Data from the CSV files is imported into the corresponding tables.

## Code Overview

### Main Components
- **ReepiCheep Class**: Core logic for handling database connections, dynamic table creation, and CSV import.
  - `create_table`: Dynamically generates tables based on CSV headers.
  - `import_csv_to_table`: Reads and imports CSV data.
  - `process_directory`: Uses multithreading to handle multiple files concurrently.

### Example Entry Point
```python
if __name__ == "__main__":
    db_config = { ... }  # Database configuration
    directory = "..."  # Directory containing CSV files

    importer = ReepiCheep(db_config, directory, max_threads=4)
    importer.process_directory()
```

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed explanation of your changes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
For issues or support, please create an issue in the repository or reach out to the maintainer.
