import pandas as pd

# MAIN
data = pd.read_csv("https://covid19.isciii.es/resources/serie_historica_acumulados.csv", encoding='cp1252')
cond = (data['CCAA']=='AN') & (data['CASOS'].notnull()) & (data['Hospitalizados'].notnull()) & (data['UCI'].notnull()) & (data['Recuperados'].notnull()) & (data['Fallecidos'].notnull())
andalucia = data[cond]
andalucia['Activos'] = andalucia['CASOS'] - andalucia['Fallecidos'] - andalucia['Recuperados']

# Cambiar índice por la fecha
andalucia = andalucia.set_index('FECHA')

# Información del dataframe para ANDALUCÍA
print(andalucia)


import matplotlib.pyplot as plt
ax = plt.gca()
ax1 = andalucia.plot(kind='line', lw=4, grid=True, figsize=(15,10), ax=ax)
ax2 = andalucia.plot(kind='bar', alpha=0, lw=4, grid=True, figsize=(15,10), ax=ax, legend=None)
plt.show()
plt.clf()


# Define new daily cases ('New')
daily_list = []
for i, active in enumerate(andalucia['CASOS']):
    if i==0:
        daily_list.append(active)
    else:
        daily_list.append(active-prev_active)
    prev_active = active 
andalucia['NUEVOS'] = daily_list



ax = plt.gca()
ax3 = andalucia['NUEVOS'].plot(kind='bar', alpha=1, color='purple', grid=True, figsize=(15,10), ax=ax, legend=None)
plt.show()