import re

with open(r'C:\Users\nicko\Desktop\Proyectos\SISA-Ingeniería de Software 1\project-frontend\src\constants\mapZones.ts', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r"id: '([^']+)',\s*name: '([^']+)',\s*route: '([^']+)',\s*description: '([^']*)',\s*bounds: \{ south: ([0-9.\-]+), west: ([0-9.\-]+), north: ([0-9.\-]+), east: ([0-9.\-]+) \}"
matches = re.findall(pattern, content, re.DOTALL)

lines = []
lines.append('from django.db import migrations')
lines.append('')
lines.append('')
lines.append('def seed_zones(apps, schema_editor):')
lines.append('    Zone = apps.get_model("core", "Zone")')
lines.append('    zones = [')
for m in matches:
    zid, name, route, desc, south, west, north, east = m
    name_esc = name.replace("'", "\\'")
    desc_esc = desc.replace("'", "\\'")
    lines.append(f"        Zone(zone_id='{zid}', name='{name_esc}', route='{route}', description='{desc_esc}', bounds_south={south}, bounds_west={west}, bounds_north={north}, bounds_east={east}),")
lines.append('    ]')
lines.append('    Zone.objects.bulk_create(zones)')
lines.append('')
lines.append('')
lines.append('class Migration(migrations.Migration):')
lines.append('')
lines.append('    dependencies = [')
lines.append("        ('core', '0013_create_zone_table'),")
lines.append('    ]')
lines.append('')
lines.append('    operations = [')
lines.append('        migrations.RunPython(seed_zones, migrations.RunPython.noop),')
lines.append('    ]')

output = '\n'.join(lines)
outpath = r'C:\Users\nicko\Desktop\Proyectos\SISA-Ingeniería de Software 1\project-backend\src\core\migrations\0014_seed_zones.py'
with open(outpath, 'w', encoding='utf-8') as f:
    f.write(output)
print(f'Written {len(matches)} zones to {outpath}')
