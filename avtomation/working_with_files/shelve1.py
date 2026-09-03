import shelve

shelfFile = shelve.open('mydata')
cats=['Zophie', 'Pooka', 'Simon']
shelfFile['cats'] = cats
shelfFile.close()

"""shelve moduli orqliy saqlangan filelar faqatgina qaytadan python orqaliygina o'qish mumkun bo'ladi.
 agar filelarni inson o'qiy oladigon shakilda saqlamoqchi bo'lsak uni txt kengaytmasi orqaliy saqlagan afzal bo'ladi."""