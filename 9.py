import re
from pathlib import Path

text1 = "I visited Kyiv, London and San in the summer. I also saw kyiv and LONDON and New-York."
pattern1 = re.compile(r'\b[A-Z][a-z]+\b')
matches1 = pattern1.findall(text1)
print("Task 1:", matches1)

text2 = "Orders: ORD-2010-00001, ORD-2023-12345, ORD-2009-99999, ORD-2026-00001"
pattern2 = re.compile(r'\bORD-((?:201[0-9]|202[0-5]))-(\d{5})\b')
matches2 = pattern2.findall(text2)
order_codes = ['ORD-'+y+'-'+d for y,d in matches2]
years = [int(y) for y,_ in matches2]
print("Task 2 codes:", order_codes)
print("Task 2 years:", years)

pattern3 = re.compile(r'\b(1[0-2]|0?[1-9]):([0-5][0-9])\s*([AaPp][Mm])\b')
def to_24h(h, m, suffix):
    h = int(h)
    m = int(m)
    suf = suffix.lower()
    if suf == 'am':
        if h == 12:
            h = 0
    else:
        if h != 12:
            h += 12
    return f"{h:02d}:{m:02d}"
text3 = "We meet at 9:05 am, or maybe at 12:00PM, or at 01:30 pm, or at 12:15 am."
pairs3 = []
for match in pattern3.finditer(text3):
    hh, mm, suf = match.groups()
    orig = match.group(0)
    norm = to_24h(hh, mm, suf)
    pairs3.append((orig, norm))
print("Task 3:")
for o,n in pairs3:
    print(f"{o} -> {n}")

text4 = """Check https://sub.domain.example.com/path?q=1 and http://example.org and https://example.com:8080/page and https://sub.domain.example.com/other."""
pattern4 = re.compile(r'https?://([^/\s]+)')
domains = set()
for m in pattern4.findall(text4):
    domain = m.split(':')[0]
    domains.add(domain)
print("Task 4:", sorted(domains))

email_re = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
name_re = re.compile(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b')
phone_re = re.compile(r'(\+?\d[\d\-\s().]{6,}\d)')
amount_re = re.compile(r'([€$]?\s*\d{1,3}(?:[ ,]\d{3})*(?:[.,]\d+)?|\d+(?:[.,]\d+)?)')

def normalize_phone(raw):
    digits = re.sub(r'\D', '', raw)
    if digits.startswith('380') and len(digits) == 12:
        core = digits[3:]
    elif digits.startswith('0') and len(digits) == 10:
        core = digits[1:]
    elif digits.startswith('+380') and len(digits) == 13:
        core = digits[4:]
    else:
        if len(digits) == 9:
            core = digits
        else:
            core = digits[-9:] if len(digits) >= 9 else digits
    if len(core) == 9:
        return f"+380 ({core[:2]}) {core[2:5]} {core[5:7]} {core[7:9]}"
    else:
        return '+' + digits if digits else raw

def parse_amount(raw):
    if not raw:
        return None
    s = raw.strip()
    s = re.sub(r'[^\d,.\-]', '', s)
    if s.count(',') == 1 and s.count('.') > 1:
        s = s.replace('.', '')
        s = s.replace(',', '.')
    if s.count(',') > 0 and s.count('.') == 1 and s.find('.') > s.find(','):
        s = s.replace(',', '')
    s = s.replace(' ', '')
    s = s.replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return None

def parse_clients(file_path):
    clients = []
    text = Path(file_path).read_text(encoding='utf-8')
    for line in text.splitlines():
        if not line.strip():
            continue
        name = None
        email = None
        phone = None
        amount = None
        e_match = email_re.search(line)
        if e_match:
            email = e_match.group(0)
        n_match = name_re.search(line)
        if n_match:
            name = n_match.group(1)
        p_match = phone_re.search(line)
        if p_match:
            phone_raw = p_match.group(0)
            phone = normalize_phone(phone_raw)
        a_matches = amount_re.findall(line)
        amount_val = None
        if a_matches:
            chosen = None
            for am in a_matches:
                if re.search(r'[€$]', am) or re.search(r'[.,]\d+', am):
                    chosen = am
                    break
            if not chosen:
                chosen = a_matches[-1]
            amount_val = parse_amount(chosen)
            amount = amount_val
        clients.append({
            'raw_line': line,
            'name': name,
            'email': email,
            'phone': phone,
            'amount': amount
        })
    return clients

if __name__ == "__main__":
    print("Task 5:")
    clients = parse_clients("clients.txt")
    for c in clients:
        print(c)
