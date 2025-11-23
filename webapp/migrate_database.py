#!/usr/bin/env python3
"""
Database Migration Script for Pantry Tracker Extended Features
Adds: Location table, min_stock, location_id, expiry_date, notes columns
"""

import sqlite3
import shutil
from datetime import datetime
import os

# Database path
DB_PATH = '/data/pantry_data.db'
BACKUP_PATH = f'/data/pantry_data_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'

def backup_database():
    """Create a backup of the current database"""
    print(f"📦 Creating backup: {BACKUP_PATH}")
    if os.path.exists(DB_PATH):
        shutil.copy2(DB_PATH, BACKUP_PATH)
        print("✅ Backup created successfully")
    else:
        print("⚠️  No existing database found, starting fresh")

def migrate_database():
    """Perform database migration"""
    print("\n🔄 Starting database migration...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if locations table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='locations'")
        if not cursor.fetchone():
            print("\n📍 Creating 'locations' table...")
            cursor.execute("""
                CREATE TABLE locations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(50) NOT NULL UNIQUE,
                    description VARCHAR(200)
                )
            """)
            print("✅ 'locations' table created")
            
            # Insert default location
            cursor.execute("INSERT INTO locations (name, description) VALUES (?, ?)", 
                         ('Pantry', 'Default storage location'))
            print("✅ Default location 'Pantry' added")
        else:
            print("ℹ️  'locations' table already exists")
        
        # Check and add columns to products table
        cursor.execute("PRAGMA table_info(products)")
        existing_columns = [column[1] for column in cursor.fetchall()]
        
        print("\n📦 Updating 'products' table...")
        
        # Add min_stock column
        if 'min_stock' not in existing_columns:
            cursor.execute("ALTER TABLE products ADD COLUMN min_stock INTEGER DEFAULT 5")
            print("✅ Added 'min_stock' column (default: 5)")
        else:
            print("ℹ️  'min_stock' column already exists")
        
        # Add location_id column
        if 'location_id' not in existing_columns:
            cursor.execute("ALTER TABLE products ADD COLUMN location_id INTEGER REFERENCES locations(id)")
            print("✅ Added 'location_id' column")
        else:
            print("ℹ️  'location_id' column already exists")
        
        # Add expiry_date column
        if 'expiry_date' not in existing_columns:
            cursor.execute("ALTER TABLE products ADD COLUMN expiry_date DATE")
            print("✅ Added 'expiry_date' column")
        else:
            print("ℹ️  'expiry_date' column already exists")
        
        # Add notes column
        if 'notes' not in existing_columns:
            cursor.execute("ALTER TABLE products ADD COLUMN notes TEXT")
            print("✅ Added 'notes' column")
        else:
            print("ℹ️  'notes' column already exists")
        
        # Commit changes
        conn.commit()
        print("\n✅ Migration completed successfully!")
        
        # Show summary
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM locations")
        location_count = cursor.fetchone()[0]
        
        print("\n📊 Database Summary:")
        print(f"   - Products: {product_count}")
        print(f"   - Locations: {location_count}")
        print(f"   - Backup saved at: {BACKUP_PATH}")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("  Pantry Tracker - Database Migration")
    print("=" * 60)
    
    # Create backup
    backup_database()
    
    # Perform migration
    migrate_database()
    
    print("\n" + "=" * 60)
    print("  Migration Complete! You can now restart the add-on.")
    print("=" * 60)
