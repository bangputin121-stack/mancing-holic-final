class Database:
    def __init__(self):
        # Ini adalah tempat simpan data sementara
        self.players = {}

    def get_player(self, user_id):
        return self.players.get(user_id)

    def register_player(self, user_id, username, full_name):
        if user_id not in self.players:
            self.players[user_id] = {
                'username': username,
                'full_name': full_name,
                'coins': 500,
                'level': 1,
                'total_fish': 0
            }
            return True
        return False
