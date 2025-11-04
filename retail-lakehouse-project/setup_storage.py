"""
Setup Medallion Architecture Storage Structure
Creates Bronze, Silver, and Gold layer directories with subdirectories
"""

import os
from pathlib import Path


def setup_medallion_structure():
    """
    Set up medallion architecture directory structure
    """
    base_path = Path("data")
    
    # Define layers and their subdirectories
    layers = {
        "bronze": ["pos", "crm", "inventory", "marketing"],
        "silver": ["customers", "transactions", "products"],
        "gold": ["customer_spending", "sales_summary", "inventory_metrics"]
    }
    
    print("🏗️  Setting up Medallion Architecture storage structure...")
    print(f"Base path: {base_path.absolute()}\n")
    
    # Create directories for each layer
    for layer, subdirs in layers.items():
        for subdir in subdirs:
            path = base_path / layer / subdir
            path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created: {path}")
    
    # Create checkpoint directory for streaming
    checkpoint_path = base_path / "checkpoints"
    checkpoint_path.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created: {checkpoint_path}")
    
    # Create raw_data directory for source files
    raw_data_path = Path("raw_data")
    raw_data_path.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created: {raw_data_path}")
    
    print("\n✅ Medallion architecture structure created successfully!")
    print("\nDirectory structure:")
    print("data/")
    print("├── bronze/")
    print("│   ├── pos/")
    print("│   ├── crm/")
    print("│   ├── inventory/")
    print("│   └── marketing/")
    print("├── silver/")
    print("│   ├── customers/")
    print("│   ├── transactions/")
    print("│   └── products/")
    print("├── gold/")
    print("│   ├── customer_spending/")
    print("│   ├── sales_summary/")
    print("│   └── inventory_metrics/")
    print("└── checkpoints/")
    print("\nraw_data/  (for source CSV files)")


if __name__ == "__main__":
    setup_medallion_structure()
