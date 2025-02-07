# Подключение библиотек
import pandas as pd
import numpy  as np

# Считываем данные
df_month = pd.read_csv('путь-к-файлу\\file.csv', sep = ',', skiprows = 5)

# Переименовываем нужные колонки
df_month.rename(columns = {'MCF Channel Grouping'       : 'MCF_Channel_Grouping',
                         'Source / Medium'              : 'Source_Medium',
                         'Last Interaction Conversions' : 'Last_Click',
                         'Data-Driven Conversions'      : 'Data_Driven'},
                inplace = True)

# Удаляем ненужные колонки
df_month = df_month.drop(df_month.columns[[2, 4, 6, 7]], axis = 1)

# Удаляем ненужные строки
df_month = df_month[~df_month.MCF_Channel_Grouping.str.contains("Spend")]
df_month = df_month[~df_month.MCF_Channel_Grouping.str.contains("RUB")]

# Заменяем ненужные символы в столбцах с числами
df_month.Last_Click  = df_month.Last_Click.str.replace("[—]", "0")
df_month.Data_Driven = df_month.Data_Driven.str.replace("[—]", "0")
df_month.Data_Driven = df_month.Data_Driven.str.replace("[<]", "")

# Переводим столбцы с числами в числовой формат (по умолчанию они в формате object) 
df_month['Last_Click']  = df_month['Last_Click'].str.replace(',' ,'').astype(float)
df_month['Data_Driven'] = df_month['Data_Driven'].str.replace(',' ,'').astype(float)

# Прописываем условие для разделения источников/каналов на группы
df_month.loc[(df_month['MCF_Channel_Grouping'] == 'Direct')   		   |
             (df_month['MCF_Channel_Grouping'] == 'Referral') 		   |
             (df_month['MCF_Channel_Grouping'] == 'Organic Search')    , 'Group_channel'] = 'Органика'
df_month.loc[df_month['MCF_Channel_Grouping']  == 'Email'              , 'Group_channel'] = 'Рассылки'
df_month.loc[df_month['MCF_Channel_Grouping']  == '(Other)'            , 'Group_channel'] = 'Рассылки'
df_month.loc[df_month['MCF_Channel_Grouping']  == 'Paid Search'        , 'Group_channel'] = 'Платные'
df_month.loc[df_month['MCF_Channel_Grouping']  == 'Other Advertising'  , 'Group_channel'] = 'Платные'
df_month.loc[df_month['MCF_Channel_Grouping']  == 'Display'            , 'Group_channel'] = 'Медийка'
df_month.loc[df_month['MCF_Channel_Grouping']  == 'Social Network'     , 'Group_channel'] = 'Медийка'
df_month.loc[df_month['Source_Medium']         == 'telecard / link'    , 'Group_channel'] = 'Моб. приложение'
df_month.loc[(df_month['Source_Medium']        == 'yandex / maps')         |
             (df_month['Source_Medium']        == 'banki / fix')           |
             (df_month['Source_Medium']        == 'sravni / fix')          |
             (df_month['Source_Medium']        == 'vbr / fix')             |
             (df_month['Source_Medium']        == 'instagram / (not set)') |
             (df_month['Source_Medium']        == 'vk / (not set)')        |
             (df_month['Source_Medium']        == 'youtube / cpv')         |
             (df_month['Source_Medium']        == 'yandexmain / cpv')      |
             (df_month['Source_Medium']        == 'httpool / cpv')         |
             (df_month['Source_Medium']        == 'native_roll / cpv')     |
             (df_month['Source_Medium']        == 'bankiros / fix')        |
             (df_month['Source_Medium']        == 'yandexzen / cpr')       |
             (df_month['Source_Medium']        == 'mytarget / (not set)')  |
             (df_month['Source_Medium']        == 'catalog-svadba / fix')  |
             (df_month['Source_Medium']        == 'rbc / fix')             |
             (df_month['Source_Medium']        == 'yandexzen / article'), 'Group_channel'] = 'Медийка'
			 
# Проверяем результат группировки
df_month

# Считаем показатели для моделей атрибуции Last Click и Data Driven
df_result_month = df_month.groupby('Group_channel') \
                          .agg({'Last_Click' : 'sum', 'Data_Driven' : 'sum'}) \
                          .sort_values (by = 'Data_Driven', ascending = False) \
                          .round(2)

# Смотрим финальный результат
df_result_month

# Записываем финальные результаты в excel-файл
df_result_month.to_excel('путь-к-файлу\\final-file.xlsx')
