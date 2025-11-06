# ETL Data Pipeline

Production-ready ETL (Extract, Transform, Load) pipeline for automated data processing. Built with Python for reliability, scalability, and ease of maintenance.

## 🔄 Pipeline Architecture
```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Extract   │  →   │  Transform  │  →   │    Load     │  →   │  Database   │
│             │      │             │      │             │      │             │
│ • CSV       │      │ • Clean     │      │ • Batch     │      │ • PostgreSQL│
│ • API       │      │ • Validate  │      │ • Insert    │      │ • MySQL     │
│ • Database  │      │ • Transform │      │ • Update    │      │ • SQLite    │
└─────────────┘      └─────────────┘      └─────────────┘      └─────────────┘
        ↓                    ↓                    ↓
    [Logging]          [Validation]         [Monitoring]
```

## ✨ Features

### Core Functionality
- ✅ **Multi-source Extraction** - CSV, databases, APIs
- ✅ **Data Transformation** - Cleaning, validation, aggregation
- ✅ **Batch Loading** - Efficient bulk inserts
- ✅ **Error Handling** - Comprehensive error management
- ✅ **Logging** - Detailed execution logs
- ✅ **Configuration** - YAML-based configuration

### Advanced Features
- 📊 **Data Validation** - Quality checks before loading
- 🔄 **Incremental Updates** - Process only new/changed data
- 📅 **Scheduled Execution** - Cron/systemd compatible
- 📧 **Notifications** - Email alerts on failures
- 🎯 **Modular Design** - Easy to extend and customize

## 🛠️ Tech Stack

- **Python 3.8+**
- **pandas** - Data manipulation
- **SQLAlchemy** - Database ORM
- **PyYAML** - Configuration management
- **psycopg2** - PostgreSQL adapter
- **PyMySQL** - MySQL adapter

## 📋 Requirements

### System Requirements
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

# Optional: Database clients for testing
sudo apt-get install postgresql-client mysql-client
```

### Python Dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### 1. Installation
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/etl-data-pipeline.git
cd etl-data-pipeline

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Copy example configuration
cp config/config.example.yaml config/config.yaml

# Edit configuration
nano config/config.yaml
```

**Example config.yaml:**
```yaml
source:
  type: csv
  path: data/input.csv

database:
  host: localhost
  port: 5432
  name: mydb
  user: dbuser
  password: ${DB_PASSWORD}  # Use environment variable

pipeline:
  batch_size: 1000
  validate_data: true
  log_level: INFO
```

### 3. Run Pipeline
```bash
# Set database password
export DB_PASSWORD='your_password'

# Run pipeline
python3 src/pipeline.py
```

## 📁 Project Structure
```
etl-data-pipeline/
├── config/
│   └── config.example.yaml    # Configuration template
├── src/
│   ├── extract.py             # Data extraction module
│   ├── transform.py           # Data transformation module
│   ├── load.py                # Data loading module
│   └── pipeline.py            # Main pipeline orchestrator
├── logs/                      # Execution logs
├── tests/                     # Unit tests
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🔧 Usage Examples

### Example 1: CSV to PostgreSQL
```yaml
# config.yaml
source:
  type: csv
  path: sales_data.csv

database:
  host: localhost
  port: 5432
  name: analytics
  user: etl_user
  password: ${DB_PASSWORD}

pipeline:
  batch_size: 1000
  validate_data: true
```
```bash
python3 src/pipeline.py
```

### Example 2: Database to Database
```python
# Custom extraction from source DB
from extract import DataExtractor

config = {
    'source': {
        'type': 'database',
        'query': 'SELECT * FROM orders WHERE date >= CURRENT_DATE - 1'
    }
}

extractor = DataExtractor(config)
data = extractor.extract()
```

### Example 3: API to Database
```python
# Extend extractor for API support
class APIExtractor(DataExtractor):
    def extract_from_api(self, url):
        response = requests.get(url)
        return pd.DataFrame(response.json())
```

## ⏰ Scheduled Execution

### Using Cron
```bash
# Edit crontab
crontab -e

# Add daily execution at 2 AM
0 2 * * * cd /path/to/etl-data-pipeline && /path/to/venv/bin/python3 src/pipeline.py >> logs/cron.log 2>&1
```

### Using Systemd

Create `/etc/systemd/system/etl-pipeline.service`:
```ini
[Unit]
Description=ETL Data Pipeline
After=network.target

[Service]
Type=oneshot
User=etl_user
WorkingDirectory=/path/to/etl-data-pipeline
Environment="DB_PASSWORD=your_password"
ExecStart=/path/to/venv/bin/python3 src/pipeline.py

[Install]
WantedBy=multi-user.target
```

Create timer `/etc/systemd/system/etl-pipeline.timer`:
```ini
[Unit]
Description=Run ETL Pipeline Daily

[Timer]
OnCalendar=daily
OnCalendar=02:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start:
```bash
sudo systemctl enable etl-pipeline.timer
sudo systemctl start etl-pipeline.timer
```

## 📊 Monitoring and Logging

### Log Locations

- **Pipeline logs:** `logs/pipeline_YYYYMMDD.log`
- **Error logs:** `logs/error_YYYYMMDD.log`

### Log Format
```
2024-01-15 02:00:01 - INFO - Starting ETL Pipeline
2024-01-15 02:00:02 - INFO - STEP 1: Extract
2024-01-15 02:00:05 - INFO - Extracted 10000 rows
2024-01-15 02:00:05 - INFO - STEP 2: Transform
2024-01-15 02:00:08 - INFO - Transformed 10000 rows
2024-01-15 02:00:08 - INFO - STEP 3: Load
2024-01-15 02:00:12 - INFO - Successfully loaded 10000 rows
2024-01-15 02:00:12 - INFO - Pipeline completed in 11.5s
```

## 🧪 Testing
```bash
# Run tests (when implemented)
python3 -m pytest tests/

# Run with coverage
python3 -m pytest --cov=src tests/
```

## 🐛 Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'pandas'`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue:** Database connection failed
```bash
# Solution: Check credentials and connection
psql -h localhost -U dbuser -d mydb  # Test connection
```

**Issue:** Permission denied on logs directory
```bash
# Solution: Create logs directory
mkdir -p logs
chmod 755 logs
```

## 🎯 Use Cases

- **Daily Data Imports** - Automated daily data ingestion
- **API to Database Sync** - Real-time or scheduled API data sync
- **Data Migration** - One-time or recurring data migrations
- **Report Generation** - Transform raw data for reporting
- **Data Warehouse Loading** - ETL for data warehouse population

## 🔒 Security Best Practices

1. **Never commit passwords** - Use environment variables
2. **Secure configuration files** - Restrict file permissions
3. **Use connection pooling** - For production deployments
4. **Validate input data** - Prevent SQL injection
5. **Encrypt sensitive data** - In transit and at rest

## 🤝 Contributing

Feel free to fork this repository and customize for your needs. This is a template designed to be extended.

## 📝 License

MIT License - Free for personal and commercial use

## 👤 Author

Available for freelance ETL and data engineering projects.

**Specialties:**
- Data pipeline development
- Database optimization
- Automation scripting
- Linux system integration

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check logs in `logs/` directory
- Review configuration in `config/`

## 🚀 Future Enhancements

- [ ] Support for more data sources (MongoDB, S3, etc.)
- [ ] Web dashboard for monitoring
- [ ] Parallel processing for large datasets
- [ ] Data quality metrics
- [ ] Automated data profiling
