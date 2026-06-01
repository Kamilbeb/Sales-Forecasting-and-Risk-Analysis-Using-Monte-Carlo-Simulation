library(dplyr)
# wczytanie danych
setwd("D:/Projekt_prognozowanie_symulacja")


data <- read.csv("Superstore.csv", fileEncoding="latin1")

data$Order.Date <- as.Date(data$Order.Date, format="%m/%d/%Y")

# agregacja miesięczna
monthly <- data %>%
  group_by(format(Order.Date, "%Y-%m")) %>%
  summarise(Sales = sum(Sales))

# konwersja do ts
ts_data <- ts(monthly$Sales,start=c(2014,1), frequency=12)

# dekompozycja
decomp <- decompose(ts_data)

plot(decomp)

#Autokorelacja ACF
acf(ts_data)


