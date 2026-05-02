import psycopg2
from config import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            best_score INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            player_id INTEGER REFERENCES players(id),
            score INTEGER NOT NULL,
            level_reached INTEGER NOT NULL,
            played_at TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def sync_player(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING", (username,))
    cur.execute("SELECT best_score FROM players WHERE username = %s", (username,))
    res = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return res[0] if res else 0

def save_result(username, score, level):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, best_score FROM players WHERE username = %s", (username,))
    p_data = cur.fetchone()
    if p_data:
        p_id, old_best = p_data
        cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)", (p_id, score, level))
        if score > old_best:
            cur.execute("UPDATE players SET best_score = %s WHERE id = %s", (score, p_id))
    conn.commit()
    cur.close()
    conn.close()

def get_top_10():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.username, s.score, s.level_reached, TO_CHAR(s.played_at, 'DD-MM HH24:MI') 
        FROM game_sessions s JOIN players p ON s.player_id = p.id 
        ORDER BY s.score DESC LIMIT 10
    """)
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res