class UserPreferenceRepository:
    def __init__(self, db_manager):
        self.conn = db_manager.connect()

    def save_preferences(self, prefs):
        self.conn.execute("""
            INSERT INTO user_preferences (user_name, preferred_temp_min, preferred_temp_max, max_precipitation,
                                          max_difficulty, max_length_km, preferred_terrain_types)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, prefs)
        self.conn.commit()

    def load_preferences(self, user_name='default'):
        cursor = self.conn.execute("""
            SELECT * FROM user_preferences WHERE user_name = ?
        """, (user_name,))
        return cursor.fetchone()
