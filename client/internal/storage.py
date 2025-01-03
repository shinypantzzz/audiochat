import tinydb

class Storage:
    def __init__(self, db_path: str):
        self.db = tinydb.TinyDB(db_path)
        self.user = self.db.table('user')
        self.servers = self.db.table('servers')

    def get_most_recent_server(self):
        if len(self.servers) > 0:
            return sorted(self.servers.all(), key=lambda server: server["connection_datetime"])[-1]
        
        return None
    
    def get_most_recent_room(self, server_url: str):
        server = self.servers.get(tinydb.where("url") == server_url)

        if not server:
            return None
        
        if "rooms" not in server or len(server["rooms"]) == 0:
            return None
        
        return sorted(server["rooms"], key=lambda room: room["connection_datetime"], reverse=True)[0]["name"]
    
    def add_server(self, server_data):
        if self.servers.count(tinydb.where("url") == server_data["url"]) > 0:
            return
        
        self.servers.insert(server_data)

    