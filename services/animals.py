from core.db import query
from core.audit import log

def list_animals():
    return query("SELECT a.*, e.name AS enclosure_name FROM animals a LEFT JOIN enclosures e ON a.enclosure_id=e.id")

def create_animal(user_id, data):
    animal_id = None
    query("INSERT INTO animals (tag_id, name, species, sex, dob, enclosure_id, health_status, notes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
          (data["tag_id"], data["name"], data["species"], data["sex"], data.get("dob"), data.get("enclosure_id"), data.get("health_status","Healthy"), data.get("notes")))
    # fetch new id
    row = query("SELECT LAST_INSERT_ID() AS id", fetchone=True)
    animal_id = row["id"]
    log(user_id, "CREATE_ANIMAL", "animals", animal_id, f"Created {data['name']} ({data['species']})")
    return animal_id

def update_health(user_id, animal_id, status):
    query("UPDATE animals SET health_status=%s, last_checkup=CURDATE() WHERE id=%s", (status, animal_id))
    log(user_id, "UPDATE_HEALTH", "animals", animal_id, f"Health -> {status}")