import pandas as pd
import sqlite3

# Define file paths for datasets
fighter_csv_path = 'raw_fighter_details.csv'
fight_csv_path = 'raw_total_fight_data.csv'

# Load datasets into pandas DataFrames
fighter_df = pd.read_csv(fighter_csv_path)
fight_df = pd.read_csv(fight_csv_path, delimiter=';') 


# Crea o connettiti a un database SQLite
conn = sqlite3.connect('ufc.db')

# Crea le tabelle nel database, se non esistono
with conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS  Fighter (
            Name VARCHAR(255) PRIMARY KEY,
            Height VARCHAR(50), -- Altezza del lottatore, es. '5\'11"'
            Weight VARCHAR(50), -- Peso del lottatore, es. '155 lbs'
            Reach VARCHAR(50),  -- Portata del lottatore, es. '72"'
            Stance VARCHAR(50), -- Posizione di combattimento, es. 'Orthodox'
            DOB DATE           -- Data di nascita, formato 'YYYY-MM-DD'
        );
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS  Fight (
            ID VARCHAR(255) PRIMARY KEY,
            Date DATE NOT NULL,
            Location VARCHAR(255) NOT NULL,
            Format VARCHAR(100), -- Formato del combattimento, es. '3 Rnd (5-5-5)'
            Referee VARCHAR(255), -- Nome dell'arbitro
            Fight_type VARCHAR(100), -- Tipo di combattimento, es. 'Bantamweight Bout'
            R_fighter VARCHAR(255), -- Lottatore angolo rosso
            B_fighter VARCHAR(255), -- Lottatore angolo blu
            Winner VARCHAR(255), -- Vincitore del combattimento
            win_by VARCHAR(100), -- Metodo di vittoria, es. 'KO/TKO'
            last_round INT, -- Ultimo round combattuto
            last_round_time VARCHAR(10), -- Tempo di fine dell'ultimo round, es. '1:23'
            FOREIGN KEY (R_fighter) REFERENCES Fighter(Name),
            FOREIGN KEY (B_fighter) REFERENCES Fighter(Name),
            FOREIGN KEY (Winner) REFERENCES Fighter(Name)
        );
    ''')


    conn.execute('''
        CREATE TABLE IF NOT EXISTS  PerformanceMetrics (
            ID VARCHAR(255) PRIMARY KEY,
            Fight_ID VARCHAR(255) NOT NULL,
            Fighter_Name VARCHAR(255) NOT NULL,
            Color CHAR(1) CHECK (Color IN ('R', 'B')), -- 'R' per l'angolo rosso, 'B' per l'angolo blu
            KD INT, -- Knockdowns
            SIG_STR VARCHAR(100), -- Colpi significativi, es. '40 of 100'
            SIG_STR_pct FLOAT, -- Percentuale colpi significativi, es. 40.0
            TOTAL_STR VARCHAR(100), -- Totale colpi, es. '50 of 110'
            TD VARCHAR(100), -- Takedowns, es. '2 of 5'
            TD_pct FLOAT, -- Percentuale di successo dei takedowns, es. 40.0
            SUB_ATT INT, -- Tentativi di sottomissione
            REV INT, -- Rovesciamenti
            CTRL VARCHAR(100), -- Tempo di controllo, es. '3:00'
            FOREIGN KEY (Fight_ID) REFERENCES Fight(ID),
            FOREIGN KEY (Fighter_Name) REFERENCES Fighter(Name)
        );
    ''')

# Preprocess Fighter DataFrame
def preprocess_fighter_data(df):
    # Rename columns to match database schema and convert data as necessary
    df = df.rename(columns={
        'fighter_name': 'Name',
        'Height': 'Height',
        'Weight': 'Weight',
        'Reach': 'Reach',
        'Stance': 'Stance',
        'DOB': 'DOB'
    })
    # Additional data cleaning and conversion can be performed here
    return df

# Preprocess Fight DataFrame
def preprocess_fight_data(df):
    # Generate unique ID and rename columns to match the database schema
    df['ID'] = df['R_fighter'] + '_' + df['B_fighter'] + '_' + df['date']
    df = df.rename(columns={
        'date': 'Date',
        'location': 'Location',
        'Format': 'Format',
        'Referee': 'Referee',
        'Fight_type': 'Fight_type',
        'Winner': 'Winner',
        'win_by': 'win_by',
        'last_round': 'last_round',
        'last_round_time': 'last_round_time'
    })
    # Select and return only the necessary columns
    return df[['ID', 'Date', 'Location', 'Format', 'Referee', 'Fight_type', 'R_fighter', 'B_fighter', 'Winner', 'win_by', 'last_round', 'last_round_time']]

# Extract and preprocess Performance Metrics from Fight Data
def extract_performance_metrics(fight_df):
    metrics_list = []
    for index, row in fight_df.iterrows():
        for corner in ['R', 'B']:
            # Definizione di una funzione di aiuto per pulire e convertire le percentuali
            def clean_percentage(perc_str):
                if isinstance(perc_str, str) and perc_str.strip('%').replace('.', '', 1).isdigit():
                    return float(perc_str.strip('%')) / 100
                else:
                    return None
            
            # Utilizzo della funzione clean_percentage per gestire correttamente le colonne delle percentuali
            metrics_list.append({
                "ID": f"{row[corner + '_fighter']}-{row['date']}",
                "Fight_ID": row['ID'],
                "Fighter_Name": row[corner + '_fighter'],
                "Color": corner,
                "KD": row.get(f'{corner}_KD', 0),  # Assumendo che '---' possa essere interpretato come 0
                "SIG_STR": row.get(f'{corner}_SIG_STR.', '0 of 0'),
                "SIG_STR_pct": clean_percentage(row.get(f'{corner}_SIG_STR_pct', '0%')),
                "TOTAL_STR": row.get(f'{corner}_TOTAL_STR.', '0 of 0'),
                "TD": row.get(f'{corner}_TD', '0 of 0'),
                "TD_pct": clean_percentage(row.get(f'{corner}_TD_pct', '0%')),
                "SUB_ATT": row.get(f'{corner}_SUB_ATT', 0),
                "REV": row.get(f'{corner}_REV', 0),
                "CTRL": row.get(f'{corner}_CTRL', '0:00')  # Assumi una stringa predefinita se mancante
            })
    return pd.DataFrame(metrics_list)

preprocess_fighter_data(fighter_df).to_sql('Fighter', conn, if_exists='replace', index=False)
preprocess_fight_data(fight_df).to_sql('Fight', conn, if_exists='replace', index=False)
extract_performance_metrics(fight_df).to_sql('PerformanceMetrics', conn, if_exists='replace', index=False)
    
print("Data successfully loaded into the database.")

conn.close()