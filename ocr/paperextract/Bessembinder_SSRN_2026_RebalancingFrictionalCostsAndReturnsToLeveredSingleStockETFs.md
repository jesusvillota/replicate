---
schema_version: "0.3"
export_schema_version: 4
document_id: "doc_81022379704f"
work_id: "work_17c1cc47c82c"
title: "Rebalancing, Frictional Costs, and Returns to Levered Single-stock ETFs&nbsp;"
authors:
- "Hendrik (Hank) Bessembinder"
journal: null
year: 2026
volume: null
issue: null
pages: null
article_number: null
doi: "10.2139/ssrn.7383378"
arxiv: null
document_version: "unknown"
bibliographic_status: "VALIDATED_WITH_WARNINGS"
processing_status: "COMPLETE"
observed:
  title: "Rebalancing, Frictional Costs, and Returns to Levered Single-Stock ETFs"
  authors:
  - "Hendrik Bessembinder"
  identifiers: []
  doi_candidates: []
sources:
- id: "source_01"
  role: "main"
  type: "pdf"
  sha256: "81022379704f536f771cf94230a746d96644fa8640ca4ebc4d5771c46d1af7b1"
  path: "original/source_01/Bessembinder_SSRN_2026_RebalancingFrictionalCostsAndReturnsToLeveredSingleStockETFs.pdf"
  pages: 39
supplements: []
attachments: []
extraction:
  run_id: "20261007T084959Z-81022379704f-519f02"
  application_version: "0.3.2"
  adapters:
  - name: "mineru"
    version: "4.0.5"
  timestamp: "2026-10-07T10:10:01+00:00"
validation_report: "validation.json"
---


<!-- source: pdf page 1 -->
# Rebalancing, Frictional Costs, and Returns to Levered Single-Stock ETFs

Hendrik Bessembinder

WP Carey School of Business

Arizona State University

Email: hb@asu.edu

Current Draft: August 31, 2026

## Abstract

I study returns to leveraged single stock ETFs (LSS-ETFs), decomposing the return shortfall relative to a simple benchmark into a component attributable to daily rebalancing trades and one attributable to frictions such as fees, trading costs, and excess loan margins. For my main sample comprised of thirty five ETFs introduced since June 2022, LSS-ETFs underperform by an average of 0.75% per month, with 0.20% attributable to daily rebalancing and 0.55% to frictions. For a supplemental sample of 235 ETFs listed since April 2024 long levered single stock ETFs underperform by an average of 1.47% per month, with 0.42% attributable to daily rebalancing and 1.04% to frictions. Consistent with theory, rebalancing costs are negatively related to return serial correlation as captured by return variance ratios and positively related to daily volatility. Analysis of a broader sample of hypothetical single-stock ETF returns over the past fifty years reveals that LSS-ETFs underperform on average when return volatility is high, not due to volatility per se, but because high volatility periods are characterized by return reversals.

*Footnote (page 1):* * Some results reported here are extracted from a prior working paper titled “Returns to Constant Leverage Strategies: General Principles and Application to Levered Single-Stock ETFs.” I thank George Aragon, Rasoul Foroughfard, Erik Hjalmarsson, Rawley Heimer, Jarrad Harford, Lukas Kremens, Ananth Madhavan, Seth Pruitt, Denis Sosyura, Sunil Wahal, Baolian Wang, Jinming Xue, Feng Zhang, and seminar participants at Arizona State University, Oklahoma State University, and the University of Washington for insightful comments on that version.

<!-- source: pdf page 2 -->
## I. Introduction

The first levered ETFs (LETFs) were introduced in 2006, providing exposure to the returns on stock indices including the Nasdaq 100 and the S&P 500.<sup>1</sup> Additional LETFs were launched in the following years, providing exposure to a broad variety of equities, commodities, fixed income instruments, and foreign currencies. LETFs may appeal to those who wish to hedge other positions, those with strong directional views, and/or those with so-called “lottery preferences.”<sup>2</sup> The growth in LETFs likely reflects that for many investors these products comprise the easiest channel by which to obtain levered long or short positions in financial or commodity markets.

In this paper, I study returns to levered ETFs on individual common stocks, (henceforth LSS-ETFs). While LSS-ETFs were introduced in the U.S. only in 2022, more than four hundred such funds were listed as of mid-2026. This paper has three main goals. First, I document some empirical properties of the returns to LSS-ETFs. I show that while the rebalancing costs that are often but imprecisely referred to as “volatility decay” are substantial, the largest source of underperformance relative to a simple benchmark is an array of frictions including both disclosed expense ratios and the more opaque costs of obtaining leverage through swaps contracts. Second, I test implications developed in Bessembinder (2026) regarding relations between expected LETF returns and the volatility of underlying asset returns. These implications are broadly supported. Third, I obtain large sample evidence by studying the history of hypothetical leveraged ETFs on the individual stocks contained in the CRSP database since 1973.

*Footnote (page 2):* 1 Levered products available to retail investors include both exchange traded funds (ETFs) and exchange traded notes (ETNs). ETFs typically own the underlying asset, often in combination with swaps, while ETNs are unsecured obligations of the issuers.

*Footnote (page 2):* 2 Lottery preference is sometimes referred to as gambling preference or skewness preference. See, for example, Eraker and Ready (2015) and Bali, Brown, Murray, and Tang (2017). Gennaioli, Shleifer, and Vishny (2012) suggest that such investors may neglect “unlikely” risk, leading to excessive issuance of risky securities.

<!-- source: pdf page 3 -->
The main sample of LSS-ETFs that I study is comprised of the funds listed at relatively early dates, ranging from June 2022 to March 2024, to allow for return time series of non-trivial length. However, since this sample contains only thirty-five ETFs on eleven underlying stocks, I report for comparison some outcomes for a supplemental sample of 235 LSS-ETFs listed since April of 2024. To also obtain larger sample evidence, I study hypothetical levered returns to thousands of individual stocks in the CRSP database since 1973. Interestingly, I document that while higher stock-specific volatility is associated with lower average compound returns to levered ETFs in this broad sample, the outcome is attributable entirely to the highest volatility quintile, and is not due to volatility per se, but arises because high volatility periods are empirically characterized by both lower average stock returns and return reversals.

Like levered ETFs that focus on stock indices, multi-day outcomes to LSS-ETFs depend on the sometimes-counterintuitive properties induced by the compounding of random returns in combination with the daily rebalancing trades that are required to ensure constant leverage.<sup>3</sup> Since returns to individual common stocks are generally more volatile than those to diversified stock indices, it can be anticipated that returns to LSS-ETFs will be more volatile and more heavily skewed as compared to levered ETFs on stock indices.<sup>4</sup>

The complexities that arise due to high volatility and skewness in levered single-stock products will likely be accentuated by recent listing decisions. While the initial LSS-ETFs mainly focused on prominent and well-established firms including Apple, Microsoft, Alphabet, Nvidia, Amazon, and Tesla, the industry has more recently launched levered ETFs that deliver exposure to younger and less established equities, including Snowflake Inc., GameStop Inc., IonQ Inc., Roblox, Inc., Trump Media and

*Footnote (page 3):* 3 Rebalancing on a daily basis is a contract design feature of most levered ETFs. In contrast, theory, including for example Magill and Constantinides (1976), Balduzzi and Lynch (1999), and Liu (2004) often suggests the optimality of more flexible rebalancing rules that consider tradeoffs between the costs of trading and the deviation of actual portfolio weights from target weights.

*Footnote (page 3):* 4 The strong positive skewness in compound returns to individual stocks and some implications thereof are documented in Bessembinder (2018) and Farago and Hjalmarsson (2023), among others.

<!-- source: pdf page 4 -->
Technology Group, Oklo, Inc., ARM Holdings, PLC., Robinhood Markets, Inc., MicroStrategy (since renamed Strategy), and SoundHound AI, Inc.<sup>5</sup> A total of more than 400 LSS-ETFs were listed in the U.S. as of July 2026.<sup>6</sup> In addition, while the initial long LSS-ETFs targeted leverage of 2x or less, LSS-ETFs that provide 3x leverage have been proposed.<sup>7</sup>

The expansion of this product class to smaller and riskier stocks increases the relevance of the fact that target returns on levered funds can be less than or equal to -100%.<sup>8</sup> While a target daily return less than -100% has not, to my knowledge, occurred for any levered ETF listed in the U.S., this outcome was observed in October 2025 for an LETF on Advanced Micro Devices listed in London.<sup>9</sup> My calculations show that if levered ETFs had been listed on all individual common stocks contained in the CRSP database since 1973, target returns less than or equal to -100% would have been observed an average of 2.8 times per trading day for triple levered funds and 2.2 times per trading day for double inverse funds. It will likely only be a matter of time until such an event occurs for a U.S.-listed LSS-ETF.

While industry observers and academics (e.g., Pessina and Whaley (2021) and Kahn (2018)) often advise against holding levered ETFs across multiple days, it is likely that some investors do so. Indeed, the median daily turnover (volume divided by shares outstanding) for the sample of actual LSS-ETFs the sample I study is 0.22, suggesting that five days is the average holding period. Of course, the
<!-- source: pdf page 5 -->
average reflects that some traders hold their positions for a day or less, while others hold positions for longer periods.

*Footnote (page 4):* 5 For the specific examples listed, see [https://finance.yahoo.com/news/defiance-launches-first-mover-single-070000678.html,](https://finance.yahoo.com/news/defiance-launches-first-mover-single-070000678.html) as well as the listing of ETFs available at [www.tuttlecap.com/etfs.](http://www.tuttlecap.com/etfs)

*Footnote (page 4):* 6 https://www.kalkine.com/by-topic/etf/us-leveraged-etf-growth-explodes-to-a-record-700-funds-more-than-double-2024s-total?

*Footnote (page 4):* 7 See, for example, [sec.gov/Archives/edgar/data/1976322/000182912625007891/themesetftrust_485apos.htm](https://www.sec.gov/Archives/edgar/data/1976322/000182912625007891/themesetftrust_485apos.htm) and [https://www.sec.gov/Archives/edgar/data/1424958/000119312525230257/d78340d485apos.htm.](https://www.sec.gov/Archives/edgar/data/1424958/000119312525230257/d78340d485apos.htm)

*Footnote (page 4):* 8 Limited liability implies that ETF investors will not suffer a loss worse than -100%. However, some party will absorb any excess loss should it occur.

*Footnote (page 4):* 9 The event is described in https://www.bloomberg.com/news/newsletters/2025-10-10/one-day-wipeout-of-an-amd-product-reminds-investors-of-3x-etf-risks. Prior events of interest in U.S. markets include the April 20, 2020, when the futures settlement price for the May 2020 crude oil contract was negative. However, the relevant levered ETF did not track the price of that contract, but rather tracked the Bloomberg Commodity Balanced WT index, which included contracts for multiple delivery dates, and ETF prices remained positive. In February 2018 the VIX volatility index increased by 102% on a single day. However, the relevant inverse ETF promised to deliver the inverse of the VIX futures return, which was less than 100%, not the VIX itself. Thus, neither of these wellpublicized events provided indication of the distribution of losses in cases where the target ETF return is less than - 100%.

It is in any case of interest to better understand the implications of leverage, volatility, skewness, and rebalancing for compound outcomes. I therefore study both daily and compound returns to LSS-ETFs. I decompose the difference between actual ETF returns and a simple benchmark into two components. The first is attributable to the effect of the daily rebalancing trades that maintain constant leverage, and the second is attributable to the combined effects of various “frictions,” including management fees, fund trading costs, changes in ETF premia or discounts relative to underlying asset value, short selling costs, as well as any interest rate margins embedded in swap terms or borrowing rates. I find for my main sample that monthly returns to the LSS-ETFs in the sample underperform the simple benchmark by an average of 0.82% per month, with 0.44% underperformance attributable to the effects of daily rebalancing and 0.38% attributable to frictions. I also document asymmetries that are consistent with the implications of Bessembinder (2026), as friction costs in the main sample are larger for positive leverage (average of 0.53% per month) than for inverse leverage funds (average of 0.27% per month), while rebalancing costs are larger for negative (average of 0.73%) than for positive leverage (average of 0.27%) funds. For the supplemental sample of 235 LSS-ETFs listed since April 2024 monthly returns to the LSS-ETFs in the sample underperform the simple benchmark by an average of 1.34% per month, with 0.34% underperformance attributable to the effects of daily rebalancing and 0.99% attributable to frictions, It will be of interest for future research to assess the reasons for the notable increase in costs.

I also test the implications developed in Bessembinder (2026) regarding relations between return volatility and compound returns to levered ETFs. He emphasizes that in contrast to a frequently-voiced perspective, there is no hard-wired negative relation between volatility and expected levered ETF returns. He predicts that rebalancing costs (which are sometimes inaccurately referred to as “volatility drag”) depend on return serial correlations, as captured by variance ratios. He also predicts that rebalancing

<!-- source: pdf page 6 -->
costs will be asymmetric across long versus inverse levered ETFs. Each implication is strongly supported.

Perhaps not surprisingly, LSS-ETFs have attracted additional recent attention from researchers. Murray and Sammon (2026) show that LSS-ETFs tend to be launched on stocks with both high recent returns and high recent volatility, and that investor flows into these funds, while contrarian, do not predict returns. Kim, Han, and Won (2026) examine SEC filings and document that swap financing rates for LSS-ETFs are not only larger than disclosed expense ratios (thereby helping to explain the high frictional costs I report), but vary substantially across counterparties even for the same underlying stock at the same time.

## II. Benchmark Returns, Rebalancing Costs, and Frictional Costs.

Let $R _ { t } ^ { s }$ denote the day t return on the underlying stock, and let $\beta$ denote the fund’s target leverage ratio. While the expressions here are equally valid for any $\beta ,$ I will focus on levered ETFs, for which $\beta$ is typically greater than one or less than zero. Letting $r _ { t }$ denote the day t benchmark interest rate, and ignoring frictions such as loan or swap margins in excess of benchmark rates, trading costs, and fees, Avellaneda and Zhang (2010) show that the single day return to a daily-rebalanced levered ETF is:

$$
R _ {t} ^ {R B} = \beta R _ {t} ^ {S} + (1 - \beta) r _ {t},\tag{1}
$$

Where the RB subscript refers to daily rebalancing. The interest rate appears in expression (1) to reflect the cost of borrowing to obtain positive leverage $( \beta > 1 )$ , or interest on invested capital and short sales proceeds in the case of negative leverage.<sup>10</sup> Note that expression (1) does not rule out levered returns that are less than -100%, as discussed further in Section IV.

*Footnote (page 6):* 𝛽𝛽 > 1,

*Footnote (page 6):* (𝛽𝛽 − 1).

*Footnote (page 6):* 10 Expression (1) presumes that for funds where all investor capital is placed in the underlying asset, so that the borrowing cost is only applied to the quantity If, instead, the ETF provider places a proportion of the capital, d, into a deposit account, then an additional cost in the amount of d times the excess of the borrowing rate over the deposit rate would enter the expression. This amount would be captured as part of the frictional cost in my analysis, though it might alternatively be labeled as an agency cost.

<!-- source: pdf page 7 -->
Let $R _ { T } ^ { S }$ and $R _ { T } ^ { R B }$ denote compound (buy-and-hold) T-day returns on the underlying stock and the levered ETF, respectively, determined as:

$$
R _ {T} ^ {S} = \prod_ {t = 1} ^ {T} (1 + R _ {t} ^ {S}) - 1\tag{2a}
$$

and

$$
R _ {T} ^ {R B} = \prod_ {t = 1} ^ {T} (1 + R _ {t} ^ {R B}) - 1\tag{2b}
$$

respectively, where the RB superscript in (2b) denotes rebalanced.

## a. Frictionless Benchmarks

Letting $r _ { T }$ denote the compound benchmark interest rate over the interval t = 1 to T, a simple benchmark by which to evaluate multiperiod outcomes to levered ETFs is the multiperiod analog to expression (1):

$$
R _ {T} ^ {B H} = \beta (R _ {T} ^ {S} - 1) + (1 - \beta) r _ {T},\tag{3}
$$

where the BH notation reflects that the return is to a levered “buy and hold” approach. It might be argued that the use of expression (3) to define a benchmark reflects a naïve view, because levered ETFs typically aim to deliver returns that are a fixed multiple of daily, not compound, underlying returns. Yet the focus on daily returns is a contract design choice; levered ETFs can alternatively target a multiple of multiday underlying returns.<sup>11</sup> Perhaps more important, in the absence of frictions an investor could herself capture the return specified by this expression with the simple strategy of borrowing to invest or by short selling, without the need for any trades after the position is initialized at $t = 0 .$ In contrast, maintaining constant daily leverage requires the ETF providers to make daily rebalancing trades. Expression (3) therefore comprises a natural benchmark for assessing the impact of rebalancing trades, distinct from the effects of
<!-- source: pdf page 8 -->
various frictions. In particular, expression (3) outcomes can be compared against outcomes with daily rebalancing to maintain constant leverage. Using (1) in (2b) gives the compound rebalanced return as:

*Footnote (page 7):* 11 For example, Tradr ETFs in October 2024 introduced levered ETFs that target fixed multiplies of quarterly stock index returns. Crouse (2019) examines eight exchange traded products with both daily and monthly rebalancing, and reports better average performance for the latter.

$$
R _ {T} ^ {R B} = \prod_ {t = 1} ^ {T} (1 + \beta R _ {t} ^ {S} + (1 - \beta) r _ {t}) - 1.\tag{4}
$$

## c. Rebalancing Trades

Cheng and Madhavan (2009) show that to maintain constant leverage requires end-of-day purchases (sales if negative) in the underlying asset equal to $( \beta ^ { 2 } - \beta ) R _ { t } ^ { S }$ per dollar invested at the end of the prior day.<sup>12</sup> Since $( \beta ^ { 2 } - \beta )$ is positive for $\beta \ge 1$ and for $\beta \leq 0 ,$ , both levered and inverse ETFs must trade in the same direction as the underlying return, buying after positive returns and selling after negative, to maintain constant leverage. These rebalancing trades might therefore reasonably be labeled as momentum trades.<sup>13</sup>

## d. A Return Decomposition

Let $R _ { T } ^ { R B , A c t }$ denote the outcome obtained if actual daily ETF returns are employed in expression (4). These represent outcomes to an investor who enters the levered ETF and does not trade for the rest of the T-day period, even while the ETF provider makes daily rebalancing trades. The difference between the non-rebalanced and frictionless benchmark given by expression (3) and the actual compound ETF return can be decomposed into two components:

$$
R _ {T} ^ {B H} - R _ {T} ^ {R B, A c t} = [ R _ {T} ^ {B H} - R _ {T} ^ {R B} ] + [ R _ {T} ^ {R B} - R _ {T} ^ {R B, A c t} ].\tag{5}
$$

*Footnote (page 8):* 12 The daily trading can be accomplished by negotiating with a counterparty a change in the magnitude of an existing total return swap. In this case the swap counterparty may elect to trade the underlying stock to maintain its hedge ratio.

*Footnote (page 8):* 13 An important empirical question, studied by Cheng and Madhavan (2009) and Ivanov and Lenkey (2018), among others, is whether levered ETF rebalancing trades (whether undertaken by the fund itself or swap counterparties) executed at or near the close of daily trading tend to magnify daily price moves. Trades’ price impacts are likely to be greater for less liquid securities, including some individual stocks. It will be informative to revisit this question when the time series of LSS-ETFs on less liquid common stocks becomes longer.

<!-- source: pdf page 9 -->
Positive outcomes in expression (5) represent costs for ETF investors as compared to the frictionless buy and-hold benchmark, while negative outcomes represent benefits. Even though it is misleadingly referred to by some as “volatility drag”, the first cost component, $[ R _ { T } ^ { B H } \mathrm { ~ \textbar ~ } R _ { T } ^ { R B } ]$ , is fully attributable to the effects of daily rebalancing trades, and I will refer to it as the rebalancing cost. The second cost component $[ R _ { T } ^ { R B } \textbar { - } R _ { T } ^ { R B , A c t } ]$ captures frictional costs, which include management fees, trading costs, changes in ETF premia or discounts relative to underlying asset value, or short selling costs.<sup>14</sup> Further, the interest rates embedded in swap terms typically exceed (particularly for long leverage) the benchmark interest rates employed to define the frictionless returns in expressions (3) and (4), in which case such excess interest costs comprise an additional friction. Frictional costs cause the actual compound ETF return to fall short of the frictionless benchmark given by (4). Note that since my empirical implementation is based on returns as reported by CRSP, I do not capture the additional costs incurred by investors as they trade ETFs, such as bid-ask spreads or price impacts.

Farago and Hjalmarsson (2023) show that the main determinant of positive skewness in compound returns is the volatility of single period returns. Since single stock returns tend to be more volatile than equity indices, and leverage effectively increases volatility, it can be anticipated that positive skewness will be a particularly important feature of compound LSS-ETF returns. Farago and Hjalmarsson (2023) also show that empirical estimates of the skewness coefficient are downward biased. Further, estimated skewness coefficients are known to be strongly affected by outliers. For those reasons, I report for LSS-ETFs a robust empirical measure of skewness, attributable to Bowley (1920).<sup>15</sup> Letting $P _ { i }$ denote percentile i of a given distribution, the robust skewness measure I use is: 𝑅𝑅𝑅𝑅𝑏𝑏𝑏𝑏𝑏𝑏𝑏𝑏𝑏𝑏 = $\frac { P _ { 9 9 }   +   P _ { 1 }   -   2 P _ { 5 0 } } { P _ { 9 9 }   -   P _ { 1 } }$ In a positively (negatively) skewed distribution the $9 9 ^ { \mathrm { t h } }$ percentile exceeds the median by
<!-- source: pdf page 10 -->
more (less) than the median exceeds the 1<sup>st</sup> percentile, so the robust skewness measure is positive (negative). The denominator standardizes the measure, so that the outcome always lies between -1 and 1.

*Footnote (page 9):* 75

*Footnote (page 9):* 25,

*Footnote (page 9):* 14 In addition, Bianchi and Goldberg (2026) assert that deviations of actual leverage from target leverage impose costs on investors in leveraged ETFs. Such costs would also be captured as frictional costs in this framework. 15 Bowley recommended the use of 𝑃𝑃 and 𝑃𝑃 but as noted by Hinkley (1975) any symmetric pair of percentiles can be employed. Kiman and White (2004) delve further into the robust estimation of skewness.

## III. Outcomes to Levered Single-stock ETFs Launched Since 2022

In this section I report on empirical outcomes for a sample of returns on actual single-stock ETFs. I identify the single-stock ETFs included in the study using data provided by Morningstar.<sup>16</sup> To allow for a return time series with a meaningful number of observations I retained for my main sample only those funds that were launched prior to March 31, 2024. However, I also report certain results for a supplemental sample of 235 LSS-ETFs launched between April 2024 and December 2025. I obtain from CRSP daily return and market capitalization data for these funds and their underlying stocks from the date of fund inception through December 31, 2025. To measure benchmark borrowing costs I employ data on the Federal Funds interest rate from the Federal Reserve Bank of St. Louis.<sup>17</sup> That is, the Federal Funds interest rate is included in the frictional benchmark outcomes, while any divergence of actual borrowing rates from the Federal Funds rate is a component of the frictional costs that I estimate.

Table 1 contains descriptive data regarding the main sample, which includes thirty-five ETFs that provide exposure to returns on eleven underlying stocks. Four ETFs are based on returns to Apple stock, two on Advanced Micro Devices, three on Amazon, one on Alibaba, one on Coinbase, three on Alphabet, one on Meta, four on Microsoft, seven on Nvidia, one on Paypal, and eight on Tesla. Twenty two of the funds provide levered positive exposure (ranging from $\beta = 1.25  to  2.0$ and thirteen provide inverse exposure (ranging from $\beta = -1.0   to   -2.0$ . The earliest were introduced in mid-July 2022. Two sample funds delisted prior to the end of the sample period.<sup>18</sup> Some ETFs changed leverage targets within the

*Footnote (page 10):* = 1.0

*Footnote (page 10):* β= 1.5

*Footnote (page 10):* 16 I thank Jeff Ptak at Morningstar for assistance in identifying the ETFs included in the sample.

*Footnote (page 10):* 17 The Federal Funds rate is reported on a monthly basis. To assign a daily interest rate, I divide the monthly rate by the number of trading days within the month.

*Footnote (page 10):* 18 These are ticker symbol PYPT, which provided 𝛽𝛽 = .5 positive exposure to Paypal stock and delisted in August 2023, and AMDS, which provided 𝛽𝛽 - exposure to AMD stock and delisted in June 2025.

<!-- source: pdf page 11 -->
sample period, and Table 1 reports on the minimum and maximum leverage within the sample period for each ETF. The Table also reports on the time-series average and the final-date market capitalization of each levered ETF. The largest funds are TSLL, which provides positive exposure to Tesla, with market capitalization of $5.98 billion as of the end of the sample, and NVDL which provides positive exposure to Nvidia, with market capitalization of $4.74 billion as of the end of the sample.

## A. Daily Returns

Table 1 also reports on average daily returns for each fund and for its underlying stock (during the same dates the ETF was active). The cross-fund average of daily stock returns was 0.16% per day, while the cross-fund average ETF return was 0.05% per day, with the lower mean reflecting in part the presence of negative leverage funds. The cross-fund average standard deviation of daily stock returns was 2.79%, while the cross-fund average ETF return standard deviation was 4.68%. The 0.16% mean daily stock return in this sample (with a rough annualized equivalent of 40%) is considerably larger than would have been predicted by economic models or based on broader samples of stock returns. As a consequence, the magnitudes of the positive returns to long levered funds and of the negative returns to short levered funds as described below likely reflect in part random outcomes.

The median daily turnover (trading volume divided by shares outstanding) for the full sample of ETFs is 0.222, suggesting a median holding period in the vicinity of five days. Of course, some investors may hold their ETF positions for only minutes, while others may do so for weeks. By comparison, the median daily turnover for the underlying stocks is 0.011, so it is clear that investors in LSS-ETFs are much more active than investors in the underlying shares.

Figure 1 displays the total market capitalization for sample funds on a daily basis from July 15, 2022 to December 31, 2025. The sample grew from three funds with a combined market capitalization of just $6.4 million on the first date to thirty-three funds with a combined capitalization of $17.1 billion at

<!-- source: pdf page 12 -->
the end of the sample in December 2025.<sup>19</sup> Figure 1 also displays the combined market capitalization of positive (β > 1) and inverse (β < 0) leverage funds. Long levered funds’ market capitalization has grown to more than twenty times larger than inverse funds by the end of the sample.

Table 2 provides additional information regarding daily levered ETF and underlying stock returns. It should be kept in mind that funds were introduced at various dates as summarized in Table 1, so that mean underlying stock returns as well as return volatilities and autocorrelations differ across funds, even when each is based on the same stock. For funds with positive leverage the average daily return was 0.24%. Funds with inverse leverage had a mean daily return of -0.23%. Table 2 also reports on median daily ETF returns and on the robust measure of skewness in daily ETF returns. The skewness of daily ETF returns to the pooled sample of positive leverage funds was 0.049, compared to -0.029 for all negative leverage funds.

In addition to reporting on actual ETF returns, Table 2 reports on the average frictionless ETF return implied by underlying stock returns and expression (1). The difference in mean actual returns versus mean frictionless returns reveals the average daily friction cost attributable to management fees, trade execution costs, and leverage costs that differ from the Federal Funds rate that is employed to define the frictionless benchmark. For the full sample, the average frictionless ETF return is 0.078%, compared to an average actual ETF return of 0.056%. The difference of 0.022% per day is the average friction cost.

Comparing average friction costs across positive and negative leverage funds reveals an interesting asymmetry. For funds with positive leverage, the average friction cost is 0.026% per day, while for funds with negative leverage, the average friction cost is 0.014% per day. This divergence may reflect higher implicit borrowing costs (relative to the federal funds rate) in swap terms for long leverage as compared to implicit deposit rates in swap terms for short leverage. It may also reflect that increased
<!-- source: pdf page 13 -->
short interest at an ETF-providing firm with larger long than short net asset values may reduce rather than increase the firm’s net swap positions and trading, thereby reducing rather than increasing costs.

*Footnote (page 12):* 19 By comparison, ETF.com reports that the total assets under management of 337 levered ETFs (including equity index, fixed income, foreign exchange, and commodity funds) amounted to $128.4 billion. [Levered ETFs: Strategies & News | etf.com,](https://www.etf.com/topics/leveraged) accessed June 17, 2025.

## B. Compound Returns

Table 3 reports on mean and median compound fund returns, at the weekly (Monday to Friday) and calendar month horizons. For comparison, the Table also reports mean frictionless benchmark returns that are computed based on expressions (3) and (4), as well as mean returns to the underlying stocks and mean rebalancing and frictional costs.

Bessembinder (2026) predicts that rebalancing costs will be positive if return autocorrelations are on balance negative, as evidenced by return variance ratios (VRs) less than one. This implication follows directly from the point that LSS-ETF rebalancing trades are effectively momentum trades, with purchases in response to positive returns and vice versa. I compute the VR of underlying stock returns at both the weekly (dividing the variance of the sum of returns within the week by the product of the average number of trading days per week and the variance of daily returns) and monthly (dividing the variance of the sum of returns within the month by the product of the average number of trading days per month and the variance of daily returns). The average VR across funds is 0.94 at the weekly horizon and 0.84 at the monthly horizon. Thus, consistent with empirical evidence for broader samples based on earlier decades, the prominent stocks underlying the sample ETFs display negative return autocorrelation at the weekly and monthly horizons.<sup>20</sup> Since VRs are on average less than one, positive average rebalancing costs are predicted.

Panel A of Table 3 reports results compounded across days, by week. Focusing first on the full sample of 4,941 fund/weeks, the mean levered ETF return is 0.22%, as compared to the mean frictionless benchmark of 0.37% given by expression (3). The mean underperformance of 0.15% is comprised of

*Footnote (page 13):* 20 Jegadeesh (1990) documents significant reversals of price changes for CRSP common stocks at the monthly horizon, Lehmann (1990) reports similar outcomes at the weekly horizon, and Hendershott, Menkveld, Praz, and Seasholes (2022) estimate that “pricing errors” (which are subsequently reversed) explain a significant portion of daily, monthly, and quarterly return variances for NYSE-listed stocks.

<!-- source: pdf page 14 -->
0.05% attributable to daily rebalancing and 0.10% attributable to friction costs. The mean underperformance relative to benchmark is reasonably similar across positive levered funds (0.14%) and inverse funds (0.17%). In the case of positive levered funds this underperformance is more attributable to frictional costs (0.13%) than to daily rebalancing (0.02%), while for inverse funds it is more attributable to daily rebalancing (0.11%) than to frictional costs (0.07%). The larger rebalance costs for inverse leverage funds is consistent with Implication (3) in Bessembinder (2026), and simply reflects that the term $( \beta ^ { 2 } - \beta )$ that Chen and Madhavan show to be a determinant of the quantity of trading required to rebalance is smaller for any given positive 𝛽𝛽 than for its opposite.

Results reported in Panel B of Table 3 when returns are compounded at the monthly horizon provide similar insights. For the full sample of 1158 fund/months, the mean levered ETF return is 0.76%, compared to the frictionless benchmark return of 1.58%. The mean underperformance of 0.82% is attributed 0.38% per month to daily rebalancing and 0.44% to frictional costs.

For positive leverage funds the average actual monthly fund return is 4.51%, reflecting the unusually strong performance of the underlying stocks, which averaged 3.05% per month. The average frictionless benchmark return with monthly rebalancing for the positive leverage funds was higher yet, equal to 5.27% per month. The 0.75% mean underperformance relative to benchmark for positive leverage funds is attributable 0.20% to daily rebalancing and 0.55% to frictions. Underperformance of 0.75% per month is large in economic terms, particularly when compared to the typical returns on underlying stocks rather than the unusually large returns earned by sample stocks during the period studied. The friction cost of 0.55% per month, or about 6% per year, in particular is large relative to stated fund expense ratios, and likely reflects that the implicit cost of borrowing embedded in swap terms exceeds the Federal Funds rate that I employ as the benchmark interest rate in the frictionless benchmarks, as documented in more detail by Kim, Han, and Won (2026).

For inverse funds the average frictionless benchmark return with monthly rebalancing is -4.15%, while the mean average actual fund return is -5.08%. The mean underperformance relative to benchmark
<!-- source: pdf page 15 -->
of 0.93% is attributable 0.66% to daily rebalancing and 0.27% to frictions. That rebalancing costs are larger for negative than positive leverage funds again supports Implication (3) in Bessembinder (2026).

The robust skewness statistics for monthly returns reported in Panel B of Table 3 are larger than those reported in Table 2 for daily returns. For positive levered ETFs the robust skewness statistic is 0.24, while for negative levered ETFs it is 0.14. By comparison, daily negative leverage ETF returns were slightly negatively skewed. These results reflect that compounding induces and magnifies positive skewness. It bears emphasizing that the large positive skewness in compound LSS-ETF returns implies that the majority of potential outcomes will be less than the mean or expected outcome.

My main sample focuses on thirty five LSS-ETFs listed at least 21 months before the end of the sample period. However, for comparison I also compute outcomes at the monthly horizon for a supplemental sample of 235 LSS-ETFs that were listed subsequent to March 2024. These results are reported in Panel C of Table 3. While mean rebalance costs are similar for the main sample (0.38%) and for the supplemental sample (0.34%), mean frictional costs have more than doubled, from 0.44% per month in the main sample to 0.99% per month in the supplemental sample. The reasons for the dramatic increase in frictional costs to an average of more than 12% per year on an annualized basis are deserving of careful additional study.

I next report on more specific tests regarding rebalance costs. In particular, I estimate cross-sectional regressions where the dependent variable is the mean rebalancing cost for each of the thirty five funds in the main sample, and explanatory variables are the mean daily return, the variance of daily returns, and the return VR of the underlying stock. Standard errors are clustered at the stock level. Bessembinder (2026) predicts that rebalancing costs should increase with return volatility, and decrease with return autocorrelations, as captured by the VR.

<!-- source: pdf page 16 -->
Results obtained by estimating this regression are reported in Panel A of Table 4. Coefficient estimates on the mean daily return are insignificant.<sup>21</sup> The coefficient estimates on the variance of daily returns are positive and, despite the small sample size, are significant at both the weekly and monthly horizons (t-statistics are 2.54 and 2.36, respectively). Coefficient estimates on the return VR are negative and significant at both the weekly and monthly horizons; t-statistics are -2.59 and -3.17, respectively). That is, average rebalancing costs increase with return volatility and decrease with return serial correlations as captured by return VRs, as predicted in Bessembinder (2026).

In Panel B of Table 4, I report outcomes obtained from cross-sectional regressions of mean fundlevel rebalancing costs on predicted costs obtained when employing stock parameter estimates in Expression (13) developed in Bessembinder (2026). Slope coefficients are positive and highly significant (t-statistics are equal to 9.94 and 4.78) at both the weekly and monthly horizons. Further, the slope coefficient estimates of 1.11 and 0.88, respectively, do not differ significantly from the benchmark of one. The regression r-squared statistics are 0.77 and 0.59 at the weekly and monthly horizons. That is, despite the facts that simplifying assumptions are employed, the predicted costs are based on a third-order approximation, and input parameters including mean returns, return volatilities, and VRs are estimates obtained from relatively short sample periods, the actual rebalancing costs for the thirty-five LSS-ETFs in the sample are quite well explained by expression (13) in Bessembinder (2026).

## IV. How would Levered Single-stock ETFs have performed historically?

While studying returns to actual LSS-ETFs launched since mid-2022 is informative, the analysis is limited by the relatively short time series of returns and by the fact that the main sample is based on only eleven stocks. Historical daily returns are available for thousands of common stocks across multiple decades, allowing for the computation of millions of hypothetical daily levered returns on individual stocks. In particular, the data on actual daily stock returns and interest rates can be used in expression (1)

*Footnote (page 16):* 21 Bessembinder (2026) notes the rebalance costs are predicted to decline with mean stock returns in the two period case, but that the relation is ambiguous over longer horizons.

<!-- source: pdf page 17 -->
to obtain hypothetical levered daily returns and in expression (4) to obtain hypothetical compound levered returns. Further, the hypothetical compound ETF return given by expression (4) can be compared to the levered buy-and-hold benchmark return implied by expression (3) to assess the effect of daily rebalancing in a much broader sample. While these hypothetical returns do not reflect the frictional costs that would have applied to actual ETFs, they are informative regarding the effects of leverage-enhanced risk and daily rebalancing for single-stock ETFs. All references to levered ETF returns in this section should be understood to apply to hypothetical historical returns in the absence of any frictions.

## A. Hypothetical Daily Levered Returns

To compute hypothetical LSS-ETF returns, I obtain daily return data for all common stocks contained in the CRSP database from January 1974 to December 2024.<sup>22</sup> As in the analysis of actual ETF returns, I rely on Federal Funds interest rate data from the Federal Reserve Bank of St. Louis as the benchmark interest rate. I compute hypothetical levered daily returns according to expression (1) for leverage factors β = 3, β = 2, β = 1 (unlevered), β = -1, and β = -2.

Panel A of Table 5 reports summary statistics regarding the 69.6 million hypothetical daily ETF returns. The mean unlevered daily stock return is 0.083%. Mean hypothetical ETF returns increase with leverage, to 0.147% with β = 2 and to 0.210% with β = 3, and are negative for inverse funds (-0.043% for $\beta = -1   and   -0.107\%   for   \beta = -2$

The distribution of daily returns to unlevered stocks is positively skewed with a robust skewness statistic equal to 0.088. For daily returns, leverage does not meaningfully alter the skewness statistic, though inverse leverage reverses the sign. The presence of skewness can also be observed from the facts that, for positively levered positions, mean returns exceed median returns (while with negative leverage
<!-- source: pdf page 18 -->
medians exceed means), and $9 9 ^ { \mathrm { t h } }$ percentile returns are large, equal for example to 42.21% when $\beta = 3$ and to 23.69% when $\beta = - 2$

*Footnote (page 17):* 22 The CRSP return data includes delisting returns, which reflect CRSP’s assessment of the final payment or market value subsequent to delisting events.

## a. Target Returns Less than -100%.

A potentially underappreciated complexity is that the levered return specified by expression (1) can be less than -100%. The higher volatility of single stocks as compared to stock indices brings this issue to the fore. Ignoring daily interest for simplicity, positively levered daily returns computed according to (1) are less than -100% if $R _ { S } < - \left( \frac { 1 } { \beta } \right)$ , while inverse levered returns are less than -100% if $R _ { S } > - \left( \frac { 1 } { \beta } \right)$ . While returns outside these boundaries have not, to date, been observed for any of the eleven stocks that underlie the LSS-ETFs studied in Section III above in the period since the funds were launched, they have occurred historically with some frequency. For example, the return to Apple stock on September 29, 2000, was -51.9%, implying target returns less than -100% for hypothetical funds with $\beta > 1 . 9 3$

The data reported in Panel A of Table 5 shows that hypothetical returns less than -100% would have been observed for 0.053% of stock/days for funds with leverage equal to $\beta = 3, 0.027\%$ of stock days with leverage of $\beta = 2, 0.054\%$ of stock days with leverage of $\beta = - 1$ , and 0.082% of stock days with leverage of $\beta = - 2$ . The sample includes 69.6 million returns on 12,861 trading days, so levered returns as implied by expression (1) less than -100% would have been observed an average of 2.8 times per trading day for triple levered (β = 3) funds and 2.2 times per trading day for double inverse (β = -2) funds.

The implied losses from a single-day target return less than -100% can be very large. GameStop Inc. (GME) provides a noteworthy example. The cumulative (buy-and-hold) value as of January 28, 2021 of $1 invested at the end of December 2020 in a hypothetical $\beta = 3$ fund would have been, according to expression (2b), negative $150.85. Because of the well-publicized runup in the GME stock price earlier in the month, the value of the $1 investment in this hypothetical ETF grew to $458.94 as of January 27. On January 28, the non-levered GME return was -44.3%, leading to a target $\beta = 3$ ETF return of -132.9%.

<!-- source: pdf page 19 -->
With the buy-and-hold strategy this return would have applied not to the original $1 investment, but to the prior day value of $458.94, implying an end-of-day value of -$150.85.

Of course, a target return less than -100% does not apply to an investor who enjoys limited liability, whose return cannot be less than -100%. The monetary gains and losses on levered ETFs ultimately reflect a zero-sum wager across participants; if a levered ETF participant loses a given amount, then one or more other participants gain the same amount. Consequently, if the product of target leverage and the underlying return is less than -100%, the excess loss is absorbed by someone; if not by the ETF investor herself, then by other ETF investors, the sponsoring firm, a swap counterparty, a lender, or some other party. While a target daily return less than -100% has not, to my knowledge, occurred for any levered ETF listed in the U.S., this outcome was recently observed for a β = -3 ETF on Advanced Micro Devices listed in London.<sup>23</sup> It will likely only be a matter of time until such an event occurs for a U.S.- listed product.

As noted, the data in Panel A of Table 5 pertains to all common stocks in the CRSP database. However, smaller capitalization stocks tend to be less liquid and less frequently traded. It seems likely that, had single stock ETFs existed in the past, they would have focused on larger stocks, consistent with the evidence provided by Murray and Sammon (2026) regarding actual recent listings. Panel B of Table 5 reports on daily returns for the subsample of stocks with a minimum prior-day inflation-adjusted (to December 2024 dollars) market capitalization of $1 billion. This restriction reduces the sample size to 18.7 million stock days, and results in mean returns closer to zero, fewer returns that are less than -100%, and less skewness.

*Footnote (page 19):* 23 The event is described in https://www.bloomberg.com/news/newsletters/2025-10-10/one-day-wipeout-of-an-amd-product-reminds-investors-of-3x-etf-risks. Prior events of interest in U.S. markets include the April 20, 2020, when the futures settlement price for the May 2020 crude oil contract was negative. However, the relevant levered ETF did not track the price of that contract, but rather tracked the Bloomberg Commodity Balanced WT index, which included contracts for multiple delivery dates, and ETF prices remained positive. In February 2018 the VIX volatility index increased by 102% on a single day. However, the relevant inverse ETF promised to deliver the inverse of the VIX futures return (which was less than 100%), not the VIX itself. Thus, neither of these wellpublicized events provided indication of the distribution of losses in cases where the target ETF return is less than -100%.

<!-- source: pdf page 20 -->
For the remainder of this section, I focus on outcomes that incorporate the $1 billion minimum market capitalization requirement. In the remaining cases where a daily return is less than 100%, I compute the compound return up to and including that date only, omitting returns for the remainder of the calendar interval. For these cases I compile the compound return both assuming a floor of -100% (i.e., that the additional loss is absorbed by a party other than the ETF investor) and without the floor.

## B. Compound Returns to Hypothetical ETFs

I use expression (4) to compute compound returns to hypothetical single-stock ETFs and expression (3) to compute levered, non-rebalanced, benchmarks. I study non-overlapping weeks (Monday to Friday) and calendar months. Table 6 reports on the frequencies with which compound returns exceed or fall short of certain benchmarks, including -100%, zero, the levered but non-rebalanced return given by expression (3), and the non-levered return to a value-weighted portfolio of all common stocks over the same days as the ETF return is computed.<sup>24</sup> Most of the patterns that can be observed in Table 6 are attributable to: (1) negative leverage positions are on average “fighting the flow” attributable to positive mean return to the underlying stocks, while levered positive positions are “going with the flow,” (2) the distribution of compound returns is positively skewed, and (3) leverage, both positive and negative, increases both volatility and skewness.

Negative returns occurred more frequently than positive returns, especially at longer horizons. Focusing on β = -2, for example, the percentage of ETF returns that are positive are 47.5% and 42.5% at the weekly and monthly horizons, respectively. While positive levered ETFs are more likely to deliver positive returns than inverse ETFs, and despite the fact that unlevered stock positions are more likely to deliver positive returns as the horizon increases (60.9% of unlevered annual returns are positive), positive levered ETF positions are also less likely to deliver positive returns as the horizon lengthens. Focusing

*Footnote (page 20):* 24 The Table also reports on the average number of trading days employed to compute the ETF returns. The number of trading days is reduced for all stocks by exchange holidays, and is reduced for some stocks during some periods because the stock is initially listed after the start or delisted prior to the end of the calendar interval. Further, I drop some stocks for the remainder of a calendar interval after the realization of an ETF return less than -100%.

<!-- source: pdf page 21 -->
on $\beta = 3 ,$ , for example, the percentage of ETF returns that are positive are 49.5% and 49.4% at the weekly and monthly horizons.

The likelihood that a LSS-ETF generates a target compound return less than -100% is small, but increases with horizon. With $\beta = 3$ , the percentage of levered return outcomes less than -100% are 0.04% and 0.18% at the weekly and monthly horizons, respectively.

The percentage of levered ETF returns that outperform their corresponding levered but non-rebalanced benchmark as specified by equation (3) is always below 40%, and is relatively stable across compounding horizons and leverage, ranging from 38.06% $( \beta = 3$ in weekly returns) to 32.53% $( \beta = - 1$ in monthly returns). The difference between the levered ETF returns computed according to expression (4) and the benchmark return given by expression (3) is attributable to daily rebalancing, so these outcomes indicate that daily rebalancing reduces ETF returns more often than not.

Finally, the percentage of hypothetical levered ETFs that outperform the unlevered return to the value-weighted portfolio of all common stocks is always less than 50%, is greater for positive levered than inverse levered stocks, and decreases with compounding horizon. At the weekly horizon, for example, the percentage of $\beta = 2$ ETFs that outperform the unlevered value-weighted market return is 48.99%, while the percentage of β = -2 ETFs that outperform the value weighted market return is 46.11%.

Table 7 provides additional information regarding the distribution of compound returns to hypothetical LSS-ETFs. Panels A and B pertain to weekly and monthly holding periods, respectively. Except where noted all statistics on Table 7 are based on the returns computed according to expressions (4), without a floor at -100%. Several noteworthy results can be observed.

First, compound returns for both positively and negatively levered ETFs are positively skewed. In contrast, daily returns are negatively skewed for inverse funds. That is, as implied by the analysis in Farago and Hjalmarsson (2023), compounding induces positive skewness even in those cases where daily returns are negatively skewed. Skewness is greater for all of the levered ETF returns as compared to

<!-- source: pdf page 22 -->
unlevered returns. At the monthly horizon, for example, the robust skewness statistic is 0.188 for $\beta = 3$ and 0.197 for $\beta = - 2 ,$ , compared to 0.020 for unlevered returns.

It is useful to keep in mind that positive skewness in compound LSS-ETF returns implies that most individual outcomes will be less than the mean or expected outcome. On Table 7, mean returns in all cases exceed median returns. Despite simplifying assumptions, differences between mean and median returns are reasonably similar to those predicted in Table 1 of Bessembinder (2026). At the monthly horizon with $\beta = 3$ for example, the mean return is 1.78%, compared to a median return of -0.33%, a difference of 2.1%, while Table 1 in Bessembinder (2026) predicts a differential of 2.0%.

The outcome that median returns to the triple levered (β = 3) strategy are negative is of practical importance, as it implies that this strategy most often led to investment losses, even though there was a positive “risk premium” in the overall market during the decades studied. Median returns are also negative for all horizons considered for negative leverage funds. Only unlevered returns and moderate positive (β = 2) have positive median returns. On the other hand the strong positive skewness implies the possibility of large returns. With β = 3, for example, 99<sup>th</sup> percentile returns are 53.5% and 114.7% at the weekly and monthly horizons.

## C. Rebalancing Costs

Table 7 also reports the mean of levered but non-rebalanced benchmark returns computed according to expression (3). As noted, the difference between the return computed according to expression (4) and this benchmark quantifies the effect of daily rebalancing. The effect of daily rebalancing is to reduce mean returns for all leverage levels. Cross-stock average VRs (discussed further below) are 0.96 and 0.90 at the weekly and monthly horizons, respectively. The pattern in mean rebalancing costs is broadly consistent with Implication (2) in Bessembinder (2026), that rebalancing costs will tend to be positive when return VRs are less than one.

<!-- source: pdf page 23 -->
Comparing average rebalancing costs across symmetric long versus short leverage supports Implication (3) in Bessembinder (2026), which predicts larger rebalancing costs for inverse funds. Rebalancing costs are zero for unlevered $( \beta = 1 )$ funds, but are positive for $\beta = - 1$ funds. Average rebalancing costs for $\beta = - 2$ funds also exceed those for $\beta = 2$ funds. Mean rebalancing costs are notably generally greater at the monthly horizons. The data on Table 7 also support Bessembinder (2026) Implication (4,) that rebalancing costs will be asymmetric across negative leverage as compared to “matched” positive leverage funds. Comparing average rebalancing costs across $\beta = - 2$ and $\beta = 3$ funds, the former are greater by 0.01% and 0.21% at the weekly and monthly horizons, respectively.

## D. ETF Returns and Volatility

Much discussion of levered ETFs has highlighted a negative relation between compound levered ETF returns and stock return volatility. I therefore assess relations between stock return volatility and average returns to hypothetical levered ETFs, focusing in particular on the costs associated with daily rebalancing. To do so, I assign each calendar interval for each stock to one of five quintiles. The periods with the lowest 20% of daily return standard deviations for that stock over the relevant horizon are assigned to the first quintile, those with standard deviations between the $2 0 ^ { \mathrm { t h } }$ and $4 0 ^ { \mathrm { t h } }$ percentile are assigned to the second quintile, etc.

For each return interval and stock, I compute the levered ETF return with daily rebalancing according to (4), the levered but non-rebalanced return benchmark according to (3), and the difference, which measures rebalancing costs, and I report means of each variable for weekly and monthly horizons and volatility quintile in Table 8. I also report the median cost for each horizon and volatility quintile.

In addition to levered returns, I report on average unlevered returns by stock volatility quintile. These differ systematically across volatility groups. At the weekly horizon, mean returns increase for higher volatility quintiles, from 0.07% for the lowest volatility group to 0.51% for the highest volatility group. At the monthly horizon, returns decrease for higher volatility quintiles, consistent with the results
<!-- source: pdf page 24 -->
reported by Blitz and van Vliet (2007). At the monthly horizon, mean unlevered returns are 1.18% and 0.05% for the lowest and highest volatility quintiles, respectively. Since unlevered returns differ notably across volatility quintiles, levered returns can be expected to differ as well, with or without daily rebalancing. The comparison of mean ETF returns across volatility quintiles is therefore not directly informative regarding interactions between leverage and volatility. However, the differences between levered outcomes with and without daily rebalancing remain informative regarding rebalancing costs.

Bessembinder (2026) shows that return serial correlations as captured by VRs are key determinants of average rebalancing costs. In addition to computing VRs for each stock while employing the full time series of available data, I compute separate VRs within each daily return volatility quintile. Table 9 presents cross sectional mean VRs, after winsorizing at the first and ninety-ninth percentiles, by stock-specific volatility quintile. The most relevant pattern that can be observed on Table 9 is that VRs are consistently largest when the stock-specific daily return volatility is lowest. In the lowest quintile of stock-specific daily return volatility, both weekly and monthly VRs are greater than one, indicating positive return serial correlation. In contrast, in the highest quintile of stock-specific daily return volatility, average VRs are less than one, indicating negative return serial correlation. That is, return volatility and serial correlations are empirically intertwined. High volatility periods also tend to be periods with greater reversals. While high volatility need not be associated with greater average rebalancing costs (and would not be, if return autocorrelations were on balance positive), the empirical overlap of high volatility with negative serial correlation implies particularly large rebalancing costs during these periods.

The data reported in Table 8 supports this reasoning. For all leverage parameters average rebalancing costs are positive and greatest in the highest volatility quintile. For example, at the monthly horizon with leverage of β = -2, average rebalance costs are 2.48% in the highest volatility quintile, but are -0.32% when the volatility of daily returns is in the lowest volatility quintile. For all leverage parameters, average rebalancing costs are negative (implying that rebalancing trades improve average

<!-- source: pdf page 25 -->
returns) and smallest for returns in the lowest volatility quintile. For example, at the monthly horizon with leverage of β = 3, average rebalance costs are -0.31% in the lowest daily return volatility quintile, compared to 1.54% in the highest volatility quintile.

These results support Implication 2 in Bessembinder (2026) that return volatility can improve average levered returns by reducing rebalance costs, if return serial correlation is positive. However, the results also affirm in a limited sense the widespread perception that high volatility is associated with lower compound returns to levered ETFs, once it is recognized that high volatility periods also tend to be periods when return serial correlations at relevant horizons are on balance negative, implying return reversals.

## V. Conclusions

I study outcomes to investing in leveraged single stock ETFs, which are of particular interest because levered returns to single stocks are both more volatile and more highly skewed than levered returns to stock indices. I decompose the divergence between actual levered ETF returns and the simple non-rebalanced benchmark defined by expression (3) into two components, one attributable to frictions (including management fees, trading costs, short selling costs, any deviations of actual from target leverage, and any interest rate margins embedded in swap terms or borrowing/lending rates) and the second attributable to the rebalancing trades undertaken to maintain constant ETF leverage. I also test several implications developed in Bessembinder (2026).

I show that LSS-ETFs underperform a simple benchmark by 0.82% per month in my main sample, and by 1.34% per month in the supplemental sample of funds listed after March 2024. Such underperformance is likely to loom larger in the future, should returns on underlying stocks be lower than in the relatively short historical sample. Average rebalancing costs align closely with the implications of the theory presented in Bessembinder (2026), increasing with return volatility and decreasing with return
<!-- source: pdf page 26 -->
serial correlation as captured by return variance ratios. However, average frictional costs are larger than the rebalancing costs emphasized in the prior literature, and are deserving of additional study.

I also document and provide explanations for interesting asymmetries, as costs attributable to frictions are larger for positive leverage than for inverse leverage funds, while costs attributable to daily rebalancing are larger for negative than for positive leverage funds.

The second set of results focuses on historical returns to hypothetical ETFs, with target leverage applied to the millions of actual historical daily stock returns in the CRSP database. I document that, when considering all common stocks, target returns less than -100% would have occurred multiple times per trading day on average. I therefore mainly focus on a subsample of larger capitalization stocks. I show that hypothetical LSS-ETF returns would have been highly volatile and positively skewed, particularly when returns are compounded over multiple days. As a consequence of the skewness, fewer than half of hypothetical LSS-ETF returns are positive at any horizon considered, (except with moderate 2x leverage), and less than 40% of hypothetical ETF returns exceed the non-rebalanced benchmark. On the other hand, average returns for hypothetical funds with positive leverage are strong.

Finally, I examine relations between stock volatility and ETF returns. My findings are consistent with the often-expressed view that higher return volatility is associated with lower returns to levered ETFs. However, I show that this outcome is not attributable to volatility per se, but arises because in the historical data return autocorrelations are lower on average (implying return reversals) during high volatility periods.

The findings compiled herein are likely to be of interest to both participants in and regulators of financial markets. In practice, some brokerage firms (e.g. Fidelity) allow retail investors to buy and sell levered ETFs, while others (e.g., Vanguard) do not.<sup>25</sup> Some observers, e.g. Heimer and Simsek (2019),
<!-- source: pdf page 27 -->
argue that warnings regarding the risks involved in levered positions are not sufficient, and that formal leverage constraints are “the most effective policy.” Similarly, Crouse (2022) urges regulators to limit permissible ETF leverage, and more strictly so for assets with greater return volatility. An alternative is to require that investors in levered products be certified, along the lines of “accredited investor” status. The conceptual discussion and empirical outcomes provided herein might play an educational role that would be useful in such certification.

*Footnote (page 26):* 25 See [www.fidelity.com/viewpoints/active-investor/inside-etfs](http://www.fidelity.com/viewpoints/active-investor/inside-etfs) and [http://investor.vanguard.com/investor-resources-education/etfs/leveraged-inverse-etf-etn.](http://investor.vanguard.com/investor-resources-education/etfs/leveraged-inverse-etf-etn)

<!-- source: pdf page 28 -->
## References

Avellaneda, M. and S. Zhang, 2010, Path-Dependence of Leveraged ETF Returns, Siam Journal of Financial Mathematics, 1, 586-603.

Balduzzi, P., and A. Lynch, 1999, Transactions costs and predictability: some utility cost calculations, Journal of Financial Economics, 52, 47-79.

Bali, T., S. Brown, S. Murray, and Y. Tang, 2017, [A Lottery Demand-Based Explanation of the Beta Anomaly,](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/abs/lotterydemandbased-explanation-of-the-beta-anomaly/B5B9F0A65256E6E86B45D72AE0A256C4) [Journal of Financial and Quantitative Analysis,](http://depts.washington.edu/jfqa/) 52, 2369-2397.

Bessembinder, H., 2026, Volatility and Returns to Leveraged ETFs, working paper, downloadable at [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7376118.](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7376118)

Bessembinder, H., 2018, Do stocks outperform Treasury bills? Journal of Financial Economics, 129, 440-457.

Bianchi, S., and L. Goldberg, 2026, A levered ETF anomaly explained, downloadable at [[2604.27287] A Levered ETF Anomaly Explained.](https://arxiv.org/abs/2604.27287)

Blitz, D., and P. van Vliet, 2007, The volatility effect, Journal of Portfolio Management, 34, 102-113.

Bowley, A.L. 1920, Elements of Statistics, Scribner’s, New York, NY.

Cheng, M. and A. Madhavan, 2009, The dynamics of leveraged and inverse exchange-traded funds, Journal of Investment Management, 7, 43-62.

Cheng, M. and A. Madhavan, 2026, Twenty years of leveraged and inverse ETP: What have we learned?, Journal of Investment Management, forthcoming.

Crouse, M., 2019, Leveraged Investment Products: Monthly Rebalancing Boosts Performance, but Tail Risk Looms, The Journal of Index Investing, Winter 2019, 58-69.

Crouse, M., 2022, Averting Disaster: Leverage Limits for Single Stock Leveraged ETFs, Journal of Mathematical Finance, 12, 629-645.

Eraker, B., and M. Ready, 2015, Do investors overpay for stocks with lottery-like payoffs? An examination of the returns of OTC stocks, Journal of Financial Economics, 115, 486-504.

Farago, A., Hjalmarsson, E., 2023, Compound returns are positively skewed, Review of Finance, 27, 495-538.

Gennaioli, N., A. Shleifer, and R. Vishny, 2021, Neglected risks, financial innovation, and financial fragility, Journal of Financial Economics, 104, 452-468.

Hendershott, T., A. Menkveld, R. Praz, and M. Seasholes, 2022, Asset price dynamics with limited attention, Review of Financial Studies, 35, 962-1008.

Heimer, R., and A. Simsek, 2019, Should retail investors’ leverage be limited?, Journal of Financial Economics, 132, 1-21.

Hinkley, D.V., 1975, On power transformations to symmetry, Biometrika 62, 101–111.

<!-- source: pdf page 29 -->
Ivanov, I. and S. Lenkey, Do levered ETFs really amplify late-day returns and volatility? Journal of Financial Markets, November 2018, Pages 36-56.

Jegadeesh, N., 1990, Evidence of predictable behavior of security returns, The Journal of Finance, 45, 881–98.

Kahn, M. 2018, Run, don’t walk from leveraged ETFs, Kiplinger Newsletter, www.kiplinger.com/article/investing/t022-c009-s001-run-don-t-walk-from-leveraged-etfs.html

Kim, H., J. Han, and P. Won, 2026, Same risk, different price: Dealer rents in Single-Stock Leveraged ETFs”, working paper, available at [Same Risk, Different Price: Dealer Rents in Single-Stock Leveraged ETFs by Hanjun Kim, Jaehee Han, Peter Y. Won :: SSRN.](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7030278)

Kiman, Tae-Hwan, and Halbert White, 2004, On more robust estimation of skewness and kurtosis, Finance Research Letters, 1, 56–73.

Lehmann, B.., 1990, Fads, martingales, and market efficiency, The Quarterly Journal of Economics, 105, 1–28.

Liu, H., 2004, Optimal consumption and investment with transaction costs and multiple risky assets, Journal of Finance, 59, 289-338.

Magill, M., and G. Constantinides, 1976, Portfolio selection with transaction costs, Journal of Economic Theory, 13, 245-263.

Murray, C., and M. Sammon, 2026, The costs and benefits of leveraged ETFs, working paper, available at [The Costs and Benefits of Leveraged ETFs by Chris Murray, Marco Sammon :: SSRN.](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7133021)

Pessina, C., and R. Whaley, 2021, Levered and Inverse Exchange-Traded Products: Blessing or Curse?, Financial Analysts Journal, 77, 10-29.

Wang, Baolian, 2025, Multi-day Return Properties of Leveraged Index ETFs, working paper, available at [https://ssrn.com/abstract=5119860.](https://ssrn.com/abstract=5119860)

<!-- source: pdf page 30 -->
**Figure 1**

![Figure 1](figures/fig_2c36870a370e.png)

**Published caption:** Figure 1: Total Market Capitalization and number of Levered Single-Stock ETFs included in the sample, July 2022 to December 2025. For each date, the figure displays total market capitalization, as well as capitalization of long and short exposure funds.

<!-- source: pdf page 31 -->
**Table 1**

**Published caption:** Table 1: Descriptive Data for Thirty-Five Levered Single Stock ETFs Included in Sample.

| Single Stock ETFs, from F ETF Le |  |  |  | irst Date L verage | isted to December 31, 20 ETF Market Cap ($M) |  | 25Daily Returns |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Underlying Stock | ETF Ticker | First Trade Date | Min | Max | Mean | Last | Stock Mean | ETF Mean | Stock Standard Deviation | ETF Standard Deviation |
| APPLE INC | AAPB | 10-Aug-22 | 1.75 | 2.00 | 14.8 | 28.2 | 0.08% | 0.11% | 1.72% | 3.26% |
| APPLE INC | AAPD | 10-Aug-22 | -1.00 | -1.00 | 26.6 | 20.0 | 0.08% | -0.05% | 1.72% | 1.72% |
| APPLE INC | AAPU | 10-Aug-22 | 1.50 | 2.00 | 87.2 | 152.8 | 0.08% | 0.11% | 1.72% | 3.09% |
| APPLE INC | AAPX | 12-Jan-24 | 2.00 | 2.00 | 8.1 | 11.3 | 0.09% | 0.14% | 1.76% | 3.52% |
| ADVANCED MICRO DEVICES INC | AMDL | 19-Mar-24 | 2.00 | 2.00 | 302.6 | 577.4 | 0.08% | 0.12% | 3.43% | 6.86% |
| ADVANCED MICRO DEVICES INC | AMDS | 23-Aug-23 | -1.00 | -1.00 | 2.0 | 2.8 | 0.09% | -0.06% | 3.18% | 3.19% |
| AMAZON COM INC | AMZD | 8-Sep-22 | -1.00 | -1.00 | 5.0 | 6.5 | 0.09% | -0.06% | 2.13% | 2.13% |
| AMAZON COM INC | AMZU | 8-Sep-22 | 1.50 | 2.00 | 132.6 | 360.0 | 0.09% | 0.12% | 2.13% | 3.71% |
| AMAZON COM INC | AMZZ | 19-Mar-24 | 2.00 | 2.00 | 35.5 | 55.7 | 0.08% | 0.13% | 2.00% | 3.99% |
| ALIBABA GROUP HOLDING LTD | BABX | 14-Dec-22 | 1.75 | 2.00 | 50.4 | 162.2 | 0.10% | 0.18% | 2.69% | 5.19% |
| COINBASE GLOBAL INC | CONL | 10-Aug-22 | 1.50 | 2.00 | 390.4 | 464.0 | 0.25% | 0.38% | 5.33% | 9.40% |
| ALPHABET INC | GOOX | 12-Jan-24 | 2.00 | 2.00 | 13.3 | 48.8 | 0.18% | 0.31% | 1.89% | 3.80% |
| ALPHABET INC | GGLL | 8-Sep-22 | 1.50 | 2.00 | 166.9 | 1,036.6 | 0.15% | 0.23% | 1.98% | 3.49% |
| ALPHABET INC | GGLS | 8-Sep-22 | -1.00 | -1.00 | 5.3 | 13.4 | 0.15% | -0.12% | 1.98% | 1.97% |
| META PLATFORMS INC | FBL | 14-Dec-22 | 1.50 | 2.00 | 104.1 | 379.1 | 0.25% | 0.39% | 2.41% | 4.39% |
| MICROSOFT CORP | MSFD | 8-Sep-22 | -1.00 | -1.00 | 7.1 | 9.8 | 0.09% | -0.06% | 1.58% | 1.58% |
| MICROSOFT CORP | MSFL | 19-Mar-24 | 2.00 | 2.00 | 21.1 | 45.7 | 0.05% | 0.05% | 1.41% | 2.82% |
| MICROSOFT CORP | MSFU | 8-Sep-22 | 1.50 | 2.00 | 91.5 | 254.9 | 0.09% | 0.11% | 1.58% | 2.71% |
| MICROSOFT CORP | MSFX | 12-Jan-24 | 2.00 | 2.00 | 8.5 | 24.6 | 0.06% | 0.07% | 1.40% | 2.82% |
| NVIDIA CORP | NVD | 23-Aug-23 | -2.00 | -1.50 | 75.1 | 90.0 | 0.28% | -0.52% | 3.07% | 6.01% |
| NVIDIA CORP | NVDD | 14-Sep-23 | -1.00 | -1.00 | 21.8 | 32.5 | 0.29% | -0.26% | 3.09% | 3.09% |
| NVIDIA CORP | NVDL | 14-Dec-22 | 1.50 | 2.00 | 2,618.6 | 4,737.6 | 0.36% | 0.58% | 3.17% | 5.82% |
| NVIDIA CORP | NVDQ | 20-Oct-23 | -2.00 | -2.00 | 31.5 | 28.4 | 0.32% | -0.62% | 3.13% | 6.24% |
| NVIDIA CORP | NVDS | 15-Jul-22 | -1.50 | -1.25 | 54.2 | 28.2 | 0.34% | -0.41% | 3.25% | 4.43% |
| NVIDIA CORP | NVDU | 14-Sep-23 | 1.50 | 2.00 | 433.4 | 685.7 | 0.29% | 0.48% | 3.09% | 5.91% |
| NVIDIA CORP | NVDX | 20-Oct-23 | 2.00 | 2.00 | 534.9 | 585.7 | 0.32% | 0.58% | 3.13% | 6.24% |
| PAYPAL HOLDINGS INC | PYPT | 15-Jul-22 | 1.50 | 1.50 | 1.5 | 2.3 | -0.01% | -0.02% | 2.78% | 4.18% |
| TESLA INC | TSDD | 23-Aug-23 | -2.00 | -1.50 | 36.9 | 67.7 | 0.18% | -0.34% | 3.86% | 7.55% |
| TESLA INC | TSL | 10-Aug-22 | 1.25 | 1.25 | 9.8 | 33.3 | 0.13% | 0.13% | 3.82% | 4.77% |
| TESLA INC | TSLL | 10-Aug-22 | 1.50 | 2.00 | 2,455.0 | 5,981.9 | 0.13% | 0.23% | 3.82% | 6.93% |
| TESLA INC | TSLQ | 15-Jul-22 | -2.00 | -1.00 | 167.0 | 304.1 | 0.15% | -0.22% | 3.82% | 6.04% |
| TESLA INC | TSLR | 23-Aug-23 | 1.75 | 2.00 | 124.9 | 348.4 | 0.18% | 0.32% | 3.86% | 7.63% |
| TESLA INC | TSLS | 10-Aug-22 | -1.00 | -1.00 | 52.0 | 72.4 | 0.13% | -0.10% | 3.82% | 3.83% |
| TESLA INC | TSLT | 20-Oct-23 | 2.00 | 2.00 | 358.8 | 340.6 | 0.20% | 0.34% | 3.89% | 7.76% |
| TESLA INC | TSLZ | 20-Oct-23 | -2.00 | -2.00 | 57.7 | 86.5 | 0.20% | -0.39% | 3.89% | 7.76% |
| Simple Cross-Fund Mean |  |  | 0.54 | 0.76 | 243.0 | 488.0 | 0.16% | 0.05% | 2.79% | 4.68% |

*Merged cells are shown once, at their first row and column; the HTML and cells files keep the exact structure.*

Table files: [HTML](tables/tbl_1bb9d731730f.html), [cells](tables/tbl_1bb9d731730f.json), [image](tables/tbl_1bb9d731730f.jpg)

<!-- source: pdf page 32 -->
**Table 2**

**Published caption:** Table 2: Daily returns to thirty five levered single stock ETFs. Returns from the date of initial listing to December 31, 2025 are obtained from CRSP, while federal funds interest rates are obtained from the Federal Reserve Bank of St. Louis. The friction cost is the difference between the outcome implied by expression (1) and the actual ETF return.

| Daily ETF Returns to Sample Funds, fron Inception to December 31, 2025, by Target Leverage |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Leverage | Number Daily Obs | Mean Actual ETF Return | Median Actual ETF Return | Mean - Median, Actial ETF Return | Robust Skewness, Actual ETF Return | Mean Stock Return | Mean Interest Rate | Mean Frictionless ETF Return | Mean Friction Cost |
| All | 23,680 | 0.056% | 0.000% | 0.056% | 2.325% | 0.162% | 0.019% | 0.078% | 0.022% |
| Positive | 14,419 | 0.238% | 0.170% | 0.069% | 4.860% | 0.152% | 0.019% | 0.265% | 0.026% |
| Negative | 9,261 | -0.228% | -0.142% | -0.086% | -2.882% | 0.178% | 0.019% | -0.214% | 0.014% |
| 2.00 | 9,505 | 0.276% | 0.208% | 0.068% | 2.875% | 0.162% | 0.018% | 0.306% | 0.030% |
| 1.75 | 741 | -0.046% | -0.065% | 0.019% | 6.029% | -0.002% | 0.019% | -0.018% | 0.028% |
| 1.50 | 3,321 | 0.221% | 0.120% | 0.100% | 8.844% | 0.166% | 0.019% | 0.239% | 0.019% |
| 1.25 | 852 | 0.134% | 0.028% | 0.106% | 2.488% | 0.127% | 0.018% | 0.154% | 0.019% |
| -1.00 | 5,736 | -0.093% | -0.093% | 0.001% | -0.135% | 0.121% | 0.019% | -0.084% | 0.009% |
| -1.25 | 501 | -0.566% | -0.582% | 0.016% | -3.989% | 0.479% | 0.019% | -0.557% | 0.009% |
| -1.50 | 575 | -0.172% | -0.286% | 0.114% | -1.088% | 0.138% | 0.019% | -0.159% | 0.013% |
| -2.00 | 2,449 | -0.490% | -0.382% | -0.109% | -4.243% | 0.259% | 0.019% | -0.462% | 0.029% |

*Table note:* Daily ETF Returns to Sample Funds, fron Inception to December 31, 2025, by Target Leverage

*Merged cells are shown once, at their first row and column; the HTML and cells files keep the exact structure.*

Table files: [HTML](tables/tbl_88b4d83ca99c.html), [cells](tables/tbl_88b4d83ca99c.json), [image](tables/tbl_88b4d83ca99c.jpg)

<!-- source: pdf page 33 -->
**Table 3**

**Published caption:** Table 3: Compound weekly and monthly returns to levered single stock ETFs. Returns for each fund are form date of initial listing to June 30, 2025, and are obtained from CRSP. Federal funds interest rates are obtained from the Federal Reserve Bank of St. Louis. Friction costs are the difference between expression (4) outcomes and actual ETF returns, while rebalance costs are expression (3) outcomes minus expression (4) outcomes. Panels A and B pertain to the main sample of 35 funds listed prior to March 2024, while Panel C pertains to a supplemental sample of 235 funds listed thereafter.

| Actual and Frictionless Returns to Levered Single Stock ETFs |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |  |  |
| Panel A: Main Sample, Weekly Outcomes, July 2022 to December 2025 |  |  |  |  |  |  |  |  |  |  |  |
| Num Obs | Leverage |  | Mean Underlying Stock Return | Mean Benchmark Return: With Weekly Rebalance (Expression 3) | Mean Benchmark Return With Daily Rebalance (Expression 4) | Mean Actual ETF Return | Median Actual ETF Return | Robust Skewness, Actual ETF Return | Mean Rebalance Cost | Mean Frictional Cost | Mean Total Cost vs. Exp (3) |
| 4941 | All |  | 0.76% | 0.37% | 0.32% | 0.22% | -0.14% | 10.26% | 0.05% | 0.10% | 0.15% |
| 3010 | Long |  | 0.72% | 1.25% | 1.23% | 1.11% | 0.52% | 18.40% | 0.02% | 0.13% | 0.14% |
| 1931 | Short |  | 0.83% | -0.99% | -1.10% | -1.17% | -0.87% | 3.64% | 0.11% | 0.07% | 0.17% |
|  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |
| Panel B: Main Sample, Monthly Outcomes, July 2022 to December 2025 |  |  |  |  |  |  |  |  |  |  |  |
| Num Obs | Leverage |  | Mean Underlying Stock Return | Mean Benchmark Return: With Monthly Rebalance (Expression 3) | Mean Benchmark Return With Daily Rebalance (Expression 4) | Mean Actual ETF Return | Median Actual ETF Return | Robust Skewness, Actual ETF Return | Mean Rebalance Cost | Mean Frictional Cost | Mean Total Cost vs. Exp (3) |
| 1158 | All |  | 3.23% | 1.58% | 1.20% | 0.76% | -1.10% | 25.55% | 0.38% | 0.44% | 0.82% |
| 705 | Long |  | 3.05% | 5.27% | 5.06% | 4.51% | 2.48% | 24.41% | 0.20% | 0.55% | 0.75% |
| 453 | Short |  | 3.51% | -4.15% | -4.81% | -5.08% | -4.72% | 13.64% | 0.66% | 0.27% | 0.93% |
|  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |
| Panel C: Recent List Sample, Monthly Outcomes, April 2024 to December 2025 |  |  |  |  |  |  |  |  |  |  |  |
| Num Obs | Leverage |  | Mean Underlying Stock Return | Mean Benchmark Return: With Monthly Rebalance (Expression 3) | Mean Benchmark Return With Daily Rebalance (Expression 4) | Mean Actual ETF Return | Median Actual ETF Return | Robust Skewness, Actual ETF Return | Mean Rebalance Cost | Mean Frictional Cost | Mean Total Cost vs. Exp (3) |
| 1544 | All |  | 2.02% | 2.51% | 2.16% | 1.17% | -2.52% | 28.37% | 0.34% | 0.99% | 1.34% |
| 1271 | Long |  | 1.89% | 3.44% | 3.02% | 1.97% | -1.63% | 27.94% | 0.42% | 1.04% | 1.47% |
| 273 | Short |  | 2.66% | -1.81% | -1.80% | -2.54% | -4.41% | 21.38% | -0.01% | 0.74% | 0.73% |

*Merged cells are shown once, at their first row and column; the HTML and cells files keep the exact structure.*

Table files: [HTML](tables/tbl_80015599b157.html), [cells](tables/tbl_80015599b157.json), [image](tables/tbl_80015599b157.jpg)

<!-- source: pdf page 34 -->
**Table 4**

**Published caption:** Table 4. Estimates from Cross-Sectional Regressions Explaining Mean Rebalance Costs for Thirty-Five Levered Single Stock ETFs. Mean estimated rebalance costs are regressed on (Panel A) the mean daily return, the variance of daily returns, and return autocorrelations as captured by the return Variance Ratio, and on (Panel B) the rebalance costs predicted by Equation A8. Standard errors are clustered by underlying stock.

| Cross-Sectional Regressions to Explain Mean Rebalance Costs to Actual Leveraged ETFs |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |
|  |  | Weekly Horizon |  |  |  | Monthly Horizon |  |  |
|  |  | Coefficient Estimate | Standard Error | T-statistic |  | Coefficient Estimate | Standard Error | T-statistic |
|  |  |  |  |  |  |  |  |  |
| Panel A: Mean Rebalance Costs Vs. Mean, Variance, and Variance Ratio (Autocorrelations) of Stock Returns |  |  |  |  |  |  |  |  |
| Intercept |  | -0.001 | 0.000 | -1.78 |  | -0.006 | 0.002 | -2.40 |
| Mean Daily Return |  | -0.116 | 0.080 | -1.46 |  | 0.202 | 0.572 | 0.35 |
| Variance of Daily Return |  | 0.863 | 0.339 | 2.54 |  | 6.459 | 2.736 | 2.36 |
| Variance Ratio Minus 1 |  | -0.007 | 0.003 | -2.59 |  | -0.024 | 0.008 | -3.17 |
| Regression R-squared |  | 0.403 |  |  |  | 0.424 |  |  |
|  |  |  |  |  |  |  |  |  |
| Panel B: Mean Rebalance Costs vs. Predicted Costs |  |  |  |  |  |  |  |  |
| Intercept |  | 0.000 | 0.000 | 2.36 |  | 0.003 | 0.001 | 2.80 |
| Predicted Cost |  | 1.108 | 0.157 | 7.08 |  | 0.883 | 0.185 | 4.78 |
| Regression R-squared |  | 0.768 |  |  |  | 0.589 |  |  |

*Merged cells are shown once, at their first row and column; the HTML and cells files keep the exact structure.*

Table files: [HTML](tables/tbl_d6fb2262698c.html), [cells](tables/tbl_d6fb2262698c.json), [image](tables/tbl_d6fb2262698c.jpg)

<!-- source: pdf page 35 -->
**Table 5**

**Published caption:** Table 5: Daily returns to hypothetical levered single-stock ETFs from January 1, 1974 to December 2024. Returns are implied by text expression (1) when using CRSP stock returns and federal funds interest rates obtained from the Federal Reserve Bank of St. Louis.

| Daily Stock Returns and Hypothetical ETF Returns, CRSP Stocks Jan. 1974 to Dec. 2024 |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |
| Panel A: All Stocks (69.6 million stock/days) |  |  |  |  |  |  |  |
| Leverage | Mean Return | Median Return | Percent of Returns &lt; -100% | Mean Daily Number &lt; -100% | 1st Percentile Return | 99th Percentile Return | Robust Skewness |
| 3 | 0.210% | -0.055% | 0.053% | 2.843 | -35.485% | 42.209% | 0.088 |
| 2 | 0.147% | -0.027% | 0.013% | 0.703 | -23.652% | 28.145% | 0.088 |
| 1 | 0.083% | 0.000% | 0.000% | 0.000 | -11.818% | 14.082% | 0.087 |
| -1 | -0.043% | 0.054% | 0.007% | 0.360 | -14.050% | 11.859% | -0.089 |
| -2 | -0.107% | 0.082% | 0.040% | 2.185 | -28.114% | 23.694% | -0.088 |
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
| Panel B: Stocks With Min $1 Billion Prior Market Capitalization (18.7 million stock/days) |  |  |  |  |  |  |  |
| Leverage | Mean Return | Median Return | Percent of Returns &lt; -100% | Mean Daily Number &lt; -100% | 1st Percentile Return | 99th Percentile Return | Robust Skewness |
| 3 | 0.104% | -0.044% | 0.008% | 0.123 | -21.774% | 23.125% | 0.032 |
| 2 | 0.074% | -0.022% | 0.002% | 0.028 | -14.512% | 15.421% | 0.032 |
| 1 | 0.045% | 0.000% | 0.000% | 0.000 | -7.248% | 7.717% | 0.031 |
| -1 | -0.015% | 0.042% | 0.000% | 0.005 | -7.691% | 7.275% | -0.033 |
| -2 | -0.044% | 0.064% | 0.003% | 0.041 | -15.395% | 14.537% | -0.033 |

*Merged cells are shown once, at their first row and column; the HTML and cells files keep the exact structure.*

Table files: [HTML](tables/tbl_1ab0513cf681.html), [cells](tables/tbl_1ab0513cf681.json), [image](tables/tbl_1ab0513cf681.jpg)

<!-- source: pdf page 36 -->
**Table 6**

**Published caption:** Table 6: Frequencies of indicated outcomes for compound returns to hypothetical levered single-stock ETFs from January 1, 1974 to December 2024. Daily returns are as implied by text expression (1) applied to CRSP stock returns. The non-rebalanced benchmark is implied by text expression (3). Results pertain to those stocks with a minimum inflation-adjusted market capitalization of $1 billion as of the end of the preceding calendar period.

| Compound Returns to Hypothetical Single Stock ETFs (min. $1 billion market cap) |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
| Leverage | percent &gt; 0 | Percent &lt; - 1 | Percent &gt; VW Market | % &gt; Non-Reblanced Benchmark | Mean Number Days Employed |
|  |  |  |  |  |  |
| Panel A: Weekly Outcomes |  |  |  |  |  |
| 3 | 49.486% | 0.040% | 48.638% | 38.062% | 4.83 |
| 2 | 50.151% | 0.009% | 48.990% | 38.040% | 4.83 |
| 1 | 50.906% | 0.000% | 48.694% | 0.000% | 4.83 |
| -1 | 48.668% | 0.002% | 46.057% | 38.024% | 4.83 |
| -2 | 47.545% | 0.013% | 46.114% | 38.029% | 4.83 |
|  |  |  |  |  |  |
| Panel B: Monthly Outcomes |  |  |  |  |  |
| 3 | 49.424% | 0.179% | 47.353% | 32.787% | 20.91 |
| 2 | 51.536% | 0.040% | 48.622% | 32.667% | 20.93 |
| 1 | 54.005% | 0.000% | 48.727% | 0.000% | 20.93 |
| -1 | 45.234% | 0.007% | 41.959% | 32.534% | 20.93 |
| -2 | 42.463% | 0.061% | 40.931% | 32.556% | 20.92 |

*Merged cells are shown once, at their first row and column; the HTML and cells files keep the exact structure.*

Table files: [HTML](tables/tbl_19ae0771dae1.html), [cells](tables/tbl_19ae0771dae1.json), [image](tables/tbl_19ae0771dae1.jpg)

<!-- source: pdf page 37 -->
**Table 7**

**Published caption:** Table 7: Compound returns to hypothetical levered single-stock ETFs from January 1, 1974 to December 2024. Daily returns are as implied by text expression (1) applied to CRSP stock returns and compound returns are obtained by text expression (4). The non-rebalanced benchmark is implied by text expression (3), and rebalance rebalance costs are expression (3) outcomes minus expression (4) outcomes. Results pertain to those stocks with a minimum inflation-adjusted market capitalization of $1 billion as of the end of the preceding calendar period.

| Hypothetical Frictionless Holding Period Returns on Levered Single Stock ETFs |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |
|  | Levered Holding Period Returns with Daily Rebalancing (Expr. 5) |  |  |  |  |  | Effect of Daily Rebalance |  |
| Leverage | Mean (all observations) | Mean (with -100% floor) | Median | P1 | P99 | Non-Parametric Skew | Mean Non-Rebalanced Return (Exp. 3) | Mean Daily Rebalance Cost |
| Panel A: Period = Week. N = 3,876,436 |  |  |  |  |  |  |  |  |
| 3 | 0.48% | 0.49% | -0.16% | -45.26% | 53.46% | 0.086 | 0.49% | 0.02% |
| 2 | 0.35% | 0.35% | 0.04% | -31.10% | 34.79% | 0.055 | 0.35% | 0.01% |
| 1 | 0.21% | 0.21% | 0.11% | -15.98% | 16.99% | 0.024 | 0.21% | 0.00% |
| -1 | -0.08% | -0.08% | -0.12% | -16.03% | 17.03% | 0.037 | -0.07% | 0.01% |
| -2 | -0.23% | -0.23% | -0.43% | -31.30% | 34.90% | 0.067 | -0.21% | 0.02% |
|  |  |  |  |  |  |  |  |  |
| Panel B: Period = Month. N = 893,039 |  |  |  |  |  |  |  |  |
| 3 | 1.78% | 1.85% | -0.33% | -78.92% | 114.72% | 0.188 | 2.07% | 0.28% |
| 2 | 1.39% | 1.40% | 0.57% | -58.48% | 72.90% | 0.101 | 1.49% | 0.10% |
| 1 | 0.90% | 0.90% | 0.79% | -31.69% | 34.58% | 0.020 | 0.90% | 0.00% |
| -1 | -0.42% | -0.41% | -0.91% | -29.74% | 36.26% | 0.126 | -0.27% | 0.14% |
| -2 | -1.35% | -1.31% | -2.88% | -55.39% | 75.47% | 0.197 | -0.86% | 0.49% |

*Merged cells are shown once, at their first row and column; the HTML and cells files keep the exact structure.*

Table files: [HTML](tables/tbl_5284ac7afd32.html), [cells](tables/tbl_5284ac7afd32.json), [image](tables/tbl_5284ac7afd32.jpg)

<!-- source: pdf page 38 -->
**Table 8**

**Published caption:** Table 8: Compound returns to hypothetical levered single-stock ETFs from January 1, 1974 to December 2024, By Volatility Quintiles. Volatility quintiles are based on the individual stock’s standard deviation of daily returns across calendar periods. Compound returns are obtained by text expression (4), while rebalance costs are expression (3) outcomes minus expression (4) outcomes.). Results pertain to those stocks with a minimum inflation-adjusted market capitalization of $1 billion as of the end of the preceding calendar period.

|  | Mean Hy | pothetical ETF Returns based on CRSP data, Jan. 1974 to Dec. 2024, by Stock Volatility Quintile |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | We | ekly Horizon | (N = 19,361,0 | 50) | Mo | nthly Horizo | n (N = 4,462,9 | 75) |
| Leverage | Volatility Quintile (Stock) | Mean Return, Daily Rebalance | Mean Return, Weekly Rebalance | Mean Rebalance Cost | Median Rebalance Cost | Mean Return, Daily Rebalance | Mean Return, Monthly Rebalance | Mean Rebalance Cost | Median Rebalance Cost |
| 3 | 1 | 0.25% | 0.06% | -0.18% | -0.01% | 3.26% | 2.95% | -0.31% | 0.17% |
| 3 | 2 | 0.34% | 0.16% | -0.17% | 0.03% | 3.04% | 2.89% | -0.15% | 0.50% |
| 3 | 3 | 0.44% | 0.31% | -0.13% | 0.10% | 2.86% | 2.86% | 0.01% | 0.82% |
| 3 | 4 | 0.58% | 0.56% | -0.02% | 0.23% | 1.91% | 2.25% | 0.34% | 1.31% |
| 3 | 5 | 0.78% | 1.38% | 0.60% | 0.64% | -2.03% | -0.49% | 1.54% | 2.60% |
| 2 | 1 | 0.13% | 0.07% | -0.06% | 0.00% | 2.17% | 2.06% | -0.10% | 0.06% |
| 2 | 2 | 0.19% | 0.13% | -0.06% | 0.01% | 2.08% | 2.03% | -0.05% | 0.17% |
| 2 | 3 | 0.27% | 0.23% | -0.04% | 0.03% | 2.01% | 2.02% | 0.00% | 0.27% |
| 2 | 4 | 0.40% | 0.40% | -0.01% | 0.08% | 1.50% | 1.61% | 0.11% | 0.44% |
| 2 | 5 | 0.74% | 0.94% | 0.20% | 0.21% | -0.73% | -0.22% | 0.51% | 0.89% |
| 1 | 1 | 0.07% |  |  |  | 1.18% |  |  |  |
| 1 | 2 | 0.10% |  |  |  | 1.17% |  |  |  |
| 1 | 3 | 0.15% |  |  |  | 1.17% |  |  |  |
| 1 | 4 | 0.24% |  |  |  | 0.97% |  |  |  |
| 1 | 5 | 0.51% |  |  |  | 0.05% |  |  |  |
| -1 | 1 | 0.13% | 0.07% | -0.06% | 0.00% | -0.48% | -0.59% | -0.11% | 0.05% |
| -1 | 2 | 0.10% | 0.04% | -0.06% | 0.01% | -0.50% | -0.55% | -0.05% | 0.17% |
| -1 | 3 | 0.04% | -0.01% | -0.04% | 0.03% | -0.54% | -0.53% | 0.01% | 0.27% |
| -1 | 4 | -0.08% | -0.09% | -0.01% | 0.08% | -0.43% | -0.31% | 0.12% | 0.44% |
| -1 | 5 | -0.57% | -0.36% | 0.21% | 0.21% | -0.14% | 0.60% | 0.74% | 0.94% |
| -2 | 1 | 0.26% | 0.07% | -0.19% | -0.01% | -1.16% | -1.47% | -0.32% | 0.16% |
| -2 | 2 | 0.19% | 0.01% | -0.18% | 0.03% | -1.25% | -1.41% | -0.16% | 0.49% |
| -2 | 3 | 0.04% | -0.09% | -0.13% | 0.10% | -1.41% | -1.38% | 0.03% | 0.82% |
| -2 | 4 | -0.23% | -0.25% | -0.02% | 0.23% | -1.32% | -0.95% | 0.37% | 1.32% |
| -2 | 5 | -1.43% | -0.80% | 0.64% | 0.64% | -1.61% | 0.87% | 2.48% | 2.85% |

*Merged cells are shown once, at their first row and column; the HTML and cells files keep the exact structure.*

Table files: [HTML](tables/tbl_e07fa5ef85f4.html), [cells](tables/tbl_e07fa5ef85f4.json), [image](tables/tbl_e07fa5ef85f4.jpg)

<!-- source: pdf page 39 -->
**Table 9**

**Published caption:** Table 9: Variance Ratios for Hypothetical Historical Levered Single-Stock ETFs, by Volatility Quintile. Reported are cross-stock mean return volatility and variance ratios, at the weekly, monthly, six-month, and yearly horizons. Volatility quintiles are defined based on the standard deviation of own-stock daily returns within the indicated interval. All parameters are winsorized at the 1% and 99% levels, and results are reported only for those stocks with a minimum of ten years return history in CRSP.

| Cross Secti | onal Mean Varia | nce and Variance | Ratio, by Daily Vo | latiilty Quintile |
| --- | --- | --- | --- | --- |
| Daily |  |  |  |  |
| Return |  |  |  |  |
| Volatilty | Week Return | Week vs. Day | Month Return | Month vs. Day |
| Quintile | Variance | Variance Ratio | Variance | Variance Ratio |
| All | 0.0029 | 0.96 | 0.0118 | 0.90 |
| 1 | 0.0009 | 2.19 | 0.0034 | 1.23 |
| 2 | 0.0013 | 1.53 | 0.0054 | 1.05 |
| 3 | 0.0018 | 1.23 | 0.0077 | 0.97 |
| 4 | 0.0026 | 1.01 | 0.0115 | 0.90 |
| 5 | 0.0078 | 0.79 | 0.0304 | 0.80 |

Table files: [HTML](tables/tbl_a65ff1001c7a.html), [cells](tables/tbl_a65ff1001c7a.json), [CSV](tables/tbl_a65ff1001c7a.csv), [image](tables/tbl_a65ff1001c7a.jpg)
