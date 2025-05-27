import os
import subprocess

DB_FILE = "hotel.db"
ER_OUTPUT_FILE = "schema.er"

def generate_er_diagram(db_path=DB_FILE, er_file=ER_OUTPUT_FILE):
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"{db_path} does not exist. Run your setup_database script first.")

    subprocess.run(["eralchemy", "-i", f"sqlite:///{db_path}", "-o", er_file], check=True)
    print(f"ER file generated: {er_file}")

if __name__ == "__main__":
    generate_er_diagram()
