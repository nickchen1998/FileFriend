# 檔案好朋友 FileFriend

## 專案介紹

這是一個簡單的檔案管理系統，可以讓使用者上傳檔案及針對檔案做標籤設定，並且可以設定檔案的分享權限，讓其他使用者可以下載檔案。

本專案採用 streamlit 進行開發，目的在於練習使用 streamlit 進行快速的網頁開發。

系統架構及操作可以參考 [這個網址](https://hackmd.io/@nickchen1998/檔案好朋友-系統架構及操作)，本處僅撰寫部署方式。

## Build With

* python 3.11.6
* streamlit 1.29.0
* streamlit-authenticator 0.2.3
* pydantic-settings 2.1.0
* click 8.1.7
* sqlalchemy 2.0.23

## requirements.txt 輸出方式

```bash
poetry export --without-hashes --format=requirements.txt > requirements.txt
```

## .env 設定

請於專案根目錄設定 .env 檔案，內容如下：

```dotenv
PORT=""
FFD_DATA_PATH=""

ROOT_EMAIL=""
ROOT_PASSWORD=""
```

變數介紹如下：

- PORT：網頁埠號，預設為 8501，docker compose 部署會用到。
- FFD_DATA_PATH：檔案好朋友的資料儲存路徑，預設為 ./data，docker compose 部署會用到。
- ROOT_EMAIL：系統管理員的信箱，執行 `python ./tools.py init-system` 時會用到。
- ROOT_PASSWORD：系統管理員的密碼，執行 `python ./tools.py init-system` 時會用到。

## 本機執行

- 設定 ROOT 相關環境變數
- 執行 `python ./tools.py init-system` 初始化系統
- 確認專案根目錄下有自動長出 volumes 目錄，且目錄中有兩個檔案，分別是 **ffd.sqlite3** 及 **credentials.yaml**
- 執行 `streamlit run ./home.py` 啟動網頁伺服器

## Docker Compose 部署

- 設定四個環境變數：PORT、FFD_DATA_PATH、ROOT_EMAIL、ROOT_PASSWORD
- 執行 `docker-compose up -d --build --force-create` 部署專案
- 按照環境變數設定的埠號，連線到網頁伺服器即可

## 版權聲明

版權所有 © 2024.01.06 陳柏翰。保留所有權利。

本專案包含的所有材料，包括但不限於文本、圖像、音頻、視頻和任何其他形式的內容，均受版權法保護。

除非另有明確許可，否則嚴禁將本專案的任何部分用於商業目的。

未經陳柏翰明確書面同意，不得複製、修改、發布、傳播或以其他方式使用本專案內容。

對於教育目的和非商業性質的使用，可以在不更改內容並且明確註明來源的情況下進行，但必須遵守相關的版權法規和條款。

任何違反本版權聲明的行為，陳柏翰保留追究法律責任的權利。

