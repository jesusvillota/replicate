![The Ohio State University logo, a red block letter O.](c97aa0bea44f5da94a3637273e56b49c_1_img.webp)

*Charles A. Dice Center for  
Research in Financial Economics*

# The Unintended Consequences of Rebalancing

Campbell R. Harvey,  
Duke University and NBER

Michele G. Mazzoleni,  
Capital Group

Alessandro Melone,  
The Ohio State University

Dice Center WP 2025-01  
Fisher College of Business WP 2025-03-001

January 14, 2026# The Unintended Consequences of Rebalancing<sup>\*</sup>

Campbell R. Harvey<sup>†</sup>    Michele G. Mazzoleni<sup>‡</sup>    Alessandro Melone<sup>§</sup>

January 14, 2026

## Abstract

Institutional investors engage in trillions of dollars of regular portfolio rebalancing, often based on calendar schedules or deviations from allocation targets. We document that such rebalancing has a market-wide impact and generates predictable price patterns. When stocks are overweight, funds sell stocks and buy bonds, leading to a decrease in equity returns of 17 basis points over the next day. Our results are robust to controls for momentum, reversals, and macroeconomic information. Importantly, we estimate that current rebalancing practices cost investors about \$16 billion annually – or \$200 per U.S. household. Moreover, the predictability of these trades enables certain market participants to profit by front-running the orders of large institutional funds. While rebalancing remains a fundamental tool for investors, our findings highlight the costs associated with prevailing strategies and emphasize the need for innovative approaches to mitigate these costs.

**Keywords:** Rebalancing, Institutional Investors, Return Dynamics, Price Pressures, Reversal.

**JEL codes:** G11, G12, G23.

---

<sup>\*</sup>We thank Aleksandar Andonov, Philippe van der Beck, Zahi Ben-David, Hank Bessembinder, Andrea Buffa, Aditya Chaudhry, Huaizhi Chen (discussant), Zhi Da (discussant), Magnus Dahlquist, Kent Daniel (discussant), Valentin Haddad (discussant), Paul Huebner, Kristy Jansen, Greg Kadlec, Paymon Khorrami, Antonia Kirilova (discussant), Federico Mainardi, Jim Masturzo, Lira Mota, Christian Opp, Jonathan Parker (discussant), Taisiya Sikorskaya, Amar Soebhag, René Stulz, Matti Suominen (discussant), Costanza Torricelli (discussant), Stijn Van Nieuwerburgh, Fernando Zapatero, as well as seminar and conference participants at Cornell University, Carnegie Mellon University, University of Oxford, Georgia State University, The Ohio State University, Einaudi Institute of Economics and Finance, European Securities and Markets Authority, Council of Institutional Investors, CFA UK, Vanguard, Bloomberg, INQUIRE Europe, the AFA 2026 Annual Meeting, the NBER Asset Pricing Spring 2025 Meeting, the CEPR Paris Symposium 2025, the Red Rock Finance Conference 2025, the SFS Cavalcade 2025 Annual Meeting, the Imperial College Hedge Fund Conference 2025, the Isenberg Finance Conference 2025, the Esade Spring Workshop 2025, and the LTI-Bank of Italy Workshop 2025 for helpful comments and discussions. The views expressed in this article are those of the authors and do not necessarily reflect those of Capital Group.

<sup>†</sup>Fuqua School of Business, Duke University and NBER. E-mail: [cam.harvey@duke.edu](mailto:cam.harvey@duke.edu).

<sup>‡</sup>Capital Group. E-mail: [mazzoleni.research@gmail.com](mailto:mazzoleni.research@gmail.com).

<sup>§</sup>Fisher College of Business, The Ohio State University. E-mail: [melone.11@osu.edu](mailto:melone.11@osu.edu).*“JPMorgan Says Stocks to Suffer \$150 Billion Rebalancing Sales”*

Bloomberg (June 15, 2023)

*“Pension Rebalancing Threatens to Spur \$26 Billion Equity Selloff”*

Bloomberg (September 29, 2022)

*“Big investors to shift billions from bonds into stock markets”*

Financial Times (March 11, 2022)

## Introduction

For more than three decades, investment managers have employed regular rebalancing – selling stocks and purchasing bonds when equities outperform bonds, and vice versa – as a key strategy to align portfolio weights with their target allocations.<sup>1</sup> Although this rebalancing activity is often perceived as a significant driver of aggregate price fluctuations, the academic literature has only recently begun to investigate whether and why this is the case. For example, [Parker, Schoar, and Sun \(2023\)](#) find that, while rebalancing by target date funds (TDFs) influences the cross-sectional pattern of returns across stocks, the aggregate effects are likely to be negligible given the current size of TDFs. However, most investors – including pension, sovereign wealth, and mutual funds – have relatively tight mandates and maintain stable asset shares (see, e.g., [Gabaix and Kojien, 2021](#)). Therefore, as prices fluctuate over time, these funds must buy losers and sell winners, which indicates a potentially broader and stronger rebalancing impact on aggregate dynamics.

In this paper, we study the market-wide economic implications of rebalancing. While rebalancing is a core strategy for maintaining portfolio diversification and managing liquidity, our results highlight that existing rebalancing policies induce significant predictability, costing investors billions of dollars every year. Furthermore, mechanical rebalancing enables certain traders to front-run the predictable orders of large funds, generating significant risk-adjusted profits. A key challenge in studying rebalancing is that institutional policies are heterogeneous and partially unobserved. Some investors rebalance quarterly, others monthly or even daily, and many adjust their portfolios only when asset weights deviate sufficiently from target allocations. Rather than attempting to measure exact individual rebalancing strategies, we adopt a time-series approach that captures common rebalancing incentives implied by realized asset returns. This “macro identification” strategy allows us to uncover systematic and predictable components of rebalancing activity shared across institutional investors and to study their implications for asset prices.

---

<sup>1</sup>See, e.g., [Perold and Sharpe \(1988\)](#) for an early contribution on rebalancing.To develop comprehensive measures of rebalancing activity, we analyze weight deviations in balanced equity–bond portfolios. Specifically, consider a portfolio with 60% of its capital invested in the S&P 500 Index and 40% in 10-year U.S. Treasury note. We calculate weight deviations of this simulated 60/40 portfolio using daily futures returns during the period 1997–2023. When stocks outperform bonds, they become overweight, and rebalancers must sell stocks and buy bonds to realign portfolio weights to their target allocations. Thus, weight deviations represent a natural proxy for rebalancing activities: the larger the deviation, the greater the likelihood and the potential magnitude of rebalancing.

We compute weight deviations from portfolio targets using two rule-based rebalancing approaches, Threshold and Calendar, that reflect the investment policies of different institutions. The Threshold (or state-dependent) approach adjusts positions when portfolio weights exceed predetermined distances from targets, reflecting the idea that allowing for portfolio drifts within defined ranges helps minimize transaction costs. Furthermore, many institutional investors have regular cash flow needs at the beginning of every month (see, e.g., [Etula, Rinne, Suominen, and Vaittinen, 2020](#)). For example, mature pension funds often sell assets at month-end to raise cash for member benefit payments. The Calendar approach captures these scheduled rebalancing activities and can be viewed as a time-dependent rebalancing. Because Threshold and Calendar signals are measured with noise, they should be interpreted as capturing the likely direction and magnitude of rebalancing activity. Importantly, because trading activity is naturally coordinated in both direction and timing by past returns, such rebalancing may generate price impact. Both rebalancing signals are easy to compute, available in real-time, and applicable for any frequency with available return data.

Using these rebalancing signals, we provide novel evidence on U.S. aggregate price dynamics related to rebalancing activities. We find a one-standard-deviation increase in the Threshold (Calendar) signal leads to a *decrease* in equity returns of approximately 16 basis points (bps) (17 bps) and an *increase* in bond returns of about 4 bps (2 bps) over the next trading day. Rebalancing pressures revert almost entirely within two weeks, consistent with the fact that rebalancing is a by-product of institutional investors’ mandates that likely conveys little information about market fundamentals. Our results are robust to including controls for momentum, reversals, macroeconomic activity, and sentiment indicators. Weargue that these results are conservative. Without actual daily trades from all rebalancers, our rebalancing signals only proxy for a representative rebalancer's activity. Consequently, the documented effects likely underestimate the true impact we would observe if we knew the precise timing of individual investors' rebalancing activities.

A back-of-the-envelope calculation using our predictability results estimates that the rebalancing costs borne by institutional investors can exceed 8 bps per year. For a market potentially exceeding \$20 trillion in size, rebalancing pressures could translate into an annual cost of \$16 billion, or about \$200 per U.S. household each year. To put these numbers in perspective, these costs are higher than those institutional investors pay to invest passively across equity and bond markets. In other words, rebalancing a balanced equity–bond portfolio might cost more than the fees to access those markets in the first place. Moreover, since rebalancing costs recur annually, their true present value is substantially larger. At the same time, we show that simple randomization in rebalancing schedules – all else being equal – largely eliminates these costs, underscoring that much of this burden arises from mechanical rebalancing pressures.

We leverage four datasets to link our rebalancing signals to actual quantities. First, we use weekly CFTC futures positions and show that hedgers sell (buy) equities when they are overweight (underweight) relative to bonds. We then exploit CFTC's weekly Large Trader Net Position Changes and ANcerno's daily data on institutional equity transactions, which reveal that asset managers and pension funds act as rebalancers. Finally, ICI mutual fund flows show that mutual funds sell equities and buy bonds when equities become overweight. Taken together, these diverse sources suggest that institutional investors' trading behavior is broadly consistent with our interpretation.

We conduct several additional analyses to validate the economic interpretation of our rebalancing signals. First, we identify seasonal patterns in the predictability of the Threshold and Calendar signals, observing that Calendar predictability is strong at month-end but absent at other times and that the predictive power and economic significance of both signals increase as the quarter-end approaches. These patterns are consistent with month- or quarter-end trades motivated by liquidity needs or benchmark tracking, rather than risk or behavioral factors. Second, we demonstrate that our signals predict equity and bond excess returns with opposite signs, indicating trades in both markets consistent with our interpre-tation. Third, we find that the predictive power of these signals became significant in the early 2000s, which reflects changes in pension fund allocations, cash flow demands, and 2006 legislation affecting the TDF industry. Fourth, we show that our rebalancing predictions apply to large- and small-cap stocks but not to value and growth stocks, aligning with funds targeting specific equity market segments. Finally, we document that the Threshold and Calendar signals also extend to international equity markets.

Finally, mechanical rebalancing offers certain investors the opportunity to front-run the predictable trades of large funds. To explore the potential economic value of these front-running strategies, we construct a managed portfolio that replicates the trades of an investor anticipating rebalancing activities. This portfolio uses our Threshold and Calendar signals to develop a cross-asset trading strategy. This strategy involves taking either a long position in S&P 500 futures while shorting 10-year Treasury note futures, or vice versa, based on the rebalancing signals. The managed portfolio constructed using these rebalancing signals delivers significant positive alphas and achieves a Sharpe ratio exceeding 1 over the 1997 to 2023 sample period.

Our work contributes to a growing literature on the effects of rebalancing by institutional investors.<sup>2</sup> [Da, Larraín, Sialm, and Tessada \(2018\)](#) document market-wide price pressure for stocks and bonds in Chile following recommendations for asset reallocation. [Camanho, Hau, and Rey \(2022\)](#) show that aggregate fund flows prompted by global portfolio rebalancing affect exchange rate dynamics. [Peng and Wang \(2023\)](#) document that mutual funds have persistent factor demand that forces them to frequently rebalance their portfolios' factor exposures, which leads to predictable stock-level trading and price pressure. [Parker, Schoar, and Sun \(2023\)](#) demonstrate that rebalancing by TDFs influences the fund flow patterns across mutual funds and the cross-sectional patterns of returns across stocks. [Andonov, Eiling, and Xu \(2024\)](#) extend the TDFs evidence to international capital markets, showing that these funds frequently engage in contrarian rebalancing between domestic and foreign equities. [Chen \(2025\)](#) shows that active mutual funds rebalance their portfolios by selling shares in recently well-performing positions, in line with diversification and risk management motives. [Parker and Sun \(2025\)](#) document that trading by TDFs acted as a significant stabilizing force in U.S. equity markets during the COVID-19 pandemic. [Lu and Wu \(2025\)](#)

---

<sup>2</sup>[Buffa, Vayanos, and Woolley \(2022\)](#) provide a theoretical model to study the equilibrium effects of rebalancing.find that rebalancing pressures play a significant role in the transmission of monetary shocks to the stock market. [Sammon and Shim \(2026\)](#) find that index funds incur adverse selection costs from rebalancing in response to stock market composition changes, buying at high prices when firms issue shares and selling at low prices when firms repurchase them. Our paper provides the first evidence of aggregate price effects for U.S. stocks and bonds arising from portfolio rebalancing activity.

This paper is also broadly related to the literature on price pressures. Since the work of [Shleifer \(1986\)](#) and [Harris and Gurel \(1986\)](#), an important strand of the literature has focused on event studies (e.g., index inclusion or new regulations) to understand cross-sectional price patterns; however, the literature has only recently started to explore potential aggregate price effects.<sup>3</sup> If aggregate demand is inelastic, shifts in institutional demand can generate large price impact ([Kojien and Yogo, 2019](#); [Gabaix and Kojien, 2021](#); [Pavlova and Sikorskaya, 2023](#)). [Li, Pearson, and Zhang \(2021\)](#) document that flows based on IPO regulations influence the Chinese aggregate stock market. [Jansen \(2021\)](#) investigates the effect of long-term investors demand shifts on government bond yields. [Bretscher, Schmid, Sen, and Sharma \(2025\)](#) study the price impact of demand shocks for the corporate bond market both for large institutions and at the aggregate level. [Haddad, Huebner, and Loualiche \(2025\)](#) find that the rise of passive investing over the last 20 years has lowered the elasticity of aggregate demand. Most closely related to our paper, [Hartzmark and Solomon \(2025\)](#) find that uninformed, predictable buying pressures from dividend payments are associated with higher aggregate market returns. In addition, [Chen, Noronha, and Singal \(2006\)](#) and [Petajisto \(2011\)](#) find that index funds incur substantial costs due to mechanically buying stocks at elevated prices following index inclusion and selling them at depressed prices after index deletion. Our contribution is to show that mechanical rebalancing exerts a significant *market-wide* price impact. We then use our regression estimates to quantify the economic costs of current rebalancing activity.

The paper is organized as follows. In the next section, we provide institutional details on

---

<sup>3</sup>[Warther \(1995\)](#) and [Edelen and Warner \(2001\)](#) are two notable early contributions documenting a positive relationship between aggregate flows and *concurrent* aggregate market returns. Another interesting early paper is [Ritter and Chopra \(1989\)](#), who attributes the turn-of-the-year effect – the fact that returns on small firms are unusually high in January – to buying pressure from individuals reinvesting the proceeds of December’s tax-motivated sales and from institutional investors shifting their portfolio allocations to small, risky stocks after year-end window dressing.rebalancing and construct our return-based rebalancing proxies. Section 2 presents our main evidence on the relationship between rebalancing activities and aggregate price dynamics. In Section 3, we conduct several validation analyses for the economic interpretation of our rebalancing signals. Section 4 uses rebalancing signals to construct a portfolio that exploits market reversals. Section 5 discusses both the costs and benefits of rebalancing. Some concluding remarks are offered in the final section.

# 1 Rebalancing: Motivation, Measurement, and Interpretation

## 1.1 Evidence on Institutional Rebalancing Practices

We define *rebalancing* as the activity of selling recent winners and buying recent losers to restore portfolio weights to their target allocations. In a multi-asset context, a 60/40 equity–bond portfolio is a commonly employed target asset allocation; for an early reference, see [Ambachtsheer \(1987\)](#), and for a more recent discussion, see [Rattray, Granger, Harvey, and Van Hemert \(2020\)](#). For example, large pension plans and sovereign wealth funds commonly target the 60/40 asset mix (e.g., [Chambers, Dimson, and Ilmanen, 2012](#)). Also, [Gabaix and Kojien \(2021\)](#) document that, on average, pension funds hold 60% in equities. Target allocations can be derived from theoretical considerations – such as TDF glide paths – or can be decided by investment committees based on multiple inputs, as with public pension funds.

As the value of risky assets fluctuate over time, so do their relative allocations or weights within a portfolio. This simple observation carries important asset management implications. In fact, most institutional investors, such as pension funds or mutual funds, are expected – as stipulated by their investment policies – to maintain their asset weights within certain ranges.<sup>4</sup> For example, Figure 1 in [Gabaix and Kojien \(2021\)](#) documents that the relative

---

<sup>4</sup>Rebalancers include various institutional investors, such as public and private pension funds, endowments, sovereign wealth funds, asset managers, and wealth managers. In the U.S. retirement industry, as of year-end 2022, DB plans, defined contribution (DC) plans, and individual retirement accounts (IRAs) held \$37.8 trillion, according to data from the Federal Reserve’s Financial Accounts database. Other typesequity share in the portfolios of institutional investors remains relatively stable over time. Figure 1 complements these findings by focusing on U.S. defined benefit (DB) pension funds. Over the last two decades, the relative allocations to public equity and fixed income have closely tracked their stated targets, resembling the classic 60/40 portfolio and suggesting that public pension funds must regularly engage in rebalancing.

![Line graph showing U.S. Defined Benefit Pension Funds' Asset Allocation Over Time from 2003 to 2022. The Y-axis is Relative Asset Allocation (0.0 to 1.0). The X-axis is Fiscal Year (2003 to 2022). The graph displays four series: Equity Actual (solid blue line with dots), Equity Target (dashed blue line), Fixed Income Actual (solid orange line with dots), and Fixed Income Target (dashed orange line). Equity allocations are consistently around 64-66%, and Fixed Income allocations are consistently around 34-36%.](c612471efd459a5cada3a6b41c33d2fb_2_img.webp)

<table border="1">
<thead>
<tr>
<th>Fiscal Year</th>
<th>Equity Actual</th>
<th>Equity Target</th>
<th>Fixed Income Actual</th>
<th>Fixed Income Target</th>
</tr>
</thead>
<tbody>
<tr><td>2003</td><td>0.62</td><td>0.65</td><td>0.36</td><td>0.35</td></tr>
<tr><td>2004</td><td>0.65</td><td>0.65</td><td>0.34</td><td>0.34</td></tr>
<tr><td>2005</td><td>0.65</td><td>0.65</td><td>0.34</td><td>0.34</td></tr>
<tr><td>2006</td><td>0.66</td><td>0.65</td><td>0.33</td><td>0.33</td></tr>
<tr><td>2007</td><td>0.67</td><td>0.65</td><td>0.33</td><td>0.33</td></tr>
<tr><td>2008</td><td>0.63</td><td>0.65</td><td>0.36</td><td>0.34</td></tr>
<tr><td>2009</td><td>0.62</td><td>0.65</td><td>0.37</td><td>0.34</td></tr>
<tr><td>2010</td><td>0.63</td><td>0.65</td><td>0.36</td><td>0.34</td></tr>
<tr><td>2011</td><td>0.65</td><td>0.65</td><td>0.35</td><td>0.34</td></tr>
<tr><td>2012</td><td>0.64</td><td>0.65</td><td>0.35</td><td>0.34</td></tr>
<tr><td>2013</td><td>0.66</td><td>0.65</td><td>0.33</td><td>0.34</td></tr>
<tr><td>2014</td><td>0.67</td><td>0.65</td><td>0.33</td><td>0.34</td></tr>
<tr><td>2015</td><td>0.66</td><td>0.65</td><td>0.33</td><td>0.34</td></tr>
<tr><td>2016</td><td>0.65</td><td>0.65</td><td>0.34</td><td>0.34</td></tr>
<tr><td>2017</td><td>0.67</td><td>0.65</td><td>0.32</td><td>0.34</td></tr>
<tr><td>2018</td><td>0.65</td><td>0.65</td><td>0.34</td><td>0.34</td></tr>
<tr><td>2019</td><td>0.65</td><td>0.65</td><td>0.34</td><td>0.34</td></tr>
<tr><td>2020</td><td>0.64</td><td>0.65</td><td>0.35</td><td>0.34</td></tr>
<tr><td>2021</td><td>0.67</td><td>0.65</td><td>0.32</td><td>0.34</td></tr>
<tr><td>2022</td><td>0.64</td><td>0.65</td><td>0.35</td><td>0.34</td></tr>
</tbody>
</table>

**Figure 1: U.S. Defined Benefit Pension Funds' Asset Allocation Over Time.** This figure shows the average relative allocations by fiscal year across U.S. defined benefit pension funds produced by the Center for Retirement Research at the Boston College and available at [Public Plans Data](#). Equity allocations include investments in domestic and international public equity markets. Fixed income includes cash allocations in addition to bonds. Relative allocations are computed by normalizing portfolio weights for the sum of equity and fixed income allocations. As of the end of fiscal year 2022, public equity and fixed income allocations amounted to about 64% of total portfolio weights. Annual observations. The sample period is 2003 to 2022.

Rebalancing frequency varies across investor types and often reflects cash flow management. For instance, pension funds, which typically face greater outflows than inflows, tend to rebalance at month-end to raise capital for benefit payments (e.g., [Etula et al., 2020](#)). Mutual funds, by contrast, experience continuous inflows and outflows and may rebalance daily to adjust allocations, e.g., by deploying inflows into underweight assets.<sup>5</sup>

of asset owners may also have an influence. Among sovereign wealth funds, the Norges Bank Investment Management, which targets approximately a 70/30 equity–bond portfolio, alone held slightly more than 1% of the U.S. stock market at the end of year 2023. U.S. university endowments also accounted for almost \$1 trillion at the end of fiscal year 2021, holding about 0.5% of the stock market assuming a 25% allocation to U.S. public equities, according to data from the National Center for Education Statistics.

<sup>5</sup>For example, a prospectus for a BlackRock balanced fund reports: “(...) the Fund’s portfolio may beBenchmark design also shapes rebalancing practices, as managers seeking to minimize tracking error often align with their benchmark's schedule. Practices can vary: Vanguard's TDF benchmarks used to rebalance daily, the S&P 500 Target Date Index series monthly, and the Morningstar Target Risk Series quarterly.<sup>6</sup> Rebalancing is often implemented through derivatives such as futures and swaps.

Evidence from public pension plans provides additional insights into institutional practices. A Seattle City Employees' Retirement System memo (September 2020) reports that most rebalancing is conducted "synthetically" by an overlay manager using futures tied to major equity benchmarks (e.g., S&P 500, MSCI EAFE) and U.S. Treasuries, with periodic use of physical securities to adjust notional exposure. The overlay manager noted that most clients rebalance at month-end to minimize tracking error versus benchmarks – also rebalanced monthly – or within a few days of month-end to align with external cash flows. Similarly, a Sacramento County Employees' Retirement System memo (February 2024) describes how State Street Global Advisors rebalances the total fund through a hybrid approach combining calendar- and threshold-based rules: rebalancing occurs quarterly at quarter-end unless tolerance bands are breached mid-quarter. A February 2018 San Francisco Employees' Retirement System memo highlights the role of tolerance bands, cash flows, and tracking error in overlay program design, while a 2015 Montgomery County Public Schools memo documents a month-end overlay-based rebalancing policy.<sup>7</sup>

These institutional case studies are in line with broader survey evidence and related empirical research. According to a recent survey of rebalancing policies conducted by the National Association of State Retirement Administrators (NASRA) – a national organization with over 50 members representing \$3.5 trillion in AUM – all public pension funds in the survey use either a predetermined schedule rebalancing policy, a threshold-based approach triggered when an allocation range is breached, or a combination of the two (see [NASRA](#)). Related discussions on the merits of different rebalancing approaches appear in

---

brought closer to the Fund's target asset allocation either through the direction of daily cash flows to suitable underlying funds or by interim rebalancings" (see [SEC report](#)).

<sup>6</sup>For example, as Vanguard reports in relation to its TDFs: "In practice, we first use daily cash flows to maintain portfolio level allocations. If daily cash flows are insufficient to bring the portfolios within the Threshold band of the target asset allocation, we then buy and sell securities to realign the funds' asset allocation back with the target" (see [Vanguard](#)).

<sup>7</sup>Documentation can be found here: [SCERS](#); [SFERS](#); and [Montgomery](#).research by Meketa Investment Group, one of the largest institutional investment advisory firms (Benham, Obregon, and Simanovich, 2018)), in studies by Vanguard Group on TDF rebalancing (Zhang et al., 2022; Zhang and Ahluwalia, 2024), and in a 2018 discussion note by Norges Bank Investment Management (see Norges). Both Vanguard and Norges Bank adopt a threshold-based rebalancing approach.

## 1.2 Measuring Rebalancing Activity

**Rule-Based Rebalancing: Threshold and Calendar Approaches.** Building on our research on institutional rebalancing policies, we construct two measures of rebalancing activity by focusing on the most widely used rule-based approaches: threshold rebalancing and calendar rebalancing. *Threshold rebalancing* seeks to minimize transaction costs by allowing portfolio weights to drift within tolerance bands around target allocations. When an asset's weight deviates from its target by more than a preset threshold – for example, two percentage points – the portfolio is rebalanced. Accordingly, threshold rebalancing can be interpreted as state-dependent, as trading is triggered by the realized state of the portfolio. *Calendar rebalancing*, by contrast, is time-dependent, following a deterministic schedule, typically monthly or quarterly. Notice that while the timing of Calendar rebalancing is predetermined, the magnitude of the rebalancing trades remains unknown. The Threshold signal captures faster, intra-month rebalancing, whereas the Calendar signal captures slower, month-end rebalancing. Importantly, these approaches are not mutually exclusive, and portfolio managers may combine them in practice.

**Extracting Predictive Signals from Rebalancing Processes.** We simulate the daily dynamics of 60/40 equity–bond portfolios rebalanced with Threshold and Calendar methodologies. The Threshold methodology rebalances a portfolio back to target weights when the weights deviate beyond a set distance from their targets, while the Calendar methodology rebalances to target weights on the last business day of each month.

We extract Threshold and Calendar rebalancing signals by measuring the *distance* of the equity allocation from its target at the end of the previous trading day. The equity allocation is a function of trailing equity and bond market returns. At any point in time  $t$ , portfolioweights  $w$  are updated as a function of past weights, equity returns, and bond returns:

$$w_{t+1}(w_t; R_{t+1}^{SP}; R_{t+1}^{10Y}) = \frac{w_t(1 + R_{t+1}^{SP})}{w_t(1 + R_{t+1}^{SP}) + (1 - w_t)(1 + R_{t+1}^{10Y})},$$

where  $R_{t+1}^{SP}$  and  $R_{t+1}^{10Y}$  indicate the returns earned by the S&P500 and the 10-year Treasury note, respectively. After one period, the deviation from the target equity allocation is given by  $w_{t+1}(w_t; R_{t+1}^{SP}; R_{t+1}^{10Y}) - 60\%$ . For example, if the equity market outperforms the bond market by 10% on a single day within the 60/40 portfolio, both rebalancing signals should increase by approximately 2.26%. The only exceptions to this rule occur when rebalancing is triggered – either because the equity weight breaches its predefined range (Threshold signal) or because day  $t$  is the last business day of the month (Calendar signal).<sup>8</sup> Appendix B provides a detailed explanation of their construction. Thus, both Threshold and Calendar signals should negatively predict equity market returns and positively predict Treasury market returns. Positive values for these signals indicate overweight positions in equities and equivalent underweight positions in bonds, which would trigger rebalancing.

We highlight two key parameters for constructing and testing our signals: (i) the rebalancing range used in the Threshold signal’s construction and (ii) the range of days when the Calendar signal is expected to display the strongest predictability. We posit two hypotheses. First, the relevant range for the Threshold signal should cluster around 2 percentage points, consistent with institutional rebalancing practices and published guidance by large investors such as Norges and Vanguard. Second, that the predictability of the Calendar signal should concentrate toward month-end, when pension funds typically face liquidity needs. We test these hypotheses next.

**Signal Calibrations and Univariate Predictive Regressions.** We define a Threshold signal by  $\text{Threshold Signal}_t^\delta$ , where  $\delta$  indicates the rebalancing range (i.e., portfolio rebalancing occurs when the distance of a portfolio weight from its target exceeds  $\delta$ ). To evaluate different calibrations of  $\text{Threshold Signal}_t^\delta$ , we run the following regression for different values

---

<sup>8</sup>Consider a 60/40 portfolio in dollars. If the equity market increases by 10% and the bond market remains unchanged, the portfolio value becomes  $66 + 40 = \$106$ . The equity allocation is now  $66/106 = 62.26\%$ . To restore the original allocation, we need to rebalance by trading  $0.60 \times 0.40 \times 10\% = 2.4\%$  of the initial \$100 portfolio value – i.e., sell \$2.4 of equities and buy \$2.4 of bonds.of  $\delta$ :

$$Ret_{t+1} = \gamma_0 + \gamma_1 \text{Threshold Signal}_t^\delta + \epsilon_{t+1} , \quad (1)$$

where  $Ret_{t+1}$  is the difference between S&P 500 and 10-year Treasury note futures returns, and  $\text{Threshold Signal}_t^\delta$  is constructed as in (B.1). Detailed information about the data sources is provided in Appendix A. In Figure 2, we show the  $t$ -statistics of the  $\gamma_1$  coefficient as a function of the chosen  $\delta$  value, which in effect determines how often a threshold rebalancer may realign their portfolio weights.<sup>9</sup>

![Figure 2: A bar chart showing t-statistics for the predictive coefficient of Threshold Signal_t^delta as a function of the rebalancing range delta (%). The x-axis represents Threshold delta (%) from 0 to 4. The y-axis represents t-stat from -4 to 0. Blue bars show the t-stat for each delta value. A horizontal dashed red line is at approximately -2.58, representing the 1% critical value. The t-stat values are mostly negative, with a peak around delta = 2%.](0eaafd422a14359a586f13df57275755_4_img.webp)

<table border="1">
<caption>Approximate data points from Figure 2</caption>
<thead>
<tr>
<th>Threshold <math>\delta</math> (%)</th>
<th>t-stat</th>
</tr>
</thead>
<tbody>
<tr><td>0.0</td><td>-3.8</td></tr>
<tr><td>0.2</td><td>-3.7</td></tr>
<tr><td>0.4</td><td>-3.6</td></tr>
<tr><td>0.6</td><td>-3.5</td></tr>
<tr><td>0.8</td><td>-3.4</td></tr>
<tr><td>1.0</td><td>-3.3</td></tr>
<tr><td>1.2</td><td>-3.2</td></tr>
<tr><td>1.4</td><td>-3.1</td></tr>
<tr><td>1.6</td><td>-3.0</td></tr>
<tr><td>1.8</td><td>-2.9</td></tr>
<tr><td>2.0</td><td>-2.8</td></tr>
<tr><td>2.2</td><td>-2.7</td></tr>
<tr><td>2.4</td><td>-2.6</td></tr>
<tr><td>2.6</td><td>-2.5</td></tr>
<tr><td>2.8</td><td>-2.4</td></tr>
<tr><td>3.0</td><td>-2.3</td></tr>
<tr><td>3.2</td><td>-2.2</td></tr>
<tr><td>3.4</td><td>-2.1</td></tr>
<tr><td>3.6</td><td>-2.0</td></tr>
<tr><td>3.8</td><td>-1.9</td></tr>
<tr><td>4.0</td><td>-1.8</td></tr>
</tbody>
</table>

**Figure 2: Threshold Calibrations and Predictability.** This figure shows the  $t$ -statistics for the predictive coefficient of  $\text{Threshold Signal}_t^\delta$  in (1) for different values of  $\delta$ , where  $\delta$  indicates the rebalancing range (i.e., portfolio rebalancing occurs when the distance of a portfolio weight from its target exceeds  $\delta$ ). The dependent variable is the difference between the S&P 500 and the 10-year Treasury note futures returns.  $t$ -statistics are based on heteroskedasticity-consistent standard errors. The dashed red line denotes the 1% critical value assuming a single test. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

We focus on two results. First, consistent with our interpretation, the Threshold signal is negatively related to subsequent daily S&P 500 returns in excess of the 10-year Treasury note. Second, the signal’s predictive power peaks around 2 percentage points and declines

<sup>9</sup>Because residual autocorrelation does not display systematic persistence across lags, we report heteroskedasticity-robust standard errors throughout the paper. Using heteroskedasticity- and autocorrelation-consistent standard errors yields virtually identical result; see Appendix Figure D.1. Additional robustness checks for other main results are reported in Appendix D.for values of  $\delta$  above 2.5%. This evidence aligns with our first hypothesis, which is supported by institutional practices of large funds, and is intuitive when viewed through the lens of rebalancing frequency. When  $\delta = 0$ , the 60/40 portfolio rebalances 252 times per year (i.e., every business day). When  $\delta = 1.1\%$ , rebalancing occurs about once per month, and at  $\delta = 2.5\%$  it happens about once per quarter. Given the need to manage cash flows, rebalancing less frequently than once per quarter on average is unlikely for large institutional investors.

Because Threshold is a function of past returns, one concern is that the predictability documented in Figure 2 simply reflects serial correlation in returns. We address this concern by exploiting the state-dependent nature of Threshold-based rebalancing, which implies inherently nonlinear predictability. Specifically, for each  $\delta$ , we estimate predictive regressions separately for days with  $|\text{Threshold Signal}_t^\delta| \geq \delta$ , corresponding to predicted rebalancing days, and for days with  $|\text{Threshold Signal}_t^\delta| < \delta$ , corresponding to periods outside predicted rebalancing days. Appendix Figure D.3 shows that predictability is systematically concentrated – up to  $\delta \approx 2.5\%$  – in periods when funds are more likely to rebalance, consistent with our interpretation.

In the remainder of this paper, we adopt a Threshold signal that is defined as the average of Threshold signals computed using  $\delta$  values that span the range 0%–2.5% with increments of 0.1%.<sup>10</sup> Formally,

$$\text{Threshold Signal}_t = \frac{1}{N} \sum_{\delta=0}^{2.5\%} \text{Threshold Signal}_t^\delta. \quad (2)$$

Averaging different rebalancing calibrations approximates what a heterogeneous group of investors might implement while also reducing the set of potential predictors.<sup>11</sup> Consistent with these observations, introducing the Threshold signal in (2) yields a  $t$ -statistic for the

---

<sup>10</sup>Appendix Table D.6 shows that the results are similar when the Threshold signal is averaged over the range 0%–2%, or excludes zero, averaging over the range 0.1%–2.5%. Also, one might be concerned that our calibration exploits information from the full sample. To address this, we re-estimated the signal using only the first half of the sample and found qualitatively similar results, with predictability becoming insignificant for  $\delta$  values above 2.5%.

<sup>11</sup>Chinco and Fos (2021) find that this heterogeneity can be a source of computational complexity. Our results indicate robust and consistent predictability associated with the Threshold signal for economically meaningful rebalancing ranges.predictive coefficient exceeding 4 (in absolute terms), which is higher than the median  $t$ -statistics across the range of  $\delta$  values used to construct the aggregate signal.

![Bar chart showing t-statistics for different values of Days to end-of-month. The x-axis ranges from -10 to -1, and the y-axis ranges from -3.0 to 0.0. The bars show a general downward trend, with the most negative values occurring around -4 to -5 days. A dashed red line is at approximately -2.6.](0628bfc9715593b95a086963ae434d6c_2_img.webp)

<table border="1">
<caption>Estimated data for Figure 3: Calendar Signals and End-of-Month Effect</caption>
<thead>
<tr>
<th>Days to end-of-month</th>
<th>t-stat</th>
</tr>
</thead>
<tbody>
<tr><td>-10</td><td>-0.2</td></tr>
<tr><td>-9</td><td>-0.6</td></tr>
<tr><td>-8</td><td>-1.0</td></tr>
<tr><td>-7</td><td>-1.4</td></tr>
<tr><td>-6</td><td>-2.4</td></tr>
<tr><td>-5</td><td>-2.8</td></tr>
<tr><td>-4</td><td>-3.2</td></tr>
<tr><td>-3</td><td>-1.0</td></tr>
<tr><td>-2</td><td>-1.2</td></tr>
<tr><td>-1</td><td>-0.8</td></tr>
</tbody>
</table>

**Figure 3: Calendar Signals and End-of-Month Effect.** This figure shows the  $t$ -statistics for the predictive coefficient  $\beta_2$  in (3) for different values of  $\text{Dummy}_t^{\text{N Days}}$ .  $\text{Dummy}_t^{\text{N Days}}$  is a dummy variable that takes the value of 1 during the last  $N$ -days of the month. The dependent variable is the difference between S&P 500 and 10-year Treasury note futures returns.  $t$ -statistics are based on heteroskedasticity-consistent standard errors. The dashed red line denotes the 1% critical value assuming a single test. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

A second important parameter in our study is the range of days when the Calendar rebalancing effect is expected to materialize. To investigate this variable, we estimate the following predictive models:

$$Ret_{t+1} = \beta_0 + \beta_1 \text{Calendar Signal}_t + \beta_2 \text{Calendar Signal}_t \cdot \text{Dummy}_t^{\text{N Days}} + \beta_3 \text{Dummy}_t^{\text{N Days}} + \epsilon_{t+1}, \quad (3)$$

where  $\text{Dummy}_t^{\text{N Days}}$  is a dummy variable that takes the value of 1 during the last  $N$ -days of a month, and  $\text{Calendar Signal}_t$  is constructed as in (B.2). Hence, (3) allows us to test whether the predictive power of Calendar signal concentrate towards month-end, as we expect.

In line with the second hypothesis, we find that the Calendar signal is negatively related to future S&P 500 returns in excess of the 10-year Treasury note, with this predictability concentrated in the final days of the month. Figure 3 shows the  $t$ -statistics for the predictivecoefficient  $\beta_2$  in (3). Calendar predictability peaks in the last four days of the month, consistent with liquidity-driven trading by pension funds. Moreover, Figure 3 suggests that funds attempt to minimize market impact by avoiding trades on the very last day while spreading trades over several days. Therefore, our focus for the rest of the paper is the interaction between the Calendar signal and the last week of the month, labeled as  $\text{week4}_t$ , which corresponds to  $\text{Dummy}_t^{5 \text{ Days}}$ .<sup>12</sup>

### 1.3 Interpreting Rebalancing Signals

Appendix Figure C.1 plots the time-series of the Threshold and Calendar signals, while Appendix Table C.1 shows summary statistics. Both series display high-frequency movements around periods of market turmoil. The Calendar signal shows the greatest absolute deviations, which are due to intra-month market volatility combined with an end-of-month rebalancing approach. We find that the median rebalancing frequency of the Threshold signal is about 16 times per year, higher than the 12 times per year of the Calendar approach. The average values of the Threshold and Calendar signals are positive, reflecting the fact that S&P 500 returns in excess of the 10-year Treasury note average about 3% per year in our sample. As a result, rebalancers tend to sell equities and buy bonds more often. The two signals are positively correlated, with a correlation coefficient of approximately 60%.

By construction, the Threshold and Calendar signals are positively correlated with trailing equity excess returns computed over different time frames. Since the Threshold signal tends to rebalance more frequently than the Calendar signal, it should be more closely related to short-term rather than long-term trailing excess returns.

In Appendix Table D.1, we report the estimated coefficients from regressing Threshold and Calendar signals onto trailing excess returns of selected horizons. The sums of the coefficients for each regression are close to 0.24, which reflects our decision to simulate a

---

<sup>12</sup>This effect is distinct from the turn-of-the-month anomaly (e.g., [Ariel, 1987](#); [Lakonishok and Smidt, 1988](#)), which refers to the observation that the U.S. stock index performs significantly better from the last trading day of the month through either the first three ([Lakonishok and Smidt, 1988](#)) or nine ([Ariel, 1987](#)) trading days of the following month. [Ogden \(1990\)](#) attributes this pattern to investors reinvesting cash payments – including wages, dividends, interest, and principal payments – at the turn of each calendar month.60/40 portfolio's dynamics.<sup>13</sup> The Threshold signal displays its highest sensitivities to short horizon trailing returns, as is consistent with its higher turnover statistics. The Calendar signal displays a hump-shaped relationship that reflects how its horizon grows every month until the last business day. Hence, the Threshold signal and Calendar signal resemble the actions of a more frequent rebalancer and a less frequent rebalancer, respectively.

## 2 Rebalancing Pressures

This section documents market-wide pressures associated with rebalancing activity. We examine the price impact on stocks and bonds around rebalancing signals, analyze how institutional investors adjust their trading in response, and draw on conversations with pension fund leaders to provide further institutional context on the relevance of rebalancing pressures.

### 2.1 Return-Based Evidence of Rebalancing

#### 2.1.1 Rebalancing and Cross-Asset Return Predictability

Many factors can affect aggregate returns. For example, time-series momentum appears as a ubiquitous driver of return dynamics (see, e.g., [Moskowitz, Ooi, and Pedersen, 2012](#)). Furthermore, asset volatility is a well-known predictor of future returns, including at high-frequency (e.g., [Nagel, 2012](#)), and sentiment is an important driver of returns, especially at short-horizons (e.g., [Da, Engelberg, and Gao, 2015](#)). Thus, multivariate regressions are the natural setting to study if and how rebalancing activity affects future returns. Finally, we also want to understand whether Threshold and the Calendar signals contain different informative predictive content, i.e., if they are jointly significant predictors of future cross-asset returns.

---

<sup>13</sup>Since  $60\% \times 40\% = 0.24$ , we can approximate the S&P 500 weight deviation from its target allocation as  $\approx 0.24(R^E - R^B)$ , where  $R^E - R^B$  measures the equity excess returns since the last rebalancing. Importantly, from a predictive standpoint, our decision to simulate 60/40 portfolios rather than other allocations – such as 50/50 or 70/30 – does not affect our results qualitatively. From an economic perspective, an equal-allocation portfolio implies the largest potential portfolio deviations and, therefore, the highest rebalancing pressures.To this end, we run the cross-asset predictive multivariate regression:

$$Ret_{t+1} = \beta_0 + \beta' RebalancingSignal_t + \psi Momentum_t + \zeta Ret_t + \gamma' X_t + \epsilon_{t+1} , \quad (4)$$

where, for the benchmark analysis,  $Ret$  is the difference between S&P 500 and 10-year Treasury note futures returns. We naturally refer to this analysis as *cross-asset* (or, abbreviated, XA) return predictability.

The  $RebalancingSignal_t$  vector contains the Threshold and the Calendar signal constructed in Section 1.2; the Calendar signal is also interacted with a dummy variable taking the value of 1 the last week (i.e., 5 days) of any month or 0 otherwise. Momentum and rebalancing signals have a correlation higher than 67% (see Table C.2) but yield opposite predictions, so controlling for momentum in our setting is important. As trailing returns over different horizons convey distinct information (see, e.g., [Goulding, Harvey, and Mazoleni, 2023](#)), we calculate fast, medium, and slow momentum signals. Since we find that the fast momentum signal lacks predictive power in our specification, we construct our momentum signal,  $Momentum_t$ , by averaging the medium and slow momentum signals.<sup>14</sup> We also control for trailing one-day returns,  $Ret_t$ .

The vector  $X_t$  contains three categories of control variables motivated by prior research. First, as proxies for aggregate volatility, we use the Chicago Board Options Exchange (CBOE) daily market volatility index (VIX), which measures the implied volatility of S&P 500 index options, together with the ICE BofA MOVE index, which tracks fixed income market option volatility. The inclusion of the MOVE index is motivated by the fact that we study both stock and bond return dynamics. Second, as controls for macroeconomic conditions, we use the news-based measure of economic policy uncertainty developed by [Baker, Bloom, and Davis \(2016\)](#) and the real-time business conditions index constructed in [Aruoba, Diebold, and Scotti \(2009\)](#). Finally, as sentiment proxy, we include the daily news-based sentiment index constructed in [Shapiro, Sudhof, and Wilson \(2022\)](#). In Appendix Table C.2, we report the correlation among all the predictors in our benchmark specification.

---

<sup>14</sup>Momentum fast is calculated as the average of the signs of trailing 1 to 10 daily excess returns; momentum medium averages the signs of 11 to 20 daily excess returns; momentum slow averages the signs of 21, 42, 63, 126, and 252 daily excess returns. In Appendix Table D.3, we report robustness results using these three distinct momentum signals.**Table 1: Cross-Asset Predictive Regressions**

This table reports estimates for the multivariate predictive regression (4).  $Ret$  is the difference between S&P 500 and 10-y Treasury note futures returns. Threshold and Calendar signals are constructed as described in Section 1.2. Momentum is computed by averaging the sign of 11 to 20, and 21, 42, 63, 126, and 252 trailing equity returns in excess of the 10-year Treasury note. VIX is the CBOE equity option-implied volatility index (divided by 100); MOVE is the U.S. bond market option-implied volatility index (divided by 100); EPU is the news-based measure of economic policy uncertainty from [Baker, Bloom, and Davis \(2016\)](#); ADS is the [Aruoba, Diebold, and Scotti \(2009\)](#) real-time business conditions index; Sentiment is the daily news-based sentiment index constructed in [Shapiro, Sudhof, and Wilson \(2022\)](#). Values in parentheses are heteroskedasticity-consistent standard errors. Constant estimates are not tabulated. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

<table border="1">
<thead>
<tr>
<th></th>
<th>(1)</th>
<th>(2)</th>
<th>Ret<sub>t+1</sub><br/>(3)</th>
<th>(4)</th>
<th>(5)</th>
</tr>
</thead>
<tbody>
<tr>
<td>Threshold</td>
<td>-0.4144***<br/>(0.1148)</td>
<td>-0.4208***<br/>(0.1164)</td>
<td>-0.4254***<br/>(0.1098)</td>
<td>-0.4254***<br/>(0.1133)</td>
<td>-0.4226***<br/>(0.1139)</td>
</tr>
<tr>
<td>Calendar</td>
<td>0.0553<br/>(0.0709)</td>
<td>0.0689<br/>(0.0686)</td>
<td>0.0572<br/>(0.0696)</td>
<td>0.0542<br/>(0.0713)</td>
<td>0.0666<br/>(0.0686)</td>
</tr>
<tr>
<td>week4</td>
<td>0.0002<br/>(0.0004)</td>
<td>0.0002<br/>(0.0004)</td>
<td>0.0002<br/>(0.0004)</td>
<td>0.0002<br/>(0.0004)</td>
<td>0.0002<br/>(0.0004)</td>
</tr>
<tr>
<td>Calendar *week4</td>
<td>-0.3029***<br/>(0.0808)</td>
<td>-0.3036***<br/>(0.0808)</td>
<td>-0.3026***<br/>(0.0805)</td>
<td>-0.3032***<br/>(0.0806)</td>
<td>-0.3033***<br/>(0.0808)</td>
</tr>
<tr>
<td>Momentum</td>
<td>0.0023***<br/>(0.0006)</td>
<td>0.0024***<br/>(0.0007)</td>
<td>0.0024***<br/>(0.0006)</td>
<td>0.0025***<br/>(0.0006)</td>
<td>0.0024***<br/>(0.0007)</td>
</tr>
<tr>
<td>Ret</td>
<td>-0.0203<br/>(0.0289)</td>
<td>-0.0167<br/>(0.0289)</td>
<td>-0.0198<br/>(0.0281)</td>
<td>-0.0192<br/>(0.0287)</td>
<td>-0.0173<br/>(0.0286)</td>
</tr>
<tr>
<td>VIX</td>
<td></td>
<td>0.0090*<br/>(0.0053)</td>
<td></td>
<td></td>
<td>0.0076<br/>(0.0062)</td>
</tr>
<tr>
<td>MOVE</td>
<td></td>
<td>-0.0020*<br/>(0.0011)</td>
<td></td>
<td></td>
<td>-0.0019*<br/>(0.0011)</td>
</tr>
<tr>
<td>EPU</td>
<td></td>
<td></td>
<td>0.0005*<br/>(0.0003)</td>
<td></td>
<td>0.0002<br/>(0.0004)</td>
</tr>
<tr>
<td>ADS</td>
<td></td>
<td></td>
<td>0.0000<br/>(0.0002)</td>
<td></td>
<td>0.0001<br/>(0.0002)</td>
</tr>
<tr>
<td>Sentiment</td>
<td></td>
<td></td>
<td></td>
<td>-0.0016<br/>(0.0012)</td>
<td>-0.0003<br/>(0.0013)</td>
</tr>
<tr>
<td>Observations</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
</tr>
<tr>
<td>Adjusted R<sup>2</sup></td>
<td>0.0239</td>
<td>0.0252</td>
<td>0.0243</td>
<td>0.0242</td>
<td>0.0248</td>
</tr>
</tbody>
</table>Table 1 reports results for different specifications of the multivariate predictive regression (4). In Column (1), both Threshold and Calendar signals significantly predict future daily XA returns, with associated t-statistics around 4. The negative signs for both signals are consistent with their role as rebalancing indicators: when stocks outperform bonds, stocks become overweight in portfolios and need to be sold. Thus, rebalancers act as macro-contrarians, as the TDF evidence in [Parker, Schoar, and Sun \(2023\)](#) suggests.<sup>15</sup> This, in turn, exerts downward pressure on XA returns. By contrast, momentum positively predicts daily returns, consistent with the literature.

Columns (2) to (4) report results for regression (4) including as controls proxies for volatility, macro conditions, and sentiment, respectively. This analysis shows that, while some regressors (e.g., volatility and economic uncertainty) partially explain future return dynamics, the two rebalancing signals remain strong predictors alongside momentum. Finally, we also include all regressors jointly. Column (5) reports this result showing that Threshold and Calendar are highly significant determinants of future XA returns.<sup>16</sup>

The predictability of the rebalancing signals is both statistically and economically significant: a one-standard-deviation decrease in the Threshold (Calendar) signal is associated with an increase in XA returns of about 20 bps (19.2 bps) over the next trading day, and vice versa. This is remarkable when compared to other daily return predictability results. For example, [Da, Engelberg, and Gao \(2015\)](#) find that a one-standard-deviation increase in their investor sentiment measure, FEARS, predicts an increase of 7.1 bps in the S&P 500. Or, more recently, [Hartzmark and Solomon \(2025\)](#) document a 3.2 bps increase in aggregate market returns for a one-standard-deviation increase in dividend payout. Furthermore, positive rebalancing signal values significantly predict future negative returns, while negative values significantly predict future positive returns, i.e., predictability is not concentrated in

---

<sup>15</sup>Using individual portfolio data from Sweden, [Calvet, Campbell, and Sodini \(2009\)](#) find that households are, on average, macro-contrarians. More recently, [Gabaix, Kojien, Mainardi, Oh, and Yogo \(2023\)](#) find that U.S. households, by contrast, are on average pro-cyclical investors, with the important exception of ultra-high-net-worth individuals.

<sup>16</sup>Appendix Table D.4 uses the return differential between the S&P 500 Index and the Bloomberg Aggregate Bond Index, showing qualitatively and quantitatively similar results that indicate our findings are not specific to the financial instrument used to analyze rebalancing pressures. Appendix Table D.5 shows that using changes in the control variables ( $\Delta X_t = X_t - X_{t-1}$ ) leads to similar results. Appendix Table D.6 shows that constructing the Threshold signal as the average of Threshold measures computed over  $\delta$  values spanning 0% to 2% (Columns (1) and (2)) or over  $\delta$  values spanning 0.1% (i.e., excluding every-day rebalancing) to 2.5% (Columns (3) and (4)) leads to comparable results.bad times. Finally, we find that the predictability associated with Threshold is stronger when the signal magnitude is larger, aligning with its economic interpretation.

These results indicate that investors may incur meaningful costs when rebalancing. To quantify these costs, we adopt a two-step procedure. First, we estimate costs in percentage terms by multiplying the estimated price impact by the average rebalancing trade. Specifically, we measure price impact using the predictive regression in equation (4), estimated over periods in which rebalancing trades are expected to occur – namely, the last week of the month for Calendar rebalancing, or the subsample of days for which the rebalancing signal exceeds a given threshold for Threshold rebalancing. We then multiply the estimated price impact by the average absolute distance to target at the time of rebalancing and by the number of rebalancing trades per year.<sup>17</sup> For the Calendar strategy, the implied annual costs are  $\widehat{\text{Price Impact}} \times \text{Average Trade Size} \times \text{Trades per Year} = |-0.39| \times 1\% \times 12 \approx 5$  bps. Applying the same procedure to the Threshold strategy yields annualized costs ranging from 6 to 27 bps across  $\delta$  values between 0 and 2.5%, with an average of 15 bps.<sup>18</sup>

To estimate rebalancing costs, we make assumptions about the timing of trades under both rebalancing rules. For the Calendar strategy, focusing on the last week of the month is natural, as institutional investors typically rebalance at month- or quarter-end. The timing is inherently more nuanced for the Threshold strategy. However, discussions with market participants indicate that discretion in practice is limited. In particular, when rebalancing is delegated to overlay managers – as suggested by institutional evidence discussed above – execution tends to follow standardized procedures with limited scope for opportunistic timing. To be conservative, we also consider a scenario in which managers rebalance before the signal fully breaches the threshold, when the average trade size is approximately 1%, similar to the Calendar case. Under this assumption, implied costs are about 11 bps. Averaging between the Calendar and Threshold estimates yields an annual rebalancing cost of approximately 8 bps, which we use in subsequent calculations.

Consider the economic context of our 8 bps estimate. First, institutional investors typ-

---

<sup>17</sup>An alternative specification estimates a single regression using the full sample and interacts the rebalancing signal with an indicator equal to one during rebalancing periods, either in the last week of the month or when the signal exceeds a threshold. Results are largely the same.

<sup>18</sup>Etula et al. (2020) document that pension funds must sell securities at least four business days before month-end to meet benefit payments. Consistent with their findings, a Calendar rebalancer trading on day  $T - 4$  would incur a cost of roughly 9 bps. Costs are also higher in the post-PPA period (i.e., after 2006).ically pay about 3 bps per year to invest passively across equity and bond markets. This implies that mechanical rebalancing is nearly three times as costly as accessing these markets in the first place. Second, [Chen, Noronha, and Singal \(2006\)](#) quantify the losses incurred by index fund investors due to cross-sectional price pressures around the effective dates of index additions and deletions. They find that, on average, S&P 500 index investors lose approximately 4 bps per year. In addition, as TDFs and balanced funds are expected to grow (e.g., [Parker, Schoar, and Sun, 2023](#); [Parker and Sun, 2025](#)), the costs associated with mechanical rebalancing could rise substantially over time.<sup>19</sup>

As a further benchmark, we consider a hypothetical *random rebalancing* strategy that rebalances once per month on a randomly chosen day, yielding the same expected frequency of 12 rebalancing events per year as our Calendar approach. We simulate the strategy 10,000 times and report average costs across simulations. Appendix Figure D.5 displays the distribution of economic costs. The average cost is 0.6 bps (median of 0.5 bps), indicating that this simple randomization is associated with economically negligible price effects.<sup>20</sup> Thus, all else equal, investors may be able to meaningfully reduce rebalancing costs by avoiding the specific days on which other institutions concentrate their trading activity.

Finally, to translate these costs in dollar terms, we multiply the percentage cost by the estimated dollar size of rebalancers. According to the Federal Reserve's Financial Accounts, U.S. retirement assets – including public and private DB and DC plans and IRAs but excluding Social Security – totaled \$37.8 trillion at year-end 2022. By our calculations, more than \$20 trillion of these assets may have been invested in public equity and debt.<sup>21</sup> Thus, current rebalancing policies cost approximately \$16 billion per year. As a sense of scale, [Chen, Noronha, and Singal \(2006\)](#) estimate that index reconstitutions generate annual losses of \$1.0–2.1 billion for investors in funds linked to the S&P 500 and Russell 2000. Using a

---

<sup>19</sup>According to the Investment Company Institute (ICI), total U.S. retirement assets reached \$45.8 trillion as of June 30, 2025 – an increase of more than 15% since 2023; see [ICI](#).

<sup>20</sup>We deliberately allow random rebalancing dates to fall within the final week of the month, coinciding with Calendar rebalancing. When we exclude the final week from the random selection, the resulting costs are even smaller.

<sup>21</sup>According to a 2023 study by the Congressional Research Service (CRS), of the \$14 trillion in public DB and DC plans, approximately \$7.2 trillion is allocated to public equity and fixed income. In private DC plans, which total \$8.1 trillion, about \$6.8 trillion is invested in TDFs or directly in equities and fixed income. Additionally, an estimated \$2.3 trillion in private DB plans and \$4.8 trillion in IRAs may be allocated to public equity and debt. For the full report, see [CRS Report](#).different approach, [Petajisto \(2011\)](#) estimates annual index turnover costs of \$2.5–3.4 billion for S&P 500 index funds and \$170–340 million for Russell 2000 index funds. These findings led index providers to revise reconstitution and index design policies. This comparison provides an additional benchmark for gauging the economic significance of our \$16 billion annual estimate. Furthermore, about two-thirds of U.S. households have a financial stake in the U.S. retirement system, according to the Survey of Consumer Finances (SCF). Given that there were about 127 million households in the U.S., as reported by the Census Bureau in 2022, the annual cost of rebalancing per household reaches almost \$200.

### 2.1.2 Price Pressures

Threshold and Calendar signals are proxies for rebalancing activity, largely reflecting institutional mandates and expected to convey limited information about market fundamentals. Nevertheless, several models predict that even uninformed trades can influence prices (see, e.g., [Grossman and Miller, 1988](#); [De Long, Shleifer, Summers, and Waldmann, 1990](#) for early work, or more recently, [Vayanos and Vila, 2021](#); [Gabaix and Kojien, 2021](#)).

We investigate the persistence of rebalancing price pressures by running the regression:

$$Ret_{t+1:t+i} = \beta_0 + \beta' RebalancingSignal_t + \psi Momentum_t + \zeta Ret_t + \epsilon_{t+i} , \quad (5)$$

where  $Ret_{t+1:t+i}$  are cumulative log returns up to  $t+i$ . To address potential inference issues related to overlapping observations, we follow [Ang and Bekaert \(2007\)](#) and use conservative standard errors from reverse regressions to compute confidence bands, as proposed by [Hodrick \(1992\)](#). Furthermore, [Appendix Figure 4](#) shows results for non-overlapping returns.

[Figure 4](#) shows the estimated coefficients for Threshold in Panel (a) and Calendar in Panel (b) from the multivariate predictive regression (5), along with their 95% confidence intervals. Point estimates reach their trough in Day 4 and Day 2 for Threshold and Calendar, respectively, before nearly reverting within 15 days. The predictive coefficients become statistically indistinguishable from zero at the 5% level by Day 9 for Threshold and Day 6 for Calendar.

Increasing the predictability horizon of (5), while introducing significant noise to ourestimates, reveals that point estimates for both rebalancing signals would completely revert within less than two months. Thus, while our point estimates indicate that rebalancing pressures are not quickly reversed in full, this evidence suggests that these pressures eventually dissipate. As discussed in [Hartzmark and Solomon \(2025\)](#), although reversals have been extensively studied in the cross-section, understanding the speed and extent to which a market-level pattern like ours should reverse remains an important avenue for future research.

![Figure 4: Rebalancing and Horizon of Cross-Asset Return Predictability. Two line plots showing Predictive Coefficients vs Days Ahead (1-15). Plot (a) shows the Threshold signal (blue line) with a 95% confidence interval (dotted lines). Plot (b) shows the Calendar * week4 signal (green line) with a 95% confidence interval (dotted lines). Both plots show a U-shaped trend, dipping around day 4-5 and rising towards day 15.](a0ac78723cf816759a3860b6223e59bc_2_img.webp)

Figure 4 consists of two line plots, (a) and (b), showing Predictive Coefficients on the y-axis (ranging from -1.0 to 0.5) against Days Ahead on the x-axis (ranging from 1 to 15). Both plots include a horizontal dashed line at 0.0 and dotted lines representing 95% confidence intervals.

Plot (a) is titled '(a) Threshold'. It features a solid blue line representing the point estimate. The coefficient starts at approximately -0.45 at day 1, decreases to a minimum of about -0.95 at day 5, and then rises to approximately -0.15 by day 15. The 95% confidence interval is shown by dotted lines, which are wider at the beginning and end of the horizon.

Plot (b) is titled '(b) Calendar \* week4'. It features a solid green line representing the point estimate. The coefficient starts at approximately -0.35 at day 1, dips to about -0.55 at day 2, and then fluctuates between -0.4 and -0.2 for the remainder of the horizon. The 95% confidence interval is shown by dotted lines, which are wider at the beginning and end of the horizon.

**Figure 4: Rebalancing and Horizon of Cross-Asset Return Predictability.** This figure shows coefficient estimates and 95% confidence intervals for Threshold and Calendar signals for the multivariate predictive regression (5). Confidence bands are computed using [Hodrick \(1992\)](#) standard errors. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

### 2.1.3 Robustness

**Different Portfolio Weights.** Our decision to simulate 60/40 portfolios rather than other calibrations simply influences the magnitude of the estimated predictive coefficients. To illustrate this point, Appendix Table D.7 replicates Column (1) of Table 1 using rebalancing signals derived from simulated balanced portfolios with different equity–bond allocations.

The first column of Appendix Table D.7 reports results for an 86/14 equity–bond portfolio. The resulting signals exhibit statistical significance comparable to the baseline specifica-tion, but with coefficients that are approximately twice as large. This scaling is mechanical and expected, as the magnitude of rebalancing signals constructed from an 86/14 portfolio is roughly half that of signals based on the 60/40 calibration.<sup>22</sup> The second and third columns report results for 50/50 and 70/30 equity–bond portfolios, respectively. In both cases, alternative calibrations rescale the magnitude of the predictive coefficients while leaving the predictive power and statistical significance of the rebalancing signals largely unchanged. The results are economically intuitive. When equity markets rise sharply, funds sell equities regardless of the target allocation.

**Threshold is Not Simply Capturing Return Autocorrelation.** One potential concern is that the Threshold signal predicts returns simply because it captures return autocorrelation. This concern does not apply to the Calendar signal, which exploits a seasonal pattern and is therefore not susceptible to this critique. To address this concern, we exploit the state-dependent nature of the Threshold signal. We show that the predictability associated with Threshold is not purely driven by return autocorrelation but instead exhibits economically meaningful non-linearities linked to the rebalancing process. Specifically, Columns (1) and (2) of Appendix Table D.8 decompose the Threshold signal into periods of large deviations (above its median, Threshold Large) and small deviations (below its median, Threshold Small). Column (1) reveals a pronounced non-linearity in Threshold effects: only Threshold Large generates statistically significant predictability. This finding is consistent with the notion that, during these periods, portfolio deviations are larger and rebalancing activity is more likely, leading to price impact. Column (2) includes additional controls and shows that the results are largely unchanged.

Finally, we construct an alternative Threshold signal,  $\text{Threshold}^\perp$ , defined as the original

---

<sup>22</sup>For example, if equities earn a 10% excess return while bonds are flat, the deviation of the S&P 500 from a 60% target allocation is

$$0.60 \times 0.40 \times 10\% = 0.24 \times 10\% = 2.4\%.$$

In contrast, the deviation from an 86% target allocation is

$$0.86 \times 0.14 \times 10\% \approx 0.12 \times 10\% = 1.2\%.$$

Thus, selecting a different target allocation – such as an 86/14 equity–bond mix – effectively rescales the  $\delta$  range used to construct the Threshold signal.Threshold orthogonalized with respect to momentum and therefore exhibiting less serial correlation. Columns (3) and (4) of Appendix Table D.8 demonstrate that our interpretation continues to hold under this alternative specification.

**Alternative Controls.** Appendix Table D.9 shows results when we consider alternative control variables in our main predictive regression Table 1. Specifically, in Columns (1) to (3) of Table D.9, we replace our main economic uncertainty and sentiment indexes with, respectively, the uncertainty indexes constructed in [Bekaert, Engstrom, and Xu \(2022\)](#) and the FEARs index constructed in [Da, Engelberg, and Gao \(2015\)](#) and show that it has little effect on the results.<sup>23</sup>

Furthermore, we include the aggregate retail attention (ARA) index proposed by [Da, Hua, Hung, and Peng \(2025\)](#) as a control, since attention-induced contrarian trading may offer an alternative explanation for the market-wide pressures we document. [Da et al. \(2025\)](#) show that ARA negatively predicts market returns, with stronger predictive power during periods of high volatility and illiquidity – precisely when rebalancing-driven predictability is also more pronounced. Moreover, ARA tends to spike at month-end, and when recent excess returns are more salient, as captured by the Threshold signal. Column (4) of Table D.9 reports the results, which remain largely unchanged after including ARA, suggesting that our findings reflect a distinct dimension of return predictability.

**The Role of Reversal.** A potential concern is whether alternative reversal signals could subsume the predictive content of Threshold and Calendar. To study this question, we test two reversal measures. First, inspired by [Nagel \(2012\)](#), we construct a short-term reversal signal as the 5-day trailing XA returns. Second, following [Fama and French \(1996\)](#), we calculate a long-term reversal signal as the 5-year trailing returns (i.e., 1260 days) skipping the last year.

Table D.10 evaluates the predictive power of these two reversal measures. Column (1) shows that short-term reversal significantly predict future daily XA returns and displays the expected negative sign, although its effect is relatively small: a one-standard-deviation increase in short-term reversal leads to an increase in XA returns of about 1.1 bps over

---

<sup>23</sup>We thank the authors for making their FEARs time series available to us.the next trading day. This finding complements previous work focused on stock returns alone (e.g., [Nagel, 2012](#)). In contrast, as shown in Column (3), long-term reversal does not appear to predict XA returns at a daily frequency. In columns (2), (4), and (5), we expand our main empirical specification by adding the two reversal measures. Including either or both variables does not change our interpretation of the Threshold and Calendar signals. Instead, the short-term reversal measure is not significant in the joint regression in Column (2), suggesting that our rebalancing proxies capture its effect.<sup>[24](#)</sup>

## 2.2 Rebalancing and Institutional Investors' Trades

We leverage four datasets to directly examine how our rebalancing signals relate to investors' trades.

First, we use publicly available futures positions from the Commodity Futures Trading Commission (CFTC). Futures positions provide insight into trading in key instruments used for rebalancing and risk management. Our analysis investigates weekly position changes for different types of traders. The CFTC requires all large traders to identify as either commercial or non-commercial. The former report using futures for hedging purposes. The weekly Commitment of Traders (COT) reports detail the aggregate long and short positions of futures market participants for these trader types. Following the previous literature (e.g., [Bessembinder, 1992](#); [De Roon, Nijman, and Veld, 2000](#); [Moskowitz, Ooi, and Pedersen, 2012](#)), we refer to commercial traders as *hedgers* and to non-commercial traders as *speculators*. We argue that hedgers primarily act as rebalancers: to mitigate tracking risk when portfolios drift from their target allocations, they buy underweight assets and sell overweight assets.

We use CFTC data on S&P 500 and 10-year Treasury futures to construct a variable capturing the trading behavior of hedgers and speculators, starting in August 2006. Following [Kang, Rouwenhorst, and Tang \(2020\)](#), we compute net trading  $Q$  as the cross-asset net position change between  $t + 1$  and  $t$ , scaled by open interest (i.e., the total number of

---

<sup>24</sup>Appendix Table [D.11](#) investigates whether the end-of-month return patterns documented in [Graziani \(2024\)](#) relate to our findings. We construct the end-of-month reversal signal (EoM Rev), defined as the return between the fourth Friday's close and the month-end close, and find that it has very low correlation with our Calendar and Threshold signals ( $-0.062$  and  $0.038$ , respectively); in addition, EoM Rev is statistically insignificant and does not affect the predictability of our rebalancing signals.contracts outstanding) in week  $t$ . We calculate this measure separately for both hedgers and speculators and examine the relation between future net trading positions and current rebalancing signals.

The first part of Figure 5 shows that future hedger positions are negatively related to both Threshold and Calendar signals, whereas speculators display a positive relation. When equities are overweight (underweight) relative to bonds, hedgers sell (buy) equities and speculators take the opposite side, consistent with our interpretation.

![Bar chart showing Correlation between various institutional investors' trades and (lagged) rebalancing signals. The chart compares Threshold (blue) and Calendar (green) signals across four categories: Hedgers, Specs, Asset Mgrs, and Lev Funds. The y-axis represents Correlation from -0.2 to 0.2. The x-axis shows four datasets: CFTC 2006-2023, LTPos 2009-2011, ANcerno 1999-2011, and ICI 2007-2023.](68c7be372a640af17bec554f1560911f_3_img.webp)

<table border="1">
<thead>
<tr>
<th>Investor Type</th>
<th>Signal Type</th>
<th>CFTC 2006-2023</th>
<th>LTPos 2009-2011</th>
<th>ANcerno 1999-2011</th>
<th>ICI 2007-2023</th>
</tr>
</thead>
<tbody>
<tr>
<td rowspan="2">Hedgers</td>
<td>Threshold</td>
<td>-0.10</td>
<td>-0.08</td>
<td>-0.10</td>
<td>-0.15</td>
</tr>
<tr>
<td>Calendar</td>
<td>-0.12</td>
<td>-0.12</td>
<td>-0.10</td>
<td>-0.18</td>
</tr>
<tr>
<td rowspan="2">Specs</td>
<td>Threshold</td>
<td>0.11</td>
<td>0.18</td>
<td>0.00</td>
<td>0.00</td>
</tr>
<tr>
<td>Calendar</td>
<td>0.17</td>
<td>0.13</td>
<td>0.00</td>
<td>0.00</td>
</tr>
<tr>
<td rowspan="2">Asset Mgrs</td>
<td>Threshold</td>
<td>-0.08</td>
<td>-0.08</td>
<td>-0.08</td>
<td>-0.08</td>
</tr>
<tr>
<td>Calendar</td>
<td>-0.12</td>
<td>-0.12</td>
<td>-0.10</td>
<td>-0.18</td>
</tr>
<tr>
<td rowspan="2">Lev Funds</td>
<td>Threshold</td>
<td>0.00</td>
<td>0.00</td>
<td>0.00</td>
<td>0.00</td>
</tr>
<tr>
<td>Calendar</td>
<td>0.00</td>
<td>0.00</td>
<td>0.00</td>
<td>0.00</td>
</tr>
</tbody>
</table>

**Figure 5: Rebalancing Signals and Trading Positions.** This figure shows the correlation between various institutional investors' trades and (lagged) rebalancing signals.

To further investigate which institutional investors trade in the direction of rebalancing pressures and which take the opposite side, we exploit the Large Trader Net Position Changes dataset. Published by the CFTC on June 30, 2011, this one-time report covers the period from January 2009 to May 2011 and provides the daily average aggregate net position changes for large traders across 35 futures markets. The report classifies financial futures traders into four groups: dealers/intermediaries, asset managers/institutional investors, leveraged funds, and other reportables. According to the CFTC, the dataset captures at least 80% of open interest in futures markets.<sup>25</sup> We focus on asset managers – which include pension funds,

<sup>25</sup>Further details can be found on the [CFTC website](#).endowments, insurance companies, mutual funds, and portfolio/investment managers whose clients are primarily institutional – and on leveraged funds, which typically comprise hedge funds and other money managers such as commodity trading advisors.

The second group in Figure 5 reports the correlation between weekly net trading by these two groups and lagged Threshold and Calendar signals. On average, asset managers sell equities and buy bonds when equities are overweight, whereas leveraged funds tend to take the opposite side of these trades. Because the CFTC data are available only at weekly frequency, they inevitably aggregate substantial within-week dynamics: hedge funds that temporarily trade in the same direction as pensions for a few days and subsequently unwind their positions would appear as providing liquidity over the full week. Thus, the evidence should not be interpreted as ruling out front-running or other short-horizon strategies. Rather, these results offer a more granular counterpart to our first-panel findings and remain broadly consistent with viewing the Threshold and Calendar signals as capturing rebalancing activity – where some hedge funds act as liquidity providers to pensions, while others may be aligned with them at higher frequencies that our data cannot detect.

Then, we use the ANcerno (formerly Abel Noser) dataset, which reports daily, trade-level equity transactions for hundreds of institutional investors. As documented by [Puckett and Yan \(2011\)](#), the sample includes institutions such as CalPERS and the YMCA Retirement Fund and, in aggregate, accounts for about 8% of daily CRSP trading volume. For our analysis, we focus on the period from January 1999 to September 2011, which corresponds to the years in which pension plan sponsors can be identified, and we restrict attention to trades in S&P 500 constituents to align with our empirical design. While limited, these data provide a rare window into high-frequency pension fund trading; other (public) sources offer only quarterly or annual aggregates (e.g., 13F filings and CRSP/Thomson Reuters holdings).

The third part of Figure 5 reports the correlation between the aggregate buy ratio – the dollar value of the ANcerno institutional buy transactions divided by the sum of buy and sell dollar values – and our lagged rebalancing signals. Consistent with our interpretation, the pattern indicates that pension plans act as rebalancers. Moreover, the magnitude of this correlation is comparable to that for CFTC hedgers in the first panel, further validating the economic content of these data.

Finally, we also use estimated weekly net equity flows from the Long-Term Mutual FundFlows data provided by the Investment Company Institute (ICI), defined as U.S. total equity flows minus bond flows. These data are available starting in January 2007. The fourth grouping in Figure 5 shows that, on average, when equities are overweight relative to bonds, mutual funds sell equities and buy bonds, consistent with our interpretation.

## 2.3 External Validity

We shared our preliminary empirical results with a group representing a global network of public pensions. The director suggested that we host a roundtable with 16 different pensions and present our preliminary findings. Held June 19, 2024, the meeting featured CIOs and other senior executives representing approximately \$2 trillion in pension assets.

At first, the discussion only touched on general rebalancing information. Are there target allocations? How frequently is rebalancing conducted? Is rebalancing performed on a Calendar or Threshold basis? If on the former, how often do you rebalance? If on the latter, what are the thresholds? Would derivatives be used for rebalancing? What market considerations, if any, might delay or accelerate rebalancing? Based on the information we gathered, all pensions had systematic rebalancing procedures, with some variation across Calendar- and Threshold-based approaches.

We then presented our evidence that rebalancing induces predictability. Many pensions acknowledged that they were aware of this phenomenon. When we explained that potential front-runners could exploit such predictability, one pension replied, “We know about that.” Others agreed.<sup>26</sup> When we suggested a more dynamic rebalancing policy might reduce the potential for front-running, one pension remarked, “It is easier for us to task our alpha desk with addressing this predictability than to try to convince our investment committee to change our rebalancing policy.”

In summary, all pensions in our roundtable sample rebalance mechanically based on Calendar and Threshold rules. They understand these policies induce predictability and believe that traders will front-run their rebalancing. At least some of the funds appear

---

<sup>26</sup>Interestingly, in a March 2024 episode of the podcast *Flirting with Models*, an executive at one of the world’s largest hedge funds described a front-running rebalancing strategy as an example of a widely used systematic portfolio approach. Listen to the episode [here](#).to front-run their own and their peers' rebalancing. Finally, the funds perceive changing rebalancing policies as very challenging given institutional constraints.

### 3 Further Validation of Rebalancing Signals

This section further investigates the economic interpretation of our rebalancing signals through five analyses. First, we document seasonal patterns in the predictability of the Threshold and Calendar signals and find that (i) Calendar predictability is strong at month-end but absent at other times, and (ii) both signals' predictive power and economic significance increase toward the quarter-end. These seasonal patterns align with month- or quarter-end trades driven by liquidity needs or benchmark tracking considerations rather than risk or behavioral factors. Second, we show that our signals independently predict both equity and bond excess returns, suggesting trades occur in both markets, consistent with our interpretation. Third, we find that the signals' predictive power became significant in the early 2000s, coinciding with shifts in pension fund allocations, cash flow needs, and 2006 legislation affecting the Target Date Fund industry. Fourth, we demonstrate that our rebalancing predictions extend to large- and small-cap stocks but do not extend to value and growth stocks, consistent with the fact that many funds have target allocations to small and large capitalization stocks but few have targets to growth and value. Lastly, we show that the Threshold and Calendar signals extend to international equity returns.

#### 3.1 Seasonal Patterns

In Panel A of Table 2, Column (2) indicates that the predictability of the Calendar signal concentrates at month-end, while outside of these days, Calendar does not exhibit predictive power (Column (1)).<sup>27</sup> In Column (3), we demonstrate that this finding does not apply to the Threshold signal. This distinction validates their interpretation: despite a correlation higher than 60% (see Appendix Table C.2), these results show that the signals capture two

---

<sup>27</sup> Appendix Table D.12 further decomposes the Calendar effect across the four weeks of the month. While month-end predictability is strongest, we also find statistically significant predictability in weeks 1 and 3. In these weeks, however, the predictive coefficient is positive, consistent with a reversal of rebalancing pressures, in line with our interpretation.**Table 2: Seasonal Patterns**

This table reports estimates for the multivariate predictive regression (4).  $Ret$  is the difference between S&P 500 and 10-year Treasury note futures returns. Threshold and Calendar signals are constructed as described in Section 1.2. Values in parentheses are heteroskedasticity-consistent standard errors. Constant estimates as well as Calendar, week4, Momentum, and one-day trailing returns are not tabulated. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

**Panel A: Seasonal Patterns at Month-End**

<table border="1">
<thead>
<tr>
<th></th>
<th colspan="3">Ret<sub>t+1</sub></th>
</tr>
<tr>
<th></th>
<th>(1)</th>
<th>(2)</th>
<th>(3)</th>
</tr>
</thead>
<tbody>
<tr>
<td>Threshold</td>
<td>−0.3281***<br/>(0.1113)</td>
<td>−0.4144***<br/>(0.1148)</td>
<td>−0.4789***<br/>(0.1308)</td>
</tr>
<tr>
<td>Calendar</td>
<td>−0.0778<br/>(0.0582)</td>
<td>0.0553<br/>(0.0709)</td>
<td>0.0735<br/>(0.0749)</td>
</tr>
<tr>
<td>Calendar *week4</td>
<td></td>
<td>−0.3029***<br/>(0.0808)</td>
<td>−0.3511***<br/>(0.0963)</td>
</tr>
<tr>
<td>Threshold *week4</td>
<td></td>
<td></td>
<td>0.2137<br/>(0.1620)</td>
</tr>
<tr>
<td>Observations</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
</tr>
<tr>
<td>Adjusted R<sup>2</sup></td>
<td>0.0130</td>
<td>0.0239</td>
<td>0.0244</td>
</tr>
</tbody>
</table>

**Panel B: Seasonal Patterns Across the Months of Each Quarter**

<table border="1">
<thead>
<tr>
<th></th>
<th colspan="3">Ret<sub>t+1</sub></th>
</tr>
<tr>
<th></th>
<th>1st Month of Q</th>
<th>2nd Month of Q</th>
<th>3rd Month of Q</th>
</tr>
<tr>
<th></th>
<th>(1)</th>
<th>(2)</th>
<th>(3)</th>
</tr>
</thead>
<tbody>
<tr>
<td>Threshold</td>
<td>−0.2723<br/>(0.2075)</td>
<td>−0.4153**<br/>(0.1666)</td>
<td>−0.5845***<br/>(0.2083)</td>
</tr>
<tr>
<td>Calendar * week4</td>
<td>−0.2509<br/>(0.1590)</td>
<td>−0.3487***<br/>(0.1062)</td>
<td>−0.3400***<br/>(0.1300)</td>
</tr>
<tr>
<td>Observations</td>
<td>2,078</td>
<td>2,052</td>
<td>2,097</td>
</tr>
<tr>
<td>Adjusted R<sup>2</sup></td>
<td>0.0110</td>
<td>0.0234</td>
<td>0.0469</td>
</tr>
</tbody>
</table>distinct rebalancing pressures.

Panel B of Table 2 shows that the predictability of our rebalancing signals varies across the months within a quarter. Specifically, we divide the sample into three groups: the first months of each quarter (January, April, July, and October), the second months of each quarter (February, May, August, and November), and the third months of each quarter (March, June, September, and December). Estimating our baseline regression conditional on these samples reveals that the predictive power and economic significance of rebalancing signals increase toward end-of-quarter.

The seasonal patterns in both the Threshold and Calendar signals align with the broader tendency of capital markets to rebalance at least quarterly. For instance, performance reports are often prepared quarterly, motivating portfolio managers to rebalance their allocations according to this schedule. While portfolio managers may not strictly adhere to a single rebalancing strategy – for instance, they might employ a mix of Threshold and Calendar indicators – there is a collective tendency to adjust portfolios at least once per quarter. The conditional estimates of the rebalancing signals’ coefficients reflect this behavior.

### 3.2 Dissecting Cross-Asset Predictability

If Threshold and Calendar are valid proxies for rebalancing activity, they should also predict aggregate stocks and bonds *individually*. Specifically, Threshold and Calendar should *negatively* predict equity excess returns and *positively* predict bond excess returns. To test this, we run our benchmark regression (4) when  $Ret_{t+1}$  is either S&P 500 or 10-year Treasury note futures returns.

Table 3 reports the results.<sup>28</sup> Columns (1) and (2) show results for equity, and Columns (3)-(4) for bonds. As expected, when stocks are overweight, future stock returns are lower, while future bond returns are higher, and vice versa. This effect is statistically significant for both rebalancing proxies, even after including controls. Economically, a one-standard-deviation decrease in the Threshold (Calendar) signal corresponds to an increase in equity returns of about 15.9 bps (16.9 bps) and a decrease in bond returns of about 4.1 bps (2.3

---

<sup>28</sup>In untabulated analysis provided to us by a major asset manager, using the 3:30 PM price to compute stock and bond returns instead of the closing price leads to largely the same results.**Table 3: Dissecting Cross-Asset Return Predictability**

This table reports estimates for the multivariate predictive regression (4).  $Ret$  is the S&P 500 futures excess returns (first two columns) or 10-y Treasury note futures excess returns (last two columns). Values in parentheses are heteroskedasticity-consistent standard errors. Constant estimates are not tabulated. Appendix Table D.13 reports the coefficient estimates for all regressors. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

<table border="1">
<thead>
<tr>
<th></th>
<th colspan="2"><math>Ret_{t+1}^{S\&amp;P\ 500}</math></th>
<th colspan="2"><math>Ret_{t+1}^{10-y}</math></th>
</tr>
<tr>
<th></th>
<th>(1)</th>
<th>(2)</th>
<th>(3)</th>
<th>(4)</th>
</tr>
</thead>
<tbody>
<tr>
<td>Threshold</td>
<td>-0.3302***<br/>(0.1062)</td>
<td>-0.3261***<br/>(0.1049)</td>
<td>0.0842***<br/>(0.0269)</td>
<td>0.0841***<br/>(0.0270)</td>
</tr>
<tr>
<td>Calendar</td>
<td>0.0424<br/>(0.0665)</td>
<td>0.0441<br/>(0.0645)</td>
<td>-0.0129<br/>(0.0116)</td>
<td>-0.0148<br/>(0.0113)</td>
</tr>
<tr>
<td>week4</td>
<td>0.0005<br/>(0.0004)</td>
<td>0.0005<br/>(0.0004)</td>
<td>0.0004***<br/>(0.0001)</td>
<td>0.0004***<br/>(0.0001)</td>
</tr>
<tr>
<td>Calendar * week4</td>
<td>-0.2667***<br/>(0.0758)</td>
<td>-0.2671***<br/>(0.0762)</td>
<td>0.0362***<br/>(0.0128)</td>
<td>0.0372***<br/>(0.0127)</td>
</tr>
<tr>
<td>Momentum</td>
<td>0.0018***<br/>(0.0005)</td>
<td>0.0018***<br/>(0.0006)</td>
<td>-0.0005***<br/>(0.0001)</td>
<td>-0.0005***<br/>(0.0001)</td>
</tr>
<tr>
<td>Ret</td>
<td>-0.0223<br/>(0.0264)</td>
<td>0.0030<br/>(0.0430)</td>
<td>-0.0020<br/>(0.0065)</td>
<td>-0.0027<br/>(0.0093)</td>
</tr>
<tr>
<td>Controls</td>
<td>NO</td>
<td>YES</td>
<td>NO</td>
<td>YES</td>
</tr>
<tr>
<td>Observations</td>
<td>6,223</td>
<td>6,223</td>
<td>6,223</td>
<td>6,223</td>
</tr>
<tr>
<td>Adjusted R<sup>2</sup></td>
<td>0.0225</td>
<td>0.0242</td>
<td>0.0078</td>
<td>0.0072</td>
</tr>
</tbody>
</table>bps) over the next trading day.<sup>29</sup>

### 3.3 Long-Term Evidence

There are several reasons to believe that Threshold and Calendar signals were less relevant prior to the 2000s. First, portfolios are more diversified today than they used to be in the past, and higher diversification should imply more rebalancing.<sup>30</sup> Second, liquidity needs have also changed, which requires pension funds to regularly sell assets to pay member benefits at the beginning of each month.<sup>31</sup> Finally, the TDF industry’s growth may have also contributed to rebalancing’s rising importance. The 2006 Pension Protection Act (PPA) designated TDFs and balanced funds as default options in DC plans, which helped propel their growth and attract new savers to such contrarian strategies. Since TDFs inherently engage in rebalancing, as demonstrated by [Parker, Schoar, and Sun \(2023\)](#), we would expect stronger rebalancing pressures in recent years.

To test our hypothesis, in Table 4, we employ a longer dataset starting in the mid-1960s. We use daily U.S. equity market total returns from Kenneth French’s database and estimate daily 10-year Treasury note total returns using Federal Reserve Board Treasury data. In the first column, we present whole-sample evidence. In the second and third columns, we split the sample at September 10, 1997, which coincides with the start date of our evidence in Table 1. The number of observations differs between Table 4 and 1 (6,421 vs. 6,226) due to variations in trading days between CRSP and Bloomberg futures data.

The evidence reported aligns with our expectations. While Column (1) shows that Threshold and Calendar signals are significant predictors of future XA returns, splitting

---

<sup>29</sup>[Pitkäjärvi, Suominen, and Vaittinen \(2020\)](#) explore cross-asset predictability, demonstrating that past bond returns predict future equity market returns, and past equity market returns predict future bond market returns. Our findings complement their results by revealing that the *same* (rebalancing) signals convey predictive power for *both* equities and bonds.

<sup>30</sup>Until the early 1990s, pension funds were mostly invested in fixed-income securities due to stricter regulations, better funding conditions, and a higher interest rate environment. As interest rates declined, pension plans began shifting large portions of their portfolios away from bonds and toward equities. For example, the 2014 report “*State Public Pension Investments Shift Over Past 30 Years*” by the Pew Charitable Trusts shows that, until the 1980s, over 80% of public pension fund assets were invested in cash and bonds; see [report](#).

<sup>31</sup>Due to changing demographics, most U.S. DB pension funds began experiencing negative cash flows by the early 2000s (see, e.g., OECD reports *Pension Markets in Focus*).**Table 4: Long-Term Evidence**

This table reports estimates for the multivariate predictive regression (4) by using a longer dataset.  $Ret$  is the difference between daily U.S. equity total returns from Kenneth French’s database and daily 10-year Treasury note total returns calculated using U.S. Treasury yield curve data from [Gürkaynak, Sack, and Wright \(2007\)](#). Threshold and Calendar signals are constructed as described in Section 1.2. Momentum is computed by averaging the sign of 11 to 20, and 21, 42, 63, 126, and 252 trailing equity returns in excess of the 10-year Treasury note. The data spans from 1961-06-16 to 2023-03-17 (the entire sample is used in the first column of the table). For consistency with our previous estimations, the estimations in the second column end on 1997-09-09, while those in the third column begin on 1997-09-10. Values in parentheses are heteroskedasticity-consistent standard errors. Constant estimates are not tabulated. Daily observations.

<table border="1">
<thead>
<tr>
<th></th>
<th colspan="3">Ret<sub>t+1</sub></th>
</tr>
<tr>
<th></th>
<th>(1)</th>
<th>(2)</th>
<th>(3)</th>
</tr>
<tr>
<th>Sample</th>
<th>1961-2023</th>
<th>1961-1997</th>
<th>1997-2023</th>
</tr>
</thead>
<tbody>
<tr>
<td>Threshold</td>
<td>−0.1809***<br/>(0.0620)</td>
<td>−0.0157<br/>(0.0576)</td>
<td>−0.3685***<br/>(0.1103)</td>
</tr>
<tr>
<td>Calendar</td>
<td>0.0259<br/>(0.0411)</td>
<td>−0.0204<br/>(0.0495)</td>
<td>0.0573<br/>(0.0612)</td>
</tr>
<tr>
<td>week4</td>
<td>0.0004<br/>0.0002</td>
<td>0.0005**<br/>(0.0002)</td>
<td>0.0000<br/>(0.0004)</td>
</tr>
<tr>
<td>Calendar * week4</td>
<td>−0.1536***<br/>(0.0471)</td>
<td>−0.0284<br/>(0.0596)</td>
<td>−0.2569***<br/>(0.0670)</td>
</tr>
<tr>
<td>Momentum</td>
<td>0.0013***<br/>(0.0003)</td>
<td>0.0004<br/>(0.0003)</td>
<td>0.0020***<br/>(0.0005)</td>
</tr>
<tr>
<td>Ret</td>
<td>0.0216<br/>(0.0192)</td>
<td>0.1433***<br/>(0.0245)</td>
<td>−0.0144<br/>(0.0280)</td>
</tr>
<tr>
<td>Observations</td>
<td>15,291</td>
<td>8,870</td>
<td>6,421</td>
</tr>
<tr>
<td>Adjusted R<sup>2</sup></td>
<td>0.0053</td>
<td>0.0204</td>
<td>0.0170</td>
</tr>
</tbody>
</table>the sample allows for a deeper understanding of aggregate dynamics. Over the past approximately 30 years, the rebalancing coefficients are both quantitatively large and statistically significant, whereas they are indistinguishable from zero over the preceding four decades. These findings support the view that Threshold and Calendar signals effectively capture the behavior of large groups of rebalancers. Finally, we note that the estimates for the period 1997–2023 closely resemble those presented in Table 1, providing an additional robustness check for our main results.<sup>32</sup>

### 3.4 Rebalancing Pressures across Equity Indices

Some TDFs have specific allocations to large- and small-capitalization stocks, suggesting that the impact of rebalancing pressures may extend beyond aggregate markets. For example, PGIM Target Date and BlackRock LifePath funds allocate capital explicitly between large-cap and small-cap stocks. Recent work by [Pavlova and Sikorskaya \(2023\)](#) further motivates our analysis, showing that investor demand is highly sensitive to changes in the composition of the Russell 1000 and Russell 2000 indices. Although such allocations apply only to a subset of institutional investors, they enable us to test our empirical strategy across different equity indices.

To study this rebalancing mechanism, we apply the empirical framework outlined in Section 1, with a few modifications. To emulate TDF design, we analyze a portfolio invested in the Russell 1000 and Russell 2000 indices. To reflect typical allocations, the portfolio maintains a 90%/10% split between the Russell 1000 and Russell 2000 rather than the conventional 60/40 allocation for stock/bond portfolios. Our analysis begins in August 2006, when TDFs started to come into broad use.

We also conduct a falsification test by examining rebalancing pressures across growth and value stocks using the Russell 1000 Value and Russell 1000 Growth indices. Since institutional investors do not generally target allocations between these two market segments, we expect Threshold and Calendar signals to be insignificant predictors of excess returns between value and growth stocks.

The results reported in Panel A of Table 5 offer some insights. For large- and small-

---

<sup>32</sup>We have extended the sample through 2025 and find that the results become even stronger.cap stocks, the Threshold and Calendar signals exhibit predictive power consistent with our rebalancing interpretation. However, their statistical and economic significance is smaller than that reported in Table 4, aligning with our observation that only a subset of institutional investors may target allocations within specific segments of the U.S. equity market. Finally, as expected, the rebalancing signals show no predictive power for excess returns between value and growth stocks.

**Table 5: Rebalancing across Equity Indices**

In Column (1), we predict the returns of the Russell 1000 Index (R1K) in excess of the Russell 2000 Index (R2K). In Columns (2), we predict the returns of the Russell 1000 Value Index (R1K Value) in excess of the Russell 1000 Growth Index (R1K Growth). Threshold and Calendar signals are constructed within their respective equity segments. We use momentum and one-day trailing returns as controls. Values in parentheses are heteroskedasticity-consistent standard errors. Constant and control estimates are not tabulated. Daily observations. The sample period is 2006-08-17 to 2023-03-17.

<table border="1">
<thead>
<tr>
<th></th>
<th>(1)<br/>R1K / R2K</th>
<th>(2)<br/>R1K Value / R1K Growth</th>
</tr>
</thead>
<tbody>
<tr>
<td>Threshold</td>
<td>−0.2054***<br/>(0.0597)</td>
<td>−0.0339<br/>(0.0478)</td>
</tr>
<tr>
<td>Calendar * week4</td>
<td>−0.1174*<br/>(0.0683)</td>
<td>−0.0678<br/>(0.0654)</td>
</tr>
<tr>
<td>Observations</td>
<td>4,175</td>
<td>4,175</td>
</tr>
<tr>
<td>Adjusted R<sup>2</sup></td>
<td>0.0094</td>
<td>0.0023</td>
</tr>
</tbody>
</table>

### 3.5 Spillover Effects in International Equity

We expect international equity prices to be similarly affected by rebalancing activities as U.S. equities. Allocations in international equities can constitute half or more of the size of allocations to domestic equities. Additionally, the returns of domestic and international equities are positively correlated. This implies that when an investor needs to rebalance their domestic equity positions, it is likely that they also need to rebalance their international equity positions.

To extend our analysis to international equities, we modify our empirical specificationto account for different closing times across stock markets. As international markets close before the U.S. stock market, one-day U.S. equity returns are highly and *positively* correlated with the subsequent one-day returns of international equity indices. We control for the two-day trailing returns of the S&P 500 in order to characterize cross-market serial correlations. Since our rebalancing signals depend on trailing returns, we lag them by one day. While introducing this lag might reduce predictive power, it helps disentangle the positive cross-market correlation due to time differences from the rebalancing effects we aim to measure.

Table [D.14](#) shows that both Threshold and Calendar signal coefficients are negative and significant, with magnitudes similar to the ones reported in Table [1](#). The  $R^2$  from the predictive regression is approximately 2.5%, indicating that the total variation explained is also similar. Overall, this evidence suggests that rebalancing signals based on the dynamics of U.S. equity and bond markets are predictive of the returns of international equity markets.

## 4 Front-Running Rebalancers

We construct a simple, implementable real-time trading strategy by combining Threshold and Calendar signals. This strategy simulates the actions of an investor who, based on rebalancing signals, enters the equity and bond markets as a front-runner. On average, this investor buys equities and sells bonds after bonds have relatively outperformed and buys bonds while selling equities after equities have outperformed.

The trading strategy takes a position in a S&P 500 futures contract and an opposite position in a 10-year Treasury note futures contract as follows:

$$R_{t+1}^{\text{Strategy}} = (R_{t+1}^{\text{S\&P 500}} - R_{t+1}^{10-y}) \cdot w_t^{\text{Strategy}},$$

where the portfolio weight  $w_t^{\text{Strategy}}$  is defined as the average of modified versions of the Threshold and Calendar signals defined in Appendix B (see Eqs. [\(B.1\)](#)–[\(B.2\)](#)). We modify Threshold signal by rescaling to  $-\frac{\text{Threshold Signal}_t}{1.5\%}$  so that the two rebalancing signals have the same risk contribution to the strategy; in our sample, both signals exhibit an annualized volatility of 11.6%. The signal is multiplied by  $-1$  because a positive Threshold value indicates that the S&P 500 is overweight relative to the 10-year Treasury note.While the Threshold strategy can take a position on any day of the month, the Calendar strategy focuses on the end-of-month effect. Therefore, the Calendar signal is modified to  $\text{sign}(-\text{Calendar Signal}_t)$  if  $t$  falls within the last week of a month, to capture the “week4” effect. Furthermore, on the first business day of a new month, the modified Calendar signal is set to  $\text{sign}(\text{Calendar Signal}_{-4})$  to capture potential reversal effects (see Figure 4). On any other day, the modified version of the signal is set to zero.

**Table 6: Performance of Front-Running Trading Strategies**

This table reports performance results for the rebalancing-based dynamic strategy  $R_t^{\text{Strategy}}$  constructed as described in Section 4. Panel A reports several summary statistics. Panel B reports the alphas from regressing  $R_t^{\text{Strategy}}$  on the excess market returns (CAPM), on the four-factor Carhart (1997) model (C4), on the five-factor Fama and French (2015) (FF5), or on the Hou, Xue, and Zhang (2015)  $q$ -factors (HXZ). Panel C reports  $R_t^{\text{Strategy}}$  over high- and low-friction regimes, defined using the sample median of several variables; the columns labeled “H” (“L”) correspond to the sample period with above (below) median friction level. Idiosyncratic volatility (ivol) is calculated as the cross-sectional standard deviation of individual CRSP stock returns; liquidity risk is the BofA GFSI Liquidity Risk measure; VIX is the CBOE equity option-implied volatility index (divided by 100); MOVE is the U.S. bond market option-implied volatility index (divided by 100); EPU is the news-based measure of economic policy uncertainty from Baker, Bloom, and Davis (2016). Means, volatilities, and alphas are expressed in annualized percentage. Values in parentheses are heteroskedasticity-consistent standard errors. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

<table border="1">
<thead>
<tr>
<th colspan="11">Panel A: Descriptive Statistics</th>
</tr>
<tr>
<th></th>
<th colspan="2">Ex. Returns (in % p.a.)</th>
<th colspan="2">Volatility (in % p.a.)</th>
<th colspan="2">Sharpe Ratio</th>
<th colspan="4">Skewness</th>
</tr>
</thead>
<tbody>
<tr>
<td><math>R_t^{\text{SP500}}</math></td>
<td colspan="2">7.11</td>
<td colspan="2">20.05</td>
<td colspan="2">0.35</td>
<td colspan="4">-0.08</td>
</tr>
<tr>
<td><math>R_t^{10T}</math></td>
<td colspan="2">2.92</td>
<td colspan="2">6.13</td>
<td colspan="2">0.48</td>
<td colspan="4">0.03</td>
</tr>
<tr>
<td><math>R_t^{\text{Strategy}}</math></td>
<td colspan="2">10.20</td>
<td colspan="2">9.17</td>
<td colspan="2">1.11</td>
<td colspan="4">5.23</td>
</tr>
</tbody>
</table>

  

<table border="1">
<thead>
<tr>
<th colspan="5">Panel B: Alphas (in % p.a.)</th>
</tr>
<tr>
<th></th>
<th>CAPM</th>
<th>C4</th>
<th>FF5</th>
<th>HXZ</th>
</tr>
</thead>
<tbody>
<tr>
<td><math>\alpha</math></td>
<td>9.61***</td>
<td>9.64***</td>
<td>9.49***</td>
<td>9.43***</td>
</tr>
<tr>
<td></td>
<td>(1.77)</td>
<td>(1.78)</td>
<td>(1.74)</td>
<td>(1.75)</td>
</tr>
</tbody>
</table>

  

<table border="1">
<thead>
<tr>
<th colspan="11">Panel C: High- and Low-Friction Periods (in % p.a.)</th>
</tr>
<tr>
<th></th>
<th colspan="2">ivol</th>
<th colspan="2">liquidity risk</th>
<th colspan="2">VIX</th>
<th colspan="2">MOVE</th>
<th colspan="2">EPU</th>
</tr>
<tr>
<th></th>
<th>H</th>
<th>L</th>
<th>H</th>
<th>L</th>
<th>H</th>
<th>L</th>
<th>H</th>
<th>L</th>
<th>H</th>
<th>L</th>
</tr>
</thead>
<tbody>
<tr>
<td><math>R_t^{\text{Strategy}}</math></td>
<td>15.68***</td>
<td>5.09***</td>
<td>17.96***</td>
<td>3.79**</td>
<td>16.50***</td>
<td>3.91***</td>
<td>14.85***</td>
<td>5.55***</td>
<td>15.16***</td>
<td>5.24***</td>
</tr>
<tr>
<td></td>
<td>(3.44)</td>
<td>(1.28)</td>
<td>(3.33)</td>
<td>(1.85)</td>
<td>(3.44)</td>
<td>(1.11)</td>
<td>(3.32)</td>
<td>(1.43)</td>
<td>(3.26)</td>
<td>(1.56)</td>
</tr>
</tbody>
</table>Panel A of Table 6 summarizes the trading strategy’s statistics. The rebalancing-based strategy generates annualized average returns of approximately 10%, with a Sharpe ratio above 1, much higher than the 0.35 and 0.48 of the equity and bond markets, respectively, during our sample period. Importantly, our strategy is robust to the inclusion of transaction costs. Following the conservative assumptions of [Harvey et al. \(2018\)](#), we estimate that the Sharpe ratio net of transaction costs remains close to 1.

This performance cannot be explained by several standard factor models. In particular, Panel B of Table 6 shows the alphas from regressing the  $R_t^{\text{Strategy}}$  on the market portfolio (in excess of the risk-free asset), the [Carhart \(1997\)](#) four-factor model, the [Fama and French \(2015\)](#) five-factor model, or the [Hou, Xue, and Zhang \(2015\)](#)  $q$ -factor model. The alphas are positive, of significant magnitude, and highly significant, with a  $t$ -statistic above 4 for all combinations of factor models. This evidence supports our interpretation that rebalancing signals effectively times cross-asset returns rather than increasing exposure to systematic risk factors.

The strategy exhibits a high positive skewness of 5.23. This suggests strong performance during periods of heightened volatility, when the strategy takes larger positions, and market liquidity is lower. It is consistent with the evidence in Figure 6, which plots the cumulative log returns from investing \$1 in the front-running strategy along with the performance of \$1 invested in the  $R_t^{\text{SP500}}$  portfolio. In particular, the global financial crisis (GFC) of 2008–2009 and the 2020 COVID-19 crisis stand out as significant contributors to cumulative returns. But the economic significance of our strategy does not rely solely on these two extreme events: even after excluding the September 2008 to March 2009 and March 2020 periods, the strategy’s Sharpe ratio remains elevated at 0.90.

Limits to arbitrage are critical for front-running strategies to be profitable. Indeed, as valuations shift, rebalancers must adjust their positions to maintain target allocations, while constrained liquidity providers cannot fully absorb the rebalancing pressures and instead trade more slowly (see, e.g., [Ben-David, Franzoni, and Moussawi, 2012](#); [Gârleanu and Pedersen, 2013](#); [Vayanos and Vila, 2021](#)). Front-runners anticipate these dynamics and exploit the predictable price impact. However, we emphasize that front-running the rebalancing is not a risk-free strategy. Trading ahead of rebalancers is risky due to uncertainty in both the timing and magnitude of the rebalancing trades (e.g., [Dou, Kogan, and Wu, 2023](#)).![Figure 6: Front-Running Strategy Performance Over Time. A line graph showing Cumulative Gains (Log Scale) on the y-axis (0 to 6) versus time on the x-axis (2000 to 2020). Two lines are plotted: a blue line for 'Buy-and-hold R_t^{SP500}' and an orange line for 'R_t^{Strategy}'. The orange line shows significantly higher cumulative gains, especially after 2008, reaching approximately 6.5 by 2023, while the blue line reaches approximately 2.5 by the same period.](f5434f793464a5abdd7d2adcc02c7902_1_img.webp)

**Figure 6: Front-Running Strategy Performance Over Time.** This figure shows the cumulative gains of \$1 invested in the rebalancing-based strategy,  $R_t^{\text{Strategy}}$ , constructed as described in Section 4, alongside the performance of \$1 invested in the  $R_t^{\text{SP500}}$  portfolio.  $R_t$  denotes excess returns.  $R_t^{\text{Strategy}}$  is rescaled to match the volatility of  $R_t^{\text{SP500}}$ . Daily observations. The sample period is 1997-09-10 to 2023-03-17.

We examine how periods with different levels of friction affect how our strategy performs. As discussed in, e.g., [Gromb and Vayanos \(2010\)](#), limits to arbitrage can arise from a variety of frictions. First, we consider idiosyncratic volatility (ivol), which is widely considered to be a major implementation cost of short arbitrage ([Pontiff, 1996, 2006](#)). We follow the model-free approach of [Garcia, Mantilla-García, and Martellini \(2014\)](#) to compute ivol at a daily frequency as the cross-sectional standard deviation of individual CRSP stock returns.<sup>33</sup> We also examine several aggregate risk and uncertainty measures. These include: the Bank of America Global Financial Stress Index (GFSI) Liquidity Risk, which measures funding stress in the global financial system through spread-based relationships in rates, credit, and currencies; VIX and MOVE, the option-implied volatility measures for the U.S. stock and

<sup>33</sup>[Garcia, Mantilla-García, and Martellini \(2014\)](#) show that their measure is a consistent and asymptotically efficient estimator for aggregate idiosyncratic volatility. Furthermore, they find that the correlation between cross-sectional volatility and the model-based ivol as computed in [Ang, Hodrick, Xing, and Zhang \(2006\)](#) is above 99%.bond market, respectively; and the news-based measure of economic policy uncertainty from [Baker, Bloom, and Davis \(2016\)](#).

Panel C of Table 6 reports the (percentage) annualized performance of our strategy during high (H) and low (L) friction periods, defined based on the sample median of the limits of arbitrage proxy used. The analysis shows that front-running strategies perform better during high friction periods – characterized by elevated volatility, low liquidity, and heightened uncertainty – than low friction periods. This result is important as it suggests that our strategy is more profitable when liquidity providers are more constrained and price impact is larger, consistent with our interpretation.

## 5 Discussion

**Implications?** Given the economic significance of rebalancing costs, institutional investors should consider reassessing their rebalancing policies. First, the use of deterministic or systematic policies can lead to price impact. These pressures will likely intensify in the future as TDFs and other balanced funds come into broader use. Much of the institutional industry relies on Calendar or Threshold policies. This increases the likelihood that these investors will trade in the same direction at the same time and induces a mechanical predictability in returns that encourages front-running. Second, changing the design of benchmarks, such as end-of-month rebalancing, could have a major effect on rebalancing strategies. Those portfolio managers that tend to minimize tracking risk would immediately evolve their strategies to adjust to new benchmarks. Third, institutional investors should be wary of hedge funds and other investors that may anticipate their actions and attempt to profit from them. We simulate trading strategies in liquid futures that have yielded consistent and relatively large alpha over the last two decades; in addition, our own conversations with market participants have confirmed that hedge funds do deploy front-running strategies. Fourth, because rebalancing costs are borne by balanced funds, they remain hidden from individual investors who tend to focus on a fund’s explicit fees. Yet these costs represent a clear drag on performance – one that can be mitigated, as discussed next.**Can these rebalancing costs be reduced?** We are the first to document the market-wide economic implications of rebalancing strategies for equity–bond portfolios – the core allocation of institutional investors. This raises the question of whether more efficient rebalancing approaches exist beyond the commonly used Threshold and Calendar strategies. All else being equal, one could envision a cost-mitigating strategy that avoids pre-scheduled rebalancing – for example, by introducing a random component to trade execution (e.g., [Huddart, Hughes, and Levine, 2001](#)).

To explore this idea, Section 2.1 analyzed a hypothetical random rebalancing strategy that preserves the typical rebalancing frequency while eliminating predictable price pressures. We find that this strategy generates negligible price effects, largely eliminating rebalancing costs. These results indicate that a significant share of rebalancing costs arises from concentrated trading on predictable dates.

Three considerations are worth emphasizing. First, while random rebalancing substantially reduces transaction costs, it induces an average tracking error of approximately 35 bps. For a standard 60/40 equity–bond portfolio with an annualized volatility of 12% in our sample, this corresponds to about 3% of total portfolio volatility. Although this magnitude may appear small in absolute terms, its relevance varies across institutions. Investors operating under tight benchmark-tracking mandates may find even modest deviations costly, whereas others have greater flexibility. For example, Norges publicly reports a tracking error limit of 1.25% (see [Norges](#)).

Second, rebalancing decisions interact with the liability side of the balance sheet. Institutions with predictable end-of-month cash outflows may need to liquidate assets to meet liabilities. If a random rebalance occurs early in the month, such investors forgo the return on the rebalanced portfolio relative to cash over the remainder of the month, effectively incurring an additional opportunity cost.

Third, rebalancing is ultimately a coordination exercise. The actions of individual rebalancers can influence those of others, while liquidity providers and sophisticated investors may further affect the effectiveness of any given strategy.<sup>34</sup> Optimal rebalancing policies are therefore likely to depend on investor size: smaller investors may rebalance more oppor-

---

<sup>34</sup>For example, [Bessembinder, Carrion, Tuttle, and Venkataraman \(2016\)](#) show that trader competition can mitigate the price impact of predictable trades.tunistically, whereas larger investors must consider the market impact of their own trades, making aggregate liquidity conditions a central determinant of rebalancing costs.

In addition, investors may attempt to mitigate rebalancing costs through more active portfolio management. For instance, [Blume and Edelen \(2004\)](#) show that index funds can substantially enhance their performance by trading in advance of index additions and deletions.<sup>35</sup> In a similar spirit, balanced funds could potentially profit by anticipating trades driven by rebalancing pressures. This is also consistent with insights shared during the pension fund roundtable discussion mentioned earlier.

**What do investors gain from rebalancing?** Our paper documents the costs associated with large institutional investors mechanically rebalancing their portfolios. But are there corresponding benefits? One striking observation, highlighted in our initial figure, is the remarkable stability of asset allocations over time, clustered around a 60/40 equity–bond mix. Stepping back, it is far from obvious that a continuously rebalanced 60/40 portfolio is optimal for investors – or for pensioners. Determining the optimal portfolio choice lies well beyond the scope of this paper. What is clear, however, is that in the absence of rebalancing, portfolio weights mechanically drift toward equities – for example, a 60/40 portfolio would evolve to roughly 80/20 over a decade – resulting in a less diversified allocation. One may therefore argue that rebalancing preserves a degree of diversification consistent with investors’ risk preferences.<sup>36</sup> At the same time, it is not clear that a fixed weight target portfolio is itself optimal. Our analysis takes the target weights as given and shows that coordinated rebalancing activity generates predictable market impact and economically significant costs.

---

<sup>35</sup>[Khanjar \(2025\)](#) studies bond indices and reaches similar conclusions.

<sup>36</sup>We simulate three portfolios using the same data and sample period (1997–2023) as in our main empirical analysis: a buy-and-hold portfolio with an initial equity allocation of 60% that does not rebalance; a portfolio that rebalances when the equity allocation breaches a 2.5% threshold; and a portfolio that rebalances at month-end. We compute average utility as  $\bar{U} = \bar{r} - 0.5\gamma\bar{\sigma}^2$ , where  $\gamma$  denotes risk aversion and  $\bar{r}$  and  $\bar{\sigma}^2$  denote the sample mean return and variance, respectively. For  $\gamma = 3$ , threshold rebalancing generates utility gains of approximately 18 bps relative to buy-and-hold, while calendar rebalancing generates gains of about 10 bps.## 6 Conclusion

We present the first evidence of aggregate price effects for U.S. stocks and bonds driven by portfolio rebalancing activity. Using daily U.S. data, we construct two return-based proxies for institutional rebalancing behavior. When stocks outperform bonds, resulting in an overweight allocation to stocks within a balanced portfolio, rebalancers sell stocks and purchase bonds to restore target portfolio weights. On average, these rebalancing pressures lead equity returns to fall by more than 16 bps and bond returns to increase by approximately 4 bps the following day. The opposite effect occurs when bonds outperform stocks. This cross-asset return predictability cannot be explained by past returns, volatility measures, macroeconomic conditions, or sentiment indicators. Moreover, rebalancing pressures largely revert in less than two weeks, suggesting that rebalancing trades carry limited informational content about asset fundamentals.

We show that institutional investors' trading behavior is broadly consistent with our interpretation. To further validate the economic content of our rebalancing signals, we conduct several additional analyses. Specifically, we document (i) seasonal patterns consistent with a rebalancing motive, (ii) return predictability in both equity and bond markets, (iii) a marked increase in predictability over the past two decades, reflecting the growth of funds engaging in rebalancing, (iv) predictability across equity indices, and (v) corroborating international evidence.

Importantly, our results suggest that current rebalancing policies cost investors billions of dollars every year. We estimate these costs to be approximately \$16 billion per year, or \$200 per U.S. household. These costs are large compared to the cost of trading and it is much larger than the \$1.5-2.5 billion cost documented in the literature for the rebalancing of stocks within an index. As rebalancing pressures are expected to grow in the future with the expansion of TDFs and other balanced funds, these costs could increase substantially.

Furthermore, mechanical rebalancing offers certain investors the opportunity to front-run the predictable trades of large funds – a fact that, based on our conversations with several large institutional investors, is well-known to both pension funds and hedge funds. To explore the potential economic value of these front-running strategies, we construct a managed portfolio that replicates the trades of a front-runner exploiting rebalancing signals.This portfolio generates substantial positive alpha and achieves a Sharpe ratio greater than 1. Our analysis indicates that this strategy performs particularly well during periods of heightened volatility, when sophisticated investors face greater constraints, consistent with theories on the limits to arbitrage.

Overall, our findings highlight the importance of studying institutional investor trading to better understand asset price dynamics. Institutional investors operate under specific investment horizons, face unique constraints, and respond to distinct incentive structures, all of which influence how and when they trade ([Haddad and Muir, 2025](#)). Recognizing these features is essential for capturing the broader impact of their behavior on market outcomes.

We conclude by emphasizing that, while the objective of this paper is to quantify the economic costs associated with mechanical rebalancing, rebalancing remains a fundamental tool for ensuring portfolio diversification, managing liquidity, and generating utility gains for mean-variance investors compared to a non-rebalanced portfolio. Importantly, our analysis does not address whether commonly used portfolio rules – such as a 60/40 equity-bond allocation – are optimal. Rather, we take prevailing rebalancing policies as given and study their implications when implemented at scale. Finally, while investors are typically informed about fund expenses, including transaction costs and management fees, our findings uncover an additional cost that is not tabulated: the cost of rebalancing. Designing more effective rebalancing policies that preserve the benefits of rebalancing while minimizing its costs seems like a priority for future researchers and investors.## References

Ambachtsheer, K. P. 1987. Pension fund asset allocation: In defense of a 60/40 equity/debt asset mix. *Financial Analysts Journal* 43:14–24.

Andonov, A., E. Eiling, and D. Xu. 2024. Target date funds and international capital flows. *Available at SSRN 4713750* .

Ang, A., and G. Bekaert. 2007. Stock return predictability: Is it there? *Review of Financial Studies* 20:651–707.

Ang, A., R. J. Hodrick, Y. Xing, and X. Zhang. 2006. The cross-section of volatility and expected returns. *Journal of Finance* 61:259–99.

Ariel, R. A. 1987. A monthly effect in stock returns. *Journal of Financial Economics* 18:161–74.

Aruoba, S. B., F. X. Diebold, and C. Scotti. 2009. Real-time measurement of business conditions. *Journal of Business & Economic Statistics* 27:417–27.

Baker, S. R., N. Bloom, and S. J. Davis. 2016. Measuring economic policy uncertainty. *Quarterly Journal of Economics* 131:1593–636.

Bekaert, G., E. C. Engstrom, and N. R. Xu. 2022. The time variation in risk appetite and uncertainty. *Management Science* 68:3975–4004.

Ben-David, I., F. Franzoni, and R. Moussawi. 2012. Hedge fund stock trading in the financial crisis of 2007–2009. *Review of Financial Studies* 25:1–54.

Benham, F., R. Obregon, and M. Simanovich. 2018. Rebalancing. Meketa Investment Group, White Paper.

Bessembinder, H. 1992. Systematic risk, hedging pressure, and risk premiums in futures markets. *Review of Financial Studies* 5:637–67.

Bessembinder, H., A. Carrion, L. Tuttle, and K. Venkataraman. 2016. Liquidity, resiliency and market quality around predictable trades: Theory and evidence. *Journal of Financial economics* 121:142–66.

Blume, M. E., and R. M. Edelen. 2004. S & p 500 indexers, tracking errors, and liquidity. *Journal of Portfolio Management* 30:37–46.

Bretscher, L., L. Schmid, I. Sen, and V. Sharma. 2025. Institutional corporate bond pricing. *The Review of Financial Studies* hhaf067.Buffa, A. M., D. Vayanos, and P. Woolley. 2022. Asset management contracts and equilibrium prices. *Journal of Political Economy* 130:3146–201.

Calvet, L. E., J. Y. Campbell, and P. Sodini. 2009. Fight or flight? portfolio rebalancing by individual investors. *Quarterly Journal of Economics* 124:301–48.

Camanho, N., H. Hau, and H. Rey. 2022. Global portfolio rebalancing and exchange rates. *Review of Financial Studies* 35:5228–74.

Carhart, M. M. 1997. On persistence in mutual fund performance. *Journal of Finance* 52:57–82.

Chambers, D., E. Dimson, and A. Ilmanen. 2012. The Norway model. *Journal of Portfolio Management* 38:67–81.

Chen, H. 2025. Diversification driven demand for large stocks. *Journal of Financial Economics* 172:104109–.

Chen, H., G. Noronha, and V. Singal. 2006. Index changes and losses to index fund investors. *Financial Analysts Journal* 62:31–47.

Chinco, A., and V. Fos. 2021. The sound of many funds rebalancing. *Review of Asset Pricing Studies* 11:502–51.

Da, Z., J. Engelberg, and P. Gao. 2015. The sum of all fears investor sentiment and asset prices. *Review of Financial Studies* 28:1–32.

Da, Z., J. Hua, T. C.-C. Hung, and L. Peng. 2025. Market returns and a tale of two types of attention. *Management Science* 71:10505–37.

Da, Z., B. Larrain, C. Sialm, and J. Tessada. 2018. Destabilizing financial advice: Evidence from pension fund reallocations. *Review of Financial Studies* 31:3720–55.

De Long, J. B., A. Shleifer, L. H. Summers, and R. J. Waldmann. 1990. Noise trader risk in financial markets. *Journal of Political Economy* 98:703–38.

De Roon, F. A., T. E. Nijman, and C. Veld. 2000. Hedging pressure effects in futures markets. *Journal of Finance* 55:1437–56.

Dou, W. W., L. Kogan, and W. Wu. 2023. Common fund flows: Flow hedging and factor pricing. *Journal of Finance (Forthcoming)* .

Edelen, R. M., and J. B. Warner. 2001. Aggregate price effects of institutional trading: a study of mutual fund flow and market returns. *Journal of Financial Economics* 59:195–220.Etula, E., K. Rinne, M. Suominen, and L. Vaittinen. 2020. Dash for cash: Monthly market impact of institutional liquidity needs. *Review of Financial Studies* 33:75–111.

Fama, E. F., and K. R. French. 1996. Multifactor explanations of asset pricing anomalies. *Journal of Finance* 51:55–84.

———. 2015. A five-factor asset pricing model. *Journal of Financial Economics* 116:1–22.

Gabaix, X., and R. S. Koijen. 2021. In search of the origins of financial fluctuations: The inelastic markets hypothesis. Working Paper, National Bureau of Economic Research.

Gabaix, X., R. S. Koijen, F. Mainardi, S. Oh, and M. Yogo. 2023. Asset demand of U.S. households. *Available at SSRN 4251972* .

Garcia, R., D. Mantilla-García, and L. Martellini. 2014. A model-free measure of aggregate idiosyncratic volatility and the prediction of market returns. *Journal of Financial and Quantitative Analysis* 49:1133–65.

Gârleanu, N., and L. H. Pedersen. 2013. Dynamic trading with predictable returns and transaction costs. *Journal of Finance* 68:2309–40.

Goulding, C. L., C. R. Harvey, and M. G. Mazzoleni. 2023. Momentum turning points. *Journal of Financial Economics* 149:378–406.

Graziani, G. 2024. Time series reversal: An end-of-the-month perspective. *Available at SSRN 4349253* .

Gromb, D., and D. Vayanos. 2010. Limits of arbitrage. *Annual Review of Financial Economics* 2:251–75.

Grossman, S. J., and M. H. Miller. 1988. Liquidity and market structure. *Journal of Finance* 43:617–33.

Gürkaynak, R. S., B. Sack, and J. H. Wright. 2007. The U.S. treasury yield curve: 1961 to the present. *Journal of Monetary Economics* 54:2291–304.

Haddad, V., P. Huebner, and E. Loualiche. 2025. How competitive is the stock market? theory, evidence from portfolios, and implications for the rise of passive investing. *American Economic Review* 115:975–1018.

Haddad, V., and T. Muir. 2025. Market macrostructure: Institutions and asset prices. *Annual Review of Financial Economics* 17.

Harris, L., and E. Gurel. 1986. Price and volume effects associated with changes in the s&p 500 list: New evidence for the existence of price pressures. *Journal of Finance* 41:815–29.Hartzmark, S. M., and D. H. Solomon. 2025. Marketwide predictable price pressure. *American Economic Review* 115:3171–213.

Harvey, C. R., E. Hoyle, R. Korgaonkar, S. Rattray, M. Sargaison, and O. Van Hemert. 2018. The impact of volatility targeting. *Journal of Portfolio Management* 45:14–33.

Hodrick, R. J. 1992. Dividend yields and expected stock returns: Alternative procedures for inference and measurement. *Review of Financial Studies* 5:357–86.

Hou, K., C. Xue, and L. Zhang. 2015. Digesting anomalies: An investment approach. *Review of Financial Studies* 28:650–705.

Huddart, S., J. S. Hughes, and C. B. Levine. 2001. Public disclosure and dissimulation of insider trades. *Econometrica* 69:665–81.

Jansen, K. A. 2021. Long-term investors, demand shifts, and yields. Working paper.

Kang, W., K. G. Rouwenhorst, and K. Tang. 2020. A tale of two premiums: The role of hedgers and speculators in commodity futures markets. *Journal of Finance* 75:377–417.

Khanjar, A. 2025. Index rebalancing strategies in fixed income. Bloomberg Research, White Paper.

Koijen, R. S., and M. Yogo. 2019. A demand system approach to asset pricing. *Journal of Political Economy* 127:1475–515.

Lakonishok, J., and S. Smidt. 1988. A ninety-year perspective. *Review of Financial Studies* 1:403–25.

Li, J. J., N. D. Pearson, and Q. Zhang. 2021. Impact of demand shocks on the stock market: Evidence from chinese ipos. Working paper.

Lu, X., and L. Wu. 2025. Monetary transmission and portfolio rebalancing: a cross-sectional approach. *Available at SSRN 4413059* .

Moskowitz, T. J., Y. H. Ooi, and L. Pedersen. 2012. Time series momentum. *Journal of Financial Economics* 104:228–50.

Nagel, S. 2012. Evaporating liquidity. *Review of Financial Studies* 25:2005–39.

Ogden, J. P. 1990. Turn-of-month evaluations of liquid profits and stock returns: A common explanation for the monthly and January effects. *Journal of Finance* 45:1259–72.

Parker, J. A., A. Schoar, and Y. Sun. 2023. Retail financial innovation and stock market dynamics: The case of target date funds. *Journal of Finance* 78:2673–723.Parker, J. A., and Y. Sun. 2025. Target date funds as asset market stabilizers: evidence from the pandemic. *Journal of Pension Economics & Finance* 24:183–208.

Pavlova, A., and T. Sikorskaya. 2023. Benchmarking intensity. *Review of Financial Studies* 36:859–903.

Peng, C., and C. Wang. 2023. Factor rebalancing. *Available at SSRN 3327849* .

Perold, A. F., and W. F. Sharpe. 1988. Dynamic strategies for asset allocation. *Financial Analysts Journal* 44:16–27.

Petajisto, A. 2011. The index premium and its hidden cost for index funds. *Journal of Empirical Finance* 18:271–88.

Pitkäjärvi, A., M. Suominen, and L. Vaittinen. 2020. Cross-asset signals and time series momentum. *Journal of Financial Economics* 136:63–85.

Pontiff, J. 1996. Costly arbitrage: Evidence from closed-end funds. *Quarterly Journal of Economics* 111:1135–51.

———. 2006. Costly arbitrage and the myth of idiosyncratic risk. *Journal of Accounting and Economics* 42:35–52.

Puckett, A., and X. Yan. 2011. The interim trading skills of institutional investors. *Journal of Finance* 66:601–33.

Rattray, S., N. Granger, C. R. Harvey, and O. Van Hemert. 2020. Strategic rebalancing. *Journal of Portfolio Management* 46:10–31.

Ritter, J. R., and N. Chopra. 1989. Portfolio rebalancing and the turn-of-the-year effect. *Journal of Finance* 44:149–66.

Sammon, M., and J. J. Shim. 2026. Index rebalancing and stock market composition: Do indexes time the market? *Journal of Financial Economics* 177:104229–.

Shapiro, A. H., M. Sudhof, and D. J. Wilson. 2022. Measuring news sentiment. *Journal of Econometrics* 228:221–43.

Shleifer, A. 1986. Do demand curves for stocks slope down? *Journal of Finance* 41:579–90.

Vayanos, D., and J.-L. Vila. 2021. A preferred-habitat model of the term structure of interest rates. *Econometrica* 89:77–112.

Warther, V. A. 1995. Aggregate mutual fund flows and security returns. *Journal of Financial Economics* 39:209–35.Zhang, Y., and H. Ahluwalia. 2024. A rational multi-asset portfolio rebalancing decision-making framework. *Journal of Portfolio Management* 50.

Zhang, Y., H. Ahluwalia, A. Ying, M. Rabinovich, and A. Geysen. 2022. Rational rebalancing: An analytical approach to multiasset portfolio rebalancing decisions and insights. Vanguard Research, White Paper.# Internet Appendix

## A Data Sources

We construct continuous return series for the E-mini S&P 500 futures (ES) and the 10-year U.S. Treasury note futures (TY) using Bloomberg’s nearby contracts. Specifically, ES1 refers to the front-month E-mini S&P 500 futures contract and ES2 to the second-nearest contract; similarly, TY1 denotes the front-month 10-year Treasury note futures contract and TY2 the second-nearest contract. These are reported by Bloomberg as excess return price indices, which serve as the building blocks for our continuous series. To generate continuous returns, we stitched together the first and second nearby contracts for each market while accounting for the relevant expiry calendar. Our rule specifies that positions roll from the front contract (ES1 or TY1) to the second contract (ES2 or TY2) at the end of the month preceding the contract’s expiry month. From the first day of the expiry month until the expiry date, returns are based on the second contract, while before this window and after expiry they are based on the front contract. This methodology produces continuous time series that avoid discontinuities at contract expiration and reflect an easily replicable rolling convention. Lastly, a holiday was identified whenever both front contracts, TY1 and ES1, were reported as N/A in Bloomberg, indicating that neither futures market had traded on that date. In addition, we explicitly marked September 12–14, 2001, as exchange closures. During this period ES1 displayed no prices, while ES2 appeared to carry stale values. Our series and empirical analyses start September 10, 1997, when the first E-mini S&P 500 price data is available.

From Bloomberg we also obtain daily index data for the S&P 500 Total Return Index, the Bloomberg U.S. Aggregate Bond Total Return Index, and international equities (MSCI ACWI ex USA Net Total Return Index (USD)), as well as implied volatility measures for the equity market (VIX Index) and the Treasury bond market (MOVE Index).

## B Technical Details on the Construction of Rebalancing Signals

Consider a balanced equity–bond portfolio, where equity consists of S&P500 futures and bond consists of 10-year U.S. Treasury note futures. This portfolio is rebalanced following approach  $j$ , where  $j = T, C$ , indicating Threshold and Calendar, respectively. We denote by  $w_t^j$  the proportion of the portfolio invested in equity at time  $t$  and by  $(1 - w_t^j)$  the proportion invested in bonds. Target weights follow a common 60/40 allocation. Thus, at time  $t = 0$ ,60% of the portfolio is invested in S&P500 and 40% in the 10-year U.S. Treasury note, i.e.,  $w_t^j = 60\%$ .

At any time  $t$ , weights are updated as a function of past weights, equity returns, and bond returns. Specifically, after one period we have:

$$w_{t+1}^j(w_t^j; R_{t+1}^{SP}; R_{t+1}^{10Y}) = \frac{w_t^j(1 + R_{t+1}^{SP})}{w_t^j(1 + R_{t+1}^{SP}) + (1 - w_t^j)(1 + R_{t+1}^{10Y})}$$

where  $R_{t+1}^{SP}$  and  $R_{t+1}^{10Y}$  indicate the returns earned by the S&P500 and the 10-year Treasury note, respectively.

In the absence of rebalancing, no trading takes place and the following holds true:

$$w_{t+1}^j = w_t^j(w_t^j; R_{t+1}^{SP}; R_{t+1}^{10Y})$$

Weights are allowed to drift until a portfolio is rebalanced and portfolio weights are brought back to their targets.

According to the Threshold approach, portfolio rebalancing takes place when portfolio weights exceed their targets by more than  $\delta$ :

$$w_{t+1}^T = \begin{cases} 60\% & \text{if } |w_t^T - 60\%| \geq \delta, \\ w_{t+1}^T(w_t^T; R_{t+1}^{SP}; R_{t+1}^{10Y}) & \text{otherwise.} \end{cases}$$

According to the Calendar approach, rebalancing simply takes place on the last business day of every month:

$$w_{t+1}^C = \begin{cases} 60\% & \text{if } t \text{ is the last business day of the month,} \\ w_{t+1}^C(w_t^C; R_{t+1}^{SP}; R_{t+1}^{10Y}) & \text{otherwise.} \end{cases}$$

Lastly, we can define the rebalancing signals as weight deviations from target. Specifically, the Threshold signal is defined as:

$$\text{Threshold signal}_{t+1}^\delta = w_{t+1}^T(w_t^T; R_{t+1}^{SP}; R_{t+1}^{10Y}) - 60\% \quad (\text{B.1})$$

where  $\delta$  denotes the threshold adopted to rebalance the portfolio. The Calendar signal is defined as:

$$\text{Calendar signal}_{t+1} = w_{t+1}^C(w_t^C; R_{t+1}^{SP}; R_{t+1}^{10Y}) - 60\% \quad (\text{B.2})$$

where the portfolio is rebalanced on a monthly cadence.## C Summary Statistics

![Plot (a) Threshold Signal: A time series plot showing a blue line fluctuating around zero from 2000 to 2020. The y-axis ranges from -0.08 to 0.02 with increments of 0.02. The signal is relatively stable with small fluctuations around the zero line.](10f40c6c50c7ccb33148f3d07fe4e549_2_img.webp)

(a) Threshold Signal

![Plot (b) Calendar Signal: A time series plot showing a green line fluctuating around zero from 2000 to 2020. The y-axis ranges from -0.08 to 0.02 with increments of 0.02. The signal shows more pronounced fluctuations and larger spikes compared to the threshold signal, particularly around 2008 and 2020.](10f40c6c50c7ccb33148f3d07fe4e549_4_img.webp)

(b) Calendar Signal

**Figure C.1: Rebalancing Signals.** This figure shows the two rebalancing measures constructed as described in Section 1.2. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

**Table C.1: Rebalancing Signals: Summary Statistics**

This table reports summary statistics for the two rebalancing measures constructed as described in Section 1.2. Mean and standard deviation (SD) are annualized. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

<table border="1"><thead><tr><th></th><th>Mean</th><th>SD</th><th>AR1</th><th>Skewness</th><th>Exc. Kurtosis</th></tr></thead><tbody><tr><td>Threshold Signal</td><td>0.49</td><td>0.08</td><td>0.61</td><td>-0.98</td><td>2.69</td></tr><tr><td>Calendar Signal</td><td>0.18</td><td>0.16</td><td>0.91</td><td>-1.43</td><td>6.27</td></tr></tbody></table>**Table C.2: Correlation Matrix for Different Predictors**

This table reports the correlation matrix for the signals used in our main predictive regressions. Threshold and Calendar signals are constructed as described in Section 1.2. Momentum is computed by averaging the sign of 11 to 20, and 21, 42, 63, 126, and 252 trailing equity returns in excess of the 10-year Treasury note. Controls include: VIX is the CBOE equity option-implied volatility index; MOVE is the U.S. bond market option-implied volatility index; EPU is the news-based measure of economic policy uncertainty from [Baker, Bloom, and Davis \(2016\)](#); ADS is the [Aruoba, Diebold, and Scotti \(2009\)](#) real-time business conditions index; Sentiment is the daily news-based sentiment index constructed in [Shapiro, Sudhof, and Wilson \(2022\)](#). Daily observations. The sample period is 1997-09-10 to 2023-03-17.

<table border="1">
<thead>
<tr>
<th></th>
<th>Threshold</th>
<th>Calendar</th>
<th>Momentum</th>
<th>VIX</th>
<th>MOVE</th>
<th>Econ Uncertainty</th>
<th>Econ Activity</th>
<th>Sentiment</th>
</tr>
</thead>
<tbody>
<tr>
<td>Threshold</td>
<td>1</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>Calendar</td>
<td>0.605</td>
<td>1</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>Momentum</td>
<td>0.676</td>
<td>0.676</td>
<td>1</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>VIX</td>
<td>-0.353</td>
<td>-0.408</td>
<td>-0.489</td>
<td>1</td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>MOVE</td>
<td>-0.252</td>
<td>-0.239</td>
<td>-0.373</td>
<td>0.630</td>
<td>1</td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>EPU</td>
<td>-0.062</td>
<td>-0.129</td>
<td>-0.146</td>
<td>0.443</td>
<td>0.117</td>
<td>1</td>
<td></td>
<td></td>
</tr>
<tr>
<td>ADS</td>
<td>0.058</td>
<td>0.156</td>
<td>0.190</td>
<td>-0.323</td>
<td>-0.187</td>
<td>-0.278</td>
<td>1</td>
<td></td>
</tr>
<tr>
<td>Sentiment</td>
<td>0.101</td>
<td>0.130</td>
<td>0.247</td>
<td>-0.530</td>
<td>-0.333</td>
<td>-0.560</td>
<td>0.200</td>
<td>1</td>
</tr>
</tbody>
</table>## D Additional Results

![Bar chart showing t-stat values for different threshold values delta.](4f7856744174b647f8493b9cc860ec83_2_img.webp)

A bar chart showing the t-stat values for different threshold values  $\delta$  (%). The x-axis is labeled 'Threshold  $\delta$  (%)' and ranges from 0 to 4. The y-axis is labeled 't-stat' and ranges from -4 to 0. The bars are blue and show a general downward trend as  $\delta$  increases. A horizontal dashed red line is at approximately -2.6, representing the 1% critical value.

<table border="1"><thead><tr><th>Threshold <math>\delta</math> (%)</th><th>t-stat</th></tr></thead><tbody><tr><td>0.0</td><td>-4.0</td></tr><tr><td>0.2</td><td>-4.0</td></tr><tr><td>0.4</td><td>-3.8</td></tr><tr><td>0.6</td><td>-3.5</td></tr><tr><td>0.8</td><td>-3.2</td></tr><tr><td>1.0</td><td>-3.0</td></tr><tr><td>1.2</td><td>-3.2</td></tr><tr><td>1.4</td><td>-3.5</td></tr><tr><td>1.6</td><td>-3.8</td></tr><tr><td>1.8</td><td>-4.0</td></tr><tr><td>2.0</td><td>-4.2</td></tr><tr><td>2.2</td><td>-3.8</td></tr><tr><td>2.4</td><td>-3.5</td></tr><tr><td>2.6</td><td>-3.2</td></tr><tr><td>2.8</td><td>-3.0</td></tr><tr><td>3.0</td><td>-3.2</td></tr><tr><td>3.2</td><td>-3.5</td></tr><tr><td>3.4</td><td>-3.8</td></tr><tr><td>3.6</td><td>-4.0</td></tr><tr><td>3.8</td><td>-4.2</td></tr><tr><td>4.0</td><td>-4.0</td></tr></tbody></table>

**Figure D.1: Threshold Calibrations and Predictability.** This figure replicates Figure 2 using heteroskedasticity-and-autocorrelation-consistent standard errors. The dashed red line denotes the 1% critical value assuming a single test. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

![Bar chart showing t-stat values for different days to end-of-month.](4f7856744174b647f8493b9cc860ec83_4_img.webp)

A bar chart showing the t-stat values for different days to end-of-month. The x-axis is labeled 'Days to end-of-month' and ranges from -10 to -1. The y-axis is labeled 't-stat' and ranges from -3.5 to 0.0. The bars are blue and show a general downward trend as the days to end-of-month increase (i.e., as the month ends). A horizontal dashed red line is at approximately -2.6, representing the 1% critical value.

<table border="1"><thead><tr><th>Days to end-of-month</th><th>t-stat</th></tr></thead><tbody><tr><td>-10</td><td>-0.2</td></tr><tr><td>-9</td><td>-0.7</td></tr><tr><td>-8</td><td>-1.3</td></tr><tr><td>-7</td><td>-1.7</td></tr><tr><td>-6</td><td>-2.8</td></tr><tr><td>-5</td><td>-3.4</td></tr><tr><td>-4</td><td>-3.7</td></tr><tr><td>-3</td><td>-1.2</td></tr><tr><td>-2</td><td>-1.3</td></tr><tr><td>-1</td><td>-0.8</td></tr></tbody></table>

**Figure D.2: Calendar Signals and End-of-Month Effect.** This figure replicates Figure 3 using heteroskedasticity-and-autocorrelation-consistent standard errors. The dashed red line denotes the 1% critical value assuming a single test. Daily observations. The sample period is 1997-09-10 to 2023-03-17.![Bar chart showing t-statistics for predictability outside and during predicted rebalancing days across different threshold values delta.](dee93f1c06bd8d0b3f925e8f46419234_1_img.webp)

The figure is a bar chart with the y-axis labeled 't-stat' ranging from -6 to 2, and the x-axis labeled 'Threshold  $\delta$  (%)' ranging from 0 to 4. There are two data series: 'Predictability Outside Predicted Rebalancing Days' represented by orange bars and 'Predictability During Predicted Rebalancing Days' represented by dark blue bars. A horizontal dashed red line is drawn at approximately -2.5, representing the 1% critical value. The orange bars are generally positive, with the highest values around  $\delta = 0.25\%$  (approx. 2.5) and  $\delta = 0.5\%$  (approx. 1.5). The blue bars are generally negative, with the lowest values around  $\delta = 1.8\%$  (approx. -6.0) and  $\delta = 2.5\%$  (approx. -4.0). The bars are grouped by threshold value, with multiple bars for each  $\delta$ .

**Figure D.3: Threshold Calibrations and Conditional Predictability.** This figure shows the  $t$ -statistics for the predictive coefficient in (1) for different values of the threshold rebalancing range  $\delta$ . The dependent variable is the difference between the S&P 500 and the 10-year Treasury note futures returns. For each  $\delta$ , predictive regressions are estimated separately for days with  $|\text{Threshold Signal}_t^\delta| \geq \delta$ , corresponding to predicted rebalancing days, and for days with  $|\text{Threshold Signal}_t^\delta| < \delta$ , corresponding to days outside predicted rebalancing periods.  $t$ -statistics are based on heteroskedasticity-consistent standard errors. The dashed red line denotes the 1% critical value assuming a single test. Daily observations. The sample period is 1997-09-10 to 2023-03-17.![Figure D.4: Rebalancing and Horizon of Cross-Asset Return Predictability: Non-Overlapping Returns. Two bar charts showing predictive coefficients and 95% confidence intervals for threshold and calendar signals over 15 days ahead.](c8be10e8ce021a18e6500bb3d9ebb8d4_1_img.webp)

Figure D.4 consists of two bar charts, (a) and (b), showing predictive coefficients and 95% confidence intervals for non-overlapping returns over a horizon of 1 to 15 days ahead. The y-axis for both charts is 'Predictive Coefficients' ranging from -0.50 to 0.50. The x-axis is 'Days Ahead' ranging from 1 to 15.

(a) Threshold Signal: The coefficients are blue bars. The 1-day horizon has a negative coefficient of approximately -0.35. The 2-day horizon is approximately -0.20. The 3-day horizon is approximately -0.10. The 4-day horizon is approximately -0.15. The 5-day horizon is approximately 0.02. The 6-day horizon is approximately 0.10. The 7-day horizon is approximately 0.12. The 8-day horizon is approximately 0.15. The 9-day horizon is approximately 0.14. The 10-day horizon is approximately 0.05. The 11-day horizon is approximately -0.02. The 12-day horizon is approximately 0.13. The 13-day horizon is approximately -0.02. The 14-day horizon is approximately 0.10. The 15-day horizon is approximately 0.12.

(b) Calendar Signal \* Week4 Dummy: The coefficients are green bars. The 1-day horizon has a negative coefficient of approximately -0.30. The 2-day horizon is approximately -0.20. The 3-day horizon is approximately 0.05. The 4-day horizon is approximately -0.02. The 5-day horizon is approximately 0.12. The 6-day horizon is approximately 0.15. The 7-day horizon is approximately 0.02. The 8-day horizon is approximately 0.02. The 9-day horizon is approximately 0.05. The 10-day horizon is approximately -0.02. The 11-day horizon is approximately -0.02. The 12-day horizon is approximately 0.12. The 13-day horizon is approximately -0.02. The 14-day horizon is approximately -0.02. The 15-day horizon is approximately 0.08.

**Figure D.4: Rebalancing and Horizon of Cross-Asset Return Predictability: Non-Overlapping Returns.** This figure shows coefficient estimates and 95% heteroskedasticity-consistent confidence intervals for threshold and calendar signals for the multivariate predictive regression (4). We predict non-overlapping returns  $n$  days ahead, with  $n = 1 : 15$ . Daily observations. The sample period is 1997-09-10 to 2023-03-17.![Histogram of Economic Costs (in bps) for a randomly rebalanced portfolio. The x-axis ranges from -8 to 6, and the y-axis (Frequency) ranges from 0 to 1000. The distribution is centered around -0.6 bps, with a 95% interval marked by orange dotted lines.](3a86139e380ed13a1477d48a17a3a40a_1_img.webp)

The figure is a histogram showing the frequency distribution of economic costs in basis points (bps). The x-axis is labeled 'Economic Costs (in bps)' and ranges from -8 to 6 with major ticks every 2 units. The y-axis is labeled 'Frequency' and ranges from 0 to 1000 with major ticks every 200 units. The histogram consists of dark blue bars representing the frequency of costs in 1-bps bins. A red dashed vertical line is positioned at -0.6 bps, labeled 'Mean = -0.6 bps'. Two orange dotted vertical lines are positioned at approximately -4.6 and 3.4 bps, labeled '95% Interval'. The distribution is roughly bell-shaped, peaking at 0 bps with a frequency of approximately 1000, and tapering off towards the tails.

<table border="1">
<caption>Estimated data for Figure D.5: Economic Costs of Random Monthly Rebalancing</caption>
<thead>
<tr>
<th>Economic Costs (in bps)</th>
<th>Frequency</th>
</tr>
</thead>
<tbody>
<tr><td>-7.5</td><td>10</td></tr>
<tr><td>-7.0</td><td>20</td></tr>
<tr><td>-6.5</td><td>40</td></tr>
<tr><td>-6.0</td><td>60</td></tr>
<tr><td>-5.5</td><td>100</td></tr>
<tr><td>-5.0</td><td>150</td></tr>
<tr><td>-4.5</td><td>200</td></tr>
<tr><td>-4.0</td><td>300</td></tr>
<tr><td>-3.5</td><td>380</td></tr>
<tr><td>-3.0</td><td>570</td></tr>
<tr><td>-2.5</td><td>660</td></tr>
<tr><td>-2.0</td><td>780</td></tr>
<tr><td>-1.5</td><td>950</td></tr>
<tr><td>-1.0</td><td>1000</td></tr>
<tr><td>-0.5</td><td>1020</td></tr>
<tr><td>0.0</td><td>990</td></tr>
<tr><td>0.5</td><td>840</td></tr>
<tr><td>1.0</td><td>620</td></tr>
<tr><td>1.5</td><td>520</td></tr>
<tr><td>2.0</td><td>380</td></tr>
<tr><td>2.5</td><td>220</td></tr>
<tr><td>3.0</td><td>170</td></tr>
<tr><td>3.5</td><td>90</td></tr>
<tr><td>4.0</td><td>60</td></tr>
<tr><td>4.5</td><td>30</td></tr>
<tr><td>5.0</td><td>10</td></tr>
<tr><td>5.5</td><td>5</td></tr>
<tr><td>6.0</td><td>2</td></tr>
</tbody>
</table>

**Figure D.5: Economic Costs of Random Monthly Rebalancing.** This figure shows the distribution of economic costs for a randomly rebalanced portfolio that rebalances once per month on a randomly selected day. We simulate the strategy 10,000 times and report the resulting distribution of costs. Daily observations. The sample period is 1997-09-10 to 2023-03-17.**Table D.1: Explaining Rebalancing Signals with Trailing Returns**

This table reports the estimates from regressing Threshold and Calendar on the trailing returns of S&P 500 futures in excess of the trailing returns of 10-year Treasury note futures. Threshold and Calendar signals are constructed as described in Section 1.2. The horizon of the trailing returns is indicated in the table. Values in parentheses are heteroskedasticity- and autocorrelation-robust standard errors. Constant estimates are not tabulated. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

<table border="1">
<thead>
<tr>
<th></th>
<th>Threshold Signal</th>
<th>Calendar Signal</th>
</tr>
</thead>
<tbody>
<tr>
<td>1-Day Returns</td>
<td>0.1466***<br/>(0.0100)</td>
<td>0.0023<br/>(0.0030)</td>
</tr>
<tr>
<td>2-Day Returns</td>
<td>0.0278***<br/>(0.0030)</td>
<td>0.0041<br/>(0.0050)</td>
</tr>
<tr>
<td>3-Day Returns</td>
<td>0.0134***<br/>(0.0040)</td>
<td>0.0024<br/>(0.0040)</td>
</tr>
<tr>
<td>4-Day Returns</td>
<td>0.0129***<br/>(0.0020)</td>
<td>−0.0027<br/>(0.0070)</td>
</tr>
<tr>
<td>5-Day Returns</td>
<td>0.0177***<br/>(0.0020)</td>
<td>0.0298***<br/>(0.0070)</td>
</tr>
<tr>
<td>10-Day Returns</td>
<td>0.0145***<br/>(0.0020)</td>
<td>0.0611***<br/>(0.0060)</td>
</tr>
<tr>
<td>15-Day Returns</td>
<td>0.0051***<br/>(0.0020)</td>
<td>0.0607***<br/>(0.0050)</td>
</tr>
<tr>
<td>21-Day Returns</td>
<td>0.0061**<br/>(0.0020)</td>
<td>0.0502***<br/>(0.0070)</td>
</tr>
<tr>
<td>42-Day Returns</td>
<td>0.0025<br/>(0.0020)</td>
<td>0.0133*<br/>(0.0070)</td>
</tr>
<tr>
<td>63-Day Returns</td>
<td>0.0001<br/>(0.0010)</td>
<td>0.0024<br/>(0.0050)</td>
</tr>
<tr>
<td>126-Day Returns</td>
<td>0.0000<br/>(0.0010)</td>
<td>0.0010<br/>(0.0030)</td>
</tr>
<tr>
<td>252-Day Returns</td>
<td>0.0020***<br/>(0.0010)</td>
<td>0.0014<br/>(0.0020)</td>
</tr>
<tr>
<td>Adjusted <math>R^2</math></td>
<td>0.8020</td>
<td>0.7194</td>
</tr>
</tbody>
</table>**Table D.2: Cross-Asset Predictive Regressions Using HAC Covariance Matrix**

This table reports estimates for the multivariate predictive regression (4).  $Ret$  is the difference between S&P 500 and 10-y Treasury note futures returns. Threshold and Calendar signals are constructed as described in Section 1.2. Momentum is computed by averaging the sign of 11 to 20, and 21, 42, 63, 126, and 252 trailing equity returns in excess of the 10-year Treasury note. VIX is the CBOE equity option-implied volatility index (divided by 100); MOVE is the U.S. bond market option-implied volatility index (divided by 100); EPU is the news-based measure of economic policy uncertainty from Baker, Bloom, and Davis (2016); ADS is the Aruoba, Diebold, and Scotti (2009) real-time business conditions index; Sentiment is the daily news-based sentiment index constructed in Shapiro, Sudhof, and Wilson (2022). Values in parentheses are heteroskedasticity-and-autocorrelation-consistent standard errors. Constant estimates are not tabulated. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

<table border="1">
<thead>
<tr>
<th></th>
<th>(1)</th>
<th>(2)</th>
<th>Ret<sub>t+1</sub><br/>(3)</th>
<th>(4)</th>
<th>(5)</th>
</tr>
</thead>
<tbody>
<tr>
<td>Threshold</td>
<td>-0.4144***<br/>(0.1151)</td>
<td>-0.4208***<br/>(0.1174)</td>
<td>-0.4254***<br/>(0.1148)</td>
<td>-0.4254***<br/>(0.1146)</td>
<td>-0.4226***<br/>(0.1178)</td>
</tr>
<tr>
<td>Calendar</td>
<td>0.0553<br/>(0.0600)</td>
<td>0.0689<br/>(0.0597)</td>
<td>0.0572<br/>(0.0545)</td>
<td>0.0542<br/>(0.0604)</td>
<td>0.0666<br/>(0.0551)</td>
</tr>
<tr>
<td>week4</td>
<td>0.0002<br/>(0.0004)</td>
<td>0.0002<br/>(0.0004)</td>
<td>0.0002<br/>(0.0004)</td>
<td>0.0002<br/>(0.0004)</td>
<td>0.0002<br/>(0.0004)</td>
</tr>
<tr>
<td>Calendar *week4</td>
<td>-0.3029***<br/>(0.0662)</td>
<td>-0.3036***<br/>(0.0662)</td>
<td>-0.3026***<br/>(0.0670)</td>
<td>-0.3032***<br/>(0.0658)</td>
<td>-0.3033***<br/>(0.0667)</td>
</tr>
<tr>
<td>Momentum</td>
<td>0.0023***<br/>(0.0006)</td>
<td>0.0024***<br/>(0.0007)</td>
<td>0.0024***<br/>(0.0006)</td>
<td>0.0025***<br/>(0.0006)</td>
<td>0.0024***<br/>(0.0007)</td>
</tr>
<tr>
<td>Ret</td>
<td>-0.0203<br/>(0.0270)</td>
<td>-0.0167<br/>(0.0271)</td>
<td>-0.0198<br/>(0.0253)</td>
<td>-0.0192<br/>(0.0269)</td>
<td>-0.0173<br/>(0.0255)</td>
</tr>
<tr>
<td>VIX</td>
<td></td>
<td>0.0090**<br/>(0.0041)</td>
<td></td>
<td></td>
<td>0.0076<br/>(0.0051)</td>
</tr>
<tr>
<td>MOVE</td>
<td></td>
<td>-0.0020**<br/>(0.0010)</td>
<td></td>
<td></td>
<td>-0.0019*<br/>(0.0010)</td>
</tr>
<tr>
<td>EPU</td>
<td></td>
<td></td>
<td>0.0005*<br/>(0.0003)</td>
<td></td>
<td>0.0002<br/>(0.0003)</td>
</tr>
<tr>
<td>ADS</td>
<td></td>
<td></td>
<td>0.0000<br/>(0.0002)</td>
<td></td>
<td>0.0001<br/>(0.0002)</td>
</tr>
<tr>
<td>Sentiment</td>
<td></td>
<td></td>
<td></td>
<td>-0.0016<br/>(0.0011)</td>
<td>-0.0003<br/>(0.0013)</td>
</tr>
<tr>
<td>Observations</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
</tr>
<tr>
<td>Adjusted R<sup>2</sup></td>
<td>0.0239</td>
<td>0.0252</td>
<td>0.0243</td>
<td>0.0242</td>
<td>0.0248</td>
</tr>
</tbody>
</table>**Table D.3: Cross-Asset Predictive Regressions: Dissecting Momentum**

This table reports estimates for the multivariate predictive regression (4). *Ret* is the difference between S&P 500 and 10-year Treasury note futures returns. Threshold and Calendar signals are constructed as described in Section 1.2. Momentum fast is calculated as the average of the signs of trailing 1 to 10 daily excess returns; momentum medium averages the signs of 11 to 20 daily excess returns; momentum slow averages the signs of 21, 42, 63, 126, and 252 daily excess returns. VIX is the CBOE equity option-implied volatility index (divided by 100); MOVE is the U.S. bond market option-implied volatility index (divided by 100); EPU is the news-based measure of economic policy uncertainty from Baker, Bloom, and Davis (2016); ADS is the Aruoba, Diebold, and Scotti (2009) real-time business conditions index; Sentiment is the daily news-based sentiment index constructed in Shapiro, Sudhof, and Wilson (2022). Values in parentheses are heteroskedasticity-consistent standard errors. Constant estimates are not tabulated. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

<table border="1">
<thead>
<tr>
<th></th>
<th>(1)</th>
<th>(2)</th>
<th>Ret<sub>t+1</sub><br/>(3)</th>
<th>(4)</th>
<th>(5)</th>
</tr>
</thead>
<tbody>
<tr>
<td>Threshold</td>
<td>-0.4789***<br/>(0.1237)</td>
<td>-0.4864***<br/>(0.1260)</td>
<td>-0.4858***<br/>(0.1210)</td>
<td>-0.4851***<br/>(0.1233)</td>
<td>-0.4859***<br/>(0.1243)</td>
</tr>
<tr>
<td>Calendar</td>
<td>0.0449<br/>(0.0747)</td>
<td>0.0592<br/>(0.0702)</td>
<td>0.0480<br/>(0.0728)</td>
<td>0.0463<br/>(0.0742)</td>
<td>0.0573<br/>(0.0700)</td>
</tr>
<tr>
<td>week4</td>
<td>0.0002<br/>(0.0004)</td>
<td>0.0002<br/>(0.0004)</td>
<td>0.0002<br/>(0.0004)</td>
<td>0.0002<br/>(0.0004)</td>
<td>0.0002<br/>(0.0004)</td>
</tr>
<tr>
<td>Calendar *week4</td>
<td>-0.2986***<br/>(0.0811)</td>
<td>-0.2995***<br/>(0.0810)</td>
<td>-0.2986***<br/>(0.0808)</td>
<td>-0.2994***<br/>(0.0809)</td>
<td>-0.2992***<br/>(0.0809)</td>
</tr>
<tr>
<td>Momentum fast</td>
<td>0.0006<br/>(0.0005)</td>
<td>0.0007<br/>(0.0005)</td>
<td>0.0006<br/>(0.0005)</td>
<td>0.0006<br/>(0.0005)</td>
<td>0.0006<br/>(0.0005)</td>
</tr>
<tr>
<td>Momentum medium</td>
<td>0.0013***<br/>(0.0004)</td>
<td>0.0012***<br/>(0.0004)</td>
<td>0.0012***<br/>(0.0004)</td>
<td>0.0012***<br/>(0.0004)</td>
<td>0.0012***<br/>(0.0004)</td>
</tr>
<tr>
<td>Momentum slow</td>
<td>0.0010**<br/>(0.0004)</td>
<td>0.0011**<br/>(0.0005)</td>
<td>0.0011***<br/>(0.0004)</td>
<td>0.0012***<br/>(0.0004)</td>
<td>0.0011**<br/>(0.0005)</td>
</tr>
<tr>
<td>Ret</td>
<td>-0.0184<br/>(0.0282)</td>
<td>-0.0148<br/>(0.0284)</td>
<td>-0.0183<br/>(0.0276)</td>
<td>-0.0177<br/>(0.0281)</td>
<td>-0.0155<br/>(0.0281)</td>
</tr>
<tr>
<td>VIX</td>
<td></td>
<td>0.0085<br/>(0.0053)</td>
<td></td>
<td></td>
<td>0.0074<br/>(0.0062)</td>
</tr>
<tr>
<td>MOVE</td>
<td></td>
<td>-0.0021**<br/>(0.0011)</td>
<td></td>
<td></td>
<td>-0.0020*<br/>(0.0011)</td>
</tr>
<tr>
<td>EPU</td>
<td></td>
<td></td>
<td>0.0005<br/>(0.0003)</td>
<td></td>
<td>0.0002<br/>(0.0004)</td>
</tr>
<tr>
<td>ADS</td>
<td></td>
<td></td>
<td>0.0000<br/>(0.0002)</td>
<td></td>
<td>0.0001<br/>(0.0002)</td>
</tr>
<tr>
<td>Sentiment</td>
<td></td>
<td>62</td>
<td></td>
<td>-0.0014<br/>(0.0012)</td>
<td>-0.0002<br/>(0.0013)</td>
</tr>
<tr>
<td>Observations</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
</tr>
<tr>
<td>Adjusted R<sup>2</sup></td>
<td>0.0241</td>
<td>0.0253</td>
<td>0.0245</td>
<td>0.0243</td>
<td>0.0250</td>
</tr>
</tbody>
</table>**Table D.4: Cross-Asset Predictive Regressions Using Index Returns**

This table reports estimates for the multivariate predictive regression (4).  $Ret$  is the difference between S&P 500 Index and Bloomberg Aggregate Bond Index returns. Threshold and Calendar signals are constructed as described in Section 1.2. Momentum is computed by averaging the sign of 11 to 20, and 21, 42, 63, 126, and 252 trailing equity returns in excess of the 10-year Treasury note. VIX is the CBOE equity option-implied volatility index (divided by 100); MOVE is the U.S. bond market option-implied volatility index (divided by 100); EPU is the news-based measure of economic policy uncertainty from Baker, Bloom, and Davis (2016); ADS is the Aruoba, Diebold, and Scotti (2009) real-time business conditions index; Sentiment is the daily news-based sentiment index constructed in Shapiro, Sudhof, and Wilson (2022). Values in parentheses are heteroskedasticity-consistent standard errors. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

<table border="1">
<thead>
<tr>
<th></th>
<th>(1)</th>
<th>(2)</th>
<th><math>Ret_{t+1}</math><br/>(3)</th>
<th>(4)</th>
<th>(5)</th>
</tr>
</thead>
<tbody>
<tr>
<td>Threshold</td>
<td>-0.3970***<br/>(0.1199)</td>
<td>-0.4048***<br/>(0.1203)</td>
<td>-0.4137***<br/>(0.1163)</td>
<td>-0.4131***<br/>(0.1182)</td>
<td>-0.4039***<br/>(0.1195)</td>
</tr>
<tr>
<td>Calendar</td>
<td>0.0570<br/>(0.0740)</td>
<td>0.0743<br/>(0.0715)</td>
<td>0.0597<br/>(0.0729)</td>
<td>0.0560<br/>(0.0744)</td>
<td>0.0734<br/>(0.0716)</td>
</tr>
<tr>
<td>week4</td>
<td>0.0006<br/>(0.0005)</td>
<td>0.0006<br/>(0.0004)</td>
<td>0.0006<br/>(0.0005)</td>
<td>0.0006<br/>(0.0005)</td>
<td>0.0006<br/>(0.0005)</td>
</tr>
<tr>
<td>Calendar *week4</td>
<td>-0.3189***<br/>(0.0866)</td>
<td>-0.3199***<br/>(0.0863)</td>
<td>-0.3187***<br/>(0.0863)</td>
<td>-0.3194***<br/>(0.0863)</td>
<td>-0.3194***<br/>(0.0864)</td>
</tr>
<tr>
<td>Momentum</td>
<td>0.0021***<br/>(0.0006)</td>
<td>0.0023***<br/>(0.0007)</td>
<td>0.0023***<br/>(0.0007)</td>
<td>0.0023***<br/>(0.0007)</td>
<td>0.0023***<br/>(0.0007)</td>
</tr>
<tr>
<td>Ret</td>
<td>-0.0299<br/>(0.0311)</td>
<td>-0.0255<br/>(0.0311)</td>
<td>-0.0289<br/>(0.0306)</td>
<td>-0.0279<br/>(0.0308)</td>
<td>-0.0265<br/>(0.0309)</td>
</tr>
<tr>
<td>VIX</td>
<td></td>
<td>0.0117**<br/>(0.0060)</td>
<td></td>
<td></td>
<td>0.0108<br/>(0.0070)</td>
</tr>
<tr>
<td>MOVE</td>
<td></td>
<td>-0.0023**<br/>(0.0012)</td>
<td></td>
<td></td>
<td>-0.0021*<br/>(0.0012)</td>
</tr>
<tr>
<td>EPU</td>
<td></td>
<td></td>
<td>0.0007**<br/>(0.0003)</td>
<td></td>
<td>0.0003<br/>(0.0004)</td>
</tr>
<tr>
<td>ADS</td>
<td></td>
<td></td>
<td>0.0000<br/>(0.0002)</td>
<td></td>
<td>0.0001<br/>(0.0002)</td>
</tr>
<tr>
<td>Sentiment</td>
<td></td>
<td></td>
<td></td>
<td>-0.0018<br/>(0.0013)</td>
<td>0.0003<br/>(0.0013)</td>
</tr>
<tr>
<td>Observations</td>
<td>6,226</td>
<td>6,226<sup>63</sup></td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
</tr>
<tr>
<td>Adjusted R<sup>2</sup></td>
<td>0.0238</td>
<td>0.0258</td>
<td>0.0247</td>
<td>0.0242</td>
<td>0.0255</td>
</tr>
</tbody>
</table>**Table D.5: Cross-Asset Predictive Regressions Using Changes**

This table reports estimates for the multivariate predictive regression (4).  $Ret$  is the difference between S&P 500 and 10-year Treasury note futures returns. Threshold and Calendar signals are constructed as described in Section 1.2. Momentum is computed by averaging the sign of 11 to 20, and 21, 42, 63, 126, and 252 trailing equity returns in excess of the 10-year Treasury note. All control variables are expressed in changes. VIX is the CBOE equity option-implied volatility index (divided by 100); MOVE is the U.S. bond market option-implied volatility index (divided by 100); EPU is the news-based measure of economic policy uncertainty from Baker, Bloom, and Davis (2016); ADS is the Aruoba, Diebold, and Scotti (2009) real-time business conditions index; Sentiment is the daily news-based sentiment index constructed in Shapiro, Sudhof, and Wilson (2022). Values in parentheses are heteroskedasticity-consistent standard errors. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

<table border="1">
<thead>
<tr>
<th></th>
<th colspan="4"><math>Ret_{t+1}</math></th>
</tr>
<tr>
<th></th>
<th>(1)</th>
<th>(2)</th>
<th>(3)</th>
<th>(4)</th>
</tr>
</thead>
<tbody>
<tr>
<td>Threshold</td>
<td>-0.4049***<br/>(0.1148)</td>
<td>-0.4217***<br/>(0.1135)</td>
<td>-0.4122***<br/>(0.1152)</td>
<td>-0.4103***<br/>(0.1136)</td>
</tr>
<tr>
<td>Calendar</td>
<td>0.0570<br/>(0.0709)</td>
<td>0.0570<br/>(0.0687)</td>
<td>0.0557<br/>(0.0708)</td>
<td>0.0589<br/>(0.0685)</td>
</tr>
<tr>
<td>week4</td>
<td>0.0002<br/>(0.0004)</td>
<td>0.0002<br/>(0.0004)</td>
<td>0.0002<br/>(0.0004)</td>
<td>0.0002<br/>(0.0004)</td>
</tr>
<tr>
<td>Calendar *week4</td>
<td>-0.3048***<br/>(0.0812)</td>
<td>-0.3024***<br/>(0.0806)</td>
<td>-0.3029***<br/>(0.0808)</td>
<td>-0.3043***<br/>(0.0810)</td>
</tr>
<tr>
<td>Momentum</td>
<td>0.0023***<br/>(0.0006)</td>
<td>0.0023***<br/>(0.0006)</td>
<td>0.0023***<br/>(0.0006)</td>
<td>0.0023***<br/>(0.0006)</td>
</tr>
<tr>
<td>Ret</td>
<td>0.0031<br/>(0.0463)</td>
<td>-0.0179<br/>(0.0283)</td>
<td>-0.0207<br/>(0.0289)</td>
<td>0.0057<br/>(0.0461)</td>
</tr>
<tr>
<td><math>\Delta</math>VIX</td>
<td>0.0191<br/>(0.0367)</td>
<td></td>
<td></td>
<td>0.0196<br/>(0.0375)</td>
</tr>
<tr>
<td><math>\Delta</math>MOVE</td>
<td>0.0135*<br/>(0.0071)</td>
<td></td>
<td></td>
<td>0.0138*<br/>(0.0072)</td>
</tr>
<tr>
<td><math>\Delta</math>EPU</td>
<td></td>
<td>-0.0006<br/>(0.0004)</td>
<td></td>
<td>-0.0006*<br/>(0.0004)</td>
</tr>
<tr>
<td><math>\Delta</math>ADS</td>
<td></td>
<td>-0.0010<br/>(0.0039)</td>
<td></td>
<td>-0.0010<br/>(0.0040)</td>
</tr>
<tr>
<td><math>\Delta</math>Sentiment</td>
<td></td>
<td></td>
<td>-0.0044<br/>(0.0115)</td>
<td>-0.0041<br/>(0.0113)</td>
</tr>
<tr>
<td>Observations</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
</tr>
<tr>
<td>Adjusted <math>R^2</math></td>
<td>0.0257</td>
<td>0.0243</td>
<td>0.0238</td>
<td>0.0261</td>
</tr>
</tbody>
</table>**Table D.6: Cross-Asset Predictive Regressions Using Different Threshold Signals**

This table reports estimates for the multivariate predictive regression (4).  $Ret$  is the difference between S&P 500 and 10-y Treasury note futures returns. Threshold and Calendar signals are constructed as described in Section 1.2. Threshold 0–2% averages Threshold signals computed over  $\delta \in [0\%, 2\%]$ , while Threshold 0.1–2.5% averages Threshold signals computed over  $\delta \in [0.1\%, 2.5\%]$ . Momentum is computed by averaging the sign of 11 to 20, and 21, 42, 63, 126, and 252 trailing equity returns in excess of the 10-year Treasury note. Controls include: VIX is the CBOE equity option-implied volatility index (divided by 100); MOVE is the U.S. bond market option-implied volatility index (divided by 100); EPU is the news-based measure of economic policy uncertainty from Baker, Bloom, and Davis (2016); ADS is the Aruoba, Diebold, and Scotti (2009) real-time business conditions index; Sentiment is the daily news-based sentiment index constructed in Shapiro, Sudhof, and Wilson (2022). Values in parentheses are heteroskedasticity-consistent standard errors. Constant estimates are not tabulated. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

<table border="1">
<thead>
<tr>
<th></th>
<th colspan="4">Ret<sub>t+1</sub></th>
</tr>
<tr>
<th></th>
<th>(1)</th>
<th>(2)</th>
<th>(3)</th>
<th>(4)</th>
</tr>
</thead>
<tbody>
<tr>
<td>Threshold 0–2%</td>
<td>−0.3938***<br/>(0.1237)</td>
<td>−0.4003***<br/>(0.1225)</td>
<td></td>
<td></td>
</tr>
<tr>
<td>Threshold 0.1–2.5%</td>
<td></td>
<td></td>
<td>−0.3980***<br/>(0.1104)</td>
<td>−0.4060***<br/>(0.1095)</td>
</tr>
<tr>
<td>Calendar</td>
<td>0.0484<br/>(0.0707)</td>
<td>0.0604<br/>(0.0685)</td>
<td>0.0552<br/>(0.0709)</td>
<td>0.0665<br/>(0.0686)</td>
</tr>
<tr>
<td>week4</td>
<td>0.0002<br/>(0.0004)</td>
<td>0.0002<br/>(0.0004)</td>
<td>0.0002<br/>(0.0004)</td>
<td>0.0002<br/>(0.0004)</td>
</tr>
<tr>
<td>Calendar *week4</td>
<td>−0.2994***<br/>(0.0808)</td>
<td>−0.2998***<br/>(0.0809)</td>
<td>−0.3029***<br/>(0.0808)</td>
<td>−0.3033***<br/>(0.0808)</td>
</tr>
<tr>
<td>Momentum</td>
<td>0.0019***<br/>(0.0006)</td>
<td>0.0020***<br/>(0.0007)</td>
<td>0.0023***<br/>(0.0006)</td>
<td>0.0024***<br/>(0.0007)</td>
</tr>
<tr>
<td>Ret</td>
<td>−0.0189<br/>(0.0306)</td>
<td>−0.0157<br/>(0.0303)</td>
<td>−0.0242<br/>(0.0283)</td>
<td>−0.0212<br/>(0.0280)</td>
</tr>
<tr>
<td>Controls</td>
<td>NO</td>
<td>YES</td>
<td>NO</td>
<td>YES</td>
</tr>
<tr>
<td>Observations</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
</tr>
<tr>
<td>Adjusted <math>R^2</math></td>
<td>0.0228</td>
<td>0.0237</td>
<td>0.0239</td>
<td>0.0248</td>
</tr>
</tbody>
</table>**Table D.7: Cross-Asset Predictive Regressions: Different Portfolio Weights**

This table reports estimates for the multivariate predictive regression (4).  $Ret$  is the difference between S&P 500 and 10-year Treasury note futures returns. Threshold and Calendar signals are constructed as described in Section 1.2. Momentum is computed by averaging the sign of 11 to 20, and 21, 42, 63, 126, and 252 trailing equity returns in excess of the 10-year Treasury note. Values in parentheses are heteroskedasticity-consistent standard errors. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

<table border="1">
<thead>
<tr>
<th rowspan="2">equity–bond Allocation</th>
<th colspan="3">Ret<sub>t+1</sub></th>
</tr>
<tr>
<th>86/14</th>
<th>50/50</th>
<th>70/30</th>
</tr>
</thead>
<tbody>
<tr>
<td>Threshold</td>
<td>-0.8453***<br/>(0.212)</td>
<td>-0.4098***<br/>(0.107)</td>
<td>-0.4822***<br/>(0.131)</td>
</tr>
<tr>
<td>Calendar</td>
<td>0.1021<br/>(0.143)</td>
<td>0.0522<br/>(0.066)</td>
<td>0.0622<br/>(0.081)</td>
</tr>
<tr>
<td>week4</td>
<td>0.0001<br/>(0.000)</td>
<td>0.0002<br/>(0.000)</td>
<td>0.0001<br/>(0.000)</td>
</tr>
<tr>
<td>Calendar × week4</td>
<td>-0.6008***<br/>(0.160)</td>
<td>-0.2914***<br/>(0.076)</td>
<td>-0.3460***<br/>(0.091)</td>
</tr>
<tr>
<td>Momentum</td>
<td>0.0023***<br/>(0.001)</td>
<td>0.0023***<br/>(0.001)</td>
<td>0.0024***<br/>(0.001)</td>
</tr>
<tr>
<td>Ret</td>
<td>-0.0177<br/>(0.027)</td>
<td>-0.0186<br/>(0.029)</td>
<td>-0.0191<br/>(0.029)</td>
</tr>
<tr>
<td>Observations</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
</tr>
<tr>
<td>Adjusted <math>R^2</math></td>
<td>0.025</td>
<td>0.024</td>
<td>0.025</td>
</tr>
</tbody>
</table>**Table D.8: Cross-Asset Predictive Regressions: State-Dependent Effects**

This table reports estimates for the multivariate predictive regression (4).  $Ret$  is the difference between S&P 500 and 10-y Treasury note futures returns. Threshold and Calendar signals are constructed as described in Section 1.2. Threshold Small and Threshold Large correspond to the Threshold signal when its absolute value is below and above its median, respectively. Threshold<sup>⊥</sup> denotes the Threshold signal orthogonalized with respect to Momentum. Momentum is computed by averaging the sign of 11 to 20, and 21, 42, 63, 126, and 252 trailing equity returns in excess of the 10-year Treasury note. Controls include: VIX is the CBOE equity option-implied volatility index (divided by 100); MOVE is the U.S. bond market option-implied volatility index (divided by 100); EPU is the news-based measure of economic policy uncertainty from Baker, Bloom, and Davis (2016); ADS is the Aruoba, Diebold, and Scotti (2009) real-time business conditions index; Sentiment is the daily news-based sentiment index constructed in Shapiro, Sudhof, and Wilson (2022). Values in parentheses are heteroskedasticity-consistent standard errors. Constant estimates are not tabulated. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

<table border="1">
<thead>
<tr>
<th></th>
<th colspan="4">Ret<sub>t+1</sub></th>
</tr>
<tr>
<th></th>
<th>(1)</th>
<th>(2)</th>
<th>(3)</th>
<th>(4)</th>
</tr>
</thead>
<tbody>
<tr>
<td>Threshold Small</td>
<td>−0.2289<br/>(0.1637)</td>
<td>−0.2306<br/>(0.1619)</td>
<td></td>
<td></td>
</tr>
<tr>
<td>Threshold Large</td>
<td>−0.4264***<br/>(0.1143)</td>
<td>−0.4344***<br/>(0.1135)</td>
<td></td>
<td></td>
</tr>
<tr>
<td>Threshold<sup>⊥</sup></td>
<td></td>
<td></td>
<td>−0.4144***<br/>(0.1148)</td>
<td>−0.4226***<br/>(0.1139)</td>
</tr>
<tr>
<td>Calendar</td>
<td>0.0575<br/>(0.0708)</td>
<td>0.0690<br/>(0.0685)</td>
<td>0.0553<br/>(0.0709)</td>
<td>0.0666<br/>(0.0686)</td>
</tr>
<tr>
<td>week4</td>
<td>0.0002<br/>(0.0004)</td>
<td>0.0002<br/>(0.0004)</td>
<td>0.0002<br/>(0.0004)</td>
<td>0.0002<br/>(0.0004)</td>
</tr>
<tr>
<td>Calendar *week4</td>
<td>−0.3040***<br/>(0.0807)</td>
<td>−0.3044***<br/>(0.0807)</td>
<td>−0.3029***<br/>(0.0808)</td>
<td>−0.3033***<br/>(0.0808)</td>
</tr>
<tr>
<td>Momentum</td>
<td>0.0022***<br/>(0.0006)</td>
<td>0.0023***<br/>(0.0007)</td>
<td>0.0004<br/>(0.0005)</td>
<td>0.0004<br/>(0.0007)</td>
</tr>
<tr>
<td>Ret</td>
<td>−0.0196<br/>(0.0288)</td>
<td>−0.0166<br/>(0.0286)</td>
<td>−0.0203<br/>(0.0289)</td>
<td>−0.0173<br/>(0.0286)</td>
</tr>
<tr>
<td>Controls</td>
<td>NO</td>
<td>YES</td>
<td>NO</td>
<td>YES</td>
</tr>
<tr>
<td>Observations</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
</tr>
<tr>
<td>Adjusted <math>R^2</math></td>
<td>0.0242</td>
<td>0.0252</td>
<td>0.0239</td>
<td>0.0248</td>
</tr>
</tbody>
</table>**Table D.9: Cross-Asset Predictive Regressions: Alternative Controls**

This table reports estimates for the multivariate predictive regression (4).  $Ret$  is the difference between S&P 500 and 10-year Treasury note futures returns. Threshold and Calendar signals are constructed as described in Section 1.2. Momentum is computed by averaging the sign of 11 to 20, and 21, 42, 63, 126, and 252 trailing equity returns in excess of the 10-year Treasury note.  $ra^{BEX}$  and  $unc^{BEX}$  are, respectively, the risk aversion and economic uncertainty indexes constructed in Bekaert, Engstrom, and Xu (2022); FEARS is the Financial and Economic Attitudes Revealed by Search index constructed in Da, Engelberg, and Gao (2015) available from 2004-07-01 to 2016-12-30; ARA is the aggregate retail attention index constructed in Da et al. (2025) available from 2004-07-01 to 2019-12-31. Values in parentheses are heteroskedasticity-consistent standard errors. Daily observations.

<table border="1">
<thead>
<tr>
<th></th>
<th colspan="4">Ret<sub>t+1</sub></th>
</tr>
<tr>
<th></th>
<th>(1)</th>
<th>(2)</th>
<th>(3)</th>
<th>(4)</th>
</tr>
</thead>
<tbody>
<tr>
<td>Threshold</td>
<td>-0.4493***<br/>(0.1152)</td>
<td>-0.4375***<br/>(0.1134)</td>
<td>-0.4226**<br/>(0.1719)</td>
<td>-0.3731**<br/>(0.1537)</td>
</tr>
<tr>
<td>Calendar</td>
<td>0.1059*<br/>(0.0616)</td>
<td>0.0599<br/>(0.0704)</td>
<td>0.1000<br/>(0.1134)</td>
<td>0.1100<br/>(0.0980)</td>
</tr>
<tr>
<td>week4</td>
<td>0.0001<br/>(0.0004)</td>
<td>0.0001<br/>(0.0004)</td>
<td>0.0003<br/>(0.0006)</td>
<td>0.0003<br/>(0.0005)</td>
</tr>
<tr>
<td>Calendar *week4</td>
<td>-0.3048***<br/>(0.0807)</td>
<td>-0.3075***<br/>(0.0813)</td>
<td>-0.4011***<br/>(0.1309)</td>
<td>-0.3823***<br/>(0.1173)</td>
</tr>
<tr>
<td>Momentum</td>
<td>0.0025***<br/>(0.0006)</td>
<td>0.0026***<br/>(0.0007)</td>
<td>0.0020**<br/>(0.0010)</td>
<td>0.0016**<br/>(0.0008)</td>
</tr>
<tr>
<td>Ret</td>
<td>-0.0115<br/>(0.0289)</td>
<td>-0.0208<br/>(0.0290)</td>
<td>-0.0087<br/>(0.0389)</td>
<td>-0.0223<br/>(0.0350)</td>
</tr>
<tr>
<td>ra<sup>BEX</sup></td>
<td>0.0009<br/>(0.0006)</td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>unc<sup>BEX</sup></td>
<td></td>
<td>0.0007<br/>(0.0007)</td>
<td></td>
<td></td>
</tr>
<tr>
<td>FEARS</td>
<td></td>
<td></td>
<td>0.0009<br/>(0.0007)</td>
<td></td>
</tr>
<tr>
<td>ARA</td>
<td></td>
<td></td>
<td></td>
<td>0.0001<br/>(0.0060)</td>
</tr>
<tr>
<td>Observations</td>
<td>6,124</td>
<td>6,124</td>
<td>3,149</td>
<td>3,903</td>
</tr>
<tr>
<td>Adjusted R<sup>2</sup></td>
<td>0.0300</td>
<td>0.0249</td>
<td>0.0298</td>
<td>0.0270</td>
</tr>
</tbody>
</table>**Table D.10: Cross-Asset Predictive Regressions: The Role of Reversal**

This table reports estimates for the multivariate predictive regression (4).  $Ret$  is the difference between S&P 500 and 10-year Treasury note futures returns. Threshold and Calendar signals are constructed as described in Section 1.2. Momentum is computed by averaging the sign of 11 to 20, and 21, 42, 63, 126, and 252 trailing equity returns in excess of the 10-year Treasury note. Short-Term Reversal are the trailing 5-day returns; Long-Term Reversal are the trailing 5-year (i.e., 1260 days) returns with the last year skipped. Values in parentheses are heteroskedasticity-consistent standard errors. Constant estimates are not tabulated. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

<table border="1">
<thead>
<tr>
<th></th>
<th colspan="4">Ret<sub>t+1</sub></th>
</tr>
<tr>
<th></th>
<th>(1)</th>
<th>(2)</th>
<th>(3)</th>
<th>(4)</th>
<th>(5)</th>
</tr>
</thead>
<tbody>
<tr>
<td>Threshold</td>
<td></td>
<td>−0.4313***<br/>(0.1256)</td>
<td></td>
<td>−0.5644***<br/>(0.1140)</td>
<td>−0.5446***<br/>(0.1542)</td>
</tr>
<tr>
<td>Calendar</td>
<td></td>
<td>0.0694<br/>(0.0707)</td>
<td></td>
<td>0.0632<br/>(0.0840)</td>
<td>0.0691<br/>(0.0839)</td>
</tr>
<tr>
<td>week4</td>
<td></td>
<td>0.0001<br/>(0.0004)</td>
<td></td>
<td>0.0001<br/>(0.0005)</td>
<td>0.0001<br/>(0.0005)</td>
</tr>
<tr>
<td>Calendar *week4</td>
<td></td>
<td>−0.3077***<br/>(0.0814)</td>
<td></td>
<td>−0.2835***<br/>(0.0966)</td>
<td>−0.2858***<br/>(0.0978)</td>
</tr>
<tr>
<td>Momentum</td>
<td></td>
<td>0.0024***<br/>(0.0006)</td>
<td></td>
<td>0.0025***<br/>(0.0007)</td>
<td>0.0025***<br/>(0.0008)</td>
</tr>
<tr>
<td>Short-Term Reversal</td>
<td>−0.0377***<br/>(0.0136)</td>
<td>−0.0122<br/>(0.0195)</td>
<td></td>
<td></td>
<td>−0.0054<br/>(0.0236)</td>
</tr>
<tr>
<td>Long-Term Reversal</td>
<td></td>
<td></td>
<td>−0.0004<br/>(0.0004)</td>
<td>−0.0001<br/>(0.0004)</td>
<td>−0.0001<br/>(0.0004)</td>
</tr>
<tr>
<td>Observations</td>
<td>6,473</td>
<td>6,226</td>
<td>5,218</td>
<td>5,218</td>
<td>5,218</td>
</tr>
<tr>
<td>Adjusted R<sup>2</sup></td>
<td>0.0057</td>
<td>0.0240</td>
<td>−0.0001</td>
<td>0.0263</td>
<td>0.0262</td>
</tr>
</tbody>
</table>**Table D.11: Cross-Asset Predictive Regressions: End-of-Month Reversal**

This table reports estimates for the multivariate predictive regression (4). The dependent variable is the difference between S&P 500 futures excess returns and 10-year Treasury note futures excess returns (Columns (1) to (3)), S&P 500 futures excess returns in Column (4), or 10-year Treasury note futures excess returns in Column (5). EoM Rev is constructed as in [Graziani \(2024\)](#), defined as the realized return between the closing price on the fourth Friday of the month and the monthly closing price of the S&P 500 *index*. Threshold and Calendar signals are constructed as described in Section 1.2. Momentum is computed by averaging the sign of 11 to 20, and 21, 42, 63, 126, and 252 trailing equity returns in excess of the 10-year Treasury note. VIX is the CBOE equity option-implied volatility index (divided by 100); MOVE is the U.S. bond market option-implied volatility index (divided by 100); Econ Uncertainty is the news-based measure of economic policy uncertainty from [Baker, Bloom, and Davis \(2016\)](#); Econ Activity is the [Aruoba, Diebold, and Scotti \(2009\)](#) real-time business conditions index; Sentiment is the daily news-based sentiment index constructed in [Shapiro, Sudhof, and Wilson \(2022\)](#). Values in parentheses are heteroskedasticity-consistent standard errors. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

<table border="1">
<thead>
<tr>
<th></th>
<th><math>\text{Ret}_{t+1}^{S\&amp;P500} - \text{Ret}_{t+1}^{10-y}</math><br/>(1)</th>
<th><math>\text{Ret}_{t+1}^{S\&amp;P500}</math><br/>(2)</th>
<th><math>\text{Ret}_{t+1}^{10-y}</math><br/>(3)</th>
<th><math>\text{Ret}_{t+1}^{S\&amp;P500}</math><br/>(4)</th>
<th><math>\text{Ret}_{t+1}^{10-y}</math><br/>(5)</th>
</tr>
</thead>
<tbody>
<tr>
<td>EoM Rev</td>
<td>-0.0159<br/>(0.0154)</td>
<td></td>
<td>-0.0209<br/>(0.0157)</td>
<td>-0.0178<br/>(0.0146)</td>
<td>0.0031<br/>(0.0032)</td>
</tr>
<tr>
<td>Threshold</td>
<td></td>
<td>-0.4185***<br/>(0.1157)</td>
<td>-0.4116***<br/>(0.1163)</td>
<td>-0.3271***<br/>(0.1077)</td>
<td>0.0845***<br/>(0.0272)</td>
</tr>
<tr>
<td>Calendar</td>
<td></td>
<td>0.0554<br/>(0.0714)</td>
<td>0.0469<br/>(0.0729)</td>
<td>0.0351<br/>(0.0686)</td>
<td>-0.0118<br/>(0.0118)</td>
</tr>
<tr>
<td>week4</td>
<td></td>
<td>0.0001<br/>(0.0004)</td>
<td>0.0001<br/>(0.0004)</td>
<td>0.0005<br/>(0.0004)</td>
<td>0.0004***<br/>(0.0001)</td>
</tr>
<tr>
<td>Calendar *week4</td>
<td></td>
<td>-0.3052***<br/>(0.0812)</td>
<td>-0.3050***<br/>(0.0812)</td>
<td>-0.2687***<br/>(0.0763)</td>
<td>0.0363***<br/>(0.0128)</td>
</tr>
<tr>
<td>Momentum</td>
<td></td>
<td>0.0023***<br/>(0.0006)</td>
<td>0.0024***<br/>(0.0006)</td>
<td>0.0019***<br/>(0.0006)</td>
<td>-0.0005***<br/>(0.0001)</td>
</tr>
<tr>
<td>Ret</td>
<td></td>
<td>-0.0196<br/>(0.0292)</td>
<td>-0.0203<br/>(0.0292)</td>
<td>-0.0225<br/>(0.0267)</td>
<td>-0.0022<br/>(0.0065)</td>
</tr>
<tr>
<td>Observations</td>
<td>6,173</td>
<td>6,173</td>
<td>6,173</td>
<td>6,173</td>
<td>6,173</td>
</tr>
<tr>
<td>Adjusted R<sup>2</sup></td>
<td>0.0003</td>
<td>0.0241</td>
<td>0.0247</td>
<td>0.0236</td>
<td>0.0074</td>
</tr>
</tbody>
</table>**Table D.12: Cross-Asset Predictive Regressions: Calendar Effects Across Weeks**

This table reports estimates for the multivariate predictive regression (4).  $Ret$  is the difference between S&P 500 and 10-y Treasury note futures returns. Threshold and Calendar signals are constructed as described in Section 1.2. Momentum is computed by averaging the sign of 11 to 20, and 21, 42, 63, 126, and 252 trailing equity returns in excess of the 10-year Treasury note. Values in parentheses are heteroskedasticity-consistent standard errors. Constant estimates are not tabulated. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

<table border="1">
<thead>
<tr>
<th></th>
<th colspan="6">Ret<sub>t+1</sub></th>
</tr>
<tr>
<th></th>
<th>(1)</th>
<th>(2)</th>
<th>(3)</th>
<th>(4)</th>
<th>(5)</th>
<th>(6)</th>
</tr>
</thead>
<tbody>
<tr>
<td>Threshold</td>
<td>-0.3286***<br/>(0.1104)</td>
<td>-0.3152***<br/>(0.1175)</td>
<td>-0.3394***<br/>(0.1110)</td>
<td>-0.4103***<br/>(0.1150)</td>
<td>-0.3763***<br/>(0.1176)</td>
<td>-0.4056***<br/>(0.1165)</td>
</tr>
<tr>
<td>Calendar</td>
<td>-0.1000*<br/>(0.0604)</td>
<td>-0.0692<br/>(0.0587)</td>
<td>-0.1529**<br/>(0.0618)</td>
<td>0.0357<br/>(0.0784)</td>
<td>0.1240*<br/>(0.0729)</td>
<td>-0.0101<br/>(0.0910)</td>
</tr>
<tr>
<td>week1</td>
<td>0.0007<br/>(0.0004)</td>
<td></td>
<td></td>
<td>0.0009*<br/>(0.0005)</td>
<td></td>
<td></td>
</tr>
<tr>
<td>Calendar *week1</td>
<td>0.2262**<br/>(0.1018)</td>
<td></td>
<td></td>
<td>0.1109<br/>(0.1099)</td>
<td></td>
<td></td>
</tr>
<tr>
<td>week2</td>
<td></td>
<td>0.0002<br/>(0.0004)</td>
<td></td>
<td></td>
<td>0.0004<br/>(0.0005)</td>
<td></td>
</tr>
<tr>
<td>Calendar *week2</td>
<td></td>
<td>-0.0500<br/>(0.1123)</td>
<td></td>
<td></td>
<td>-0.2195*<br/>(0.1177)</td>
<td></td>
</tr>
<tr>
<td>week3</td>
<td></td>
<td></td>
<td>-0.0012***<br/>(0.0005)</td>
<td></td>
<td></td>
<td>-0.0013***<br/>(0.0005)</td>
</tr>
<tr>
<td>Calendar *week3</td>
<td></td>
<td></td>
<td>0.2579***<br/>(0.0887)</td>
<td></td>
<td></td>
<td>0.1305<br/>(0.1065)</td>
</tr>
<tr>
<td>week4</td>
<td></td>
<td></td>
<td></td>
<td>0.0004<br/>(0.0005)</td>
<td>0.0003<br/>(0.0005)</td>
<td>-0.0002<br/>(0.0005)</td>
</tr>
<tr>
<td>Calendar *week4</td>
<td></td>
<td></td>
<td></td>
<td>-0.2831***<br/>(0.0866)</td>
<td>-0.3745***<br/>(0.0843)</td>
<td>-0.2401**<br/>(0.0978)</td>
</tr>
<tr>
<td>Momentum</td>
<td>0.0021***<br/>(0.0006)</td>
<td>0.0021***<br/>(0.0006)</td>
<td>0.0022***<br/>(0.0006)</td>
<td>0.0023***<br/>(0.0006)</td>
<td>0.0022***<br/>(0.0006)</td>
<td>0.0023***<br/>(0.0006)</td>
</tr>
<tr>
<td>Ret</td>
<td>-0.0247<br/>(0.0290)</td>
<td>-0.0202<br/>(0.0292)</td>
<td>-0.0195<br/>(0.0291)</td>
<td>-0.0230<br/>(0.0291)</td>
<td>-0.0261<br/>(0.0290)</td>
<td>-0.0198<br/>(0.0290)</td>
</tr>
<tr>
<td>Observations</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
</tr>
<tr>
<td>Adjusted R<sup>2</sup></td>
<td>0.0161</td>
<td>0.0129</td>
<td>0.0211</td>
<td>0.0249</td>
<td>0.0273</td>
<td>0.0261</td>
</tr>
</tbody>
</table>**Table D.13: Dissecting Cross-Asset Return Predictability**

This table reports estimates for the multivariate predictive regression (4).  $Ret$  is the S&P 500 futures excess returns in Panel A; Panel B reports results for 10-year Treasury note futures excess returns. Values in parentheses are heteroskedasticity-consistent standard errors. Constant estimates are not tabulated. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

**Panel A: S&P 500 in excess of cash**

<table border="1">
<thead>
<tr>
<th></th>
<th>(1)</th>
<th>(2)</th>
<th><math>Ret_{t+1}</math><br/>(3)</th>
<th>(4)</th>
<th>(5)</th>
</tr>
</thead>
<tbody>
<tr>
<td>Threshold</td>
<td>-0.3302***<br/>(0.1062)</td>
<td>-0.3250***<br/>(0.1062)</td>
<td>-0.3344***<br/>(0.1048)</td>
<td>-0.3272***<br/>(0.1067)</td>
<td>-0.3261***<br/>(0.1049)</td>
</tr>
<tr>
<td>Calendar</td>
<td>0.0424<br/>(0.0665)</td>
<td>0.0428<br/>(0.0666)</td>
<td>0.0433<br/>(0.0646)</td>
<td>0.0430<br/>(0.0664)</td>
<td>0.0441<br/>(0.0645)</td>
</tr>
<tr>
<td>week4</td>
<td>0.0005<br/>(0.0004)</td>
<td>0.0005<br/>(0.0004)</td>
<td>0.0005<br/>(0.0004)</td>
<td>0.0005<br/>(0.0004)</td>
<td>0.0005<br/>(0.0004)</td>
</tr>
<tr>
<td>Calendar *week4</td>
<td>-0.2667***<br/>(0.0758)</td>
<td>-0.2674***<br/>(0.0763)</td>
<td>-0.2664***<br/>(0.0757)</td>
<td>-0.2667***<br/>(0.0758)</td>
<td>-0.2671***<br/>(0.0762)</td>
</tr>
<tr>
<td>Momentum</td>
<td>0.0018***<br/>(0.0005)</td>
<td>0.0018***<br/>(0.0006)</td>
<td>0.0018***<br/>(0.0006)</td>
<td>0.0018***<br/>(0.0005)</td>
<td>0.0018***<br/>(0.0006)</td>
</tr>
<tr>
<td>Ret</td>
<td>-0.0223<br/>(0.0264)</td>
<td>0.0015<br/>(0.0431)</td>
<td>-0.0209<br/>(0.0259)</td>
<td>-0.0229<br/>(0.0265)</td>
<td>0.0030<br/>(0.0430)</td>
</tr>
<tr>
<td>VIX</td>
<td></td>
<td>0.0211<br/>(0.0342)</td>
<td></td>
<td></td>
<td>0.0217<br/>(0.0351)</td>
</tr>
<tr>
<td>MOVE</td>
<td></td>
<td>0.0082<br/>(0.0067)</td>
<td></td>
<td></td>
<td>0.0083<br/>(0.0067)</td>
</tr>
<tr>
<td>EPU</td>
<td></td>
<td></td>
<td>-0.0004<br/>(0.0003)</td>
<td></td>
<td>-0.0004<br/>(0.0003)</td>
</tr>
<tr>
<td>ADS</td>
<td></td>
<td></td>
<td>-0.0006<br/>(0.0035)</td>
<td></td>
<td>-0.0005<br/>(0.0036)</td>
</tr>
<tr>
<td>Sentiment</td>
<td></td>
<td></td>
<td></td>
<td>-0.0061<br/>(0.0103)</td>
<td>-0.0063<br/>(0.0101)</td>
</tr>
<tr>
<td>Observations</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
</tr>
<tr>
<td>Adjusted R<sup>2</sup></td>
<td>0.0229</td>
<td>0.0239<sub>72</sub></td>
<td>0.0229</td>
<td>0.0228</td>
<td>0.0239</td>
</tr>
</tbody>
</table>**Panel B:** 10-year Treasury note in excess of cash

<table border="1">
<thead>
<tr>
<th></th>
<th>(1)</th>
<th>(2)</th>
<th>Ret<sub>t+1</sub><br/>(3)</th>
<th>(4)</th>
<th>(5)</th>
</tr>
</thead>
<tbody>
<tr>
<td>Threshold</td>
<td>0.0842***<br/>(0.0269)</td>
<td>0.0799***<br/>(0.0269)</td>
<td>0.0873***<br/>(0.0270)</td>
<td>0.0850***<br/>(0.0270)</td>
<td>0.0841***<br/>(0.0270)</td>
</tr>
<tr>
<td>Calendar</td>
<td>-0.0129<br/>(0.0116)</td>
<td>-0.0141<br/>(0.0116)</td>
<td>-0.0137<br/>(0.0114)</td>
<td>-0.0127<br/>(0.0116)</td>
<td>-0.0148<br/>(0.0113)</td>
</tr>
<tr>
<td>week4</td>
<td>0.0004***<br/>(0.0001)</td>
<td>0.0004***<br/>(0.0001)</td>
<td>0.0004***<br/>(0.0001)</td>
<td>0.0004***<br/>(0.0001)</td>
<td>0.0004***<br/>(0.0001)</td>
</tr>
<tr>
<td>Calendar *week4</td>
<td>0.0362***<br/>(0.0128)</td>
<td>0.0374***<br/>(0.0128)</td>
<td>0.0360***<br/>(0.0127)</td>
<td>0.0362***<br/>(0.0128)</td>
<td>0.0372***<br/>(0.0127)</td>
</tr>
<tr>
<td>Momentum</td>
<td>-0.0005***<br/>(0.0001)</td>
<td>-0.0005***<br/>(0.0001)</td>
<td>-0.0005***<br/>(0.0001)</td>
<td>-0.0005***<br/>(0.0001)</td>
<td>-0.0005***<br/>(0.0001)</td>
</tr>
<tr>
<td>Ret</td>
<td>-0.0020<br/>(0.0065)</td>
<td>-0.0015<br/>(0.0093)</td>
<td>-0.0030<br/>(0.0064)</td>
<td>-0.0022<br/>(0.0065)</td>
<td>-0.0027<br/>(0.0093)</td>
</tr>
<tr>
<td>VIX</td>
<td></td>
<td>0.0020<br/>(0.0067)</td>
<td></td>
<td></td>
<td>0.0020<br/>(0.0066)</td>
</tr>
<tr>
<td>MOVE</td>
<td></td>
<td>-0.0054***<br/>(0.0017)</td>
<td></td>
<td></td>
<td>-0.0055***<br/>(0.0017)</td>
</tr>
<tr>
<td>EPU</td>
<td></td>
<td></td>
<td>0.0002***<br/>(0.0001)</td>
<td></td>
<td>0.0003***<br/>(0.0001)</td>
</tr>
<tr>
<td>ADS</td>
<td></td>
<td></td>
<td>0.0005<br/>(0.0006)</td>
<td></td>
<td>0.0005<br/>(0.0007)</td>
</tr>
<tr>
<td>Sentiment</td>
<td></td>
<td></td>
<td></td>
<td>-0.0017<br/>(0.0031)</td>
<td>-0.0021<br/>(0.0031)</td>
</tr>
<tr>
<td>Observations</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
<td>6,226</td>
</tr>
<tr>
<td>Adjusted R<sup>2</sup></td>
<td>0.0074</td>
<td>0.0102</td>
<td>0.0087</td>
<td>0.0072</td>
<td>0.0117</td>
</tr>
</tbody>
</table>**Table D.14: Cross-Asset Predictive Regressions: International Equity**

This table reports estimates for the multivariate predictive regression (4) for international equity returns.  $Ret$  is the difference between MSCI ACWI ex U.S. Index and the U.S. 3-month Treasury bill. Threshold and Calendar signals are constructed as described in Section 1.2. Momentum is computed by averaging the sign of 11 to 20, and 21, 42, 63, 126, and 252 trailing equity returns in excess of the 10-year Treasury note. VIX is the CBOE equity option-implied volatility index (divided by 100); MOVE is the U.S. bond market option-implied volatility index (divided by 100); EPU is the news-based measure of economic policy uncertainty from Baker, Bloom, and Davis (2016); ADS is the Aruoba, Diebold, and Scotti (2009) real-time business conditions index; Sentiment is the daily news-based sentiment index constructed in Shapiro, Sudhof, and Wilson (2022). Values in parentheses are heteroskedasticity-consistent standard errors. Constant estimates are not tabulated. Daily observations. The sample period is 1997-09-10 to 2023-03-17.

<table border="1">
<thead>
<tr>
<th></th>
<th>(1)</th>
<th>(2)</th>
<th>Ret<sub>t+1</sub><br/>(3)</th>
<th>(4)</th>
<th>(5)</th>
</tr>
</thead>
<tbody>
<tr>
<td>Threshold</td>
<td>-0.2723***<br/>(0.0870)</td>
<td>-0.2773***<br/>(0.0857)</td>
<td>-0.2738***<br/>(0.0870)</td>
<td>-0.2766***<br/>(0.0868)</td>
<td>-0.2749***<br/>(0.0865)</td>
</tr>
<tr>
<td>Calendar</td>
<td>0.0810*<br/>(0.0453)</td>
<td>0.0855**<br/>(0.0427)</td>
<td>0.0810*<br/>(0.0447)</td>
<td>0.0801*<br/>(0.0457)</td>
<td>0.0818*<br/>(0.0433)</td>
</tr>
<tr>
<td>week4</td>
<td>0.0007**<br/>(0.0003)</td>
<td>0.0007**<br/>(0.0003)</td>
<td>0.0007**<br/>(0.0003)</td>
<td>0.0007**<br/>(0.0003)</td>
<td>0.0007**<br/>(0.0003)</td>
</tr>
<tr>
<td>Calendar *week4</td>
<td>-0.2060***<br/>(0.0535)</td>
<td>-0.2055***<br/>(0.0539)</td>
<td>-0.2056***<br/>(0.0536)</td>
<td>-0.2061***<br/>(0.0535)</td>
<td>-0.2055***<br/>(0.0539)</td>
</tr>
<tr>
<td>Momentum</td>
<td>0.0004<br/>(0.0003)</td>
<td>0.0003<br/>(0.0004)</td>
<td>0.0004<br/>(0.0003)</td>
<td>0.0005<br/>(0.0003)</td>
<td>0.0003<br/>(0.0004)</td>
</tr>
<tr>
<td>2-day Trailing Returns</td>
<td>0.0708***<br/>(0.0145)</td>
<td>0.0727***<br/>(0.0141)</td>
<td>0.0703***<br/>(0.0145)</td>
<td>0.0710***<br/>(0.0145)</td>
<td>0.0707***<br/>(0.0143)</td>
</tr>
<tr>
<td>VIX</td>
<td></td>
<td>0.0035<br/>(0.0043)</td>
<td></td>
<td></td>
<td>0.0011<br/>(0.0047)</td>
</tr>
<tr>
<td>MOVE</td>
<td></td>
<td>-0.0014*<br/>(0.0008)</td>
<td></td>
<td></td>
<td>-0.0011<br/>(0.0009)</td>
</tr>
<tr>
<td>EPU</td>
<td></td>
<td></td>
<td>0.0005**<br/>(0.0002)</td>
<td></td>
<td>0.0004<br/>(0.0003)</td>
</tr>
<tr>
<td>ADS</td>
<td></td>
<td></td>
<td>0.0001<br/>(0.0002)</td>
<td></td>
<td>0.0001<br/>(0.0002)</td>
</tr>
<tr>
<td>Sentiment</td>
<td></td>
<td></td>
<td></td>
<td>-0.0008<br/>(0.0009)</td>
<td>-0.0001<br/>(0.0009)</td>
</tr>
<tr>
<td>Observations</td>
<td>6,097</td>
<td>6,097</td>
<td>6,097</td>
<td>6,097</td>
<td>6,097</td>
</tr>
<tr>
<td>Adjusted R<sup>2</sup></td>
<td>0.0255</td>
<td>0.0262</td>
<td>0.0263</td>
<td>0.0255</td>
<td>0.0265</td>
</tr>
</tbody>
</table>