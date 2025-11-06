"""
Data Extraction Module
Handles data extraction from various sources (CSV, API, Database)
"""

import pandas as pd
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataExtractor:
    """Extract data from different sources"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.source_type = config['source']['type']
        
    def extract_from_csv(self, file_path: str) -> pd.DataFrame:
        """Extract data from CSV file"""
        try:
            logger.info(f"Extracting data from CSV: {file_path}")
            df = pd.read_csv(file_path)
            logger.info(f"Extracted {len(df)} rows, {len(df.columns)} columns")
            return df
        except FileNotFoundError:
            logger.error(f"CSV file not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Error extracting CSV: {e}")
            raise
    
    def extract_from_database(self, connection_string: str, query: str) -> pd.DataFrame:
        """Extract data from database"""
        try:
            logger.info("Extracting data from database")
            from sqlalchemy import create_engine
            
            engine = create_engine(connection_string)
            df = pd.read_sql(query, engine)
            
            logger.info(f"Extracted {len(df)} rows from database")
            return df
        except Exception as e:
            logger.error(f"Error extracting from database: {e}")
            raise
    
    def extract_from_api(self, url: str, headers: Dict = None) -> pd.DataFrame:
        """Extract data from API"""
        try:
            import requests
            
            logger.info(f"Extracting data from API: {url}")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            df = pd.DataFrame(data)
            
            logger.info(f"Extracted {len(df)} rows from API")
            return df
        except Exception as e:
            logger.error(f"Error extracting from API: {e}")
            raise
    
    def extract(self) -> pd.DataFrame:
        """Main extraction method"""
        logger.info("=" * 50)
        logger.info("EXTRACTION PHASE")
        logger.info("=" * 50)
        
        if self.source_type == 'csv':
            file_path = self.config['source']['path']
            return self.extract_from_csv(file_path)
            
        elif self.source_type == 'database':
            connection_string = self.config['source']['connection_string']
            query = self.config['source']['query']
            return self.extract_from_database(connection_string, query)
            
        elif self.source_type == 'api':
            url = self.config['source']['url']
            headers = self.config['source'].get('headers', {})
            return self.extract_from_api(url, headers)
            
        else:
            raise ValueError(f"Unsupported source type: {self.source_type}")


if __name__ == "__main__":
    # Example usage
    config = {
        'source': {
            'type': 'csv',
            'path': 'data/sample.csv'
        }
    }
    
    extractor = DataExtractor(config)
    # data = extractor.extract()
    # print(f"Extracted {len(data)} rows")
    print("DataExtractor module loaded successfully")
