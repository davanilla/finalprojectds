# finalprojectsds
# To-do saraksts ar atgādinājumiem
## Uzdevums:

Diezgan vienkārša ideja - izveidot konsoles aplikāciju, kas ļautu sekot līdzi izpildāmiem darbiem.    Izstrādāta programma ļauj pievienot, saglābāt un dzēst uzdevumus, kā arī apskatīties uzdevumu sarakstu un saņemt atgādinājumus par tiem (pēdējā opcija nestrādā GitHub codespaces, jāskatās citā vidē). Programma prasa lietotājam ievadīt datus terminalī, pārbaudot datus un ļaujot lietotājam izlabot kļūdas.

---

## Izmantotās Python Bibliotēkas

- `datetime`: Nodrošina darbu ar datumiem un laiku. Izmanto, lai salīdzinātu un pārbaudītu uzdevumu termiņus.
- `time`: Izmantots, lai realizētu laika pauzi atgādinājumu cilpā (`sleep(300)`).
- `json`: Nodrošina uzdevumu saraksta saglabāšanu un ielādi JSON formātā, kas ir viegli lasāms un pārnēsājams.
- `plyer` (notification funkcija): Izmanto sistēmas paziņojumu parādīšanai lietotājam, kad kāds uzdevums tuvojas termiņam.

---

## Izmantotās datu struktūras

Projektā ir paša veidota datu struktūra - klase "Task", kas parstāv katru atsevišķu uzdevumu. Katram Task objektam ir :

- `name` (str): uzdevuma nosaukums
- `deadline` (datetime): uzdevuma termiņš
- `priority` (int): prioritātes līmenis no 1 līdz 100

Papildus tai ir definētas metodes:

- `__lt__`: lai salīdzinātu uzdevumus pēc prioritātes un termiņa (min heap vajadzībām)
- `__eq__`: lai noteiktu, vai divi uzdevumi ir vienādi
- `__repr__`: uzdevuma formatēta izdruka

Uzdevumi tiek glabāti kā `list` saraksts.

Vēl projektā ir struktūra Min Heap, kas nodrošina prioritāro sakārtošanu.

Klase satur:

- **Datu glabāšana:** Uzdevumi tiek glabāti kā saraksts (`self.data`), kas apstrādāts kā min heap koks.
- **Metodes:**
  - `_heapify_up(idx)`: rūpējas, lai ievietotais elements paaugstinātos līdz pareizajai vietai, salīdzinot ar savu vecāku, lai saglabātu min heap īpašību.
  - `_heapify_down(idx)`: pēc elementa izņemšanas no saknes veic pazemināšanu lejā pa koku, lai arī turpmāk min heap īpašība būtu spēkā.
  - `push(task)`: pievieno jaunu uzdevumu un pēc tam sakārto heap.
  - `pop()`: noņem minimālo uzdevumu (sakni) un atjauno heap struktūru.

---

## Programmatūras izmantošanas metodes

Palaidžot programmu, lietotājam pavēras iespēja izvēlēties opciju no izvēlnes:

1. **Pievienot uzdevumu**  
   Lietotājs ievada nosaukumu, termiņu un prioritāti. Programma pārbauda ievades pareizību un nepieļauj pagātnes datumus vai ārpus intervāla esošas prioritātes.

2. **Uzdevumu saraksts**  
   Tiek izvadīts uzdevumu saraksts sakārtots pēc prioritātes un termiņa, izmantojot min-heap datu strukturu.

3. **Uzdevuma dzēšana**  
   Lietotājs var izvēlēties konkrētu uzdevumu pēc tā numura, lai to dzēstu.

4. **Atgādinājumu cilpa**  
   Programma ik pēc 5 minūtēm pārbauda, kuriem uzdevumiem termiņš ir tuvāk par vienu stundu, un nosūta sistēmas paziņojumu (ja `plyer` to atbalsta attiecīgajā operētājsistēmā).

5. **Notīrīt visus uzdevumus**  
   Dzēš visus uzdevumus no saraksta pēc lietotāja apstiprinājuma.

6. **Iziet no programmas**  
   Saglabā uzdevumus un pārtrauc programmas darbību.

---

## Īpašas sistēmas prasības

- vismaz Python 3.7
- `plyer` bibliotēka (`pip install plyer`)
- Atbalsts sistēmas paziņojumiem (strādā uz Windows, Linux, daļēji macOS, bet GitHub Codespaces gan ne)

---

## Autors 

Aleksandra Daņilova
St.apl.nr: 231RWB008