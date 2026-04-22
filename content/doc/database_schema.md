# Banking Database Schema Documentation

## Overview

This document describes the database schema for a banking system with four core tables: `customers`, `accounts`, `cards`, and `transactions`. The schema is designed to support customer management, account operations, card services, and transaction processing.

## Database Schema Diagram

```
╔═══════════════╗     ╔══════════════╗     ╔═════════════╗     ╔════════════════╗
║  customers    ║     ║  accounts    ║     ║    cards    ║     ║  transactions  ║
╠═══════════════╣     ╠══════════════╣     ╠═════════════╣     ╠════════════════╣
║ customer_id   ║◄─┐  ║ account_id   ║◄─┐  ║ card_id     ║◄─┐  ║ transaction_id ║
║ first_name    ║  └──║ customer_id  ║  ├──║ account_id  ║  └──║ card_id        ║
║ last_name     ║     ║ account_type ║  │  ║ card_number ║  ┌──║ account_id     ║
║ email         ║     ║ balance      ║  │  ║ card_type   ║  │  ║ amount         ║
║ phone         ║     ║ status       ║  │  ║ expiry_date ║  │  ║ type           ║
║ address       ║     ║ created_at   ║  │  ║ status      ║  │  ║ category       ║
║ date_of_birth ║     ╚══════════════╝  │  ║ created_at  ║  │  ║ description    ║
║ status        ║                       │  ╚═════════════╝  │  ║ created_at     ║
║ created_at    ║                       └───────────────────┘  ╚════════════════╝
╚═══════════════╝                         
                                             
                                                                                                 
```

## Table Definitions

### 1. customers

Stores customer information and personal details.

| Column Name    | Data Type    | Constraints                    | Description                    |
|----------------|-------------|-------------------------------|--------------------------------|
| customer_id    | INTEGER     | PRIMARY KEY, AUTOINCREMENT    | Unique customer identifier     |
| first_name     | VARCHAR(50) | NOT NULL                      | Customer's first name          |
| last_name      | VARCHAR(50) | NOT NULL                      | Customer's last name           |
| email          | VARCHAR(100)| UNIQUE, NOT NULL              | Customer's email address       |
| phone          | VARCHAR(20) | NOT NULL                      | Customer's phone number        |
| address        | TEXT        | NOT NULL                      | Customer's full address        |
| date_of_birth  | DATE        | NOT NULL                      | Customer's date of birth       |
| created_at     | TIMESTAMP   | DEFAULT CURRENT_TIMESTAMP     | Account creation timestamp     |
| status         | TEXT        | CHECK(status IN ('active','inactive','suspended')) DEFAULT 'active' | Customer account status |

**Indexes:**
- Primary: customer_id
- Unique: email
- Index: last_name, created_at

### 2. accounts

Stores account information linked to customers.

| Column Name    | Data Type     | Constraints                   | Description                    |
|----------------|--------------|------------------------------|--------------------------------|
| account_id     | INTEGER      | PRIMARY KEY, AUTOINCREMENT   | Unique account identifier      |
| customer_id    | INTEGER      | FOREIGN KEY, NOT NULL        | Reference to customers table   |
| account_type   | TEXT         | CHECK(account_type IN ('checking','savings','business')) NOT NULL | Type of account |
| balance        | DECIMAL(15,2)| DEFAULT 0.00                 | Current account balance        |
| created_at     | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP    | Account creation timestamp     |
| status         | TEXT         | CHECK(status IN ('active','closed','frozen')) DEFAULT 'active' | Account status |

**Foreign Keys:**
- customer_id REFERENCES customers(customer_id) ON DELETE CASCADE

**Indexes:**
- Primary: account_id
- Index: customer_id, account_type, status

### 3. cards

Stores payment card information linked to accounts.

| Column Name    | Data Type    | Constraints                   | Description                    |
|----------------|-------------|------------------------------|--------------------------------|
| card_id        | INTEGER     | PRIMARY KEY, AUTOINCREMENT    | Unique card identifier         |
| account_id     | INTEGER     | FOREIGN KEY, NOT NULL         | Reference to accounts table    |
| card_number    | VARCHAR(19) | UNIQUE, NOT NULL              | Card number (masked/encrypted) |
| card_type      | TEXT        | CHECK(card_type IN ('debit','credit','prepaid')) NOT NULL | Type of card |
| expiry_date    | DATE        | NOT NULL                      | Card expiration date           |
| status         | TEXT        | CHECK(status IN ('active','blocked','expired')) DEFAULT 'active' | Card status |
| created_at     | TIMESTAMP   | DEFAULT CURRENT_TIMESTAMP     | Card creation timestamp        |

**Foreign Keys:**
- account_id REFERENCES accounts(account_id) ON DELETE CASCADE

**Indexes:**
- Primary: card_id
- Unique: card_number
- Index: account_id, status, expiry_date

### 4. transactions

Stores all transaction records for accounts and cards.

| Column Name     | Data Type     | Constraints                  | Description                    |
|----------------|--------------|------------------------------|--------------------------------|
| transaction_id | INTEGER      | PRIMARY KEY, AUTOINCREMENT   | Unique transaction identifier  |
| account_id     | INTEGER      | FOREIGN KEY, NOT NULL        | Reference to accounts table    |
| card_id        | INTEGER      | FOREIGN KEY, NULL            | Reference to cards table (if applicable) |
| amount         | DECIMAL(15,2)| NOT NULL                     | Signed transaction amount: positive = incoming (credit/transfer in), negative = outgoing (debit/fee/transfer out) |
| type           | TEXT         | CHECK(type IN ('debit','credit','transfer','fee')) NOT NULL | Transaction type |
| category       | TEXT         | NOT NULL                     | Spending category (e.g. Lebensmittel, Gesundheit, ATM, Gehalt & Einkommen) |
| description    | VARCHAR(255) | NOT NULL                     | Transaction description (German free text) |
| created_at     | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP    | Transaction timestamp          |

**Foreign Keys:**
- account_id REFERENCES accounts(account_id) ON DELETE CASCADE
- card_id REFERENCES cards(card_id) ON DELETE SET NULL

**Indexes:**
- Primary: transaction_id
- Index: account_id, created_at
- Index: card_id
- Index: type, created_at

## Relationships

### One-to-Many Relationships

1. **customers → accounts**: One customer can have multiple accounts
2. **accounts → cards**: One account can have multiple cards
3. **accounts → transactions**: One account can have multiple transactions
4. **cards → transactions**: One card can be used for multiple transactions

### Key Constraints

- Each account must belong to a customer
- Each card must be linked to an account
- Each transaction must be linked to an account
- Transactions may optionally be linked to a card (for card-based transactions)

## Business Rules

### Customer Management
- Customers must be at least 18 years old
- Email addresses must be unique across all customers
- Customer status affects ability to create new accounts

### Account Management
- Minimum balance requirements may apply based on account type
- Closed accounts cannot process new transactions
- Frozen accounts can only process certain transaction types

### Card Management
- Each account can have multiple active cards
- Expired cards are automatically blocked
- Card numbers must follow industry standards (Luhn algorithm)

### Transaction Processing
- All transactions must maintain referential integrity
- Balance calculations must be atomic
- Transaction history is immutable once created

## Sample Queries

### Customer Information with Accounts
```sql
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name as full_name,
    c.email,
    a.account_id,
    a.account_type,
    a.balance
FROM customers c
LEFT JOIN accounts a ON c.customer_id = a.customer_id
WHERE c.status = 'active'
ORDER BY c.last_name, c.first_name;
```

### Account Balance History
```sql
SELECT 
    t.transaction_id,
    t.created_at,
    t.type,
    t.amount,
    t.description
FROM transactions t
WHERE t.account_id = ?
ORDER BY t.created_at DESC
LIMIT 50;
```

### Card Usage Summary
```sql
SELECT 
    c.card_number,
    c.card_type,
    COUNT(t.transaction_id) as transaction_count,
    SUM(CASE WHEN t.type = 'debit' THEN t.amount ELSE 0 END) as total_debits,
    MAX(t.created_at) as last_used
FROM cards c
LEFT JOIN transactions t ON c.card_id = t.card_id
WHERE c.status = 'active'
GROUP BY c.card_id;
```

### Monthly Transaction Summary
```sql
SELECT 
    strftime('%Y-%m', t.created_at) as month,
    t.type,
    COUNT(*) as transaction_count,
    SUM(t.amount) as total_amount
FROM transactions t
JOIN accounts a ON t.account_id = a.account_id
WHERE a.customer_id = ?
    AND t.created_at >= date('now', '-12 months')
GROUP BY month, t.type
ORDER BY month DESC, t.type;
```

## Database Views

The schema includes several pre-defined views to simplify common queries and provide convenient access to aggregated data.

### 1. customer_summary

Provides a comprehensive overview of customers with their account statistics.

```sql
CREATE VIEW customer_summary AS
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name as full_name,
    c.email,
    c.phone,
    c.status as customer_status,
    COUNT(a.account_id) as account_count,
    COALESCE(SUM(a.balance), 0) as total_balance,
    c.created_at as customer_since
FROM customers c
LEFT JOIN accounts a ON c.customer_id = a.customer_id AND a.status = 'active'
GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.phone, c.status, c.created_at;
```

**Usage:**
- Quick customer overview for customer service
- Account relationship summaries
- Customer portfolio analysis

**Example Query:**
```sql
-- Top 10 customers by total balance
SELECT full_name, total_balance, account_count
FROM customer_summary 
WHERE customer_status = 'active'
ORDER BY total_balance DESC 
LIMIT 10;
```

### 2. account_details

Combines account information with customer data and card counts for detailed account management.

```sql
CREATE VIEW account_details AS
SELECT 
    a.account_id,
    a.account_type,
    a.balance,
    a.status as account_status,
    a.created_at as account_created,
    c.customer_id,
    c.first_name || ' ' || c.last_name as customer_name,
    c.email as customer_email,
    COUNT(card.card_id) as card_count
FROM accounts a
JOIN customers c ON a.customer_id = c.customer_id
LEFT JOIN cards card ON a.account_id = card.account_id AND card.status = 'active'
GROUP BY a.account_id, a.account_type, a.balance, a.status, a.created_at, 
         c.customer_id, c.first_name, c.last_name, c.email;
```

**Usage:**
- Account management dashboards
- Customer relationship management
- Account performance analysis

**Example Query:**
```sql
-- Business accounts with high balances and no cards
SELECT customer_name, customer_email, balance, card_count
FROM account_details 
WHERE account_type = 'business' 
  AND balance > 50000 
  AND card_count = 0
ORDER BY balance DESC;
```

---

*Schema Documentation - Last updated: April 14, 2026*
*For advanced administration topics, see: ../../database-admin/README.md*








