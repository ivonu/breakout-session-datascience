# Database Administration

This folder contains all database creation, generation, and administration tools for the banking workshop project.

## 📁 Contents

### 🐍 Scripts
- **`generate_banking_db.py`** - Main database generator script with realistic banking data

### 📖 Documentation
- **`DATABASE_GENERATOR_README.md`** - Detailed documentation for database generation scripts

### 🗃️ Database Schema
- **`banking_schema.sql`** - SQL DDL file with table creation statements

## 🚀 Quick Start

### Generate Banking Database

```bash
# Navigate to database-admin folder
cd database-admin

# Install required dependencies
pip install faker

# Generate the database
python generate_banking_db.py
```

This will create the banking database at `../content/data/banking_data.db`

## 📂 Output Location

All generated databases are saved to: `../content/data/banking_data.db`

This ensures the workshop participants can access the data from the `content/` directory without needing to know about the database generation tools.

## 🔧 Database Schema

The database schema is managed in this folder:
- SQL DDL file: `banking_schema.sql`

Workshop documentation is maintained in the content area:
- Schema documentation: `../content/doc/database_schema.md`

## 📋 Workshop Separation

This folder contains **administration tools** that are used to create and manage the database. Workshop participants work with:
- The generated database: `../content/data/banking_data.db` 
- Schema documentation: `../content/doc/`

This separation keeps the workshop content clean and focused while providing comprehensive database management tools for instructors and administrators.

---

## 📖 Database Documentation

This section contains comprehensive documentation for the banking database schema used in the workshop.

### 📋 Schema Documentation
Complete documentation of the banking database schema including:
- Visual schema diagram
- Detailed table definitions with columns, data types, and constraints
- Relationship descriptions and business rules
- Sample SQL queries for common operations
- Performance and security considerations
- Maintenance procedures

**Location:** `../content/doc/database_schema.md`

### 🗄️ Schema Overview

The database consists of four core tables:

```
customers ──┬── accounts ──┬── transactions
            │       │      │ 
            └──── cards ───┘
```

- **customers**: Customer personal information and account management
- **accounts**: Bank accounts linked to customers
- **cards**: Payment cards (debit/credit) linked to accounts  
- **transactions**: All financial transactions with full audit trail

### ✨ Key Features

- ✅ Referential integrity with foreign key constraints
- ✅ Automated balance calculations with triggers
- ✅ Comprehensive indexing for performance
- ✅ Pre-built views for common queries (customer_summary, account_details)
- ✅ Stored procedures for complex operations
- ✅ Sample data for testing and development

### 📋 Database Requirements

- SQLite 3.8+ (built into Python)
- Supports standard SQL with CHECK constraints
- No server installation required

### ⚠️ Usage Notes

- All monetary values use DECIMAL(15,2) for precision
- Timestamps are in UTC format
- Card numbers should be encrypted/tokenized in production
- Consider partitioning transactions table for large datasets

---

For detailed schema information, refer to `../content/doc/database_schema.md`.

## 📊 Database Views

The schema includes several pre-defined views for simplified data access and reporting.

### View Benefits

1. **Simplified Queries**: Complex joins are pre-computed
2. **Data Consistency**: Standardized calculations across applications
3. **Performance**: Frequently accessed data combinations are optimized
4. **Security**: Can limit access to specific columns or filtered data
5. **Maintenance**: Changes to underlying logic only need to be made in one place

### View Limitations

- Views are read-only (cannot be used for INSERT/UPDATE/DELETE)
- Complex views may have performance implications
- Nested views should be used carefully to avoid performance degradation
- Some database engines may not optimize views as efficiently as direct table access

## 🔧 Advanced Database Requirements

### Core Requirements
- SQLite 3.8+ (built into Python)
- Supports standard SQL with CHECK constraints
- No server installation required
- Cross-platform compatibility

### Indexing Strategy
- Primary keys are automatically indexed
- Foreign key columns should have indexes for join performance
- Date columns used in WHERE clauses should be indexed
- Consider composite indexes for common query patterns

### Performance Optimization
- Consider partitioning the `transactions` table by date for better performance
- Large customer bases may benefit from customer table partitioning
- Implement archival strategy for old transactions
- Consider read replicas for reporting queries

## 🔒 Security Considerations

### Data Protection
- Card numbers should be encrypted or tokenized
- Personal information should be masked in logs
- Implement audit trails for sensitive operations

### Access Control
- Implement role-based access control
- Use stored procedures for complex operations
- Log all data access and modifications

## 🛠️ Maintenance Procedures

### Regular Tasks
- Monitor table sizes and growth rates
- Update statistics for query optimization
- Perform integrity checks on foreign keys
- Archive old transaction data

### Backup Strategy
- Daily full backups with point-in-time recovery
- Transaction log backups every 15 minutes
- Test restore procedures monthly

---

*Database Administration Guide - Last updated: April 14, 2026*

