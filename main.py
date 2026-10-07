import json
import csv
import logging
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Iterator, Dict, List
from contextlib import contextmanager

# --- Configuration & Exceptions ---

class ApplicationError(Exception):
    """Base application error."""

class DataError(ApplicationError):
    """Base data error."""

class DataValidationError(DataError):
    pass

class ConfigurationError(ApplicationError):
    pass

class DataProcessor:
    def __init__(self, config: Dict[str, Any]):
        self.input_path = Path(config.get("input_path", "data.csv"))
        self.output_path = Path(config.get("output_path", "result.json"))
        self.log_file = config.get("log_file", "app.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.FileHandler(self.log_file), logging.StreamHandler()]
        )
        self.logger = logging.getLogger(__name__)

    @contextmanager
    def atomic_write(self, path: Path):
        """Context manager для атомарного запису файлу."""
        temp_file = NamedTemporaryFile('w', delete=False, dir=path.parent, suffix='.tmp')
        try:
            yield temp_file
            temp_file.close()
            os.replace(temp_file.name, path)
        except Exception as e:
            temp_file.close()
            os.remove(temp_file.name)
            raise e

    def stream_csv(self, file_path: Path) -> Iterator[Dict[str, Any]]:
        """Streaming reader для CSV файлів."""
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} not found.")
            
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, start=1):
                yield {"row": i, "data": row}

    def validate_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Валідація запису."""
        data = record["data"]
        if "id" not in data or not data["id"].isdigit():
            raise DataValidationError(f"Invalid ID at row {record['row']}")
        return {"id": int(data["id"]), "value": data.get("value", "N/A")}

    def run(self):
        """Головний пайплайн обробки."""
        self.logger.info("Starting processing...")
        results = []
        
        try:
            for record in self.stream_csv(self.input_path):
                try:
                    processed = self.validate_record(record)
                    results.append(processed)
                except DataValidationError as e:
                    self.logger.warning(f"Skipping record: {e}")
            
            with self.atomic_write(self.output_path) as f:
                json.dump(results, f, indent=4)
                
            self.logger.info(f"Successfully saved to {self.output_path}")
            
        except Exception as e:
            self.logger.error(f"Critical failure: {e}")
            raise

def main():
    # Демонстрація роботи
    config = {
        "input_path": "input.csv",
        "output_path": "output.json",
        "log_file": "process.log"
    }
    
    # Створимо тестовий файл
    with open("input.csv", "w", encoding="utf-8") as f:
        f.write("id,value\n1,Alpha\nerror,Beta\n2,Gamma")
        
    processor = DataProcessor(config)
    processor.run()

if __name__ == "__main__":
    main()