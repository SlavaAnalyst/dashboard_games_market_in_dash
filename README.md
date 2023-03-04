## Дана таблица истории состояния игровой индустрии games.csv

Из данных исключил проекты ранее 2000 года и проекты, для которых имеются пропуски данных в любой из колонок.   Используя Dash (plotly), построил дашборд, включающий: 3 фильтра, Интерактивный текст, Area plot и Scatter plot реагирующие на изменения значений всех трех фильтров одновременно.

Описание полей:
- Name - название проекта;
- Platform - платформа;
- Year_of_Release - год выпуска;
- Genre - жанр игры;
- Critic_Score - оценка критиков;
- User_Score - оценка игроков;
- Rating - возрастной рейтинг.
 
 #### Используемые библиотеки:
`pandas` `plotly.express` `dash_bootstrap_components` `Dash` `dcc` `html` `Input` `Output`
