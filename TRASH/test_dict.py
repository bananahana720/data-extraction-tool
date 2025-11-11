import yaml
from pathlib import Path

dict_file = Path('config/normalize/entity_dictionary.yaml')
with open(dict_file) as f:
    data = yaml.safe_load(f)

abbrevs = [k for k in data.keys() if k != 'expansion_settings']
print(f'Dictionary loaded: {len(abbrevs)} abbreviations')

# Count by category
categories = {}
for k, v in data.items():
    if isinstance(v, dict) and 'category' in v:
        cat = v['category']
        categories[cat] = categories.get(cat, 0) + 1

print(f'Categories: {categories}')
print('Sample entries:')
for i, (k, v) in enumerate(data.items()):
    if i >= 5:
        break
    if isinstance(v, dict) and 'full_form' in v:
        print(f'  {k}: {v["full_form"]}')
