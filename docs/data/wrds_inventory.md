# WRDS library inventory

Observed on 2026-10-22 UTC (2026-10-23 in Madrid), from the MacBook.

`wrds.Connection()` authenticated without a prompt. `db.list_libraries()` returned
229 libraries. `db.list_tables(library=...)` succeeded for every library.
The table counts below include views and foreign tables. Aliases repeat some datasets.

**A listed table does not prove data access.** Reads through the `crsp` and
`optionm` aliases can fail because the underlying schema is outside our subscription.
The relevant checks below used actual `SELECT` queries, not only the catalog.

## Libraries

| Library | Listed tables/views |
|---|---:|
| `aha_sample` | 4 |
| `ahasamp` | 4 |
| `altrata_exec_samp` | 35 |
| `altsamp` | 35 |
| `auditsmp` | 15 |
| `auditsmp_all` | 15 |
| `bank` | 43 |
| `bank_all` | 21 |
| `bank_premium_samp` | 9 |
| `banksamp` | 9 |
| `block` | 3 |
| `block_all` | 3 |
| `boardex_trial` | 40 |
| `boardsmp` | 40 |
| `bvd_amadeus_trial` | 3 |
| `bvd_bvdbankf_trial` | 6 |
| `bvd_orbis_trial` | 9 |
| `bvdsamp` | 18 |
| `calcbench_trial` | 3 |
| `calcbnch` | 26 |
| `candid_samp` | 1 |
| `cboe` | 90 |
| `cboe_all` | 1 |
| `cboe_sample` | 7 |
| `cboesamp` | 7 |
| `cddsamp` | 1 |
| `ciqsamp` | 59 |
| `ciqsamp_capstrct` | 5 |
| `ciqsamp_common` | 13 |
| `ciqsamp_keydev` | 3 |
| `ciqsamp_pplintel` | 14 |
| `ciqsamp_ratings` | 18 |
| `ciqsamp_transactions` | 12 |
| `ciqsamp_transcripts` | 2 |
| `cisdmsmp` | 2 |
| `columnar` | 5 |
| `comp` | 293 |
| `comp_bank_daily` | 20 |
| `comp_global_daily` | 125 |
| `comp_na_daily_all` | 206 |
| `comp_segments_hist_daily` | 14 |
| `compsamp` | 15 |
| `compsamp_all` | 11 |
| `compsamp_computext` | 2 |
| `compsamp_snapshot` | 10 |
| `compseg` | 14 |
| `contrib` | 44 |
| `contrib_char_returns` | 1 |
| `contrib_corp_fed_litigation` | 2 |
| `contrib_corporate_culture` | 1 |
| `contrib_general` | 20 |
| `contrib_global_factor` | 4 |
| `contrib_intangible_value` | 2 |
| `contrib_kpss` | 2 |
| `contrib_liva` | 1 |
| `contrib_patent_firm_link` | 2 |
| `crsp` | 433 |
| `crsp_a_indexes` | 113 |
| `crsp_a_stock` | 95 |
| `crsp_m_indexes` | 113 |
| `crsp_m_stock` | 93 |
| `crsp_q_indexhist` | 11 |
| `crspm` | 352 |
| `crspsamp` | 63 |
| `crspsamp_all` | 47 |
| `crspsamp_mf` | 16 |
| `csmsamp_all` | 7 |
| `djones` | 2 |
| `djones_all` | 2 |
| `dmef` | 4 |
| `dmef_all` | 4 |
| `doe` | 2 |
| `doe_all` | 2 |
| `etfg_samp` | 4 |
| `etfgsamp` | 4 |
| `factsamp_all` | 28 |
| `factsamp_revere` | 12 |
| `factset_revere_common` | 28 |
| `factset_revere_geo_rev` | 5 |
| `factset_revere_supply_chain` | 7 |
| `ff` | 12 |
| `ff_all` | 12 |
| `fisdsamp` | 9 |
| `fisdsamp_all` | 9 |
| `fjc` | 7 |
| `fjc_linking` | 3 |
| `fjc_litigation` | 4 |
| `frb` | 4 |
| `frb_all` | 4 |
| `fssamp` | 40 |
| `ftsesamp` | 3 |
| `ftsesamp_russell_us` | 3 |
| `gutenberg` | 1 |
| `hfrsamp` | 7 |
| `hfrsamp_hfrdb` | 7 |
| `ibessamp_kpi` | 9 |
| `ifgrsamp` | 4 |
| `ims_obp_trial` | 2 |
| `imssamp` | 2 |
| `infasamp` | 5 |
| `infogroupsamp_business` | 3 |
| `infogroupsamp_residential` | 1 |
| `infraclear_samp` | 5 |
| `insdsamp` | 17 |
| `iri` | 15 |
| `iri_all` | 15 |
| `kpisamp` | 9 |
| `macrofin` | 24 |
| `macrofin_comm_trade` | 24 |
| `midas` | 1 |
| `morningstarsamp_cisdm` | 2 |
| `mpsych_sample` | 1 |
| `mrktsamp` | 20 |
| `mrktsamp_cds` | 1 |
| `mrktsamp_cdx` | 2 |
| `mrktsamp_msf` | 4 |
| `mrktsamp_red` | 13 |
| `msci_climate_samp` | 16 |
| `msci_common_samp` | 3 |
| `msci_esg_samp` | 12 |
| `mscicoms` | 3 |
| `mscicsmp` | 16 |
| `msciesmp` | 18 |
| `msrb` | 3 |
| `msrb_all` | 3 |
| `msrbsamp` | 1 |
| `msrbsamp_all` | 1 |
| `niq_samp` | 6 |
| `omtrial` | 24 |
| `optionm` | 578 |
| `optionm_all` | 402 |
| `optionmsamp_europe` | 12 |
| `optionmsamp_us` | 12 |
| `otc` | 1 |
| `otc_endofday` | 1 |
| `panjiva_samp` | 4 |
| `phlx` | 2 |
| `phlx_all` | 2 |
| `pitchsmp` | 71 |
| `pnjvasmp` | 4 |
| `preqin` | 19 |
| `preqin_deals` | 2 |
| `preqin_gp` | 5 |
| `preqin_lp` | 1 |
| `preqin_pe` | 10 |
| `preqin_vc` | 1 |
| `preqsamp` | 11 |
| `preqsamp_all` | 11 |
| `public` | 15 |
| `public_all` | 11 |
| `pwt` | 7 |
| `pwt_all` | 7 |
| `ravenpack_trial` | 8 |
| `reprisk_sample` | 11 |
| `repsamp` | 11 |
| `revelio_samp` | 21 |
| `revere` | 66 |
| `revsamp` | 21 |
| `risksamp` | 27 |
| `risksamp_all` | 27 |
| `rpnasamp` | 8 |
| `rq_all` | 1 |
| `rstat_samp` | 1 |
| `rstatsmp` | 1 |
| `sdcsamp` | 16 |
| `secsamp` | 35 |
| `secsamp_all` | 20 |
| `shvlsamp` | 2 |
| `snapsamp` | 10 |
| `snlsamp` | 4 |
| `snlsamp_fig` | 4 |
| `sustainalyticssamp_all` | 9 |
| `sustsamp` | 9 |
| `taqmsamp` | 58 |
| `taqmsamp_all` | 58 |
| `taqsamp` | 64 |
| `taqsamp_all` | 14 |
| `totalq` | 1 |
| `totalq_all` | 1 |
| `tr_sdc_samples` | 12 |
| `trace` | 33 |
| `trace_enhanced` | 15 |
| `trace_standard` | 24 |
| `trcstsmp` | 15 |
| `trdbdmismp` | 1 |
| `trdbwbsmp` | 8 |
| `trdssamp` | 19 |
| `tresgsmp` | 1 |
| `trsamp` | 21 |
| `trsamp_all` | 13 |
| `trsamp_db_dmi` | 1 |
| `trsamp_db_wb` | 8 |
| `trsamp_ds_eq` | 8 |
| `trsamp_dscom` | 3 |
| `trsamp_dsecon` | 3 |
| `trsamp_dsfut` | 5 |
| `trsamp_esg` | 1 |
| `trsamp_sdc_ma` | 3 |
| `trsamp_sdc_ni` | 1 |
| `trsamp_worldscope` | 8 |
| `trucost_samp` | 15 |
| `twoiq_samp` | 3 |
| `twoiqsmp` | 3 |
| `wabssamp` | 4 |
| `wappsamp` | 12 |
| `wenvsmp` | 4 |
| `wmfsmp` | 21 |
| `wrds_abs_samp` | 4 |
| `wrds_environmental_samp` | 4 |
| `wrds_insiders_samp` | 17 |
| `wrds_mutualfund_samp` | 21 |
| `wrds_shortvolume_samp` | 2 |
| `wrdsapps` | 72 |
| `wrdsapps_eushort` | 1 |
| `wrdsapps_evtstudy_int` | 2 |
| `wrdsapps_evtstudy_us` | 2 |
| `wrdsapps_finratio` | 2 |
| `wrdsapps_link_comp_eushort` | 1 |
| `wrdsapps_link_crsp_bond` | 1 |
| `wrdsapps_link_crsp_factset` | 1 |
| `wrdsapps_link_crsp_optionm` | 1 |
| `wrdsapps_link_crsp_taq` | 1 |
| `wrdsapps_patents` | 3 |
| `wrdsapps_subsidiary` | 2 |
| `wrdsapps_windices` | 3 |
| `wrdsappssamp_all` | 12 |
| `wrdssec_midas` | 1 |
| `zacksamp` | 17 |
| `zacksamp_all` | 17 |

## Relevant to this replication

| Item | Available? | Tables and observed limits |
|---|---|---|
| Futures prices: ES / 10-year T-note | **No** | `trsamp_dsfut.wrds_contract_info`, `wrds_fut_contract`, `wrds_cseries_info`, `wrds_fut_series` are readable samples (also exposed through `trdssamp`). The contract metadata has no ES, TY or ZN. Its S&P match is SP, the standard contract, not E-mini. The continuous-series metadata has standard S&P series, but no requested E-mini or 10-year Treasury series. `optionm.futures` and `optionm.futures_price` deny access to `optionm_europe`. |
| CRSP Treasuries | **No** | `crsp.tfz_dly_ft` and `crsp.tfz_idx` both return `permission denied for schema crsp_a_treasuries`. CRSP Treasuries are not in our subscription. |
| CRSP Mutual Funds | **No** (full product); **Yes** (limited sample) | `crsp.fund_hdr`, `fund_hdr_hist`, `fund_names`, `daily_returns` and `daily_nav_ret` deny access to `crsp_q_mutualfunds`. `crspsamp_mf.fund_names`, `fund_hdr_hist` and `daily_nav_ret` are readable. The sample identifies VBMFX as fund 31239 and VBTLX as fund 31244 using `nasdaq`, not `ticker`. See the source card for the short coverage. |
| CRSP index files | **Yes** | Actual row reads succeeded for `crsp.dsp500` and `crsp.dsi`. Not extracted by TASK-010. |
| MSCI index data | **No** | `msci_common_samp`, `msci_climate_samp`, `msci_esg_samp` and their aliases list issuer, climate and ESG tables, including `msci_esg_samp.msci_esg_ratings`. No MSCI index-return library/table was found. These samples do not supply ACWI ex USA Net TR USD. |
| Russell / FTSE index data | **Yes** (sample only) | `ftsesamp.ctr_monthly_us` is readable: Russell Top 200 only, 2008-08-29 through 2017-09-29, monthly reports. `ftsesamp.idx_holdings_us` and `rgs_sw_us` are also listed; alias `ftsesamp_russell_us`. This is not the required daily Russell 1000/2000/value/growth history. No extraction; recorded for the M-3 planner. |
| ANcerno (Abel Noser) | **No** | No ANcerno/Abel Noser library or table appeared in the full library/table inventory. |
| Fama–French factors | **Yes** | Actual row read succeeded for `ff.factors_daily`. `ff.fivefactors_daily`, `factors_monthly` and `fivefactors_monthly` are also listed; alias `ff_all`. TASK-005 owns factor downloads. |

No absence claim above treats a connection error as proof of missing subscription.
The CRSP and OptionMetrics exclusions come from PostgreSQL permission errors.
The other exclusions describe the catalog and sample metadata inspected in this session.
This is a recorded live inventory; the repeatable CLI remains pending the TASK-010 decision.
