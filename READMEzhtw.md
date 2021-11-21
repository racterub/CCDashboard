CCDashboard - A Digital Asset Manager.
===
[ [English Version](https://github.com/racterub/ccdashboard/blob/master/README.md) ]
**目前為 beta 版本，功能與系統尚不穩定，您必須自行承擔使用風險。**
**在未來的釋出版本中可能會有必須的破壞性更動**

Inspired by [jasonyl13579/Binance-Altcoin-Asset-Cost-Calculator](https://github.com/jasonyl13579/Binance-Altcoin-Asset-Cost-Calculator).

## Introduction
CCDashboard 是一個易於使用的網站系統，主要希望可以透過各大交易所的 API 來更有系統性的管理資產。

## 使用方式 (目前不論哪種安裝方式，都將需要手動設定一些參數)
### Using docker (建議)
1. 安裝系統需求套件
我們只需要 docker 即可(請安裝最新版本).
- Windows
  - [Official tutorial](https://docs.docker.com/docker-for-windows/install/)
- macOS
  - [Official tutorial](https://docs.docker.com/docker-for-mac/install/)
- Linux
  - `curl -fsSL https://get.docker.com | sh` (也可以使用各 Linux 的套件管理系統安裝)

2. 更改設定.
- COIN (你想要取得哪個代幣的資訊, 舉個例子： DOGEUSDT -> ["DOGE", "USDT"]，請依照檔案內的格式修改)
  - [fetcher/app/config.example.py](fetcher/app/config.example.py)
  - [backend/app/app/views/fetcher/config.py](backend/app/app/views/fetcher/config.py)
- SECRETKEY (使用於網站後端，雖不必要，但是建議更改)
  - [docker-compose.yml](docker-compose.yml)
  - You can copy this line to generate secret key `python3 -c "import secrets;print(secrets.token_urlsafe(64))"`

3. 啟動伺服器
`docker compose up`

4. 新增帳戶 (目前僅支援一個帳戶)
`./createDB.sh`

### 手動安裝 (More flexible)
此系統共包含四個部分, `Frontend (Vuejs)`, `Backend (Flask)`, `APIFetcher(Python)` and `DB (MariaDB)`.

- 前端
  - 使用 `npm install` 或 `yarn install` 安裝套件
  - 使用 `npm run build` or `yarn run build` 編譯網站檔案
- 後端 & 資料抓取程式
  - 使用 `pipenv install` 安裝套件
  - 使用 `pipenv run *.py` 啟動服務
- 資料庫
  - 建議使用 Mysql 或 MariaDB。如果你選擇其他 DB 服務，請修改 DBURL
  - 在 DB CLI 內使用 `CREATE DATABASE ccdashboard CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci` 指令新增資料庫

## 捐助我
歡迎捐助我這個菜雞大學生。
USDT: TGVtSp3kCunH768Th7KLgyXCALyA2LEtwQ (TRC20)
BTC: 17PXX6bcPZUNfRQPZYQJjy54WZGQ2yyGTc
ETH: 0x661f675e39c5fbbec5303f18ed4058902a84d3db(ERC20)
BNB: 0x661f675e39c5fbbec5303f18ed4058902a84d3db(BEP20)

## TODO
- [ ] Properly handle error exceptions.
- [ ] Add more exchanges support (FTX maybe).
- [ ] Improve backend & fetcher.
- [ ] Replace apexchart with chartjs (Due to mobile accessibility issue)
- [ ] Dark mode.
 

