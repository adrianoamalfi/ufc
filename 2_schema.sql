-- Creazione della tabella Fighter
CREATE TABLE Fighter (
    Name VARCHAR(255) PRIMARY KEY,
    Height VARCHAR(50), -- Altezza del lottatore, es. '5\'11"'
    Weight VARCHAR(50), -- Peso del lottatore, es. '155 lbs'
    Reach VARCHAR(50),  -- Portata del lottatore, es. '72"'
    Stance VARCHAR(50), -- Posizione di combattimento, es. 'Orthodox'
    DOB DATE           -- Data di nascita, formato 'YYYY-MM-DD'
);

-- Creazione della tabella Fight
CREATE TABLE Fight (
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

-- Creazione della tabella PerformanceMetrics
CREATE TABLE PerformanceMetrics (
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
