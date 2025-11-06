
"""
Data Loading Module
Handles loading data to target database
"""

import pandas as pd
import logging
from sqlalchemy import create_engine, text
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Load data to database"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.db_config = config['database']
        self.batch_size = config['pipeline']['batch_size']
        self.engine = None
        
    def get_connection_string(self) -> str:
        """Build database connection string"""
        # Support for PostgreSQL and MySQL
        db_type = self.db_config.get('type', 'postgresql')
        
        if db_type == 'postgresql':
            return (
                f"postgresql://{self.db_config['user']}:"
                f"{self.db_config['password']}@"
                f"{self.db_config['host']}:"
                f"{self.db_config['port']}/"
                f"{self.db_config['name']}"
            )
        elif db_type == 'mysql':
            return (
                f"mysql+pymysql://{self.db_config['user']}:"
                f"{self.db_config['password']}@"
                f"{self.db_config['host']}:"
                f"{self.db_config['port']}/"
                f"{self.db_config['name']}"
            )
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
    
    def connect(self) -> bool:
        """Connect to database"""
        try:
            logger.info("Connecting to database...")
            connection_string = self.get_connection_string()
            self.engine = create_engine(connection_string)
            
            # Test connection
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                result.fetchone()
            
            logger.info("✓ Database connection established")
            return True
            
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False
    
    def load_to_database(self, df: pd.DataFrame, table_name: str, 
                         if_exists: str = 'append') -> bool:
        """Load dataframe to database"""
        try:
            logger.info(f"Loading {len(df)} rows to table '{table_name}'...")
            
            # Ensure connection
            if self.engine is None:
                if not self.connect():
                    raise Exception("Failed to connect to database")
            
            # Load data in batches
            df.to_sql(
                table_name,
                self.engine,
                if_exists=if_exists,  # 'append', 'replace', 'fail'
                index=False,
                chunksize=self.batch_size,
                method='multi'  # Use multi-row INSERT for better performance
            )
            
            logger.info(f"✓ Successfully loaded {len(df)} rows to '{table_name}'")
            return True
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return False
    
    def verify_load(self, table_name: str, expected_rows: int) -> bool:
        """Verify data was loaded correctly"""
        try:
            logger.info("Verifying data load...")
            
            with self.engine.connect() as conn:
                result = conn.execute(
                    text(f"SELECT COUNT(*) FROM {table_name}")
                )
                actual_rows = result.fetchone()[0]
            
            if actual_rows >= expected_rows:
                logger.info(f"✓ Verification passed: {actual_rows} rows in table")
                return True
            else:
                logger.warning(
                    f"Row count mismatch: expected {expected_rows}, "
                    f"found {actual_rows}"
                )
                return False
                
        except Exception as e:
            logger.error(f"Verification failed: {e}")
            return False
    
    def load(self, df: pd.DataFrame, table_name: str = 'target_table',
             if_exists: str = 'append', verify: bool = True) -> bool:
        """Main loading method"""
        logger.info("=" * 50)
        logger.info("LOADING PHASE")
        logger.info("=" * 50)
        
        success = self.load_to_database(df, table_name, if_exists)
        
        if success and verify:
            self.verify_load(table_name, len(df))
        
        return success
    
    def close(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")


if __name__ == "__main__":
    # Example usage
    import os
    
    config = {
        'database': {
            'type': 'postgresql',
            'host': 'localhost',
            'port': 5432,
            'name': 'testdb',
            'user': 'postgres',
            'password': os.getenv('DB_PASSWORD', 'password')
        },
        'pipeline': {
            'batch_size': 1000
        }
    }
    
    # Sample data
    data = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['A', 'B', 'C'],
        'value': [100, 200, 300]
    })
    
    loader = DataLoader(config)
    # loader.load(data, 'test_table')
    # loader.close()
    print("DataLoader module loaded successfully")
