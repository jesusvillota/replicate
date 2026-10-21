# Source card: sentiment

Status: available

## Source and URL or WRDS table

SF Fed Daily News Sentiment Index; Shapiro, Sudhof and Wilson. The workbook also credits Buckman for the Economic Letter update.

https://www.frbsf.org/research-and-insights/data-and-indicators/daily-news-sentiment-index/

Download: https://www.frbsf.org/wp-content/uploads/news_sentiment_data.xlsx

Access: public HTTPS download via `uv run python3 -m rebal.fetch.sentiment`.

## Downloaded (date)

2026-10-21.

## License class

Public, redistributable Fed data. Store under `data/public/sentiment/`; credit the SF Fed and authors.

## Series, with units

| Series | Raw units | Output units |
|---|---|---|
| `sentiment` (`News Sentiment`) | Unitless news sentiment score | Same |

## Transforms

Read the `Data` sheet and rename `News Sentiment` to `sentiment`. Keep the `Methodology` sheet in the unchanged raw workbook. No scaling, interpolation or filling.

## Coverage

`news_sentiment_data.xlsx` (Data) and `sentiment.csv`: 17,074 rows each, 1980-01-01 through 2026-10-18. Daily observations with 19 absent calendar dates in the published history; no missing scores among supplied rows.

## Known problems

Preserve all published gaps, including 1980-01-04. The live historical series can be revised. Publication dates and observation dates can differ.

## Paper datasets served (D-numbers)

D12. See `docs/contracts/daily_panel.md` for the downstream panel contract.
