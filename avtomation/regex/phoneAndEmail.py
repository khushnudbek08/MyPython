import re

def phone_email(file):
    phone = re.compile(r'\d{12}')
    emile = re.compile(r'[\w.]+@gmail\.com', (re.DOTALL|re.IGNORECASE))
    with open(file, 'r') as f:
        matn = f.read()

    found_ph = phone.findall(matn)
    found_em = emile.findall(matn)


        
    return found_ph, found_em


telefonlar, emaillar = phone_email('text.txt')
print("Telefonlar:", telefonlar)
print("Emaillar:", emaillar)