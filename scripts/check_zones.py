import re

with open(r'C:\Users\nicko\Desktop\Proyectos\SISA-Ingeniería de Software 1\project-frontend\src\constants\mapZones.ts', 'r', encoding='utf-8') as f:
    content = f.read()

all_ids = re.findall(r"id: '([^']+)'", content)
print(f'Total IDs in file: {len(all_ids)}')

pattern = r"id: '([^']+)',\s*name: '([^']+)',\s*route: '([^']+)',\s*description: '([^']*)',\s*bounds: \{ south: ([0-9.\-]+), west: ([0-9.\-]+), north: ([0-9.\-]+), east: ([0-9.\-]+) \}"
matches = re.findall(pattern, content, re.DOTALL)
matched_ids = [m[0] for m in matches]
print(f'Matched by regex: {len(matched_ids)}')

missing = [zid for zid in all_ids if zid not in matched_ids]
print(f'Missing ({len(missing)}): {missing}')
