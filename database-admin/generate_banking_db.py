#!/usr/bin/env python3
"""
Banking Database Generator

This script creates a SQLite database with random banking data based on the
banking schema documentation. Generates realistic customers, accounts, cards,
and transactions for testing and development purposes.

Created: April 14, 2026
"""

import sqlite3
import random
from datetime import datetime, timedelta, date
from faker import Faker
import os

# Initialize Faker with Swiss German locale for realistic CH addresses, names, phone numbers
fake = Faker('de_CH')

# Configuration
DB_NAME = "../content/data/banking_data.db"
NUM_CUSTOMERS = 100
NUM_ACCOUNTS_PER_CUSTOMER = (1, 3)  # Min, Max accounts per customer
NUM_CARDS_PER_ACCOUNT = (0, 2)     # Min, Max cards per account
NUM_TRANSACTIONS_PER_ACCOUNT = (5, 50)  # Min, Max transactions per account

# Enums and constants
ACCOUNT_TYPES = ['checking', 'savings', 'business']
ACCOUNT_STATUSES = ['active', 'closed', 'frozen']

CUSTOMER_STATUSES = ['active', 'inactive', 'suspended']

CARD_TYPES = ['debit', 'credit', 'prepaid']
CARD_STATUSES = ['active', 'blocked', 'expired']

TRANSACTION_TYPES = ['debit', 'credit', 'transfer', 'fee']

# Transaction templates: (kategorie, description_template, weight)
# {name} → fake.last_name(), {company} → fake.company(), {nr} → random account number
DEBIT_TEMPLATES = [
    # Lebensmittel
    ('Lebensmittel',            'Einkauf bei Migros',                           10),
    ('Lebensmittel',            'Einkauf bei Coop',                              9),
    ('Lebensmittel',            'Einkauf bei Denner',                            5),
    ('Lebensmittel',            'Einkauf bei Aldi Suisse',                       4),
    ('Lebensmittel',            'Einkauf bei Lidl Schweiz',                      4),
    ('Lebensmittel',            'Einkauf bei Manor Food',                        3),
    ('Lebensmittel',            'Einkauf bei Bäckerei {name}',                   6),
    ('Lebensmittel',            'Einkauf bei Metzgerei {name}',                  4),
    ('Lebensmittel',            'Kartenzahlung - Volg',                          3),
    # Restaurants & Gastronomie
    ('Restaurants & Gastronomie', 'Kartenzahlung - Restaurant {name}',           4),
    ('Restaurants & Gastronomie', 'Kartenzahlung - Pizzeria {name}',             3),
    ('Restaurants & Gastronomie', "Kartenzahlung - Café {name}",                 3),
    ('Restaurants & Gastronomie', "Kartenzahlung - McDonald's",                  2),
    ('Restaurants & Gastronomie', 'Kartenzahlung - Burger King',                 2),
    ('Restaurants & Gastronomie', 'Kartenzahlung - Zürich-Mövenpick',            2),
    # Gesundheit
    ('Gesundheit',              'Rechnungszahlung - Arztpraxis Dr. {name}',      3),
    ('Gesundheit',              'Rechnungszahlung - Zahnarztpraxis Dr. {name}',  2),
    ('Gesundheit',              'Rechnungszahlung - Apotheke {name}',            3),
    ('Gesundheit',              'Rechnungszahlung - Physiotherapie {name}',      2),
    ('Gesundheit',              'Online-Zahlung - Zur Rose Apotheke',            2),
    # Haus & Wohnen
    ('Haus & Wohnen',           'Rechnungszahlung - Schreinerei {name}',         2),
    ('Haus & Wohnen',           'Rechnungszahlung - Malerbetrieb {name}',        2),
    ('Haus & Wohnen',           'Rechnungszahlung - Sanitär {name}',             2),
    ('Haus & Wohnen',           'Rechnungszahlung - Elektriker {name}',          2),
    ('Haus & Wohnen',           'Rechnungszahlung - Dachdecker {name}',          1),
    ('Haus & Wohnen',           'Online-Zahlung - IKEA Schweiz',                 2),
    ('Haus & Wohnen',           'Online-Zahlung - Hornbach',                     2),
    ('Haus & Wohnen',           'Online-Zahlung - Jumbo',                        2),
    ('Haus & Wohnen',           'Kartenzahlung - Möbel Pfister',                 1),
    # Mobilität & Reisen
    ('Mobilität & Reisen',      'Einkauf bei Agrola Tankstelle',                 4),
    ('Mobilität & Reisen',      'Einkauf bei Eni Tankstelle',                    3),
    ('Mobilität & Reisen',      'Einkauf bei Migrol Tankstelle',                 3),
    ('Mobilität & Reisen',      'Online-Zahlung - SBB',                          4),
    ('Mobilität & Reisen',      'Kartenzahlung - SBB Automat',                   2),
    ('Mobilität & Reisen',      'Online-Zahlung - SWISS Air',                    2),
    ('Mobilität & Reisen',      'Online-Zahlung - Booking.com',                  2),
    ('Mobilität & Reisen',      'Kartenzahlung - Mobility Carsharing',           2),
    # Unterhaltung & Freizeit
    ('Unterhaltung & Freizeit', 'Online-Zahlung - Netflix',                      3),
    ('Unterhaltung & Freizeit', 'Online-Zahlung - Spotify',                      3),
    ('Unterhaltung & Freizeit', 'Online-Zahlung - Disney+',                      2),
    ('Unterhaltung & Freizeit', 'Online-Zahlung - Joyn',                         1),
    ('Unterhaltung & Freizeit', 'Kartenzahlung - Pathé Kino',                    2),
    ('Unterhaltung & Freizeit', 'Kartenzahlung - Fitnesscenter {name}',          2),
    ('Unterhaltung & Freizeit', 'Kartenzahlung - Hallenbad {name}',              1),
    # Telekommunikation
    ('Telekommunikation',       'Online-Zahlung - Swisscom',                     4),
    ('Telekommunikation',       'Online-Zahlung - Sunrise',                      3),
    ('Telekommunikation',       'Online-Zahlung - Salt Mobile',                  2),
    ('Telekommunikation',       'Online-Zahlung - UPC Schweiz',                  2),
    # Versicherung
    ('Versicherung',            'Lastschrift - Zürich Versicherung',             2),
    ('Versicherung',            'Lastschrift - Helvetia Versicherung',           2),
    ('Versicherung',            'Lastschrift - Baloise Versicherung',            2),
    ('Versicherung',            'Lastschrift - AXA Winterthur',                  2),
    ('Versicherung',            'Lastschrift - CSS Krankenkasse',                2),
    ('Versicherung',            'Lastschrift - Helsana',                         2),
    ('Versicherung',            'Lastschrift - Swica Krankenkasse',              2),
    # Online-Shopping
    ('Online-Shopping',         'Online-Zahlung - Digitec',                      5),
    ('Online-Shopping',         'Online-Zahlung - Galaxus',                      4),
    ('Online-Shopping',         'Online-Zahlung - Ricardo',                      3),
    ('Online-Shopping',         'Online-Zahlung - Amazon',                       3),
    ('Online-Shopping',         'Online-Zahlung - Zalando',                      2),
    ('Online-Shopping',         'Kartenzahlung - Fust Elektronik',               2),
    # ATM
    ('ATM',                     'Geldautomaten-Abhebung',                        6),
]
DEBIT_WEIGHTS = [t[2] for t in DEBIT_TEMPLATES]

CREDIT_TEMPLATES = [
    ('Gehalt & Einkommen',      'Gehaltseingang',                               40),
    ('Gehalt & Einkommen',      'Direkteinzahlung - {company}',                 15),
    ('Zinsen & Erträge',        'Zinsgutschrift',                               15),
    ('Rückerstattung',          'Rückerstattung',                               15),
    ('Eingehende Überweisung',  'Eingehende Überweisung von {name}',            15),
]
CREDIT_WEIGHTS = [t[2] for t in CREDIT_TEMPLATES]

FEE_TEMPLATES = [
    ('Gebühren', 'Monatliche Kontoführungsgebühr', 4),
    ('Gebühren', 'Geldautomatengebühr',            3),
    ('Gebühren', 'Überziehungsgebühr',             2),
    ('Gebühren', 'Überweisungsgebühr',             2),
]
FEE_WEIGHTS = [t[2] for t in FEE_TEMPLATES]


def _pick(templates, weights):
    """Pick a random template and fill placeholders using Faker."""
    category, tmpl, _ = random.choices(templates, weights=weights)[0]
    description = (tmpl
                   .replace('{name}', fake.last_name())
                   .replace('{company}', fake.company())
                   .replace('{nr}', str(random.randint(1000, 9999))))
    return category, description

# Date/DateTime conversion functions to handle Python 3.12 deprecation warnings
# SQLite's default date/datetime adapters are deprecated as of Python 3.12
# These functions provide explicit conversion to ISO format strings
def adapt_date(dt):
    """Convert date to ISO format string"""
    if isinstance(dt, date):
        return dt.isoformat()
    return dt

def adapt_datetime(dt):
    """Convert datetime to ISO format string"""
    if isinstance(dt, datetime):
        return dt.isoformat()
    return dt


class BankingDataGenerator:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

    def connect(self):
        """Connect to SQLite database"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # Register custom adapters to avoid deprecation warnings in Python 3.12
        sqlite3.register_adapter(date, adapt_date)
        sqlite3.register_adapter(datetime, adapt_datetime)

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """Create database tables based on banking schema from SQL file"""

        # Path to schema file
        schema_file = os.path.join(os.path.dirname(__file__), 'banking_schema.sql')

        try:
            # Read and execute schema from file
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema_sql = f.read()

            # Split SQL statements and execute them
            # SQLite executescript doesn't work well with complex statements, so we'll split manually
            statements = []
            current_statement = []

            for line in schema_sql.split('\n'):
                # Skip comments and empty lines for cleaner processing
                line = line.strip()
                if line.startswith('--') or not line:
                    continue

                current_statement.append(line)

                # End of statement (semicolon at end of line)
                if line.endswith(';'):
                    statement = ' '.join(current_statement).strip()
                    if statement:
                        statements.append(statement)
                    current_statement = []

            # Execute each statement
            for statement in statements:
                try:
                    self.cursor.execute(statement)
                except sqlite3.Error as e:
                    print(f"Warning: Error executing statement: {e}")
                    print(f"Statement: {statement[:100]}...")

            self.conn.commit()
            print("✅ Database tables created successfully from schema file")
            print(f"📄 Schema loaded from: {os.path.relpath(schema_file)}")

        except FileNotFoundError:
            print(f"❌ Schema file not found: {schema_file}")
            print("Please ensure the schema file exists. Exiting...")
            raise
        except Exception as e:
            print(f"❌ Error reading schema file: {e}")
            print("Please check the schema file format. Exiting...")
            raise

    def generate_card_number(self):
        """Generate a realistic (but fake) credit card number"""
        # Use common prefixes: 4 (Visa), 5 (MasterCard), 3 (Amex)
        prefixes = ['4532', '5432', '3782']
        prefix = random.choice(prefixes)

        # Generate remaining digits
        remaining_digits = 16 - len(prefix) if prefix.startswith('4') or prefix.startswith('5') else 15 - len(prefix)
        number = prefix + ''.join([str(random.randint(0, 9)) for _ in range(remaining_digits - 4)])

        # Format with dashes for readability
        if len(number) == 16:
            return f"{number[:4]}-{number[4:8]}-{number[8:12]}-{number[12:]}"
        else:
            return f"{number[:4]}-{number[4:10]}-{number[10:]}"

    def generate_customers(self):
        """Generate random customer data"""
        customers = []

        for i in range(NUM_CUSTOMERS):
            # Generate realistic customer data
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}"
            phone = fake.phone_number()
            address = fake.address().replace('\n', ', ')

            # Generate date of birth (18-80 years old)
            today = date.today()
            birth_year = today.year - random.randint(18, 80)
            date_of_birth = fake.date_between(
                start_date=date(birth_year, 1, 1),
                end_date=date(birth_year, 12, 31)
            )

            # Random account creation date (last 5 years)
            created_at = fake.date_time_between(
                start_date=datetime.now() - timedelta(days=1825),
                end_date=datetime.now()
            )

            status = random.choices(
                CUSTOMER_STATUSES,
                weights=[85, 10, 5]  # Most customers are active
            )[0]

            customer = (
                first_name, last_name, email, phone, address,
                adapt_date(date_of_birth), adapt_datetime(created_at), status
            )
            customers.append(customer)

        # Insert customers
        self.cursor.executemany('''
        INSERT INTO customers (first_name, last_name, email, phone, address, 
                              date_of_birth, created_at, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', customers)

        self.conn.commit()
        print(f"✅ Generated {NUM_CUSTOMERS} customers")

    def generate_accounts(self):
        """Generate accounts for all customers"""
        # Get all customers
        self.cursor.execute("SELECT customer_id, created_at FROM customers")
        customers = self.cursor.fetchall()

        accounts = []
        for customer_id, customer_created_at in customers:
            # Random number of accounts per customer
            num_accounts = random.randint(*NUM_ACCOUNTS_PER_CUSTOMER)

            for _ in range(num_accounts):
                account_type = random.choice(ACCOUNT_TYPES)

                # All accounts start at zero; balance builds up from transactions
                balance = 0.00

                # Account created after customer
                customer_created = datetime.fromisoformat(customer_created_at.replace('Z', '+00:00'))
                account_created = fake.date_time_between(
                    start_date=customer_created,
                    end_date=datetime.now()
                )

                status = random.choices(
                    ACCOUNT_STATUSES,
                    weights=[90, 7, 3]  # Most accounts are active
                )[0]

                account = (customer_id, account_type, balance, adapt_datetime(account_created), status)
                accounts.append(account)

        # Insert accounts
        self.cursor.executemany('''
        INSERT INTO accounts (customer_id, account_type, balance, created_at, status)
        VALUES (?, ?, ?, ?, ?)
        ''', accounts)

        self.conn.commit()
        print(f"✅ Generated {len(accounts)} accounts")

    def generate_cards(self):
        """Generate cards for accounts"""
        # Get all active accounts
        self.cursor.execute("SELECT account_id, created_at FROM accounts WHERE status = 'active'")
        accounts = self.cursor.fetchall()

        cards = []
        used_card_numbers = set()

        for account_id, account_created_at in accounts:
            # Random number of cards per account
            num_cards = random.randint(*NUM_CARDS_PER_ACCOUNT)

            for _ in range(num_cards):
                # Generate unique card number
                while True:
                    card_number = self.generate_card_number()
                    if card_number not in used_card_numbers:
                        used_card_numbers.add(card_number)
                        break

                card_type = random.choice(CARD_TYPES)

                # Card created after account
                account_created = datetime.fromisoformat(account_created_at.replace('Z', '+00:00'))
                card_created = fake.date_time_between(
                    start_date=account_created,
                    end_date=datetime.now()
                )

                # Expiry date 2-5 years from creation
                expiry_date = card_created.date() + timedelta(days=random.randint(730, 1825))

                # Status based on expiry date
                if expiry_date < date.today():
                    status = 'expired'
                else:
                    status = random.choices(
                        ['active', 'blocked'],
                        weights=[95, 5]
                    )[0]

                card = (account_id, card_number, card_type, adapt_date(expiry_date), status, adapt_datetime(card_created))
                cards.append(card)

        # Insert cards
        self.cursor.executemany('''
        INSERT INTO cards (account_id, card_number, card_type, expiry_date, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', cards)

        self.conn.commit()
        print(f"✅ Generated {len(cards)} cards")

    def generate_transactions(self):
        """Generate transactions for accounts"""
        # Get all accounts with their current balances
        self.cursor.execute("""
        SELECT account_id, balance, created_at 
        FROM accounts 
        WHERE status IN ('active', 'frozen')
        """)
        accounts = self.cursor.fetchall()

        # Get all active cards
        self.cursor.execute("SELECT card_id, account_id FROM cards WHERE status = 'active'")
        cards_by_account = {}
        for card_id, account_id in self.cursor.fetchall():
            if account_id not in cards_by_account:
                cards_by_account[account_id] = []
            cards_by_account[account_id].append(card_id)

        # Track the final computed balance per account to update accounts table later
        final_balances = {}

        transactions = []
        for account_id, initial_balance, account_created_at in accounts:
            num_transactions = random.randint(*NUM_TRANSACTIONS_PER_ACCOUNT)
            current_balance = float(initial_balance)

            # Generate transactions chronologically
            account_created = datetime.fromisoformat(account_created_at.replace('Z', '+00:00'))

            for i in range(num_transactions):
                # First transaction gets the earliest possible timestamp so it
                # stays first after the global chronological sort.
                # Subsequent transactions are spread randomly across the account's lifetime.
                if i == 0:
                    transaction_time = account_created + timedelta(hours=1)
                else:
                    transaction_time = fake.date_time_between(
                        start_date=account_created + timedelta(hours=2),
                        end_date=datetime.now()
                    )

                # First transaction must be incoming so the account starts with funds
                if i == 0:
                    transaction_type = random.choice(['credit', 'transfer'])
                else:
                    transaction_type = random.choices(
                        TRANSACTION_TYPES,
                        weights=[40, 35, 20, 5]  # debit, credit, transfer, fee
                    )[0]

                if transaction_type == 'debit':
                    if current_balance <= 0:
                        continue  # skip debit if account is empty
                    category, description = _pick(DEBIT_TEMPLATES, DEBIT_WEIGHTS)
                    amount = -round(random.uniform(5, min(current_balance * 0.8, 1000)), 2)
                    new_balance = current_balance + amount

                elif transaction_type == 'credit':
                    category, description = _pick(CREDIT_TEMPLATES, CREDIT_WEIGHTS)
                    amount = round(random.uniform(50, 5000), 2)
                    new_balance = current_balance + amount

                elif transaction_type == 'transfer':
                    outgoing = random.choice([True, False]) and current_balance >= 10 and i > 0
                    if outgoing:
                        category = 'Überweisung'
                        description = f'Überweisung an Konto {random.randint(1000, 9999)}'
                        amount = -round(random.uniform(10, min(max(current_balance * 0.5, 10), 2000)), 2)
                    else:
                        category = 'Eingehende Überweisung'
                        description = f'Überweisung von Konto {random.randint(1000, 9999)}'
                        amount = round(random.uniform(10, 2000), 2)
                    new_balance = current_balance + amount

                else:  # fee
                    category, description = _pick(FEE_TEMPLATES, FEE_WEIGHTS)
                    amount = -round(random.uniform(5, 50), 2)
                    new_balance = current_balance + amount

                # Never allow the balance to go negative
                if new_balance < 0:
                    continue

                current_balance = new_balance

                # Randomly assign card for debit transactions if cards exist
                card_id = None
                if transaction_type == 'debit' and account_id in cards_by_account:
                    if random.random() < 0.7:  # 70% chance to use card for debit
                        card_id = random.choice(cards_by_account[account_id])

                transaction = (
                    account_id, card_id, amount, transaction_type,
                    category, description, adapt_datetime(transaction_time)
                )
                transactions.append(transaction)

            # Record the final balance for this account
            final_balances[account_id] = current_balance

        # Sort transactions by timestamp to maintain chronological order
        transactions.sort(key=lambda x: x[5])  # Sort by created_at

        # Insert transactions
        self.cursor.executemany('''
        INSERT INTO transactions (account_id, card_id, amount, type, category, description, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', transactions)

        # Update account balances using the tracked final balance per account
        self.cursor.executemany(
            "UPDATE accounts SET balance = ? WHERE account_id = ?",
            [(balance, account_id) for account_id, balance in final_balances.items()]
        )

        self.conn.commit()
        print(f"✅ Generated {len(transactions)} transactions")

    def create_views(self):
        """Create useful views for querying the data"""

        # Views are now included in the schema file and created automatically
        # This method is kept for backward compatibility and potential custom views

        # Check if views were created from schema file
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
        views = [row[0] for row in self.cursor.fetchall()]

        if 'customer_summary' in views and 'account_details' in views:
            print("✅ Database views loaded from schema file")
        else:
            # Fallback: create views manually if not found in schema
            print("⚠️  Views not found in schema, creating manually...")

            # Customer summary view
            self.cursor.execute('''
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
<            LEFT JOIN accounts a ON c.customer_id = a.customer_id AND a.status = 'active'
            GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.phone, c.status, c.created_at
            ''')

            # Account details view
            self.cursor.execute('''
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
                     c.customer_id, c.first_name, c.last_name, c.email
            ''')

            self.conn.commit()
            print("✅ Created database views (manual fallback)")

    def print_statistics(self):
        """Print database statistics"""
        print("\n📊 Database Statistics:")
        print("=" * 50)

        # Customer statistics
        self.cursor.execute("SELECT COUNT(*), status FROM customers GROUP BY status")
        customer_stats = self.cursor.fetchall()
        print("Customers by status:")
        for count, status in customer_stats:
            print(f"  - {status}: {count}")

        # Account statistics
        self.cursor.execute("SELECT COUNT(*), account_type FROM accounts GROUP BY account_type")
        account_stats = self.cursor.fetchall()
        print("\nAccounts by type:")
        for count, account_type in account_stats:
            print(f"  - {account_type}: {count}")

        # Transaction statistics
        self.cursor.execute("SELECT COUNT(*), type FROM transactions GROUP BY type")
        transaction_stats = self.cursor.fetchall()
        print("\nTransactions by type:")
        for count, trans_type in transaction_stats:
            print(f"  - {trans_type}: {count}")

        # Total values
        self.cursor.execute("SELECT SUM(balance) FROM accounts WHERE status = 'active'")
        total_balance = self.cursor.fetchone()[0] or 0

        self.cursor.execute("SELECT COUNT(*) FROM cards WHERE status = 'active'")
        active_cards = self.cursor.fetchone()[0]

        print(f"\nTotal active account balance: ${total_balance:,.2f}")
        print(f"Active cards: {active_cards}")

    def generate_all_data(self):
        """Generate all banking data"""
        print("🏦 Starting banking database generation...")
        print(f"Target: {NUM_CUSTOMERS} customers")
        print("=" * 50)

        try:
            self.connect()
            self.create_tables()
            self.generate_customers()
            self.generate_accounts()
            self.generate_cards()
            self.generate_transactions()
            self.create_views()
            self.print_statistics()

            print(f"\n🎉 Database generated successfully!")
            print(f"📁 Location: {os.path.abspath(self.db_path)}")

        except Exception as e:
            print(f"❌ Error generating database: {e}")
            raise
        finally:
            self.close()

def main():
    """Main function to generate the banking database"""
    generator = BankingDataGenerator(DB_NAME)
    generator.generate_all_data()


if __name__ == "__main__":
    main()
