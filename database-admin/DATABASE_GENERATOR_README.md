# Banking Database Generator Scripts

This directory contains Python scripts to generate a SQLite database with realistic banking data based on the documented schema.

## 📁 Files

### 🐍 generate_banking_db.py
**Full-featured generator with realistic data**
- Uses the `faker` library for generating realistic names, addresses, etc.
- Creates 100 customers with comprehensive data
- Generates extensive transaction history
- Requires: `pip install faker`

## 🚀 Quick Start

```bash
pip install faker
python generate_banking_db.py
```

## 📊 Generated Data

The script creates a complete database schema with:

- **customers**: Personal information (name, email, phone, address, etc.)
- **accounts**: Bank accounts (checking, savings, business) linked to customers  
- **cards**: Payment cards (debit, credit, prepaid) linked to accounts
- **transactions**: Financial transactions with complete audit trail

## 🎯 Database Features

- ✅ **Single Source of Truth**: Schema defined in `content/doc/banking_schema.sql`
- ✅ **Referential Integrity**: Proper foreign key relationships
- ✅ **Realistic Data**: Balanced account types and transaction patterns  
- ✅ **Chronological Order**: Transactions generated in proper time sequence
- ✅ **Balance Tracking**: Automatic balance calculations
- ✅ **Performance Indexes**: Optimized for common queries

## 📁 Output Location

Generated database is saved to:
- `../content/data/banking_data.db`

## 📖 Sample Queries

After generation, you can test with these SQL queries:

```sql
-- View all customers with their account information
SELECT c.first_name, c.last_name, c.email, 
       a.account_type, a.balance, a.status
FROM customers c 
JOIN accounts a ON c.customer_id = a.customer_id
ORDER BY c.last_name;

-- Top spending accounts
SELECT account_id, 
       SUM(amount) as total_spent 
FROM transactions 
WHERE type = 'debit' 
GROUP BY account_id 
ORDER BY total_spent DESC 
LIMIT 10;

-- Card usage statistics
SELECT card_type, 
       COUNT(*) as card_count,
       COUNT(CASE WHEN status = 'active' THEN 1 END) as active_count
FROM cards 
GROUP BY card_type;

-- Monthly transaction volume
SELECT strftime('%Y-%m', created_at) as month,
       COUNT(*) as transaction_count,
       SUM(amount) as total_amount
FROM transactions
GROUP BY month
ORDER BY month DESC
LIMIT 12;
```

## 🔧 Customization

You can modify the configuration variables at the top of each script:

```python
NUM_CUSTOMERS = 50                    # Number of customers to generate
NUM_ACCOUNTS_PER_CUSTOMER = (1, 3)   # Min/Max accounts per customer
NUM_CARDS_PER_ACCOUNT = (0, 2)       # Min/Max cards per account  
NUM_TRANSACTIONS_PER_ACCOUNT = (5, 30) # Min/Max transactions per account
```

## 🔍 Viewing the Data

You can examine the generated database using:

1. **SQLite Browser**: Install DB Browser for SQLite
2. **Command Line**: `sqlite3 ../content/data/banking_data.db`
3. **Python**: Use the sqlite3 module
4. **Jupyter Notebooks**: Perfect for data analysis

## 📋 Schema Validation

The script implements the complete banking schema as documented in:
- `content/doc/database_schema.md` - Full documentation
- `content/doc/banking_schema.sql` - SQLite implementation (single source of truth)

### Schema Architecture

The Python generator uses **single source of truth** approach:

1. **Primary**: Loads schema from `content/doc/banking_schema.sql`
2. **Consistency**: All table definitions, indexes, and views in one place
3. **Reliability**: Ensures perfect synchronization between code and documentation

This ensures:
- ✅ Schema changes only need to be made in one file
- ✅ Python code and SQL documentation stay synchronized  
- ✅ Reduced duplication and maintenance overhead
- ✅ Eliminates schema drift between components

The generated data follows all business rules and constraints defined in the schema documentation.

---

**Ready to explore banking data analysis!** 🏦📊

