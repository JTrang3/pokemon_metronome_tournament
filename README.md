# pokemon_metronome_tournament
Recording data for Pokemon Showdown Team Metronome League (Season 1) tournament

Tournament Bracket & Replays for Season 1:
https://challonge.com/sjm9e5qs

Tableau Public Visuals for Season 1:
https://public.tableau.com/app/profile/jt.trang/viz/TeamMetronomeLeagueSeason1/Dashboard

Extracts match data from Pokemon Showdown's replay files using BeautifulSoup4. Stores collected data into specified excel file using Openpyxl to transfer later in a database.

Data scraped from Showdown replays:

Move: Usage Count

Pokemon: [Team, Defeats, Faints, Self-Destructs, Damage Given, Damage Taken, Battle Turns, Games Played]

Team: [[Roster], Games Won, Games Lost, Turns Played, Games Played, [Match History]]
