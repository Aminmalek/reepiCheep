import os
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class ReepiCheep:
    def __init__(self, db_config, directory, max_threads=4):
        """
        Initialize the importer with database configuration, directory containing CSV files, and threading configuration.
        """
        self.db_config = db_config
        self.directory = directory
        self.max_threads = max_threads
        self.engine = create_engine(self._get_db_url(db_config))
        self.Session = sessionmaker(bind=self.engine)

    def _get_db_url(self, db_config):
        """
        Construct the database URL for SQLAlchemy.
        """
        return f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"

    def create_table(self, table_name, columns):
        """
        Dynamically create a database table based on the CSV columns.
        """
        # Create a new class dynamically
        attributes = {'__tablename__': table_name, 'id': Column(Integer, primary_key=True)}

        for col in columns:
            attributes[col] = Column(String)

        # Create the table class dynamically and add it to the base
        table_class = type(table_name, (Base,), attributes)
        Base.metadata.create_all(self.engine)  # Create the table only once
        print(f"Table '{table_name}' created successfully.")
        return table_class

    def import_csv_to_table(self, file_path, table_name):
        """
        Import a CSV file into a specified database table using df.to_sql.
        """
        print(f"Processing file: {file_path}")
        df = pd.read_csv(file_path)
        print(df.head())
        table_class = self.create_table(table_name, df.columns)
        df.to_sql(table_class.__tablename__, self.engine, if_exists='append', index=False)

        print(f"Data from '{file_path}' imported successfully into '{table_name}'.")

    def process_file(self, file_name):
        """
        Process a single CSV file.
        """
        if file_name.endswith('.csv'):
            file_path = os.path.join(self.directory, file_name)
            table_name = os.path.splitext(file_name)[0]
            self.import_csv_to_table(file_path, table_name)

    def process_directory(self):
        """
        Process all CSV files in the directory using multithreading.
        """
        files = [f for f in os.listdir(self.directory) if f.endswith('.csv')]
        with ThreadPoolExecutor(self.max_threads) as executor:
            executor.map(self.process_file, files)


if __name__ == "__main__":
    db_config = {
        'dbname': 'sample_csv',
        'user': 'postgres',
        'password': 'your password',
        'host': 'localhost',
        'port': 5432
    }
    directory = "/path/to/your/csv/files"

    importer = ReepiCheep(db_config, directory, max_threads=4)  # Adjust max_threads as needed

    importer.process_directory()
