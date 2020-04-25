import pandas as pd
import matplotlib.pyplot as plt

class SpainGraphics:
    def __init__(self, data):
        self.comunidades = list(set([col for col in data['CCAA'].tolist() if len(col)==2]))
        self.data = data

    def get_data(self, comunidad):
        cond = (self.data['CCAA']==comunidad) & (data['CASOS'].notnull()) & (self.data['Hospitalizados'].notnull()) & (self.data['UCI'].notnull()) & (self.data['Recuperados'].notnull()) & (self.data['Fallecidos'].notnull())
        df_comunidad = self.data[cond]
        df_comunidad['Activos'] = df_comunidad['CASOS'] - df_comunidad['Fallecidos'] - df_comunidad['Recuperados']
        df_comunidad = df_comunidad.set_index('FECHA')
        self.df_comunidad = df_comunidad
        self.define_active_cases()

        return self.df_comunidad

    def get_figure(self, df_comunidad, titulo):
        ax = plt.gca()
        ax1 = df_comunidad.plot(kind='line', lw=4, grid=True, figsize=(15,10), ax=ax, style='.-', ms=20)
        ax2 = df_comunidad.plot(kind='bar', alpha=0, lw=4, grid=True, figsize=(15,10), ax=ax, legend=None)
        plt.title(f'{titulo}')
        return plt.gcf()

    def get_bars(self, df_comunidad, titulo):
        ax = plt.gca()
        ax3 = df_comunidad['NUEVOS'].plot(kind='bar', alpha=1, color='purple', grid=True, figsize=(15,10), ax=ax, legend=None)
        plt.title(f'{titulo}')
        return plt.gcf()

    def define_active_cases(self):
        daily_list = []
        for i, active in enumerate(self.df_comunidad['CASOS']):
            if i==0:
                daily_list.append(active)
            else:
                daily_list.append(active-prev_active)
            prev_active = active
            
        self.df_comunidad['NUEVOS'] = daily_list


# NOTE Coger información del Ministerio de Salud
data = pd.read_csv("https://covid19.isciii.es/resources/serie_historica_acumulados.csv", encoding='cp1252')

sg = SpainGraphics(data)

for i, comunidad in enumerate(sg.comunidades):
    if i==0:
        df_final = sg.get_data(comunidad)
    else:
        df_final += sg.get_data(comunidad)
    
    plt.show(sg.get_figure(df_final, comunidad))
       
print(df_final)

plt.show(sg.get_figure(df_final, 'España'))
plt.show(sg.get_bars(df_final, 'España'))

