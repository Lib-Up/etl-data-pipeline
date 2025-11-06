
"""
Main ETL Pipeline
Orchestrates Extract, Transform, Load operations
"""

import yaml
import logging
import sys
import os
from datetime import datetime
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from extract import DataExtractor
from transform import DataTransformer
from load import DataLoader

# Setup logging
log_dir = Path(__file__).parent.parent / 'logs'
log_dir.mkdir(exist_ok=True)

log_file = log_dir / f"pipeline_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ETLPipeline:
    """Main ETL Pipeline orchestrator"""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / 'config' / 'config.yaml'
        
        self.config_path = config_path
        self.config = self.load_config()
        self.extractor = DataExtractor(self.config)
        self.transformer = DataTransformer(self.config)
        self.loader = DataLoader(self.config)
        
    def load_config(self) -> dict:
        """Load configuration from YAML file"""
        try:
            logger.info(f"Loading configuration from: {self.config_path}")
            
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Replace environment variables
            config = self._replace_env_vars(config)
            
            logger.info("✓ Configuration loaded successfully")
            return config
            
        except FileNotFoundError:
            logger.error(f"Config file not found: {self.config_path}")
            logger.info("Please copy config/config.example.yaml to config/config.yaml")
            raise
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            raise
    
    def _replace_env_vars(self, obj):
        """Recursively replace ${VAR} with environment variables"""
        if isinstance(obj, dict):
            return {k: self._replace_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._replace_env_vars(item) for item in obj]
        elif isinstance(obj, str) and obj.startswith('${') and obj.endswith('}'):
            var_name = obj[2:-1]
            return os.getenv(var_name, obj)
        return obj
    
    def run(self) -> bool:
        """Execute the ETL pipeline"""
        start_time = datetime.now()
        
        logger.info("=" * 70)
        logger.info("ETL PIPELINE STARTED")
        logger.info("=" * 70)
        logger.info(f"Start time: {start_time}")
        logger.info(f"Config: {self.config_path}")
        
        try:
            # STEP 1: Extract
            logger.info("")
            logger.info("STEP 1: EXTRACT")
            logger.info("-" * 70)
            data = self.extractor.extract()
            
            if data.empty:
                logger.warning("No data extracted. Pipeline stopped.")
                return False
            
            logger.info(f"✓ Extracted {len(data)} rows")
            
            # STEP 2: Transform
            logger.info("")
            logger.info("STEP 2: TRANSFORM")
            logger.info("-" * 70)
            transformed_data = self.transformer.transform(data)
            logger.info(f"✓ Transformed {len(transformed_data)} rows")
            
            # STEP 3: Load
            logger.info("")
            logger.info("STEP 3: LOAD")
            logger.info("-" * 70)
            
            table_name = self.config.get('database', {}).get('table', 'etl_output')
            if_exists = self.config.get('pipeline', {}).get('if_exists', 'append')
            
            success = self.loader.load(
                transformed_data,
                table_name=table_name,
                if_exists=if_exists
            )
            
            if not success:
                raise Exception("Data loading failed")
            
            # Success
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info("")
            logger.info("=" * 70)
            logger.info("✓ PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("=" * 70)
            logger.info(f"End time: {end_time}")
            logger.info(f"Duration: {duration:.2f} seconds")
            logger.info(f"Rows processed: {len(data)} → {len(transformed_data)}")
            logger.info("=" * 70)
            
            return True
            
        except KeyboardInterrupt:
            logger.warning("Pipeline interrupted by user")
            return False
            
        except Exception as e:
            logger.error("=" * 70)
            logger.error("✗ PIPELINE FAILED")
            logger.error("=" * 70)
            logger.error(f"Error: {e}", exc_info=True)
            logger.error("=" * 70)
            return False
            
        finally:
            # Cleanup
            self.loader.close()


def main():
    """Main entry point"""
    # Check for custom config path
    config_path = None
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    
    # Create and run pipeline
    try:
        pipeline = ETLPipeline(config_path)
        success = pipeline.run()
        sys.exit(0 if success else 1)
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

---

## **Fichier : logs/.gitkeep**
```
# This file keeps the logs directory in git
```

---

## **Fichier : tests/.gitkeep**
```
# This file keeps the tests directory in git
