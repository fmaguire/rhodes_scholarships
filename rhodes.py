import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def get_mean_gdp(country):
    gdp = pd.read_csv('gdp/data/gdp.csv')
    gdp = gdp.loc[gdp.groupby('Country Name').Year.idxmax(), :]
    regions={'East Africa': ['Uganda', 'Tanzania','Rwanda', 'South Sudan', 'Burundi'],
        'Jamaica & The Commonwealth Caribbean': ['Antigua and Barbuda', 'Bahamas, The', 'Barbados',
            'Belize', 'Trinidad and Tobago', 'Jamaica', 'Dominica', 'Grenada',
            'Guyana', 'St. Lucia', 'St. Vincent and the Grenadines', 'St. Kitts and Nevis',
            'Montserrat', 'Anguilla', 'Turks and Caicos Islands',
            'Cayman Islands', 'British Virgin Islands'],
        'Southern Africa' : ['South Africa', 'Botswana', 'Lesotho', 'Malawi',
                             'Namibia', 'Swaziland'],
        'Syria, Jordan, Lebanon, & Palestine': ['Syrian Arab Republic', 'Jordan', 'Lebanon', 'Palestine'],
        'West Africa': ['Benin', 'Burkina Faso', 'Cabo Verde', 'Gambia, The',
                        'Ghana', 'Guinea', 'Guinea-Bissau', "Cote d'Ivoire",
                        'Liberia', 'Mali', 'Mauritania', 'Niger',
                        'Nigeria', 'Saint Helena', 'Senegal', 'Sierra Leone',
                        'Sao Tome and Principe', 'Togo']}


    saves = {'Montserrat': 63000000, 'Anguilla': 108900000,
             'Turks and Caicos Islands': 632000000,
             'British Virgin Islands': 853400000,
             'Palestine': 11950000000,
             'Hong Kong': 320900000000,
             'Saint Helena': 33500000}

    if country in regions:
        gdps = []
        for sub_region in regions[country]:
            if gdp[gdp['Country Name'] == sub_region].empty:
                if sub_region not in saves:
                    print(sub_region)
                else:
                    gdps.append(saves[sub_region])
            else:
                gdps.append(gdp[gdp['Country Name'] == sub_region]['Value'].values[0])
        return sum(gdps) / len(gdps)

    else:
        if gdp[gdp['Country Name'] == country].empty:
            if country not in saves:
                print(country)
            else:
                return saves[country]
        else:
            return gdp[gdp['Country Name'] == country]['Value'].values[0]


data="""Australia 9 24130000
Bermuda 1 65331
Canada 11 36290000
China 4 1379000000
East_Africa 1 131730000
Germany 2 82670000
Hong_Kong 1 7347000
India 5 1324000000
Israel 2 8547000
Jamaica_&_The_Commonwealth_Caribbean 2 6811975
Kenya 2 48460000
Malaysia 1 31190000
New_Zealand 3 4693000
Pakistan 1 193200000
Saudi_Arabia 1 32280000
Singapore 1 5607000
Southern_Africa 10 82277000
Syria,_Jordan,_Lebanon,_&_Palestine 2 38443000
United_Arab_Emirates 2 9270000
United_States 32 325700000
West_Africa 1 341746004
Zambia 2 16590000
Zimbabwe 2 16150000"""

df = {'country': [line.split()[0] for line in data.split('\n')],
      'rhodes_scholarship': [int(line.split()[1]) for line in data.split('\n')],
      'population': [float(line.split()[2]) for line in data.split('\n')]}

df = pd.DataFrame(df)
df['country'] = df['country'].str.replace('_', ' ')
df['population per scholarship'] = df['population'] / df['rhodes_scholarship']
df = df.sort_values('population per scholarship')
df['Total Mean GDP (USD)'] = df['country'].apply(get_mean_gdp)

sns.set_context("paper")
g = sns.barplot(y='country', x='population per scholarship', data=df,
                palette="GnBu_d")
plt.ylabel('Rhodes Scholarship Regions')
plt.xlabel('Population per Available Scholarship (100 millions)')
plt.tight_layout()
plt.savefig('rhodes_inequality_population.pdf')
plt.savefig('rhodes_inequality_population.png')


df['Scholarships per Mean GDP'] = df['Total Mean GDP (USD)'] / df['rhodes_scholarship']
df = df.sort_values('Scholarships per Mean GDP')
g = sns.barplot(y='country', x='Scholarships per Mean GDP', data=df,
                palette="GnBu_d")
plt.ylabel('Rhodes Scholarship Regions')
plt.xlabel('Scholarships per Regional Mean GDP (USD)')
plt.tight_layout()
plt.savefig('rhodes_inequality_GDP.pdf')
plt.savefig('rhodes_inequality_GDP.png')

