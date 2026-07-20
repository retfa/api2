# Model 憲章

## 職責

Model 負責 DTO、資料模型、JWT payload 與 API 資料結構定義。

## 遷移規範

- flask-restx `fields` model 應改為 Pydantic model 或明確型別。
- 既有 DTO 欄位名稱必須保留。
- 不得為了符合 Python 命名慣例而改變公開 JSON 欄位。
- JWT payload 欄位必須保留。

## Pydantic 使用原則

- 用於 request body 與 OpenAPI schema。
- 欄位別名應支援既有 JSON 名稱。
- 驗證錯誤格式若會影響前端，需在 Controller 層做相容處理。
