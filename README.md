CCDashboard - A Digital Asset Manager.
===
[ [中文版](https://github.com/racterub/ccdashboard/blob/master/READMEzhtw.md) ]

**This is a beta release, which only shows the basic functionality, use it at your own risk.**
**Breaking changes may needed in the future release.**

This is inspired by [jasonyl13579/Binance-Altcoin-Asset-Cost-Calculator](https://github.com/jasonyl13579/Binance-Altcoin-Asset-Cost-Calculator).

## Introduction
CCDashboard is a easy to use(?) web service which allows crypto currency trade have a clear view about their assets.

## Usage (You will need to tweak the settings whether you are using docker or install it manually, for now.)
### Using docker (Recommended)
1. Install requirements.
We only need docker here.
- Windows
  - [Official tutorial](https://docs.docker.com/docker-for-windows/install/)
- macOS
  - [Official tutorial](https://docs.docker.com/docker-for-mac/install/)
- Linux
  - `curl -fsSL https://get.docker.com | sh` (you can install it via APT as well.)

2. Edit settings.
- COIN (The coin you want to fetch, for example, DOGEUSDT -> ["DOGE", "USDT"])
  - [fetcher/app/config.example.py](fetcher/app/config.example.py)
  - [backend/app/app/views/fetcher/config.py](backend/app/app/views/fetcher/config.py)
- SECRETKEY (For backend, not necessary but recommended.)
  - [docker-compose.yml](docker-compose.yml)
  - You can copy this line to generate secret key `python3 -c "import secrets;print(secrets.token_urlsafe(64))"`

3. Start the server
`docker compose up`

4. Create a account (Currently only one account is supported.)
`./createDB.sh`

### Manually install (More flexible)
This service consists four part, `Frontend (Vuejs)`, `Backend (Flask)`, `APIFetcher(Python)` and `DB (MariaDB)`.

- Frontend
  - Install depandencies `npm install` or `yarn install`
  - Compile to production ready files `npm run build` or `yarn run build`
- Backend & API Fetcher
  - Install depandencies `pipenv install`
  - Start service `pipenv run *.py`
- DB
  - Mysql and MariaDB is recommended. If you choose other DB system, you will need to change the DBURL.
  - Create database `CREATE DATABASE ccdashboard CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci`

## Donations
All donations are welcome.
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
 

