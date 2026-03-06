import re
import json

with open('C:/Users/acer/Documents/hefbvi/Practice 5/raw.txt', 'r', encoding='utf-8') as f:
    text = f.read()

products = re.findall(r'^\d+\.\n(.+)', text, re.MULTILINE)
price_lines = re.findall(r'Стоимость\n([\d\s]+,\d{2})', text)
prices = [float(p.replace(' ', '').replace(',', '.')) for p in price_lines]

total_search = re.search(r'ИТОГО:\n([\d\s]+,\d{2})', text)
total = float(total_search.group(1).replace(' ', '').replace(',', '.')) if total_search else 0.0

dt_search = re.search(r'Время: (\d{2}\.\d{2}\.\d{4}) (\d{2}:\d{2}:\d{2})', text)
date = dt_search.group(1) if dt_search else "None"
time = dt_search.group(2) if dt_search else "None"

payment = "Card" if "Банковская карта" in text else "Cash"

result = {
    "date": date,
    "time": time,
    "products": products,
    "total": total,
    "payment": payment
}

print(json.dumps(result, indent=4, ensure_ascii=False))
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=4, ensure_ascii=False)