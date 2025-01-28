# Chip-Champs: Chips & Circuits
Chips met gelegde circuits komen in allerlei tochnologie voor en voeren verschillende functies uit, variërend van tijdwaarneming en motorbesturing tot rekenen en logica. Deze chips bestaan uit een kleine siliconen plaat met gates erop die met elkaar verbonden kunnen worden. Welke gates met elkaar verbonden moeten worden, staat in een netlist. Deze verbindingen moeten zo efficient mogelijk gelegd worden, wat betekent dat ze zo kort mogelijk moeten zijn, niet over elkaar heen kunnen lopen en elkaar zo min mogelijk moeten kruisen. Het leggen van deze connecties, waarbij rekening wordt gehouden met de genoemde restricties, is wat deze case zo moeilijk maakt. Hoe groter de chips, hoe meer gates, hoe meer connecties, en dus ook hoe moeilijker de case.

# Aan de slag
De code is volledig geschreven in Python 3.10.

Onze oplossinging voor het Chips & circuits probleem kan worden aangeroepen met:

```python main.py```

Door alleen de main aan te roepen zal er in de command terminal een aantal inputs gevraagd worden. Namelijk of je een oplossing wilt maken of een al gemaakte oplossing wilt inladen, het chip nummer, de netlist, het algoritme waarmee de connecties gemaakt moeten worden en of je de chip wilt plotten of niet.

Deze informatie kan ook al meegegeven worden in de command lijn met het format:
python main.py --solution (creating/loading) --chip_number (0,1,2) --netlist (1-9) --algorithm (alg name) --plot_chip (true/false)

Het algoritme zal dan een oude oplossing inladen of de connecties maken van de meegegeven chip en netlijst met het meegegeven algoritme. Het programma pakt zelf de beste heuristieken en penalties voor die chip en netlijst.

# Structuur
De hierop volgende lijst beschrijft de belangrijkste mappen en files in het project, en waar je ze kan vinden:
- **/algorithms**: bevat de bestande met de code voor de verschillende algoritmes en heuristieken.
- **/classes**: bevat de drie benodigde classes voor deze case (Chip, Gates, Connectios).
- **/data**: bevat de verschillende databestanden (de chips en hun netlijsten) waarop de algoritmes toegepast moeten worden.
- **/output**: bevat de verschillende outputs met verschillende heuristieken die gebruikt zijn.

# Auteurs:
- Merel Besseling
- Amy Koelman
- Kyra Paul
