import pandas as pd
import sqlite3

# Establish a connection to the database
conn = sqlite3.connect('ufc.db')  # Make sure 'ufc.db' is the path to your database

# Function to run a query and print results
def run_query(query, description):
    print(description)  # Print what this query is about
    result = pd.read_sql_query(query, conn)  # Execute the SQL query
    print(result)  # Print the result of the query
    print("\n")  # Print a new line for better readability

# Main function where the program starts
def main():
    while True:
        print("Choose an option:")
        print("1. Show top 10 fighters with the most fights")
        print("2. Show average significant strike percentages by corner color")
        print("3. Show top 10 fighters with the most wins")
        print("4. Show top 10 fight types by average last round duration")
        print("5. Exit")

        # Ask the user to choose an option
        choice = input("Enter your choice (1-5): ")

        # Check the user's choice and run the corresponding query
        if choice == '1':
            run_query("""
                SELECT Fighter_Name, COUNT(*) AS Total_Fights
                FROM (
                    SELECT R_fighter AS Fighter_Name FROM Fight
                    UNION ALL
                    SELECT B_fighter AS Fighter_Name FROM Fight
                ) AS All_Fights
                GROUP BY Fighter_Name
                ORDER BY Total_Fights DESC
                LIMIT 10;
            """, "Top 10 fighters with the most fights:")
            
        elif choice == '2':
            run_query("""
                SELECT Color, AVG(SIG_STR_pct) AS Avg_SIG_STR_pct
                FROM PerformanceMetrics
                GROUP BY Color;
            """, "Average significant strike percentages by corner color:")
            
        elif choice == '3':
            run_query("""
                SELECT Winner AS Fighter_Name, COUNT(*) AS Total_Wins
                FROM Fight
                WHERE Winner IS NOT NULL
                GROUP BY Winner
                ORDER BY Total_Wins DESC
                LIMIT 10;
            """, "Top 10 fighters with the most wins:")
            
        elif choice == '4':
            run_query("""
                SELECT Fight_type, AVG(CAST(last_round_time AS FLOAT)) AS Avg_Last_Round_Duration
                FROM Fight
                GROUP BY Fight_type
                ORDER BY Avg_Last_Round_Duration DESC
                LIMIT 10;
            """, "Top 10 fight types by average last round duration:")
            
        elif choice == '5':
            print("Exiting program.")
            break  # Exit the loop, which ends the program
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

# Run the main function
if __name__ == "__main__":
    main()