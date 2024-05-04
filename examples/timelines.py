import sys, os
sys.path.append(os.path.abspath('./'))
from history_plot.date_utils import start, end
from history_plot.history_plot import HistoryPlotter

p = HistoryPlotter("Storia dell'antica Grecia", -800)

# Contesto storico
p.section("Cronologia")
p.subsection("Guerre e battaglie", '#500000')
p.plot_timeline([(-499, -479, 'Guerre persiane'), (-460, -445, 'Prima guerra del Peloponneso'), (-431, -404, 'Guerra del Peloponneso'),
                 (-404, -403, 'Guerra civile ateniese'), (-395, -387, 'Guerra di Corinto'),
                 (-356, -346, 'Guerra sacra'), (-322, -281, 'Guerre dei diadochi') #, (-415, -413, 'Spedizione a Siracusa')
                ],
                [(-480, 'Battaglia di Salamina'), (-490, 'Battaglia di Maratona'), (-479, 'Battaglia di Platea'),
                 (-414, 'Battaglia di Siracusa'), (-331, 'Battaglia di Gaugamela'), (-146, 'Distruzione di Corinto'),
                 (-335, 'Distruzione di Tebe'), (-335, 'Battaglia di Leuttra'), (-197, 'Battaglia di Cinocefale'),
                 (-168, 'Battaglia di Pidna'), (-421, 'Pace di Nicia'), (-362, 'Battaglia di Mantinea'),
                 (-338, 'Battaglia di Cheronea')], event_label_rotation=45)
p.subsection("Politica di Atene", '#EAC102')
p.plot_timeline(interval_events=[(-561, -556, 'I Tirannide di Pisistrato'), (-546, -527, 'II Tirannide di Pisistrato'),
                                 (-527, -514, 'Tirannide di Ippia e Ipparco'), (-467, -428, 'Pericle $\it{strategos}$'),
                                 (-404, -403, 'Oligarchia dei Trenta Tiranni'), (-416, -415, 'Alcibiade $\it{strategos}$'),
                                 (-338, -311, 'Impero macedone'), (-148, end, 'Occupazione romana')],
                instant_events=[(-620, 'Legislazione di Dracone'), (-594, 'Riforma di Solone'), (-510, 'Esilio di Ippia'),
                                (-508, 'Riforme di Clistène'), (-462, 'Riforma di Efialte'), (-493, 'Arcontato di Temistocle'),
                                (-411, 'Oligarchia dei Quattrocento'), (-415, 'I Esilio di Alcibiade'), (-407, 'II Esilio di Alcibiade'),
                                (-411, 'Ritorno di Alcibiade'), (-410, 'Assemblea dei Cinquemila')#,(-472, 'Ostracizzazione di Temistocle'), (-482, 'Ostracizzazione di Aristide')
                               ], event_label_rotation=45)

# Vite dei filosofi
p.section("Vite dei filosofi", '#0055A4')
p.plot_life_bar((-640, -624), (-548, -545), 'Talete', group='Scuola di Mileto')
p.plot_life_bar(-610, -546, 'Anassimandro', group='Scuola di Mileto')
p.plot_life_bar((-586, -585), (-526, -525), 'Anassimene', group='Scuola di Mileto')
p.plot_life_bar(-570, -495, 'Pitagora')
p.plot_life_bar(-535, -475, 'Eraclito')
p.plot_life_bar((-570, -565), -475, 'Senofane', group='Scuola di Elea')
p.plot_life_bar((-520, -510), -450, 'Parmenide', group='Scuola di Elea')
p.plot_life_bar((-495, -489), -431, 'Zenone', group='Scuola di Elea')
p.plot_life_bar(-470, (-440, -400), 'Melisso', group='Scuola di Elea')
p.plot_life_bar(-492, -434, 'Empedocle')
p.plot_life_bar((-500, -497), -428, 'Anassagora')
p.plot_life_bar((-472, -457), -370, 'Democrito')
p.plot_life_bar(-490, (-420, -410), 'Protagora', group='Sofisti')
p.plot_life_bar((-485, -475), -375, 'Gorgia da Leontini', group='Sofisti')
p.plot_life_bar((-470, -469), -399, 'Socrate')
p.plot_life_bar(-446, (-366, -365), 'Antistene', group='Cinici')
p.plot_life_bar((-412, -404), -323, 'Diogene di Sinope', group='Cinici')
p.plot_life_bar(-365, -285, 'Cratete di Tebe', group='Cinici')
p.plot_life_bar(-350, -280, 'Ipparchia', group='Cinici')
p.plot_life_bar((-350, -250), -250, 'Metrocle', group='Cinici')
p.plot_life_bar(-435, -356, 'Aristippo', group='Cirenaici')
p.plot_life_bar(-435, -365, 'Euclide di Megara', group='Megarici')
p.plot_life_bar((-428, -427), (-348, -347), 'Platone')
p.plot_life_bar((-408, -393), -339, 'Speusippo', group='Platonici minori')
p.plot_life_bar(-396, -314, 'Senocrate', group='Platonici minori')
p.plot_life_bar(-384, -322, 'Aristotele')
p.plot_life_bar(-371, -287, 'Teofrasto', group='Aristotelici')
p.plot_life_bar(-335, (-274, -269), 'Stratone di Lampsaco', group='Aristotelici')
p.plot_life_bar(-299, -225, 'Licone', group='Aristotelici')
p.plot_life_bar(-341, -270, 'Epicuro')
p.plot_life_bar((-336, -332), -262, 'Zenone di Cizio', group='Stoici')
p.plot_life_bar((-331, -330), (-232, -230), 'Cleante', group='Stoici')
p.plot_life_bar((-281, -277), (-208, -204), 'Crisippo', group='Stoici')
p.plot_groups()
p.show()
