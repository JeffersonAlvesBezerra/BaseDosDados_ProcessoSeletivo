#Importações das bibliotecas utilizadas na presente análise

import basedosdados as bd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Importação do dataset PWT
query ='''
SELECT year, country, population, human_capital_index
FROM basedosdados.nl_ug_pwt.microdados 
LIMIT 100000
'''

df = bd.read_sql(query, billing_project_id="meu-projeto-360419")

'''
A seguir é criada uma função simples apenas para, caso exista, excluir dados ausentes
para a Key de interesse. Outra alternativa válida seria preencher os dados faltantes com
a média, porém, como se trata de uma análise temporal, não achei adequado.

É calculado também o log10 dos valores da Key para, caso seja um valor de alta ordem de 
grandeza, o Log10 seja usado em seu lugar.

'''
def Excluir_Dados_Vazios(Df, Key):
    '''
    Parameters
    ----------
    Df : DataFrame a se remover valores faltosos.
    Key : Key de critério para a remoção de dados faltosos.

    Returns
    ----------
    Key_df: DataFrame contendo a Key, além de ano e país:
    Log_Key: Lista contendo o Log10 dos valores da Key

    '''
    null = Df.isnull()
    List_Key = []
    Log_Key = []
    for i in range(len(Df)):
        if null.at[i, Key] == False:
            List_Key.append([Df.at[i,'year'], Df.at[i,'country'], Df.at[i, Key]])
            Log_Key.append(np.log10(Df.at[i,Key]))
    Key_df = pd.DataFrame(List_Key, columns= ['year','country', Key])
    return(Key_df, Log_Key)

#Aplicação da função utilizando a Key de critério População

Pop_df, Log_Pop = Excluir_Dados_Vazios(df, 'population')


#Adição do Log_Pop ao DataFrame de População
Pop_df['log population'] = Log_Pop

#Definindo o critério de filtro por países
Pop_df.set_index("country", inplace = True)

#Coletando dados de dois países a partir de seus valores na Key: 'country'
Pop_df_Brasil = Pop_df.loc["Brazil"]
Pop_df_Argentina = Pop_df.loc["Argentina"]

#Plotagem padrão de um gráfico de dispersão
ax = plt.gca()
Pop_df_Brasil.plot(x = 'year', y = 'log population', kind = 'scatter', ax = ax, label = 'Brasil')
Pop_df_Argentina.plot(x = 'year', y = 'log population', kind = 'scatter', ax = ax, label = 'Argentina', color = 'r')
plt.title('Log10 Pop. Argentina e Log10 Pop. Brasileira ao longo dos anos')
plt.legend()
plt.grid()
plt.show()

#Aplicação da função utilizando a Key de critério de Indice de Capital Humano
Ind_Cap_Hum_df, Log_ICP = Excluir_Dados_Vazios(df, 'human_capital_index')

#Definindo o critério de filtro por países
Ind_Cap_Hum_df.set_index("country", inplace = True)

#Coletando dados de dois países a partir de seus valores na Key: 'country'
ICP_df_Brasil = Ind_Cap_Hum_df.loc["Brazil"]
ICP_df_USA = Ind_Cap_Hum_df.loc["United States"]  


#Plotagem padrão de um gráfico de dispersão
ax = plt.gca()
ICP_df_Brasil.plot(x = 'year', y = 'human_capital_index', kind = 'scatter', ax = ax, label = 'Brasil')
ICP_df_USA.plot(x = 'year', y = 'human_capital_index', kind = 'scatter', ax = ax, label = 'USA', color = 'r')
plt.title('ICP USA e ICP Brasileiro ao longo dos anos')
plt.legend()
plt.grid()
plt.show()

'''
Para entender melhor um dos diversos fatores para o índice de capital humano brasileiro,
foram coletados dados de No Schooling brasileiro do BarroLee Data set.

fonte: http://www.barrolee.com

Por se tratar de poucos dados, esses foram baixados em planilha excel e adaptados
para conter apenas os valores brasileiros de No Schooling.
'''

#lendo os dados em Excel e separando as keys de interesse (No Schooling e ano).
Brasil_No_Schooling_df = pd.read_excel('Brazil_No_Schooling.xlsx', index_col=0)
Brasil_No_Schooling_df = Brasil_No_Schooling_df[['No Schooling', 'year']]

'''
Foi necessário Criar uma função de normalização de DataFrames para que os dois fatores
No Schooling e ICP fossem comparados, uma vez que possuem diferença em sua ordem
de grandeza.

'''
def normalize(df):
    '''
    
    Normaliza um DataFrame.
    
    Parameters
    ----------
    df : DataFrame a ser Normalizado

    Returns
    -------
    result : DataFrame Normalizado com média 0 e desvio Padrão 1.

    '''
    result = df.copy()
    for feature_name in df.columns:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result

#Aplicação da normalização
Brasil_No_Schooling_df_normalized = normalize(Brasil_No_Schooling_df)
ICP_df_Brasil_normalized = normalize(ICP_df_Brasil)


#Plotagem Padrão de um gráfico de dispersão
ax = plt.gca()
ICP_df_Brasil_normalized.plot(x = 'year', y = 'human_capital_index', kind = 'scatter', ax = ax, label = 'Brasil')
Brasil_No_Schooling_df_normalized.plot(x = 'year', y = 'No Schooling', kind = 'scatter', ax = ax, label = 'No Schooling', color = 'r')
plt.title('ICP e No Schooling Brasileiro')
plt.legend()
plt.grid()
plt.show()
        
'''
Estava em meus planos originais adicionar um gráfico de barras comparando a média
de algum parâmetro fornecido no PWT para todos os países (por exemplo quantidade 
horas trabalhadas), porém, ao gerar o mesmo, achei a visualização muito poluida.
Dessa maneira me atentei mais aos gráficos de dispersão, por ter uma vizualização
mais limpa dos dados a serem exibidos.
'''