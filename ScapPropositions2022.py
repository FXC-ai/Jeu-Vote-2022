#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 13:21:36 2022

@author: oem
"""

from bs4 import BeautifulSoup
import urllib.request
import re
import pandas as pd
import random
import pickle

url = "https://www.ifrap.org/comparateurs/presidentielle-2022#c199"


reponse = urllib.request.urlopen(url)
contenu_web = reponse.read().decode('UTF-8')

soup = BeautifulSoup(contenu_web, 'html.parser')
int_text = soup.get_text()

soup.section.h2.get_text()

sections = soup.find_all('section')

list_propositions = list()

for section in sections:
    # print('\n', 'SECTION ', section.h2.get_text())
    name_section = section.h2.get_text()
    
    details = section.find_all('details', id = re.compile("^c[1-9]{3}$"))
    
    for detail in details :
        name_item = detail.find('summary').get_text().strip()
        # print(name_item)
        
        ul_candidats = detail.find('ul')
        
        li_candidats = ul_candidats.find_all('li', class_ = re.compile("^p-4"))
        
        
        for li_candidat in li_candidats:
            name_candidat = li_candidat.figure.figcaption.get_text().strip().replace("  "," ")
            # print(li_candidat.figure.figcaption.get_text())
            
            ol_proposition = li_candidat.find('ol')
            
            if li_candidat.find('ol') != None :
                li_propositions = ol_proposition.find_all('li')
                for li_proposition in li_propositions :
                    text_proposition = li_proposition.get_text()
                    # print(li_proposition.get_text())
                    list_propositions.append((name_section, name_item, name_candidat, text_proposition))
            else :
                text_proposition = li_candidat.div.p.get_text()
                # print(li_candidat.div.p.get_text())
                list_propositions.append((name_section, name_item, name_candidat, text_proposition))
                       
                    
df_propositions = pd.DataFrame(list_propositions, columns = ('Section','Theme','Candidat','Proposition'))
#df_propositions_byCandidat = df_propositions.sort_values(by='Candidat')

indexNames = df_propositions[df_propositions['Proposition'] == 'Proposition non encore connue.'].index
df_propositions.drop(indexNames, inplace=True)

file = open('df_proposition', 'wb')
pickle.dump(df_propositions, file)
file.close()

# file = open('df_proposition', 'rb')
# data = pickle.load(file)
# file.close()

# df_propositions.iloc[1]['Proposition']

df_propositions['Section'].value_counts()

rst = pd.crosstab(df_propositions['Section'], df_propositions['Candidat'])
rst.isnull().sum()

arr_sections = df_propositions['Section'].unique()
arr_candidats = df_propositions['Candidat'].unique()

def save_df (data, filename):
    file = open(filename, 'wb')
    pickle.dump(data, file)
    file.close()

save_df(arr_sections, 'arr_sections') 
save_df(arr_candidats, 'arr_candidats')
    
    

#df_propositions.to_excel('propositions2022.xlsx')

# count = 0
# while count < 10 :
#     random_nb = random.randint(0, len(df_propositions))
#     if df_propositions.iloc[random_nb]['Proposition'] != 'Proposition non encore connue.':
#         print(df_propositions.iloc[random_nb]['Proposition'])
#         note = input('Noter de -3 à 3 la proposition :')
#         print('Ceci est une proposition de {}'.format(df_propositions.iloc[random_nb]['Candidat']))
#         count+=1
#         print('\n')
  