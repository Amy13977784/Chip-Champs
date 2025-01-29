# Chip-Champs: Chips & Circuits
Chips met gelegde circuits komen in allerlei technologie voor en voeren verschillende functies uit, variërend van tijdwaarneming en motorbesturing tot rekenen en logica. Deze chips bestaan uit een kleine siliconen plaat met gates erop die met elkaar verbonden kunnen worden. Welke gates met elkaar verbonden moeten worden, staat in een netlist. Deze verbindingen moeten zo efficient mogelijk gelegd worden, wat betekent dat ze zo kort mogelijk moeten zijn, niet over elkaar heen kunnen lopen en elkaar zo min mogelijk moeten kruisen. Het leggen van deze connecties, waarbij rekening wordt gehouden met de genoemde restricties, is wat deze case zo moeilijk maakt. Hoe groter de chips, hoe meer gates, hoe meer connecties, en dus ook hoe moeilijker de case.

# Algoritmes
Om deze case op te lossen zijn verschillende algoritmes gebruikt. Naast de baseline (een random algoritme, die zelden valide oplossingen gaf) is breadth first, A* en simulated annealing geimplementeerd om oplossingen te genereren. 

Om connecties te vormen tussen twee gates die volgens de netlijst verbonden moeten worden, wordt er vanaf de eerste gate stappen gezet totdat de tweede gate bereikt is. In de verschillende algoritmes wordt dit op hun eigen manier gedaan om uiteindelijk de kortste route te vinden tussen de twee gates en daarbij ook rekening te houden met de hierboven genoemde restricties.

Breadth first kon valide oplossingen geven door elke mogelijke stap die een connectie op de chip kan leggen af te gaan totdat hij zijn eindbestemming had bereikt. Om dit algoritme iets efficiënter te maken hebben wij ook een beam search toegevoegd, waarbij bij elke stap alleen de 2/3 beste volgende stappen verder werden onderzacht en de andere stappen te prunen. Dit duurde algoritme echter nog steeds erg lang en dit algoritme hielt geen rekening met het ontwijken van intersection van draden. 

A* kon een stuk gerichter zoeken door elke keer de volgende stap te selecteren die de minste kosten met zich mee gaf. Dit algoritme kon al veel sneller en efficienter valide oplossingen vinden en kon, daarbij, ook intersecties ontwijken door die stappen een hogere kosten waarde te geven, waardoor zij dus minder snel geselecteerd werden. 

De oplossingen die uit het A* algoritme kwamen waren allemaal valide oplossingen maar ze konden nog verbeterd worden. Om dit te doen is het simulated annealing algoritme geimplementeerd die op de oplossingen van A* kleine aanpassingen kon maken. Deze aanpassingen waren vooral gericht op de intersecties die A* nog niet kon ontwijken. Door deze op te zoeken en vervolgens één van de twee connecties die de intersectie had veroorzaakt opnieuw te laten leggen door het A* algoritme, kon simulated annealing de oplossingen verbeteren.

# Gebruik
De code is volledig geschreven in Python 3.10.

Onze oplossinging voor het Chips & circuits probleem kan worden aangeroepen met:

```python main.py```

Door alleen de main aan te roepen zal er in de command terminal een aantal inputs gevraagd worden. Namelijk of je een oplossing wilt maken of een al gemaakte oplossing wilt inladen, het chip nummer, de netlist, het algoritme waarmee de connecties gemaakt moeten worden en of je de chip wilt plotten of niet.

Deze informatie kan ook al meegegeven worden in de command lijn met het format:

```python main.py --solution (creating/loading) --chip_number (0,1,2) --netlist (1-9) --algorithm (alg name) --plot_chip (true/false)```

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
