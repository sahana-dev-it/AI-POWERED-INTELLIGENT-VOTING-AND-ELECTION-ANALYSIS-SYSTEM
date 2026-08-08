import sqlite3


# ----------------------------------
# Connect to the actual database
# ----------------------------------

connection = sqlite3.connect(
    "database/voting_system.db"
)


# ----------------------------------
# Create cursor
# ----------------------------------

cursor = connection.cursor()


# ----------------------------------
# Add position column
# ----------------------------------

try:

    cursor.execute(
        """
        ALTER TABLE candidate
        ADD COLUMN position VARCHAR(100)
        """
    )

    print(
        "Candidate position column added successfully."
    )

except sqlite3.OperationalError as error:

    if "duplicate column name" in str(error).lower():

        print(
            "Position column already exists."
        )

    else:

        print(
            "Migration error:",
            error
        )


# ----------------------------------
# Save changes
# ----------------------------------

connection.commit()


# ----------------------------------
# Close database connection
# ----------------------------------

connection.close()


print(
    "Candidate database migration completed successfully."
)