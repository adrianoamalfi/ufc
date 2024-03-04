# UFC Database Application

## Project Overview
This Python application allows users to interact with a UFC (Ultimate Fighting Championship) database. Users can load raw fight data into a SQLite database and execute predefined SQL queries to analyze fighter statistics and match outcomes.

## Features
- Load data from CSV files into a SQLite database.
- Execute predefined SQL queries for data analysis.
- User-friendly interface for running queries and viewing results.

## Prerequisites
- Python 3.x
- pandas library
- sqlite3 library

Ensure you have Python installed on your system. You can install the required Python libraries using pip:

```bash
pip install pandas sqlite3
```

## Installation
Clone the repository to your local machine:

```bash
git clone https://github.com/adrianoamalfi/ufc.git
cd ufc
```

## Usage
1. Place your `raw_fighter_details.csv` and `raw_total_fight_data.csv` files in the same directory as the script.
2. Load data:

```bash
python 4_load_data.py
```

3. Run the application:

```bash
python 5_query_interface.py
```

3. Follow the on-screen instructions to interact with the database and execute queries.

## Available Queries
1. Show the top 10 fighters with the most fights.
2. Show average significant strike percentages by corner color.
3. Show the top 10 fighters with the most wins.
4. Show the top 10 fight types by average last round duration.

## Entity-Relationship Diagram (ERD)
The ERD illustrates the database schema and the relationships between tables.

### Mermaid Format
To view the ERD in Mermaid format, check the `ERD.mermaid` file in this repository.

```mermaid
erDiagram
    Fighter {
        string Name PK "Primary Key"
        string Height "Nullable, in format ft'in''"
        string Weight "Nullable, in lbs"
        string Reach "Nullable, in inches"
        string Stance "Nullable, can be Orthodox, Southpaw, etc."
        date DOB "Nullable, Date of Birth"
    }

    Fight {
        string ID PK "Primary Key, Composite of fighters' names and date"
        date Date "Date when the fight took place"
        string Location "Location where the fight took place"
        string Format "Format of the fight, e.g., number of rounds"
        string Referee "Name of the referee"
        string Fight_type "Type of the fight, e.g., weight class"
        string Winner "Name of the winner"
        string win_by "Method of victory"
        int last_round "The last round of the fight"
        string last_round_time "Time when the last round ended"
    }

    PerformanceMetrics {
        string ID PK "Primary Key, Composite of Fight ID and fighter"
        int R_KD "Red corner Knockdowns"
        int B_KD "Blue corner Knockdowns"
        string R_SIG_STR "Red corner Significant Strikes"
        string B_SIG_STR "Blue corner Significant Strikes"
        string R_SIG_STR_pct "Red corner Significant Strikes Percentage"
        string B_SIG_STR_pct "Blue corner Significant Strikes Percentage"
        string R_TOTAL_STR "Red corner Total Strikes"
        string B_TOTAL_STR "Blue corner Total Strikes"
        string R_TD "Red corner Takedowns"
        string B_TD "Blue corner Takedowns"
        string R_TD_pct "Red corner Takedown Percentage"
        string B_TD_pct "Blue corner Takedown Percentage"
        int R_SUB_ATT "Red corner Submission Attempts"
        int B_SUB_ATT "Blue corner Submission Attempts"
        int R_REV "Red corner Reversals"
        int B_REV "Blue corner Reversals"
        string R_CTRL "Red corner Control Time"
        string B_CTRL "Blue corner Control Time"
    }

    Fighter ||--o{ Fight : "participates_in"
    Fight ||--|| PerformanceMetrics : "is_recorded_in"
    PerformanceMetrics }|--|| Fighter : "is_attributed_to"

```

### PNG Format
[ERD PNG](ERD.png)

## Contributing
Contributions to the UFC Database Application are welcome! Please ensure that your pull requests provide a clear description of what they add or fix.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Acknowledgements
This project was inspired by the rich dataset provided by the UFC and aims to provide meaningful insights into fight statistics and outcomes.