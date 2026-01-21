import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


df = pd.read_csv("wyniki_symulacji.csv")

sns.set_theme(style="whitegrid")

print("Analiza\n")

# statystyki ogólne
print("Średnie czasy (sekundy):")
print(df.groupby(['distance_cat', 'scenario'])[['car_time_s', 'bike_time_s']].mean())

# weryfiukacja, Tstudent dla KRÓTKIEGO dystansu w SZCZYCIE
short_peak = df[(df['distance_cat'] == 'SHORT') & (df['scenario'] == 'PEAK')]
t_stat, p_val = stats.ttest_rel(short_peak['car_time_s'], short_peak['bike_time_s'])

print("\nWeryfikacja HIPOTEZY 1 (Krótki + Szczyt)")
print(f"Średni czas Auto: {short_peak['car_time_s'].mean():.2f} s")
print(f"Średni czas Rower: {short_peak['bike_time_s'].mean():.2f} s")
print(f"Wynik testu t-Studenta: t={t_stat:.2f}, p-value={p_val:.5f}")
if p_val < 0.05 and t_stat > 0:
    print("WNIOSEK: Różnica jest ISTOTNA statystycznie. Rower jest szybszy -> Hipoteza potwierdzona.")
else:
    print("WNIOSEK: Brak istotnej różnicy.")

#wykresy

#Wykres 1: Pudełkowy
plt.figure(figsize=(10, 6))
df_melt = df.melt(id_vars=['distance_cat', 'scenario'], value_vars=['car_time_s', 'bike_time_s'], var_name='Vehicle', value_name='Time')
sns.boxplot(data=df_melt, x='distance_cat', y='Time', hue='Vehicle', palette=["#ff3d27", "#00b7ff"])
plt.title("Rozkład czasu podróży: Auto vs Rower")
plt.ylabel("Czas [s]")
plt.xlabel("Kategoria dystansu")
plt.savefig("wykres_box.png")
print("\nZapisano: wykres_box.png")

#Wykres 2: Zależność od liczby świateł (scatter)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='n_lights', y='diff_time', hue='distance_cat', alpha=0.7)
plt.axhline(0, color='red', linestyle='--', linewidth=1) # Linia zero
plt.title("Przewaga czasowa roweru w zależności od liczby świateł")
plt.xlabel("Liczba świateł na trasie")
plt.ylabel("Zysk czasowy roweru (Car - Bike) [s]")
plt.text(1, 10, "Powyżej 0 = Rower wygrywa", color='blue')
plt.savefig("wykres_lights.png")
print("Zapisano: wykres_lights.png")

#Wykres 3: Słupkowy
plt.figure(figsize=(10, 6))
sns.barplot(data=df_melt, x='scenario', y='Time', hue='Vehicle', ci=None, palette=["#ff3d27", "#00b7ff"])
plt.title("Średni czas przejazdu: Szczyt vs Poza Szczytem")
plt.savefig("wykres_bar.png")
print("Zapisano: wykres_bar.png")

#Wykres 4: SZCZYT : Dystans vs Czas
plt.figure(figsize=(10, 6))
#tylko dla peak
peak_data = df[df['scenario'] == 'PEAK']

#dwa linie trendu na jednym wykresie
#samochód
sns.regplot(data=peak_data, x='distance_m', y='car_time_s', 
            scatter_kws={'alpha':0.3}, line_kws={'color':'#ff3d27'}, 
            color='#ff3d27', label='Auto', ci=None)

#rower
sns.regplot(data=peak_data, x='distance_m', y='bike_time_s', 
            scatter_kws={'alpha':0.3}, line_kws={'color':'#00b7ff'}, 
            color='#00b7ff', label='Rower', ci=None)

plt.title("Porównanie trendów: Scenariusz godzin szczytu")
plt.xlabel("Dystans [m]")
plt.ylabel("Czas podróży [s]")
plt.legend()
plt.savefig("wykres_scatter_dist_PEAK.png")
print("Zapisano: wykres_scatter_dist_PEAK.png")


#Wykres 5: POZA SZCZYTEM : Dystans vs Czas
plt.figure(figsize=(10, 6))
#tylko dla peak
peak_data = df[df['scenario'] == 'OFF_PEAK']

#dwa linie trendu na jednym wykresie
#samochód
sns.regplot(data=peak_data, x='distance_m', y='car_time_s', 
            scatter_kws={'alpha':0.3}, line_kws={'color':'#ff3d27'}, 
            color='#ff3d27', label='Auto', ci=None)

#rower
sns.regplot(data=peak_data, x='distance_m', y='bike_time_s', 
            scatter_kws={'alpha':0.3}, line_kws={'color':'#00b7ff'}, 
            color='#00b7ff', label='Rower', ci=None)

plt.title("Porównanie trendów: Scenariusz poza godzinami szczytu")
plt.xlabel("Dystans [m]")
plt.ylabel("Czas podróży [s]")
plt.legend()
plt.savefig("wykres_scatter_dist_OFFPEAK.png")
print("Zapisano: wykres_scatter_dist_OFFPEAK.png")