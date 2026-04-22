# Banking Database Project Architecture

## Overview

This project implements a complete banking database system with comprehensive documentation, SQL schema definitions, and Python generators for creating realistic test data. The architecture follows a **single source of truth** principle for schema management.

## 📁 Project Structure

```
breakout-session-datascience/
├── content/
│   ├── data/
│   │   └── banking_data.db             # 🗄️ Generated SQLite database
│   ├── doc/
│   │   └── database_schema.md          # 📋 Complete schema documentation
│   ├── python_for_csharp_developers.ipynb  # 📓 Python intro for C# developers
│   └── data_science_workshop.ipynb     # 📓 Data science workshop (pandas, matplotlib, scikit-learn)
├── database-admin/
│   ├── banking_schema.sql              # 🗄️ SQLite schema definition (source of truth)
│   ├── generate_banking_db.py          # 🐍 Banking database generator (requires faker)
│   ├── DATABASE_GENERATOR_README.md    # 📖 Generator usage guide
│   └── README.md                       # 📖 Admin documentation
├── ARCHITECTURE.md                     # 📖 This file
├── README.md                           # 📖 Project overview
└── requirements.txt                    # 📦 Python dependencies
```

## 🏗️ Architecture Principles

### Single Source of Truth

The database schema is defined once in `database-admin/banking_schema.sql` and used by:

1. **Python Generator** - Reads and executes the SQL file directly
2. **Documentation** - References the same schema definitions
3. **Analysis Tools** - Work with databases created from the schema

### Benefits

- ✅ **Consistency**: All components use identical schema
- ✅ **Maintainability**: Schema changes only needed in one place
- ✅ **Reliability**: Reduced risk of drift between code and docs
- ✅ **Flexibility**: Easy to modify schema for different use cases
- ✅ **Clarity**: Single authoritative source eliminates confusion

## 🗄️ Database Schema

### Core Tables

1. **customers** - Personal information and account management
2. **accounts** - Bank accounts (`checking`, `savings`, `business`), start at balance 0
3. **cards** - Payment cards (`debit`, `credit`, `prepaid`)
4. **transactions** - Complete financial transaction history with signed amounts and spending categories

### Key Design Decisions

- **Signed amounts**: transaction `amount` is positive for incoming money (credit, incoming transfer) and negative for outgoing money (debit, fee, outgoing transfer). `SUM(amount)` over all transactions of an account equals the current account balance.
- **Spending categories**: every transaction carries a `category` (e.g. `Lebensmittel`, `Gesundheit`, `ATM`, `Gehalt & Einkommen`) in addition to the low-level `type`.
- **Swiss locale**: customer names, addresses, and phone numbers are generated with the `de_CH` Faker locale; merchant names use Swiss brands (Migros, Coop, SBB, Swisscom, etc.).
- **Chronological integrity**: the first transaction of every account is always an incoming one so the balance never starts negative.

### Relationships

```
customers ──┬── accounts ──┬── transactions
            │       │      │ 
            └──── cards ───┘
```

### Views

1. **customer_summary** - Aggregated customer data with account statistics
2. **account_details** - Combined account, customer, and card information

## 🐍 Python Generator

### Banking Data Generator (`database-admin/generate_banking_db.py`)

- **Purpose**: Production-quality realistic Swiss banking data
- **Dependencies**: `faker[de_CH]` library for realistic names, addresses, etc.
- **Output**: `content/data/banking_data.db`
- **Records**: 100 customers with extensive transaction history
- **Locale**: Swiss German (`de_CH`) — Swiss towns, names, phone formats

### Generator Features

- 📊 **Smart Data Generation**: Realistic patterns and relationships
- ⏰ **Chronological Accuracy**: Proper time sequencing; first transaction per account is always incoming
- 💰 **Balance Tracking**: Signed amounts — `SUM(amount)` = account balance
- 🏷️ **Spending Categories**: 16 categories (Lebensmittel, Gesundheit, ATM, SBB, etc.)
- 🇨🇭 **Swiss Brands**: Migros, Coop, SBB, Swisscom, Helvetia, Digitec, and more
- 🔗 **Referential Integrity**: Proper foreign key relationships
- 📈 **Performance**: Optimized indexes for common queries

## 📓 Jupyter Notebooks

### 1. `python_for_csharp_developers.ipynb`
An introduction to Python for developers coming from a C# / .NET background. Covers syntax comparison, OOP, collections, LINQ equivalents, and package management.

### 2. `data_science_workshop.ipynb`
A hands-on banking data science workshop showcasing:
- **pandas** — loading from SQLite, filtering, joins, groupby, date handling
- **matplotlib** — balance distributions, transaction timelines, pie charts, category analysis
- **scikit-learn** — feature engineering, train/test split, Decision Tree & Random Forest classification, confusion matrix, feature importance

## 🔄 Workflow

### Schema Development

1. **Define Schema**: Edit `database-admin/banking_schema.sql`
2. **Update Documentation**: Sync `content/doc/database_schema.md`
3. **Test**: Run Python generator to validate
4. **Deploy**: Use generated database for analysis

### Data Generation

```bash
pip install -r requirements.txt
cd database-admin
python generate_banking_db.py
```

Output is written to `content/data/banking_data.db`.

## 📊 Use Cases

### Educational

- SQL learning and practice
- Database design workshops
- Data analytics training for C# / .NET developers
- Business intelligence demos

### Development

- Application testing with realistic Swiss banking data
- Performance benchmarking
- Query optimization
- ETL pipeline development

### Research

- Financial analytics algorithms
- Customer segmentation studies
- Transaction pattern and category analysis
- Risk assessment models

## 🛠️ Technical Details

### Database Features

- **Engine**: SQLite (portable, no server required)
- **Size**: ~2–5 MB depending on data volume
- **Performance**: Indexed for common query patterns
- **Compatibility**: Works with any SQLite-compatible tool

### Schema Validation

- **Constraints**: CHECK constraints for data integrity
- **Foreign Keys**: Cascading deletes and updates
- **Indexes**: Performance-optimized for analytics queries
- **Views**: Pre-built aggregations for common needs

### Data Quality

- **Realistic Names**: Swiss-German names and addresses (`de_CH` locale)
- **Swiss Merchants**: Migros, Coop, Denner, SBB, Swisscom, Helvetia, Digitec, etc.
- **Valid Relationships**: Proper parent-child record linking
- **Temporal Accuracy**: Chronologically consistent timestamps
- **Business Logic**: Follows real banking rules and constraints

## 🚀 Getting Started

```bash
pip install -r requirements.txt
cd database-admin
python generate_banking_db.py
```

### Explore Data

```sql
-- Customer overview
SELECT * FROM customer_summary LIMIT 10;

-- Top spending accounts
SELECT account_id, SUM(ABS(amount)) as total_spent
FROM transactions
WHERE type = 'debit'
GROUP BY account_id
ORDER BY total_spent DESC LIMIT 5;

-- Monthly transaction trends
SELECT strftime('%Y-%m', created_at) as month,
       COUNT(*) as transaction_count
FROM transactions
GROUP BY month
ORDER BY month DESC;

-- Spending by category
SELECT category, COUNT(*) as txn_count, SUM(ABS(amount)) as total_spent
FROM transactions
WHERE type = 'debit'
GROUP BY category
ORDER BY total_spent DESC;
```

## 📈 Future Enhancements

### Planned Features

- Multiple database engine support (PostgreSQL, MySQL)
- Advanced analytics views and stored procedures
- Data export utilities (CSV, JSON, Parquet)
- Integration with popular data science tools
- Additional business domains (retail, healthcare)

### Extensibility

The modular architecture makes it easy to:

- Add new table types
- Extend existing relationships
- Create custom data generators
- Integrate with external data sources

---

**Built for data science education and practical banking analytics** 🏦📊

*Version: 3.0 - Swiss Banking Edition*
*Last Updated: April 22, 2026*
