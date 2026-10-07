---
schema_version: "0.3"
export_schema_version: 4
document_id: "doc_54bf534f3c34"
work_id: "work_0a1bb76db519"
title: "Volatility and Returns to Leveraged ETFs"
authors:
- "Hendrik (Hank) Bessembinder"
journal: null
year: 2026
volume: null
issue: null
pages: null
article_number: null
doi: "10.2139/ssrn.7376118"
arxiv: null
document_version: "unknown"
bibliographic_status: "VALIDATED_WITH_WARNINGS"
processing_status: "COMPLETE"
observed:
  title: "Volatility and Returns to Leveraged ETFs"
  authors:
  - "Hendrik Bessembinder"
  identifiers: []
  doi_candidates: []
sources:
- id: "source_01"
  role: "main"
  type: "pdf"
  sha256: "54bf534f3c34dc960fc3f20d95f81145b7594c44af19716a0c436ea6280cb43b"
  path: "original/source_01/Bessembinder_SSRN_2026_VolatilityAndReturnsToLeveragedETFs.pdf"
  pages: 21
supplements: []
attachments: []
extraction:
  run_id: "20261007T090608Z-54bf534f3c34-76a3cf"
  application_version: "0.3.2"
  adapters:
  - name: "mineru"
    version: "4.0.5"
  timestamp: "2026-10-07T10:10:07+00:00"
validation_report: "validation.json"
---


<!-- source: pdf page 1 -->
# Volatility and Returns to Leveraged ETFs

Hendrik Bessembinder

WP Carey School of Business

Arizona State University

Email: hb@asu.edu

August 31, 2026

## Abstract

Both practitioner commentary and the academic literature emphasize a negative relation between the volatility of returns and outcomes to constant leverage investment strategies such as leveraged ETFs (LETFs). I demonstrate that there is no hardwired negative relation in expectation. Rather, return serial covariances as captured by the return “Variance Ratio” are crucial; volatility increases average LETF returns in the presence of positive serial correlation and vice versa, and has no effect if returns are serially uncorrelated. In the presence of serial dependence, there are asymmetries in expected rebalancing costs across leveraged long vs. inverse strategies. However, return volatility widens the gap between expected and median compound LETF returns, because of increased skewness.

*Footnote (page 1):* * The equations contained herein are extracted from a prior working paper titled “Returns to Constant Leverage Strategies: General Principles and Application to Leveraged Single-Stock ETFs.” I thank George Aragon, Rasoul Foroughfard, Erik Hjalmarsson, Rawley Heimer, Jarrad Harford, Lukas Kremens, Ananth Madhavan, Seth Pruitt, Denis Sosyura, Sunil Wahal, Baolian Wang, Jinming Xue, Feng Zhang, and seminar participants at Arizona State University, Oklahoma State University, and the University of Washington for insightful comments on that version.

<!-- source: pdf page 2 -->
## I. Introduction

Consider a portfolio with a weight 𝛽𝛽 on a risky asset and a weight (1- 𝛽𝛽) on a riskless asset. For simplicity, assume that the risk-free rate is constant and applies to both borrowing and lending. As time passes, the weight on the risky asset evolves as a function of realized returns, unless trades are undertaken to restore the original weight. Two prominent applications are leveraged ETFs, which seek to maintain constant leverage on a daily basis, and long-only rebalancing strategies, such as periodically returning to a 60% weight on stocks in combination with a 40% weight on low-risk assets. If $R _ { t } ^ { s }$ denotes the realized return on the underlying asset from time t to $t { + } I$ then purchases (sales if negative) in the underlying asset equal to $( \beta ^ { 2 } - \beta ) R _ { t } ^ { S }$ per dollar invested at the end of the prior period are required to return to the weight to $\beta.^{1}\  If  < 0 < \beta < 1$ , that is if there are positive weights on both the risky and riskless assets, then $( \beta ^ { 2 } - \beta )   < 0$ and the requisite trades are in the opposite direction as the sign of the realized return. On the other hand $( \beta ^ { 2 } - \beta )$ is positive for $\beta \ge 1$ (leveraged long strategies) and for $\beta \leq 0$ (short or inverse strategies), both of which require rebalancing trades in the same direction as the realized return.

Leveraged ETFs, which most often seek constant leverage each day and commonly select $\beta$ values equal to 2, 3, -1, and -2, have attracted considerable attention. The first leveraged ETFs (LETFs) were introduced in 2006, providing exposure to the returns on stock indices such as the Nasdaq 100 and the $\mathrm { S \& P } ~ 5 0 0 . ^ { 2 }$ Numerous additional LETFs were launched in the following years, providing exposure to additional equity portfolios, commodities, fixed income instruments, and foreign currencies. More recently, LETFs on individual common stocks were introduced to U.S. markets in 2022, and as of mid-2026 more than four hundred such products were listed in the U.S. markets.<sup>3</sup> LETFs may appeal to those
<!-- source: pdf page 3 -->
who wish to hedge other positions, those with strong directional views, and/or those with so-called “lottery preferences.”<sup>4</sup> The growth in LETFs likely reflects that for many investors these products comprise the easiest and simplest channel by which to obtain leveraged long or short positions in financial or commodity markets.

*Footnote (page 2):* 1 See Chen and Madhavan (2009).

*Footnote (page 2):* 2 Leveraged products available to retail investors include both exchange traded funds (ETFs) and exchange traded notes (ETNs). ETFs typically own the underlying asset, often in combination with swaps, while ETNs are unsecured obligations of the issuers.

*Footnote (page 2):* 3 https://www.kalkine.com/by-topic/etf/us-leveraged-etf-growth-explodes-to-a-record-700-funds-more-than-double-2024s-total?

Much of the discussion of LETF returns, whether originating in the financial press, comments by regulators, documents provided by LETF providers or the few relevant academic papers, emphasize negative relations between the volatility of the underlying risky asset returns and compound LETF outcomes. These discussions often uses phases such as “volatility drag,” which might be interpreted to imply that a hardwired negative relation exists. In one of the pioneering studies of LETF returns Avellaneda and Zhang (2010) assert that “…. frequent rebalancing **will** lead to underperformance for the LETF relative to a static leveraged portfolio. The underperformance **will be larger in periods when volatility is high**….”. The ETF provider Direxion writes that “high volatility **causes a decay** of longterm returns for the ETFs….”<sup>5</sup> SEC commissioner Robert Jackson stated that “ …. investors in leveraged ETFs **suffer large losses in volatile markets**” and “In times of market volatility, however, investors **can and will get hurt** by these products.”6 More recently, Murray and Sammon (2026) assert that obtaining leverage through an ETF “can work,” if the underlying asset has “low volatility”. The Finance Industry Regulatory Agency, to its credit, includes the modifier “can” when observing that “ a higher degree of leverage and increased volatility of the index being tracked can lead to a greater divergence between the daily leverage factor and actual performance.”<sup>7</sup>

*Footnote (page 3):* 4 Lottery preference is sometimes referred to as gambling preference or skewness preference. See, for example, Eraker and Ready (2015), Bali, Brown, Murray, and Tang (2017) and Bian, Da, He, Lou, Shue, and Zhou (2026). Gennaioli, Shleifer, and Vishny (2021) suggest that such investors may neglect “unlikely” risk, leading to excessive issuance of risky securities.

*Footnote (page 3):* 5 https://www.direxion.com/education/volatility-matters?

*Footnote (page 3):* 6 Statement of Commissioner Robert J. Jackson, Jr. on Proposed Rules Regarding Exchange Traded Funds (ETFs), June 28, 2018, downloaded from [https://www.sec.gov/newsroom/speeches-statements/statement-jackson-exchange-traded-funds,](https://www.sec.gov/newsroom/speeches-statements/statement-jackson-exchange-traded-funds) October 4, 2025.

*Footnote (page 3):* 7 https://www.finra.org/investors/insights/lowdown-leveraged-and-inverse-exchange-traded-products?

<!-- source: pdf page 4 -->
The main goal of this paper is to reassess and clarify relations between LETF returns and the volatility of returns on the underlying assets. Since returns to single stocks are typically considerably more volatile than returns to stock portfolios, the surge in single stock LETF listings sharpens the importance of gaining a firm and accurate understanding as to the effects of return volatility on leveraged ETF returns. In the discussion that follows I will ignore financing costs and other frictions to focus directly on the role of return volatility.

## II. Relations Between Return Volatility and Leveraged ETF Returns

Let $R _ { t } ^ { s }$ denote the day t return on the underlying asset and let $R _ { T } ^ { R B }$ denote the T-day return on the LETF, where the RB superscript refers to the daily rebalancing required to maintain constant leverage. Ignoring financing costs and other frictions for simplicity,

$$
R _ {T} ^ {R B} = \prod_ {t = 1} ^ {T} (1 + \beta R _ {t} ^ {S}) - 1.\tag{1}
$$

Let $R _ { T } ^ { S }$ denote the T-day compound return on the underlying asset. A simple benchmark by which to evaluate multiperiod outcomes to leveraged ETFs is

$$
R _ {T} ^ {B H} = \beta R _ {T} ^ {S}.\tag{2}
$$

where the BH superscript reflects that the return can be obtained with a buy-and-hold strategy. In particular, in the absence of frictions (and ignoring borrowing costs) an investor could herself capture the return specified by expression (2) with the simple strategy of borrowing to invest, without the need for any trades after the position is initialized at t = 0. In contrast, maintaining constant daily leverage requires the ETF providers to make daily rebalancing trades.

<!-- source: pdf page 5 -->
The extant discussion of the role of return volatility is informed to a substantial extent by Avellaneda and Zhang (2010). Setting their terms for borrowing and shorting costs to zero, they show that the gross compound ETF return can be stated as:<sup>8</sup>

$$
1 + R _ {T} ^ {R B} \cong (1 + R _ {T} ^ {S}) ^ {\beta} e x p \left[ \left(\frac {\beta - \beta^ {2}}{2}\right) R V _ {T} \right],\tag{3}
$$

where $R V _ { T }$ is the “realized variance” of the daily stock returns over days t = 1 to T. Since for both $\beta > 1$ and $\beta \leq - 1$ the term $( \beta - \beta ^ { 2 } )$ is negative, expression (3) implies that, other things equal, the leveraged ETF return decreases if the realized variance increases. While expression (3) is mathematically sound, it is easily misinterpreted.

It is of interest to note that expression (3) is equally valid when $0 \leq \beta \leq 1$ , i.e., for long only strategies with positive weights on both the stock and the risk free asset. Then, the term $( \beta - \beta ^ { 2 } )   >   0 ,$ and expression (3) implies that other things equal, the return to a rebalanced long-only portfolio increases if the realized variance increases. While the negative relation between LETF returns and realized variance specified by (3) has often been highlighted, to my knowledge the positive relation between periodically rebalanced long-only portfolio returns and realized variance, also implied by expression (3), has not typically been emphasized.

To assess expression (3), it is important to recognize that it applies to returns and volatility within an ex post sample, not to periods varying ex ante volatility. Also important, the expression anchors on a specific benchmark, $( 1 + R _ { T } ^ { S } ) ^ { \beta }$ . This benchmark is not the return to the buy-and-hold strategy, nor can it be captured by any trading strategy specified in advance. Rather, the benchmark is the ex post outcome to the rebalanced strategy if volatility turns out to be zero in the sample. The actual sample levered return decreases relative to this benchmark if in-sample volatility increases. Since the

*Footnote (page 5):* 8 Avellaneda and Zhang (2010) include fees, short sale costs, and leverage costs in their expression, while I set these terms to zero to define a frictionless benchmark highlighting the role of return volatility. Cheng and Madhavan (2009) develop the same expression, but also omit the frictions and financing cost components. An informative and near-contemporaneous contribution is Jarrow (2010).

<!-- source: pdf page 6 -->
benchmark is already fixed in the expression, the realized variance in expression (3) is mainly informative about within-sample return reversals. Intuitively, if the relation between the time 0 value of the underlying asset and its time T value is fixed by specifying the outcome on $R _ { T } ^ { S }$ , then zero realized variance implies that underlying value evolved along a smooth curve.<sup>9</sup> Any increase in the realized variance implies larger deviations of the realized price path from the smooth curve. But, with $R _ { T } ^ { S }$ fixed, all such deviations are reversed by time T.10

If the time interval T over which compound returns are measured is modest, the effect of uncertainty is arguably better assessed by considering the effect on the expected or average return. I show that volatility matters for expected compound constant leverage returns only through its interaction with the serial dependence of daily returns. The mathematical expectation of any variable is defined as the probability-weighted average across possible sample paths, and as such has a “repeat play” interpretation.<sup>11</sup> Focusing, for example, on a T = 5 day holding period, a trader could potentially experience 52 outcomes within a calendar year. To see why a focus on the expected outcome generates different implications than the focus on a single ex post sample, it is useful to note that the expectation of the first term on the right side of expression (3), $( 1 + R _ { T } ^ { S } ) ^ { \beta }$ , increases with ex ante volatility, due to

*Footnote (page 6):* 𝑇𝑇𝑆𝑆

*Footnote (page 6):* 9 Stated alternatively, fixing 𝑅𝑅 specifies the sample geometric mean return on the underlying asset. This highlights a distinction between expression (3) and an arguably more robust use of the term “volatility drag” as the explanation for the fact that the arithmetic mean return in any sample exceeds the geometric mean return as an increasing function of return volatility. Note though that the arithmetic mean return does not appear in expression (3) and thus is not directly relevant to this discussion.

*Footnote (page 6):* 10 The confusion regarding the role of volatility may be attributable in part to the fact that some observers, for example, Chen and Madhavan (2026), Barnhorst and Cocozza (2021) and Pitcher (2025), illustrate the effect of “high volatility” with an example where price changes are quickly reversed, and/or illustrate the effect of “low volatility” with an example where price changes are reinforced. Some confusion might also trace to phrasing employed by Cheng and Madhavan (2009), who develop an expression (between their equations numbered 25 and 26) indicating that “the return” to a LETF is distributed with a mean that decreases as a function of the stock return standard deviation. However, their expression applies to the expected logarithmic return, not to the expected actual return.

*Footnote (page 6):* 11 Note that this argument is weakened as the period over which investment performance is measured becomes longer. As an extreme case, individuals experience only a single draw on their compound lifetime investment return.

<!-- source: pdf page 7 -->
Jensen’s inequality.<sup>12</sup> This increase offsets the impacts of the realized variance that would also tend to also be greater during periods with higher ex ante uncertainty.

## A. Expected Rebalancing Effects Over Two Days

The approximation provided by expression (3) does not provide a basis for understanding the effect of ex ante uncertainty on expected or average returns to constant-leverage strategies. In the absence of frictions, the LETF return differs from the buy-and-hold benchmark only because of daily rebalancing trades. These trades are of the same sign as the daily return and might therefore be viewed as momentum trades.

Much of the intuition as to how volatility affects average leveraged ETF returns can be captured when considering outcomes over just two days. In this case, the non-rebalanced benchmark is

$$
R _ {2} ^ {B H} = \beta [ (1 + R _ {1} ^ {S}) (1 + R _ {2} ^ {S}) - 1 ] = \beta [ R _ {1} ^ {S} + R _ {2} ^ {S} + R _ {1} ^ {S} R _ {2} ^ {S} ],
$$

while the rebalanced or constant leverage benchmark is

$$
R _ {2} ^ {R B} = (1 + \beta R _ {1} ^ {S}) (1 + \beta R _ {2} ^ {S}) - 1 = \beta [ R _ {1} ^ {S} + R _ {2} ^ {S} + \beta R _ {1} ^ {S} R _ {2} ^ {S} ].
$$

The excess of the buy-and-hold benchmark over the rebalanced benchmark is

$$
R _ {2} ^ {B H} - R _ {2} ^ {R B} = (\beta - \beta^ {2}) \big (R _ {1} ^ {S} R _ {2} ^ {S} \big).
$$

Letting $\mu _ { t }$ denote the mean or expected stock return in period $t , \sigma _ { t }$ denote the standard deviation of stock return in period t, and $\rho _ { 1 2 }$ denote the serial correlation in the consecutive pair of stock returns, the mean or expected effect of rebalance trades is:

*Footnote (page 7):* 10% or -10%

*Footnote (page 7):* (0.9)³ = 0.729

*Footnote (page 7):* 1β = 3.

*Footnote (page 7):* 12 A simple example illustrates the point. Suppose that the compound stock return is zero mean, and will be either 10% or -10% with equal probability. Consider a fund with 𝛽𝛽 = 3 Then, the first term is (1.1) = 1.331 or (1.1)³ = 1.331 (0.9) = 0.729 with equal probability, with average or expectation equal to 1.03. If volatility is increased such that the stock return is either 15% or -15% with equal probability, the first term will be (1.1 ) = 1.5209 or (0.8 ) = 5 3 5 3 0.6141 with equal probability, with average or expectation equal to 1.0675.

*Footnote (page 7):* 

*Footnote (page 7):* 

<!-- source: pdf page 8 -->
$$
\mathrm{E} (R _ {2} ^ {B H} - R _ {2} ^ {R B}) = (\beta - \beta^ {2}) (\mu_ {1} \mu_ {2} + \sigma_ {1} \sigma_ {2} \rho_ {1 2}),\tag{4}
$$

where $\sigma _ { 1 } \sigma _ { 2 } \rho _ { 1 2 }$ is the covariance between $R _ { 1 } ^ { s }$ and $R _ { 2 } ^ { S }$ . If (4) is positive rebalancing trades impose expected costs, if it is negative rebalancing generates expected benefits. Since $( \beta - \beta ^ { 2 } ) < 0$ for the leveraged ETFs actually traded, expression (4) implies that, other things equal, the expected costs of rebalancing trades:

• (Implication 1) Decrease if the serial correlation of stock returns is greater,

(Implication 2) Are unrelated to stock return volatility if serial correlation is zero, decrease with higher stock volatility if serial correlation is positive, but increase with higher stock volatility if serial correlation is negative.<sup>13</sup>

• (Implication 3) Will be greater in absolute value for leverage of −𝛽𝛽 as compared to leverage of $[ \beta ,$

Implication (1) reflects that positive serial correlation on average improves rebalanced returns while negative serial correlation on average imposes rebalancing costs, because of the momentum nature of rebalancing trades. Positive returns require purchases of the underlying asset to rebalance, and vice versa. With positive serial correlation prices tend to continue in the same direction as rebalancing trade, while with negative serial correlation they tend to reverse. Implication (2) shows that that volatility only affects expected rebalancing cost or benefits if the return serial correlation is non-zero, in which case the direction of the effect depends on the sign of the serial correlation. For a given positive serial correlation, expected rebalanced returns are improved (rebalancing costs decline) if return volatility is greater. In contrast, negative serial correlation in returns implies that expected rebalancing costs increase when volatility is higher. Implication (3) implies greater rebalancing costs for leverage of $\left[ \beta \right. = \left. - 2 \right.$ than for leverage of $\left[ \beta \right. = 2$ . This implication follows from the observation that the term $( \beta - \beta ^ { 2 } )$ is closer to zero
<!-- source: pdf page 9 -->
when $\beta$ is positive than negative, implying that the requisite rebalancing trades are larger, other things equal.<sup>14</sup>

*Footnote (page 8):* 13 Expression (4) also implies that expected rebalancing costs over two days decline with higher positive mean stock returns, which can be understood based on results in Wang (2025). Larger positive mean returns imply that rebalance trades tend to involve more net buying of the underlying stock, so that rebalanced positions are somewhat larger on average as compared to non-rebalanced positions. Higher mean returns therefore tend to be earned on larger positions with rebalancing than without. However, as I show below, this implication need not hold over longer time periods for typical parameters.

The effect of return serial correlation can be captured with return Variance Ratios. Assuming for simplicity that the standard deviation of returns, σ, is constant over the two periods, define the two-period VR as:

$$
V R _ {2} \equiv \frac {V a r (R _ {1} ^ {S} + R _ {2} ^ {S})}{2 \sigma^ {2}},
$$

which can be stated as $V R _ { 2 } = 1 + \rho _ { 1 2 } ,$ so the expected rebalancing cost or benefit over two periods is:

$$
\mathrm{E} (R _ {2} ^ {B H} - R _ {2} ^ {R B}) = (\beta - \beta^ {2}) [ \mu_ {1} \mu_ {2} + \sigma^ {2} (V R _ {2} - 1) ].\tag{5}
$$

## B. Expected Rebalancing Effects Over T Days

By similar reasoning as in the two period case, the rebalancing cost over three periods is

$$
R _ {3} ^ {B H} - R _ {3} ^ {R B} = (\beta - \beta^ {2}) \big (R _ {1} ^ {S} R _ {2} ^ {S} + R _ {2} ^ {S} R _ {3} ^ {S} + R _ {1} ^ {S} R _ {3} ^ {S} \big) + (\beta - \beta^ {3}) \big (R _ {1} ^ {S} R _ {2} ^ {S} R _ {3} ^ {S} \big).
$$

Note that with the addition of the third period the $( \beta - \beta ^ { 2 } )$ term now applies to the sum of the products of all unique pairs of return. In addition a new $( \beta - \beta ^ { 3 } )$ term enters the expression, and is multiplied by the product of all three returns. This general pattern applies as additional periods are added. Over T trading days the difference between the leveraged, non-rebalanced benchmark and the daily rebalanced benchmark given by text expression (5) over T trading days can be stated as:

$$
R _ {T} ^ {B H} - R _ {T} ^ {R B} = \sum_ {k = 2} ^ {T} (\beta - \beta^ {k}) e _ {k},\tag{6}
$$

$$
\text {where} e _ {k} = \sum_ {1 \leq i _ {1} <   i _ {2} \dots <   i _ {k} \leq T} (R _ {i 1} ^ {S} R _ {i 2} ^ {S} \dots .. R _ {i k} ^ {S})
$$

is the “elementary symmetric sum” that denotes the summation over the products obtained when multiplying every set of k distinct returns contained in the set of T returns. The number of terms to be
<!-- source: pdf page 10 -->
summed is equal to the binomial coefficient $\left( \begin{matrix} { T } \\ { k } \\ \end{matrix} \right)$ . Expression (6) gives the exact rebalancing cost for any given sequence of T returns. The ex-ante expectation of the difference given by expression (6) is simply

*Footnote (page 9):* 1

*Footnote (page 9):* = 1

*Footnote (page 9):* 14 This is most obvious when comparing 𝛽𝛽 = , which is a simple long position that does not requiring rebalancing at all, while the short position implied by 𝛽𝛽 - does require rebalancing to maintain the leverage.

$$
E (R _ {T} ^ {B H} - R _ {T} ^ {R B}) = \sum_ {k = 2} ^ {T} (\beta - \beta^ {k}) E (e _ {k}).\tag{7}
$$

Additional intuition can be gained through simplifying assumptions. Assume that the mean and standard deviation of daily stock returns are equal to constants, denoted µ and $\mathfrak { S } _ { \mathfrak { z } }$ respectively. Denote the correlation between any pair of returns i and j as $\rho _ { i j }$ , which need not be constant across different $i - j$ lags. The covariance between returns i and j is $\sigma _ { i j } = \sigma ^ { 2 } \rho _ { i j }$ . The variance of the sum of returns from period 1 to period T is:

$$
V a r (\sum_ {t = 1} ^ {T} R _ {t} ^ {S}) = T \sigma^ {2} + 2 \sum_ {1 \leq i <   j \leq T} \sigma^ {2} \rho_ {i j}.\tag{8}
$$

Following Lo and Mackinlay (1988), define the Variance Ratio $( \mathrm { V R _ { T } } )$ as the variance of the sum of the T returns to T times the variance of daily returns:

$$
V R _ {T} = \frac {V a r (\sum_ {t = 1} ^ {T} R _ {t} ^ {S})}{T \sigma^ {2}}.\tag{9}
$$

Using (9) in (8)

$$
V R _ {T} - 1 = \left(2 / _ {T}\right) \sum_ {1 \leq i <   j \leq T} \rho_ {i j}.\tag{10}
$$

The VR equals one if the indicated sum of serial correlations equal zero (and in particular if all return serial correlations are zero), but otherwise differs from one as a multiple of the indicated sum of return autocorrelations. Further, as Lo and Mackinlay (1988) observe, VR deviations from one depend on return autocorrelations at all lags, increasing from one if autocorrelations if the indicated sum is positive and decreasing from one if the indicated sum is negative.

Since $E \bigl ( R _ { i } ^ { S } R _ { j } ^ { S } \bigr ) =   \mu ^ { 2 } +   \sigma ^ { 2 } \rho _ { i j }$ , we can state

$$
E (e _ {2}) = \binom {T} {2} \mu^ {2} + \frac {T \sigma^ {2}}{2} (V R _ {T} - 1),\tag{11}
$$

<!-- source: pdf page 11 -->
and

$$
E (e _ {3}) \cong \binom {T} {3} \mu^ {3} + \mu (\mathrm{T} - 2) \frac {T \sigma^ {2}}{2} (V R _ {T} - 1). ^ {1 5}\tag{12}
$$

Using (11 and 12) in (7), a third-order approximation for the expected effect of rebalancing trades is given by

$$
E (R _ {T} ^ {B H} - R _ {T} ^ {R B}) \cong
$$

$$
(\beta - \beta^ {2}) \bigl [ \binom {T} {2} \mu^ {2} + \frac {T \sigma^ {2}}{2} (V R _ {T} - 1) \bigr ] + (\beta - \beta^ {3}) \bigl [ \binom {T} {3} \mu^ {3} + \mu (\mathrm{T} - 2) \frac {T \sigma^ {2}}{2} (V R _ {T} - 1) \bigr ]. ^ {1 6}\tag{13}
$$

Each of the square bracketed terms in expression (13) increases with the mean daily return, $\mu ,$ assuming it is positive.<sup>17</sup> Since the VR increases with return autocorrelations, the square bracketed terms also increase with return autocorrelation (for any positive variance). Finally, a greater daily return standard deviation, σ, increases the bracketed terms if autocorrelations are on balance positive (in the sense that the VR over T periods exceeds one), but decreases the bracketed terms if autocorrelation are on balance negative (in the sense that the VR over T periods is less than one).

Therefore, as in the two period case, expected rebalancing costs or benefits in the T-period case depend on (i) the mean return, (ii) return autocorrelation as captured by the deviation of the VR from one, and (iii) volatility only when the VR deviates from one, with the direction of the effect dependent on the sign of the deviation. That is, there is no necessary or hard-wired negative relation between return volatility and expected LETF returns.

A closer examination of the term $\left( \beta - \beta ^ { k } \right)$ leads to an additional, if less precise, implication. Consider long and short leverage pairs $\beta _ { L } = y$ and $\beta _ { S } = 1 - y ,$ , where $\mathrm { y } \ge 1$ . This pairing is somewhat
<!-- source: pdf page 12 -->
natural, in that the term $( \beta - \beta ^ { 2 } )$ that appears in expression (3) which focused on realized volatility, in expression (4) for rebalancing costs in the two-period case, as well as in the expression for the requisite size of daily rebalancing trades, is identical for the long and short leverage pairs described. For example, $( \beta - \beta ^ { 2 } )$ equals negative six for both $\beta _ { L } = 3$ and for $\beta _ { S } = - 2$ . More broadly, ${ \beta _ { L } } - { \beta _ { L } } ^ { 2 } =   { \beta _ { S } } - { \beta _ { S } } ^ { 2 }$ for all $\mathrm { y } \ge 1$ . That is, for $\mathbf { k }   =   2$ the term is equal across all long and short leverage pairs.

*Footnote (page 11):* E[(𝑅𝑅𝑖𝑖 − 𝜇𝜇)(𝑅𝑅 − 𝜇𝜇)(𝑅𝑅𝑘𝑘 − 𝜇𝜇)] = 0

*Footnote (page 11):* , j,

*Footnote (page 11):* ek

*Footnote (page 11):* in this case is . 𝐸𝐸(𝑅𝑅𝑇𝑇𝐵𝐵𝐵𝐵 − 𝑅𝑅𝑇𝑇𝑅𝑅 ) = ∑ (𝛽𝛽 − 𝛽𝛽𝑘𝑘)�𝑇𝑇𝑘𝑘�µ 𝑇𝑇 𝑘𝑘𝑘𝑘=2

*Footnote (page 11):* 15 The expression also uses the simplifying assumption that 𝑆𝑆 𝑆𝑆 𝑆𝑆  for all i and k. 16 Third order here refers to the number of elementary symmetric sums included. Since the symmetric sums refer to products of simple (not gross or “one plus”) returns, magnitudes of typically become small when k is increased. 17 Under the GBM assumption all variance ratios equal one, and only the mean return is relevant. The exact solution

However, it can be verified numerically that for all k > 2, $( \beta _ { L } - { \beta _ { L } } ^ { k } ) < ( \beta _ { S } - { \beta _ { S } } ^ { k } )$ . The remaining terms in expression (13), $E ( e _ { k } )$ , do not depend on $\beta$ . If $E ( e _ { k } )   \geq   0$ then the product $( \beta -$ $\beta ^ { k } ) E ( e _ { k } )$ is smaller for positive leverage $\beta _ { L } = y$ as compared to paired negative leverage $\beta _ { S } = - ( \mathbf { y } { - } 1 )$ and vice versa. This analysis supports an additional if less precise implication that emerges at longer horizons through higher order terms.

(Implication 4): when evaluated over longer horizons, expected or mean rebalancing costs will be asymmetric across the long vs. short leverage pairs $\beta _ { L } = y$ and $\beta _ { S } = 1 - y$ , with the sign of the asymmetry depending on a weighted average of higher order $E ( e _ { k } )$ terms.

## C. Numerical Assessment

While expression (5) for expected rebalancing costs over two days is exact, expression (13) for the T-day expectation is approximate. I implement numerical simulations to assess how precise are the approximations. Figure 1 displays the expected rebalancing costs as predicted by Expression (13), as well as average rebalancing costs computed across 50,000 simulations, for $\mathrm { T } = 5$ days (Figure 1A) and T $= 1 2 5$ days (Figure 1B), for $\beta = 3$ and $\beta = - 2$ . Simulated daily returns are distributed normally, with means and standard deviations as indicated. Outcomes are displayed for serially independent returns, as well as when returns contain positive and negative moving average representations.

Although each graph on Figure 1 displays four curves (predicted and average rebalance costs, for $\beta = 3  and  \beta = -2$ , in several panels the curves are indistinguishable. In these cases the average costs conform almost exactly to predicted costs, and rebalancing costs are essentially equal across the selected
<!-- source: pdf page 13 -->
leverage pair. Figure 1 shows that average rebalance costs decrease monotonically as return serial correlation increases, as implied, with the effect much stronger at the longer horizon. Average rebalance costs are positive and increase with higher return standard deviations when serial correlations are negative, and are negative and decline further with higher return standard deviations when serial correlations are positive, as also implied. Average rebalance costs decrease with mean stock returns at the 5-day horizon, but the relation is not monotone, as average rebalance costs increase over some ranges with β = 3 leverage, at the 125-day horizon.<sup>18</sup> While average rebalance costs are essentially equal across β = 3 and β = -2 leverage at the 5-day horizon, the asymmetry predicted by implication (4) can be observed at the 125-day horizon. Finally, while the predicted cost and average cost curves for the 125- day horizon displayed on Figure 1 Panel B are visually similar, divergences can be observed, particularly for β = 3 when return standard deviations are high. These divergences give indication of the degree to which the third order approximation is imperfect.

On balance, the data displayed on Figure 1 indicate that the third order approximation developed in the appendix is quite accurate except when horizons and long and parameters are extreme, in simulated data where stock returns are normally and identically distributed.

## D. Compound Return Skewness, and Mean vs. Median Outcomes

Prior authors (e.g. Cheng and Madhavan, 2009, and Wang, 2025) often assume that stock prices follow Geometric Brownian Motion (GBM), which implies that gross returns over any discrete interval are distributed log normal. The log normal distribution is characterized by positive skewness, with the degree of skewness increasing in return volatility and the horizon over which returns are measured. While actual ETF returns need not conform to the GBM assumption, skewness is in any case an important empirical feature of leveraged ETF returns. Importantly, greater skewness implies that a higher

*Footnote (page 13):* 18 The outcome that average rebalancing costs can increase rather than decrease with mean stock returns over longer time periods can be traced to the final term in expression (13), which involves the product of the mean return and the deviation of VR<sub>T</sub> from one.

<!-- source: pdf page 14 -->
percentage of individual outcomes are less than the mean or expected outcome.<sup>19</sup> The results developed above show that return volatility affects expected rebalancing costs or benefits only if return serial correlation, measured as deviations of VRs from the benchmark of 1, are non-zero. In contrast, return volatility is a strong determinant of the skewness in LETF returns and of the gap between the mean and median LETF return, even when underlying asset returns are serially independent.

While general expressions for relations between return volatility, skewness, and median returns in the presence of leverage are elusive, illustrative outcomes can be obtained with simplifying assumptions. In the Appendix, I show that the median LETF return when underlying asset returns are distributed zero mean iid normal is:

$$
M e d \cong - \left(\frac {S D (R _ {T} ^ {R B})}{6}\right) S k e w,\tag{14}
$$

Where $S D ( R _ { T } ^ { R B } )$ and $S k e w ( R _ { T } ^ { R B } )$ are the standard deviation and skewness of $R _ { T } ^ { R B }$ , respectively. I show in the appendix that the skewness coefficient is increasing in σ for $\sigma < { \frac { 1 } { | \beta | } } .$ Since daily return volatilities are generally well below this threshold, higher return volatility implies greater skewness over the empirically relevant range.

Table 1 displays skewness coefficients and median outcomes on leveraged ETF returns, $R _ { T } ^ { R B }$ , as implied by expression (14) when daily return volatility is $\sigma = . 0 1 5$ (which is reasonably in light of historical estimates for individual stocks), for compounding intervals of T = 5, 20, 125, and 250 days, corresponding to approximately weekly, monthly, six-month, and annual horizons. It can be observed that the median outcome is always less than the zero-mean outcome, due to the positive skewness. The divergence is greater when the horizon, T, is increased, and importantly when the absolute value of leverage, 𝛽𝛽, is increased. The divergence is economically large, especially for $\beta = 3$ , where it is equal to
<!-- source: pdf page 15 -->
-0.41%, -1.98%, -15.58%, and -39.78% at the weekly, monthly, semi-annual, and annual horizons, respectively.

*Footnote (page 14):* 19 Farago and Hjalmarsson (2023) develop a closed-form expression for the skewness of compound returns. While they do not consider the role of leverage, they show that the main determinant of the skewness of compound returns is the volatility of single-period returns.

To summarize, while volatility may or may not reduce the expected return to a constant leverage strategy depending on return serial correlations, higher volatility reliably increases the divergence of the expected or mean return from the median return over the empirically relevant ranges of leverage and daily volatility.

## III. Conclusions

Both practitioner commentary and the small academic literature emphasize a negative relation between return volatility and returns to constant leverage strategies that is easily interpreted as hardwired. I demonstrate here that there is no necessary negative relation in expectation. Rather, return serial covariances as captured by the “Variance Ratio” are crucial; if return serial correlations are on average positive then expected levered ETF returns increase in return volatility, and vice versa. Further in the presence of serial dependence, there are asymmetries in expected rebalancing costs across leveraged long vs. inverse strategies. Not only is there not a hard-wired negative relation between return volatility and expected LETF returns, in the absence of either return continuations or reversals, expected LETF returns are completely unaffected by return volatility.

On the other hand, increased return volatility does widen the gap between the median and expected leveraged ETF return, because volatility increases skewness in the distribution of compound outcomes. Further, to the extent that empirical return serial correlations for the relevant assets and time periods are empirically observed to be negative, as for example in Jegadeesh (1990) and Lehmann (1990), then higher volatility will be empirically associated with lower average leveraged ETF returns, but not for the reasons most often posited.

<!-- source: pdf page 16 -->
## Appendix: The effect of leverage and compounding on median returns

To obtain an expression for the median of the distribution of the compound rebalanced return given by (1), make the simplifying assumption that that $R _ { t } ^ { s }$ is distributed iid normal with zero mean.

In this case the expected compound return, $E ( R _ { T } ^ { R B } ) = 0$ , and the variance of the compound return is $V a r ( R _ { T } ^ { R B } ) = [ 1 +   \beta ^ { 2 } \sigma ^ { 2 } ] ^ { T } - 1 .$

Let $M _ { 3 }$ denote the third central moment of the zero-mean compound return distribution which can be expressed as

$$
M _ {3} = 2 + [ 1 + 3 \beta^ {2} \sigma^ {2} ] ^ {T} - 3 [ 1 + \beta^ {2} \sigma^ {2} ] ^ {T}.
$$

The skewness coefficient for $R _ { T } ^ { R B }$ is

$$
S k e w (R _ {T} ^ {R B}) \equiv \frac {M _ {3}}{V a r ^ {3 / 2}} = \frac {2 + \left[ 1 + 3 \beta^ {2} \sigma^ {2} \right] ^ {T} - 3 \left[ 1 + \beta^ {2} \sigma^ {2} \right] ^ {T}}{\{[ 1 + \beta^ {2} \sigma^ {2} ] ^ {T} - 1 \} ^ {3 / 2}}.
$$

Since, under these assumptions the expected or mean compound return is zero, the Cornish-Fisher (1938) approximation implies that the median outcome on $R _ { T } ^ { R B }$ , denoted Med, is approximated as:

$$
M e d (R _ {T} ^ {R B}) \cong - \left(\frac {S D (R _ {T} ^ {R B})}{6}\right) S k e w (R _ {T} ^ {R B}) = - \left(\frac {S D (R _ {T} ^ {R B})}{6}\right) \left[ \frac {2 + \left[ 1 + 3 \beta^ {2} \sigma^ {2} \right] ^ {T} - 3 \left[ 1 + \beta^ {2} \sigma^ {2} \right] ^ {T}}{\{[ 1 + \beta^ {2} \sigma^ {2} ] ^ {T} - 1 \} ^ {3 / 2}} \right].
$$

The term in backets is positive for all non-zero $\beta$ and non-zero σ, implying that the median compound return is negative (while the mean compound return is zero, due to the assumption that the mean single period return is zero.) Note that the leverage parameter appears only as $\beta ^ { 2 }$ . That is, under these assumptions the median compound return is symmetric across $\beta$ and $- \beta$

It can also be shown that the skewness coefficient is increasing in σ for $\sigma \leq 1 / | \beta | .$

## Proof:

Let $\mathbf { x } \equiv \beta ^ { 2 } \mathbf { \sigma } ^ { 2 } > 0 ,$ , and set $\mathbf { a } = 1 \mathbf { + x } ,$ so that $1+3x=3a-2$ . The skewness coefficient derived above can then be written Ske $\mathrm{w}(\mathrm{x})=\mathrm{N}(\mathrm{x}) / \mathrm{D}(\mathrm{x})^{3 / 2}$ , where $\mathrm{N}(\mathrm{x}) = (3\mathrm{a} - 2)^{\mathrm{T}} - 3\mathrm{a}^{\mathrm{T}} + 2$ and $\mathrm { D } ( \mathbf { x } ) = \mathbf { a } ^ { \mathrm { T } } - 1$

Define $\ell ( \mathbf { x } ) \equiv \ln \mathrm { S k e w } ( \mathbf { x } )$ . To obtain the first order condition for maximum skew, differentiate to obtain $\ell ^ { \prime } ( \mathrm { x } ) = \mathrm { N ^ { \prime } ( x ) / N ( x ) } - ( 3 / 2 ) \mathrm { D ^ { \prime } ( x ) / D ( x ) }$ , where $\mathrm{N}'(\mathrm{x}) = 3\mathrm{T}[(3\mathrm{a} - 2)^{\mathrm{T}-1} - \mathrm{a}^{\mathrm{T}-1}]$ and $\mathbf { D } ^ { \prime } ( \mathbf { x } ) = \mathbf { T } \mathbf { a } ^ { \mathrm { T } - 1 }$ . Setting $\ell ^ { \prime } ( \mathbf { x } ) =$ 0 and clearing denominators, the first order condition reduces to

$$
\mathrm{b} ^ {\mathrm{T} - 1} [ \mathrm{a} ^ {\mathrm{T} - 1} (2 - \mathrm{a}) - 2 ] + \mathrm{a} ^ {2 \mathrm{T} - 1} = 0 \quad (\mathrm{b} \equiv 3 \mathrm{a} - 2).
$$

Evaluating at $a = 2 ( \mathrm{i.e.,   x = 1,   b = 4} )$

$$
4 ^ {\mathrm{T} - 1} [ 2 ^ {\mathrm{T} - 1} \cdot 0 - 2 ] + 2 ^ {2 \mathrm{T} - 1} = - 2 \cdot 4 ^ {\mathrm{T} - 1} + 2 \cdot 4 ^ {\mathrm{T} - 1} = 0
$$

for every T. Hence $\ell ^ { \prime } ( \mathrm { x } ) = 0$ when $\mathrm{x}=\beta^{2} \mathrm{\sigma}^{2}=1, \mathrm{or} \mathrm{\sigma}=1 /\|\beta\|$

To verify this is a maximum, differentiate ℓ(x) again and evaluate at $\mathbf { \nabla } _ { \mathbf { X } } = 1$ , writing $z   \equiv   2 ^ { \mathrm { T } }$ , to obtain $\ell ^ { \prime \prime } ( 1 ) = - 3 \mathrm { T z } ^ { 2 } ( \mathrm { z } - \mathrm { T } - 1 ) / \left[ 1 6 ( \mathrm { z } - 1 ) ^ { 2 } ( \mathrm { z } - 2 ) \right]$ . For every integer $\mathrm{T} \geq 2, 2^{\mathrm{T}} > \mathrm{T} + 1$ (since $2 ^ { 2 } = 4 > 3$ , and $2 ^ { \mathrm { T } + 1 } =$ $2 \cdot 2^{\mathrm{T}} > 2(\mathrm{T} + 1) > \mathrm{T} + 2$ whenever $2 ^ { \mathrm { T } }   \mathrm { > T   +   1 ) }$ , so $\mathrm { z - T - 1 > 0 } ,$ , and $\ell ^ { \prime \prime } ( 1 )   \leq   0$ for every horizon considered in this paper $( \mathrm { T }   =   5 , 2 0 , 1 2 5 , 2 5 0 )$ . Since $\mathrm { S k e w ( x ) } \rightarrow 0$ as $\mathbf { x } \rightarrow 0 ^ { + }$ and rises immediately thereafter, and $\mathbf { x } =$ 1 is the only interior critical point for the horizons examined in this paper $( \mathrm { T } = 5 , 2 0 , 1 2 5 , 2 5 0$ , confirmed by direct evaluation), the skewness coefficient increases monotonically over the entire interval.

That is, the skewness coefficient of $R _ { T } ^ { R B }$ is increasing in σ for $\sigma \leq 1 / | \beta |$

<!-- source: pdf page 17 -->
Figure 1. Comparisons of predicted rebalancing costs to average rebalancing costs across 50,000 simulations, for leverage of β = 3 and β = -2. Predicted costs are based on expression (13). Simulated returns are specified for each day as:

$$
R _ {t} ^ {S} = \mu + \varepsilon_ {t} + 0. 7 5 * \mathrm{MA} * \varepsilon_ {t - 1} + 0. 5 0 * \mathrm{MA} * \varepsilon_ {t - 2} + 0. 2 5 * \mathrm{MA} * \varepsilon_ {t - 3},
$$

where $\mu$ is the mean daily return, MA is a moving average parameter that induces serial correlation in returns when non-zero, and $\varepsilon _ { t }$ is zero mean independent and identically normally distributed random component, with standard deviation equal to 0.02 or as indicated.

**Figure (unlabelled)** *(panel grouping unresolved; see validation.json)*

![Figure](figures/fig_a89ee5dc5575.png)

**Published caption:** *(none associated)* *(Panel crops: [1](figures/fig_a89ee5dc5575_p01.jpg), [2](figures/fig_a89ee5dc5575_p02.jpg), [3](figures/fig_a89ee5dc5575_p03.jpg), [4](figures/fig_a89ee5dc5575_p04.jpg), [5](figures/fig_a89ee5dc5575_p05.jpg))*

*Figure note:* Panel A: Outcomes over 5 Trading Days

<!-- source: pdf page 18 -->
**Figure (unlabelled)** *(panel grouping unresolved; see validation.json)*

![Figure](figures/fig_f412e4972ee9.png)

**Published caption:** *(none associated)* *(Panel crops: [1](figures/fig_f412e4972ee9_p01.jpg), [2](figures/fig_f412e4972ee9_p02.jpg), [3](figures/fig_f412e4972ee9_p03.jpg), [4](figures/fig_f412e4972ee9_p04.jpg), [5](figures/fig_f412e4972ee9_p05.jpg))*

<!-- source: pdf page 19 -->
**Table 1**

**Published caption:** Table 1: The Effect of Leverage and Compounding on Median leveraged ETF Returns. This Table displays median compound ETF returns as implied by expression (14), when expected returns are zero. The daily underlying returns are assumed to be zero-mean distributed independent and identical normal. The illustration assumes a daily return standard deviation of 0.015.

| Table 1: Numerical Illustration: Median Compound Returns |  |  |  |
| --- | --- | --- | --- |
|  |  | Levered Returns |  |
| Leverage | Days | Skewness Coefficient | Median (%) |
| 3 | 5 | 0.242 | -0.41% |
| 2 | 5 | 0.161 | -0.18% |
| 1 | 5 | 0.081 | -0.05% |
| -1 | 5 | 0.081 | -0.05% |
| -2 | 5 | 0.161 | -0.18% |
|  |  |  |  |
| 3 | 20 | 0.585 | -1.98% |
| 2 | 20 | 0.386 | -0.87% |
| 1 | 20 | 0.192 | -0.21% |
| -1 | 20 | 0.192 | -0.21% |
| -2 | 20 | 0.386 | -0.87% |
|  |  |  |  |
| 3 | 125 | 1.742 | -15.58% |
| 2 | 125 | 1.066 | -6.13% |
| 1 | 125 | 0.507 | -1.43% |
| -1 | 125 | 0.507 | -1.43% |
| -2 | 125 | 1.066 | -6.13% |
|  |  |  |  |
| 3 | 250 | 2.942 | -39.78% |
| 2 | 250 | 1.624 | -13.59% |
| 1 | 250 | 0.732 | -2.94% |
| -1 | 250 | 0.732 | -2.94% |
| -2 | 250 | 1.624 | -13.59% |

*Merged cells are shown once, at their first row and column; the HTML and cells files keep the exact structure.*

Table files: [HTML](tables/tbl_cfa4b18880d3.html), [cells](tables/tbl_cfa4b18880d3.json), [image](tables/tbl_cfa4b18880d3.jpg)

<!-- source: pdf page 20 -->
## References

Avellaneda, M. and S. Zhang, 2010, Path-Dependence of Leveraged ETF Returns, Siam Journal of Financial Mathematics, 1, 586-603.

Bali, T., S. Brown, S. Murray, and Y. Tang, 2017, [A Lottery Demand-Based Explanation of the Beta Anomaly,](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/abs/lotterydemandbased-explanation-of-the-beta-anomaly/B5B9F0A65256E6E86B45D72AE0A256C4) [Journal of Financial and Quantitative Analysis,](http://depts.washington.edu/jfqa/) 52, 2369-2397.

Barnhorst, B., and C. Cocozza, 2021, Inverse and Leveraged ETFs: Considering the Alternatives, downloaded from www.financialplanningassociation.org/sites/default/files/2021-08/JAN11%20Inverse%20and%20Leveraged%20ETFs%20-%20Considering%20the%20Alternatives.pdf

Bian, J., Da, Z., He, Z., Lou, D., Shue, K., and Zhou, H., 2026, The drivers and implications of retail margin trading, Journal of Finance, 81, 2217-2270.

Cheng, M. and A. Madhavan, 2009, The dynamics of leveraged and inverse exchange-traded funds, Journal of Investment Management, 7, 43-62.

Cheng, M. and A. Madhavan, 2026, Twenty years of leveraged and inverse ETP: What have we learned?, Journal of Investment Management, forthcoming.

Cornish, E., and R. Fisher, 1938, "Moments and cumulants in the specification of distributions" Review of the International Statistical Institute, 5, 307–320.

Eraker, B., and M. Ready, 2015, Do investors overpay for stocks with lottery-like payoffs? An examination of the returns of OTC stocks, Journal of Financial Economics, 115, 486-504.

Farago, A., Hjalmarsson, E., 2023, Compound returns are positively skewed, Review of Finance, 27, 495-538.

Gennaioli, N., A. Shleifer, and R. Vishny, 2021, Neglected risks, financial innovation, and financial fragility, Journal of Financial Economics, 104, 452-468.

Ivanov, I. and S. Lenkey, Do leveraged ETFs really amplify late-day returns and volatility? Journal of Financial Markets, November 2018, Pages 36-56.

Jarrow, R ., 2010, Understanding the risk of leveraged ETFs, Finance Research Letters, 7, 135-139.

Jegadeesh, N., 1990, Evidence of predictable behavior of security returns, The Journal of Finance, 45, 881–98.

Lehmann, B.., 1990, Fads, martingales, and market efficiency, The Quarterly Journal of Economics, 105, 1–28.

Lo, A., and C. MacKinlay, 1988, Stock market prices do not follow random walks: Evidence from a simple specification test, Review of Financial Studies, 1, 41-66.

Murray, C., and M. Sammon, 2026, The costs and benefits of leveraged ETFs, working paper, available at [The Costs and Benefits of Leveraged ETFs by Chris Murray, Marco Sammon :: SSRN.](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7133021)

<!-- source: pdf page 21 -->
Pitcher, Jack, 2025, Popular Leveraged Funds Shock Investors with Huge Losses, Wall Street Journal, published online October 23, 2025, at [https://www.wsj.com/finance/investing/popular-leveraged-funds-shock-investors-with-huge-losses-5714f1ac.](https://www.wsj.com/finance/investing/popular-leveraged-funds-shock-investors-with-huge-losses-5714f1ac)

Wang, Baolian, 2025, Multi-day Return Properties of Leveraged Index ETFs, working paper, available at [https://ssrn.com/abstract=5119860.](https://ssrn.com/abstract=5119860)
