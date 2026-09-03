import pypdf, os

path = "/run/media/khushnud/hdd/jp"

for foldN, subFold, files in os.walk(path):
    for file in files:
        if file.endswith('.pdf'):
            fullPath = os.path.join(foldN, file)
            
            reader = pypdf.PdfReader(fullPath)
            
            # shifrlangan bo'lsa parolni olib tashlaydi
            if reader.is_encrypted:
                reader.decrypt("unojapano.com")
                writer = pypdf.PdfWriter()

                for page in reader.pages:
                    writer.add_page(page)

                with open(fullPath, 'wb') as f:
                    writer.write(f)

                print(f"{file} — parol ochildi ✅")
            else:
                print(f"{file} — shifrlangan emas, o'tkazib yuborildi ⏭️")