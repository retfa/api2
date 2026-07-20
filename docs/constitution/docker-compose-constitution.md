# Docker Compose WebAPI 系統憲章

本文件定義 Docker Compose WebAPI 系統的強制架構規範。Compose 是系統定義，不是單純啟動腳本；正式部署必須可重現、可 scale，且服務之間保持低耦合。

## 等級

`CONSTITUTION`：強制遵守，不可違反。

## 架構原則

- 本專案所有 WebAPI 正式部署必須以 Docker container 運行。
- 所有服務必須透過 `docker compose` 管理。
- 禁止直接使用 `docker run` 作為正式部署方式。
- 所有服務必須為 stateless，不得依賴 container 本地狀態。
- 設定檔 `appsettings.json` 與 `connections.json` 不得寫死在 image 中。
- DB data 與 logs 必須使用 volume 或 bind mount 做資料持久化。
- 不允許將敏感資訊，例如密碼，寫死在 `docker-compose.yml`。
- 禁止使用 PyInstaller 取代 container 作為正式部署方式。

## 專案標準目錄結構

以下為 Docker Compose 化後的標準目錄結構。既有專案若尚未完成 Docker 化，新增或調整 Docker 部署相關檔案時，應逐步對齊此結構。

```text
root/
docker-compose.yml
.env
.env.example

services/
api/
Dockerfile
app/
worker/ (optional)

config/
appsettings.json
connections.json

data/
mssql/
redis/

logs/
```

## docker-compose.yml 規範

`docker-compose.yml` 必須包含：

- `services`
- `volumes`
- `networks`

命名規則：

- service name 使用 `kebab-case`。
- 禁止設定 `container_name`，避免影響 scale 與 Compose 自動命名。

必要設定：

- 必須使用 `restart: unless-stopped`。
- `environment` 必須使用 `.env` 或部署環境注入。
- 必要時使用 `depends_on` 表示啟動依賴。
- API service 必須設定 `healthcheck`。

## 環境變數規範

所有機密資料必須放在 `.env` 或部署環境中，例如：

```env
DB_PASSWORD=YourStrongPassword
API_ENV=production
```

禁止在 `docker-compose.yml` 直接寫死密碼。

專案應維護 `.env.example` 或等效文件，列出必要環境變數名稱與用途，但不得放入真實密碼、token 或連線密鑰。

## Service 設計規則

每個 service 僅負責單一職責：

- `api`：WebAPI。
- `db`：SQL Server。
- `redis`：cache。
- `worker`：background job。

禁止一個 container 同時執行多種角色。

## Volume 規範

必須區分不同資料類型：

- DB data：使用 named volume。
- log：使用 bind mount 或專用 volume。
- config：使用 bind mount。

禁止 DB 無 volume。

## Network 規範

- 必須使用自訂 network。
- 不允許全部使用 default network。
- API 僅允許連接必要的 backend network。

## 啟動與停止指令

標準啟動指令：

```powershell
docker compose up -d
```

標準停止指令：

```powershell
docker compose down
```

禁止使用 `docker run` 作為正式部署方式。

## Scale 規範

允許使用：

```powershell
docker compose up --scale api=3
```

前提：

- API 必須 stateless。
- API 不可依賴本地檔案作為 runtime 狀態。
- 不得設定 `container_name`。

## 健康檢查

API 必須提供：

```http
GET /health
```

`docker-compose.yml` 必須為 API service 設定 `healthcheck`。

## Logging 規範

- log 必須寫入 volume 或 bind mount。
- 不得只依賴 container stdout。
- 禁止使用 `TEMP` 作為 runtime storage。

## Image 版本策略

image 必須使用明確版本，例如：

```yaml
image: my-api:1.0.0
```

禁止使用 `latest`。

## AI Agent 操作指令

新增 service 時：

- 建立 `services/<name>/Dockerfile`。
- 更新 `docker-compose.yml`。
- 加入 network。
- 視需要加入 volume。
- 更新 `.env.example` 或環境變數契約文件。

修改 API 時：

- 不得影響 `docker-compose.yml` 結構。
- 不得破壞 environment variable contract。
- 必須保留 health endpoint。

修改 DB 時：

- 必須保留 volume。
- 不可破壞資料持久化。

## 禁止事項

- 禁止 `docker run` 作為正式部署方式。
- 禁止使用 PyInstaller 取代 container。
- 禁止在 container image 內寫死 config。
- 禁止使用 `TEMP` 當 runtime storage。
- 禁止 DB 無 volume。
- 禁止在 `docker-compose.yml` 寫死密碼。
- 禁止使用 `latest` image tag。

## 設計原則

- Compose 是系統定義，不是單純啟動腳本。
- 系統必須可重現。
- 系統必須可 scale，API 必須 stateless。
- 系統必須可替換，服務之間保持 low coupling。
