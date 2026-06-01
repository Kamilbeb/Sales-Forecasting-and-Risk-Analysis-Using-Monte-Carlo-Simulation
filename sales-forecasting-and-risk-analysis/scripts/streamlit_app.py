import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

# wczytanie danych
df = pd.read_csv("Superstore.csv", encoding='cp1252')

# podgląd danych
pd.set_option('display.width', None)
print(df.head())

# konwersja daty
df["Order Date"] = pd.to_datetime(df["Order Date"])

# ustawienie daty jako indeks
df.set_index("Order Date", inplace=True)

# Sprawdzenie brakujących danych
print(df.isnull().sum())

# agregacja miesięczna (suma sprzedaży dla każdego miesiąca)
monthly_sales = df["Sales"].resample("ME").sum()

# podgląd danych
print(monthly_sales.head())

plt.figure()
plt.plot(monthly_sales.index, monthly_sales.values)

plt.title("Sprzedaż w czasie (agregacja miesięczna)")
plt.xlabel("Data")
plt.ylabel("Sprzedaż")

plt.show()

print("*"*100)
# zamiana indeksu dat na liczby (czas jako zmienna niezależna)
monthly_sales = monthly_sales.reset_index()
monthly_sales["time_index"] = np.arange(len(monthly_sales))

# zmienne do modelu
X = monthly_sales[["time_index"]]   # czas
y = monthly_sales["Sales"]          # sprzedaż

# budowa modelu regresji liniowej
model = LinearRegression()
model.fit(X, y)

# prognoza dla istniejących danych (dopasowanie)
monthly_sales["forecast"] = model.predict(X)

# prognoza na przyszłość (np. 3 miesiące do przodu)
future_periods = 3
future_index = np.arange(len(monthly_sales), len(monthly_sales) + future_periods)

future_df = pd.DataFrame({"time_index": future_index})

future_forecast = model.predict(future_df)

print("Prognoza na kolejne miesiące:")
print(future_forecast.round(2))

print("*"*100)

#Wykres modelu
plt.figure()

plt.plot(monthly_sales["Order Date"], y, label="Dane rzeczywiste")
plt.plot(monthly_sales["Order Date"], monthly_sales["forecast"], label="Model regresji")

plt.legend()
plt.title("Regresja liniowa – dopasowanie modelu")
plt.xlabel("Data")
plt.ylabel("Sprzedaż")

plt.show()

print("*"*100)

#Symulacja Monte Carlo

n_simulations = 1000
std_dev = monthly_sales["Sales"].std()
base_forecast = future_forecast[0]

# symulacja
simulations = np.random.normal(base_forecast, std_dev, n_simulations)

# usunięcie wartości ujemnych
simulations = np.where(simulations < 0, 0, simulations)
simulations = np.round(simulations, 2)

# statystyki
print("Średnia:", round(np.mean(simulations), 2))
print("Minimum:", round(np.min(simulations), 2))
print("Maksimum:", round(np.max(simulations), 2))

#histogram symulacji
plt.figure()
plt.hist(simulations, bins=30)

plt.title("Symulacja Monte Carlo – rozkład sprzedaży")
plt.xlabel("Sprzedaż")
plt.ylabel("Częstotliwość")

plt.show()

#Tabela scenariuszy
base = future_forecast[0]

scenarios = {
    "Pesymistyczny (-10%)": round(base * 0.9, 2),
    "Realistyczny": round(base, 2),
    "Optymistyczny (+10%)": round(base * 1.1, 2)
}

for key, value in scenarios.items():
    print(key, ":", value)