-- Banking Database Schema DDL
-- Created: April 14, 2026
-- Description: SQLite Data Definition Language for banking system tables

-- Table: customers
-- Stores customer information and personal details
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT CHECK(status IN ('active', 'inactive', 'suspended')) DEFAULT 'active'
);

-- Table: accounts
-- Stores account information linked to customers
CREATE TABLE IF NOT EXISTS accounts (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    account_type TEXT CHECK(account_type IN ('checking', 'savings', 'business')) NOT NULL,
    balance DECIMAL(15,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT CHECK(status IN ('active', 'closed', 'frozen')) DEFAULT 'active',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- Table: cards
-- Stores payment card information linked to accounts
CREATE TABLE IF NOT EXISTS cards (
    card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    card_number VARCHAR(19) UNIQUE NOT NULL,
    card_type TEXT CHECK(card_type IN ('debit', 'credit', 'prepaid')) NOT NULL,
    expiry_date DATE NOT NULL,
    status TEXT CHECK(status IN ('active', 'blocked', 'expired')) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
);

-- Table: transactions
-- Stores all transaction records for accounts and cards
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    card_id INTEGER NULL,
    amount DECIMAL(15,2) NOT NULL,
    type TEXT CHECK(type IN ('debit','credit','transfer','fee')) NOT NULL,
    category TEXT NOT NULL,
    description VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
    FOREIGN KEY (card_id) REFERENCES cards(card_id) ON DELETE SET NULL
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_customers_last_name ON customers(last_name);
CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
CREATE INDEX IF NOT EXISTS idx_customers_status ON customers(status);
CREATE INDEX IF NOT EXISTS idx_customers_created_at ON customers(created_at);

CREATE INDEX IF NOT EXISTS idx_accounts_customer_id ON accounts(customer_id);
CREATE INDEX IF NOT EXISTS idx_accounts_type ON accounts(account_type);
CREATE INDEX IF NOT EXISTS idx_accounts_status ON accounts(status);
CREATE INDEX IF NOT EXISTS idx_accounts_created_at ON accounts(created_at);

CREATE INDEX IF NOT EXISTS idx_cards_account_id ON cards(account_id);
CREATE INDEX IF NOT EXISTS idx_cards_number ON cards(card_number);
CREATE INDEX IF NOT EXISTS idx_cards_status ON cards(status);
CREATE INDEX IF NOT EXISTS idx_cards_expiry_date ON cards(expiry_date);
CREATE INDEX IF NOT EXISTS idx_cards_type ON cards(card_type);

CREATE INDEX IF NOT EXISTS idx_transactions_account_id ON transactions(account_id);
CREATE INDEX IF NOT EXISTS idx_transactions_card_id ON transactions(card_id);
CREATE INDEX IF NOT EXISTS idx_transactions_created_at ON transactions(created_at);
CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(type);
CREATE INDEX IF NOT EXISTS idx_transactions_account_date ON transactions(account_id, created_at);

-- Views for common queries
-- View: customer_summary
-- Provides a summary of customers with their account information
CREATE VIEW IF NOT EXISTS customer_summary AS
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

-- View: account_details
-- Provides detailed account information with customer data
CREATE VIEW IF NOT EXISTS account_details AS
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
