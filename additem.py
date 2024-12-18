import csv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import Item, engine
# from model import Item, engine

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()

# Read the CSV file
with open('csv_file/IcomCSV.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Check if the item already exists in the database
        existing_item = session.query(Item).filter_by(code=row['CODE']).first()
        if not existing_item:
            # Create a new item
            new_item = Item(
                code=row['CODE'],
                item_name=row['Name'],
                qty=int(row['Qty']),
                unit=row['Unit'],
                category_id=None  # Set this to the appropriate category_id if needed
            )
            # Add the new item to the session
            session.add(new_item)

# Commit the session to save the new items to the database
session.commit()

# Close the session
session.close()
