import json
import os

def load_json(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def save_json(filepath, data):
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

def get_unused_procedures(procedures, checklist_order):
    used_procedures = set()
    for section in checklist_order.values():
        for item in section['items']:
            if 'checklist_entry' in item:
                used_procedures.add(item['checklist_entry'])

    unused_procedures = [{"checklist_entry": procedure['checklist_entry']} for procedure in procedures if procedure['checklist_entry'] not in used_procedures]
    return unused_procedures

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    procedures_filepath = os.path.join(base_dir, 'data/json/procedures.json')
    checklist_order_filepath = os.path.join(base_dir, 'data/json/checklist_order.json')
    unused_procedures_filepath = os.path.join(base_dir, 'data/json/unused_procedures.json')

    procedures = load_json(procedures_filepath)
    checklist_order = load_json(checklist_order_filepath)

    unused_procedures = get_unused_procedures(procedures, checklist_order)

    save_json(unused_procedures_filepath, unused_procedures)
    print(f"Unused procedures have been saved to {unused_procedures_filepath}")

if __name__ == "__main__":
    main()