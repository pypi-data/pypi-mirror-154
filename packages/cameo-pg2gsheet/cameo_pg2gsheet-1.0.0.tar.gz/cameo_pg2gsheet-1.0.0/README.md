# cameo-pg2gsheet

## 使用Docker的執行方式
1. 調整docker-compose.yaml的pg2gsheet_run及pg2gsheet_output路徑
2. 在docker-compose.yaml填入postgresql連線資訊
3. 複製src/examples.py到pg2gsheet_run目錄並調整要執行的函式
4. 輸入以下指令運行Docker
```bash
docker-compose build cameo-pg2gsheet
docker-compose up -d cameo-pg2gsheet
```
5. 執行examples.py
```bash
docker exec DockerContainerId python /app/run/examples.py
```

## 不使用Docker的執行方式
### 前置步驟
1. 安裝cameo-pg2gsheet套件
```shell
pip install cameo-pg2gsheet
```
2. 複製src/dot_env_file_template成.env檔，並填入postgresql連線資訊

### 範例 (另可參考src/examples.py)
1. 從單一table匯出CSV
```python
from cameo_pg2gsheet import export_single_table_to_csv

csv_file_path = '匯出的CSV路徑含檔名'
table_name = 'table名稱'
export_single_table_to_csv(csv_file_path, table_name)
```

2. 從SQL指令所join的table匯出CSV
```python
from cameo_pg2gsheet import export_csv_by_sql_command

csv_file_path = '匯出的CSV路徑含檔名'
sql_command = 'SQL指令'
export_csv_by_sql_command(csv_file_path, sql_command)
```

3. 將CSV匯入到Google sheet
```python
from cameo_pg2gsheet import import_csv_to_gsheet

google_api_credentials_file_path = 'Google API驗證檔路徑'
gsheet_id = 'Google sheet ID'
worksheet_name = 'worksheet名稱'
csv_file_path = '匯出的CSV路徑含檔名'
import_csv_to_gsheet(google_api_credentials_file_path, gsheet_id, worksheet_name, csv_file_path)
```
