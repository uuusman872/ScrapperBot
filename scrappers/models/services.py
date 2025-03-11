

def get_person(tx):
    res = tx.run("MATCH (person:Person) RETURN person.name AS name LIMIT 5")
    for record in res:
        print("[+] Name:", record["name"])