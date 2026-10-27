Warehouse Management System
A robust, object-oriented console application in Python designed for managing warehouse inventory, tracking product movements, and maintaining transaction logs.

Features:
Product Management: Add new products with unique identifiers (UUIDs) and edit existing items.
Inventory Control: Handle incoming shipments and outgoing write-offs with strict validation (preventing stock from dropping below zero).
Search and Filter: Find products by title, ID, or category.
Sorting: Sort items by price, title, or quantity.
Reporting: Generate overall stock valuation reports and low-stock alerts.
Persistent Storage: Data is automatically saved and loaded using JSON files (data.json and info_log.jsonl for audit trails).
Robust Error Handling: Custom exceptions and comprehensive input validation to ensure stability against invalid data or negative values.
Clean Architecture: Strictly separated business logic (classes Warehouse, Product, WarehouseJournal) from the console interface.

Tech Stack:
Language: Python 3.12+
Data Format: JSON / JSON Lines (.jsonl)
Version Control: Git and GitHub
