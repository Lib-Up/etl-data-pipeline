"""
Data Transformation Module
Handles data cleaning, validation, and transformation
"""

import pandas as pd
import logging
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataTransformer:
    """Transform and clean data"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.validate = config['pipeline']['validate_data']
        
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicates and handle missing values"""
        logger.info("Cleaning data...")
        
        initial_rows = len(df)
        
        # Remove duplicates
        df = df.drop_duplicates()
        duplicates_removed = initial_rows - len(df)
        if duplicates_removed > 0:
            logger.info(f"Removed {duplicates_removed} duplicate rows")
        
        # Handle missing values
        null_counts = df.isnull().sum()
        total_nulls = null_counts.sum()
        
        if total_nulls > 0:
            logger.info(f"Found {total_nulls} missing values")
            # Strategy: Fill numeric with 0, string with empty string
            for col in df.columns:
                if df[col].dtype in ['int64', 'float64']:
                    df[col].fillna(0, inplace=True)
                else:
                    df[col].fillna('', inplace=True)
            logger.info("Filled missing values")
        
        logger.info(f"Cleaned data: {len(df)} rows remaining")
        return df
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """Validate data quality"""
        if not self.validate:
            return True
            
        logger.info("Validating data...")
        
        # Check for empty dataframe
        if df.empty:
            logger.error("DataFrame is empty")
            return False
        
        # Check for required columns (can be customized)
        # required_cols = ['id', 'name', 'value']
        # missing = set(required_cols) - set(df.columns)
        # if missing:
        #     logger.error(f"Missing required columns: {missing}")
        #     return False
        
        # Check data types
        logger.info(f"Data types: {df.dtypes.to_dict()}")
        
        # Check for suspicious values
        for col in df.columns:
            unique_count = df[col].nunique()
            logger.info(f"Column '{col}': {unique_count} unique values")
        
        logger.info("✓ Data validation passed")
        return True
    
    def apply_transformations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply custom transformations"""
        logger.info("Applying transformations...")
        
        # Example transformations (customize as needed)
        
        # 1. Normalize column names (lowercase, replace spaces)
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        
        # 2. Convert date columns
        date_columns = [col for col in df.columns if 'date' in col.lower()]
        for col in date_columns:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                logger.info(f"Converted '{col}' to datetime")
            except:
                pass
        
        # 3. Strip whitespace from string columns
        string_columns = df.select_dtypes(include=['object']).columns
        for col in string_columns:
            df[col] = df[col].astype(str).str.strip()
        
        # 4. Add metadata columns
        df['processed_at'] = pd.Timestamp.now()
        
        logger.info(f"Applied transformations: {len(df.columns)} columns")
        return df
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Main transformation method"""
        logger.info("=" * 50)
        logger.info("TRANSFORMATION PHASE")
        logger.info("=" * 50)
        logger.info(f"Input: {len(df)} rows, {len(df.columns)} columns")
        
        # Clean data
        df = self.clean_data(df)
        
        # Validate
        if not self.validate_data(df):
            raise ValueError("Data validation failed")
        
        # Apply transformations
        df = self.apply_transformations(df)
        
        logger.info(f"Output: {len(df)} rows, {len(df.columns)} columns")
        logger.info("Transformation complete")
        
        return df


if __name__ == "__main__":
    # Example usage
    config = {
        'pipeline': {
            'validate_data': True
        }
    }
    
    # Sample data
    data = pd.DataFrame({
        'id': [1, 2, 2, 3],
        'name': ['A', 'B', 'B', 'C'],
        'value': [100, 200, 200, None],
        'Date': ['2024-01-01', '2024-01-02', '2024-01-02', '2024-01-03']
    })
    
    transformer = DataTransformer(config)
    # transformed = transformer.transform(data)
    # print(transformed)
    print("DataTransformer module loaded successfully")
