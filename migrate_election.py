import sqlite3


# ----------------------------------
# Database location
# ----------------------------------

DATABASE_PATH = "database/voting_system.db"


# ----------------------------------
# Connect to database
# ----------------------------------

connection = sqlite3.connect(
    DATABASE_PATH
)

cursor = connection.cursor()


# ----------------------------------
# Check whether column already exists
# ----------------------------------

cursor.execute(
    "PRAGMA table_info(election)"
)

columns = [
    column[1]
    for column in cursor.fetchall()
]


# ----------------------------------
# Add election_type column
# ----------------------------------

if "election_type" not in columns:

    cursor.execute(
        """
        ALTER TABLE election
        ADD COLUMN election_type
        VARCHAR(20)
        NOT NULL
        DEFAULT 'single'
        """
    )

    print(
        "Election type column added successfully."
    )

else:

    print(
        "Election type column already exists."
    )


# ----------------------------------
# Save changes
# ----------------------------------

connection.commit()


# ----------------------------------
# Close database
# ----------------------------------

connection.close()


print(
    "Database migration completed successfully."
)