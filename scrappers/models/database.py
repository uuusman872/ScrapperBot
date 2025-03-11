from neo4j import GraphDatabase

class Neo4jHandler:
    def __init__(self):
        uri = "bolt://localhost:7687"
        user = "neo4j"
        password = "root12345678"
        self.database = "test"
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.verify_connection()

    def verify_connection(self):
        try:
            self.driver.verify_connectivity()
            print(f"[+] Connected to Neo4j database: {self.database}")
        except Exception as e:
            print("[-] Connection Failed:", e)

    def close(self):
        self.driver.close()
        print("[+] Connection closed!")

    def create_person(self, profile_name, profile_image, profile_username, profile_url):
        with self.driver.session(database=self.database) as session:
            session.write_transaction(self._insert_person, profile_name, profile_image, profile_username, profile_url)

    @staticmethod
    def _insert_person(tx, profile_name, profile_image, profile_username, profile_url):
        query = """
        CREATE (p:Profile {
            profile_name: $profile_name, 
            profile_image: $profile_image, 
            profile_username: $profile_username, 
            profile_url: $profile_url
        })
        RETURN p
        """
        tx.run(query, profile_name=profile_name, profile_image=profile_image, profile_username=profile_username, profile_url=profile_url)

    def create_friends(self, profile_username, name, profile_link, username):
        with self.driver.session(database=self.database) as session:
            session.write_transaction(self._insert_friends, profile_username, name, profile_link, username)

    @staticmethod
    def _insert_friends(tx, profile_username, name, profile_link, username):
        query = """
            MATCH (p:Profile {profile_username: $profile_username})
            MERGE (f:Friends {username: $username})
            SET f.name = $name, f.profile_link = $profile_link
            MERGE (p)-[:FRIENDS_WITH]->(f)
            RETURN p, f
        """
        tx.run(query, profile_username=profile_username, name=name, profile_link=profile_link, username=username)
