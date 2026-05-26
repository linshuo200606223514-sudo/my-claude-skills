---
name: skill-stats
description: "显示每个skill的使用次数统计。Use when user wants to see skill usage stats, skill counts, how many times skills were used, 查看skill使用次数, skill统计."
---

Read `C:/Users/clown/.k-claw/skill-usage.json` and display a sorted usage table.

Run this command and show the output:

```bash
python3 -c "
import json, os
path = os.path.expanduser('~/.k-claw/skill-usage.json')
if not os.path.exists(path):
    print('No skill usage data yet.')
    exit()
with open(path, encoding='utf-8') as f:
    data = json.load(f)
skills = data.get('skills', {})
if not skills:
    print('No skills tracked yet.')
    exit()
sorted_skills = sorted(skills.items(), key=lambda x: x[1], reverse=True)
print(f'Skill Usage Stats  (updated: {data.get(\"updated\", \"unknown\")})')
print('-' * 50)
for name, count in sorted_skills:
    bar = '#' * min(count, 30)
    print(f'{name:<35} {count:>4}  {bar}')
print(f'\nTotal invocations: {sum(skills.values())}  |  Unique skills: {len(skills)}')
"
```
