"""
全球宏观-机构宏观
"""
from PPshare.economic.macro_constitute import (
    macro_cons_gold_amount,
    macro_cons_gold_change,
    macro_cons_gold_volume,
    macro_cons_opec_month,
    macro_cons_silver_amount,
    macro_cons_silver_change,
    macro_cons_silver_volume,
)

"""
全球宏观-美国宏观
"""
from PPshare.economic.macro_usa import (
    macro_usa_eia_crude_rate,
    macro_usa_non_farm,
    macro_usa_unemployment_rate,
    macro_usa_adp_employment,
    macro_usa_core_pce_price,
    macro_usa_cpi_monthly,
    macro_usa_crude_inner,
    macro_usa_gdp_monthly,
    macro_usa_initial_jobless,
    macro_usa_lmci,
    macro_usa_api_crude_stock,
    macro_usa_building_permits,
    macro_usa_business_inventories,
    macro_usa_cb_consumer_confidence,
    macro_usa_core_cpi_monthly,
    macro_usa_core_ppi,
    macro_usa_current_account,
    macro_usa_durable_goods_orders,
    macro_usa_trade_balance,
    macro_usa_spcs20,
    macro_usa_services_pmi,
    macro_usa_rig_count,
    macro_usa_retail_sales,
    macro_usa_real_consumer_spending,
    macro_usa_ppi,
    macro_usa_pmi,
    macro_usa_personal_spending,
    macro_usa_pending_home_sales,
    macro_usa_nfib_small_business,
    macro_usa_new_home_sales,
    macro_usa_nahb_house_market_index,
    macro_usa_michigan_consumer_sentiment,
    macro_usa_exist_home_sales,
    macro_usa_export_price,
    macro_usa_factory_orders,
    macro_usa_house_price_index,
    macro_usa_house_starts,
    macro_usa_import_price,
    macro_usa_industrial_production,
    macro_usa_ism_non_pmi,
    macro_usa_ism_pmi,
    macro_usa_job_cuts,
    macro_usa_cftc_nc_holding,
    macro_usa_cftc_c_holding,
    macro_usa_cftc_merchant_currency_holding,
    macro_usa_cftc_merchant_goods_holding,
    macro_usa_phs,
)

"""
全球宏观-中国宏观
"""
from PPshare.economic.macro_china import (
    macro_china_bank_financing,
    macro_china_insurance_income,
    macro_china_mobile_number,
    macro_china_vegetable_basket,
    macro_china_agricultural_product,
    macro_china_agricultural_index,
    macro_china_energy_index,
    macro_china_commodity_price_index,
    macro_global_sox_index,
    macro_china_yw_electronic_index,
    macro_china_construction_index,
    macro_china_construction_price_index,
    macro_china_lpi_index,
    macro_china_bdti_index,
    macro_china_bsi_index,
    macro_china_cpi_monthly,
    macro_china_cpi_yearly,
    macro_china_m2_yearly,
    macro_china_fx_reserves_yearly,
    macro_china_cx_pmi_yearly,
    macro_china_pmi_yearly,
    macro_china_daily_energy,
    macro_china_non_man_pmi,
    macro_china_rmb,
    macro_china_gdp_yearly,
    macro_china_shrzgm,
    macro_china_ppi_yearly,
    macro_china_cx_services_pmi_yearly,
    macro_china_market_margin_sh,
    macro_china_market_margin_sz,
    macro_china_au_report,
    macro_china_ctci_detail,
    macro_china_ctci_detail_hist,
    macro_china_ctci,
    macro_china_exports_yoy,
    macro_china_hk_market_info,
    macro_china_imports_yoy,
    macro_china_trade_balance,
    macro_china_shibor_all,
    macro_china_industrial_production_yoy,
    macro_china_gyzjz,
    macro_china_lpr,
    macro_china_new_house_price,
    macro_china_enterprise_boom_index,
    macro_china_national_tax_receipts,
    macro_china_new_financial_credit,
    macro_china_fx_gold,
    macro_china_money_supply,
    macro_china_stock_market_cap,
    macro_china_cpi,
    macro_china_gdp,
    macro_china_ppi,
    macro_china_pmi,
    macro_china_gdzctz,
    macro_china_hgjck,
    macro_china_czsr,
    macro_china_whxd,
    macro_china_wbck,
    macro_china_bond_public,
    macro_china_gksccz,
    macro_china_hb,
    macro_china_xfzxx,
    macro_china_reserve_requirement_ratio,
    macro_china_consumer_goods_retail,
    macro_china_society_electricity,
    macro_china_society_traffic_volume,
    macro_china_postal_telecommunicational,
    macro_china_international_tourism_fx,
    macro_china_passenger_load_factor,
    macro_china_freight_index,
    macro_china_central_bank_balance,
    macro_china_insurance,
    macro_china_supply_of_money,
    macro_china_swap_rate,
    macro_china_foreign_exchange_gold,
    macro_china_retail_price_index,
    macro_china_real_estate,
    macro_china_qyspjg,
    macro_china_fdi,
)
"""
英国-宏观
"""
from PPshare.economic.macro_uk import (
    macro_uk_gdp_yearly,
    macro_uk_gdp_quarterly,
    macro_uk_retail_yearly,
    macro_uk_rightmove_monthly,
    macro_uk_rightmove_yearly,
    macro_uk_unemployment_rate,
    macro_uk_halifax_monthly,
    macro_uk_bank_rate,
    macro_uk_core_cpi_monthly,
    macro_uk_core_cpi_yearly,
    macro_uk_cpi_monthly,
    macro_uk_cpi_yearly,
    macro_uk_halifax_yearly,
    macro_uk_retail_monthly,
    macro_uk_trade,
)

"""
日本-宏观
"""
from PPshare.economic.macro_japan import (
    macro_japan_bank_rate,
    macro_japan_core_cpi_yearly,
    macro_japan_cpi_yearly,
    macro_japan_head_indicator,
    macro_japan_unemployment_rate,
)

"""
瑞士-宏观
"""
from PPshare.economic.macro_swiss import (
    macro_swiss_trade,
    macro_swiss_svme,
    macro_swiss_cpi_yearly,
    macro_swiss_gbd_yearly,
    macro_swiss_gbd_bank_rate,
    macro_swiss_gdp_quarterly,
)
"""
中国-香港-宏观
"""
from PPshare.economic.macro_china_hk import (
    macro_china_hk_cpi,
    macro_china_hk_cpi_ratio,
    macro_china_hk_trade_diff_ratio,
    macro_china_hk_gbp_ratio,
    macro_china_hk_building_amount,
    macro_china_hk_building_volume,
    macro_china_hk_gbp,
    macro_china_hk_ppi,
    macro_china_hk_rate_of_unemployment,
)
"""
宏观-澳大利亚
"""
from PPshare.economic.macro_australia import (
    macro_australia_bank_rate,
    macro_australia_unemployment_rate,
    macro_australia_trade,
    macro_australia_cpi_quarterly,
    macro_australia_cpi_yearly,
    macro_australia_ppi_quarterly,
    macro_australia_retail_rate_monthly,
)
"""
宏观-加拿大
"""
from PPshare.economic.macro_canada import (
    macro_canada_cpi_monthly,
    macro_canada_core_cpi_monthly,
    macro_canada_bank_rate,
    macro_canada_core_cpi_yearly,
    macro_canada_cpi_yearly,
    macro_canada_gdp_monthly,
    macro_canada_new_house_rate,
    macro_canada_retail_rate_monthly,
    macro_canada_trade,
    macro_canada_unemployment_rate,
)
"""
中国宏观杠杆率数据
"""
from PPshare.economic.marco_cnbs import macro_cnbs
"""
德国-经济指标
"""
from PPshare.economic.macro_germany import (
    macro_germany_gdp,
    macro_germany_ifo,
    macro_germany_cpi_monthly,
    macro_germany_retail_sale_monthly,
    macro_germany_trade_adjusted,
    macro_germany_retail_sale_yearly,
    macro_germany_cpi_yearly,
    macro_germany_zew,
)
"""
金十数据中心-经济指标-欧元区
"""
from PPshare.economic.macro_euro import (
    macro_euro_gdp_yoy,
    macro_euro_cpi_mom,
    macro_euro_cpi_yoy,
    macro_euro_current_account_mom,
    macro_euro_employment_change_qoq,
    macro_euro_industrial_production_mom,
    macro_euro_manufacturing_pmi,
    macro_euro_ppi_mom,
    macro_euro_retail_sales_mom,
    macro_euro_sentix_investor_confidence,
    macro_euro_services_pmi,
    macro_euro_trade_balance,
    macro_euro_unemployment_rate_mom,
    macro_euro_zew_economic_sentiment,
    macro_euro_lme_holding,
    macro_euro_lme_stock,
)

"""
金十数据中心-经济指标-央行利率-主要央行利率
"""
from PPshare.economic.macro_bank import (
    macro_bank_australia_interest_rate,
    macro_bank_brazil_interest_rate,
    macro_bank_china_interest_rate,
    macro_bank_brazil_interest_rate,
    macro_bank_english_interest_rate,
    macro_bank_euro_interest_rate,
    macro_bank_india_interest_rate,
    macro_bank_japan_interest_rate,
    macro_bank_newzealand_interest_rate,
    macro_bank_russia_interest_rate,
    macro_bank_switzerland_interest_rate,
    macro_bank_usa_interest_rate,
)
"""
全球宏观事件
"""
from PPshare.news.news_baidu import (
    news_economic_baidu,
    news_trade_notify_suspend_baidu,
    news_report_time_baidu,
)
"""
新闻联播
"""
from PPshare.special.xwlb import news_cctv

"""
新经济
"""
from PPshare.special.xjj import (
    death_company,
    nicorn_company,
    maxima_company
)
"""
加密货币
"""
from PPshare.economic.macro_other import crypto_js_spot
"""
index-vix（恐慌指数，网站设有反爬或数据有变化，需要修改，否则报错）
"""
from PPshare.economic.macro_other import index_vix
"""
金十数据中心-外汇情绪
"""
from PPshare.economic.macro_other import macro_fx_sentiment
"""
英为财情-加密货币(无法使用）
"""
from PPshare.crypto.crypto_hist_investing import (
    crypto_hist,
    crypto_name_url_table,
)
"""
比特币持仓
"""
from PPshare.crypto.crypto_hold import crypto_bitcoin_hold_report
"""
CME 比特币成交量
"""
from PPshare.crypto.crypto_bitcoin_cme import crypto_bitcoin_cme
"""
CRIX 数据（无法使用）
"""
from PPshare.crypto.crypto_crix import crypto_crix
"""
能源-碳排放权（全国及国际无法使用）
"""
from PPshare.energy.energy_carbon import (
    energy_carbon_domestic,
    energy_carbon_bj,
    energy_carbon_eu,
    energy_carbon_gz,
    energy_carbon_hb,
    energy_carbon_sz,
)
"""
energy_oil
"""
from PPshare.energy.energy_oil_em import energy_oil_detail, energy_oil_hist
"""
空气-河北
"""
from PPshare.special.air.air_hebei import air_quality_hebei

"""
timeanddate-日出和日落
"""
from PPshare.special.air.time_and_date import sunrise_daily, sunrise_monthly
"""
air-quality
"""
from PPshare.special.air.air_zhenqi import (
    air_quality_hist,
    air_quality_rank,
    air_quality_watch_point,
    air_city_table,
)
"""
奥运奖牌
"""
from PPshare.special.sport.sport_olympic import sport_olympic_hist
"""
冬奥会历届奖牌榜
"""
from PPshare.special.sport.sport_olympic_winter import sport_olympic_winter_hist

"""
汽车销量
"""
from PPshare.special.other.other_car import car_gasgoo_sale_rank, car_cpca_energy_sale
"""
世界五百强公司排名接口
"""
from PPshare.special.fortune.fortune_500 import fortune_rank, fortune_rank_eng
"""
福布斯中国榜单（代码需要优化，访问过于频繁，容易被ban）
"""
from PPshare.special.fortune.fortune_forbes_500 import forbes_rank

"""
胡润排行榜
"""
from PPshare.special.fortune.fortune_hurun import hurun_rank

"""
新财富富豪榜
"""
from PPshare.special.fortune.fortune_xincaifu_500 import xincaifu_rank
"""
电影票房
"""
from PPshare.special.movie.movie_yien import (
    movie_boxoffice_cinema_daily,
    movie_boxoffice_cinema_weekly,
    movie_boxoffice_weekly,
    movie_boxoffice_daily,
    movie_boxoffice_monthly,
    movie_boxoffice_realtime,
    movie_boxoffice_yearly,
    movie_boxoffice_yearly_first_week,
)
"""
艺恩-视频放映
"""
from PPshare.special.movie.video_yien import video_variety_show, video_tv
"""
艺恩-艺人
"""
from PPshare.special.movie.artist_yien import (
    online_value_artist,
    business_value_artist,
)
"""
中国电竞价值排行榜
"""
from PPshare.special.other.other_game import club_rank_game, player_rank_game
"""
成本-世界各大城市生活成本
"""
from PPshare.special.cost.cost_living import cost_living
"""
微博舆情报告
"""
from PPshare.special.stock_weibo_nlp import (
    stock_js_weibo_nlp_time,
    stock_js_weibo_report,
)
"""
彭博亿万富豪指数（实时数据代码需要优化，访问频率过高，容易被ban）
"""
from PPshare.special.fortune.fortune_bloomberg import (
    index_bloomberg_billionaires,
    index_bloomberg_billionaires_hist,
)
"""
指数行情数据
"""
from PPshare.index.index_zh_em import (
    index_zh_a_hist,
    index_zh_a_hist_min_em,
    index_code_id_map_em,
)
"""
财新指数
"""
from PPshare.index.index_cx import (
    index_pmi_com_cx,
    index_pmi_man_cx,
    index_pmi_ser_cx,
    index_dei_cx,
    index_ii_cx,
    index_si_cx,
    index_fi_cx,
    index_bi_cx,
    index_ci_cx,
    index_awpr_cx,
    index_cci_cx,
    index_li_cx,
    index_neaw_cx,
    index_nei_cx,
    index_ti_cx,
)
"""
中国食糖指数
"""
from PPshare.index.index_sugar import (
    index_sugar_msweet,
    index_inner_quote_sugar_msweet,
    index_outer_quote_sugar_msweet,
)
"""
指数估值（网站数据发生变化，需要修改代码）
"""
from PPshare.index.zh_stock_index_csindex import (
    index_value_hist_funddb,
    index_value_name_funddb,
)
"""
中国公路物流运价、运量指数
"""
from PPshare.index.index_cflp import index_cflp_price, index_cflp_volume
"""
浙江省排污权交易指数
"""
from PPshare.index.index_eri import index_eri
"""
Drewry 集装箱指数
"""
from PPshare.index.drewry_index import drewry_wci_index

"""
柯桥指数
"""
from PPshare.index.index_kq_fz import index_kq_fz
from PPshare.index.index_kq_ss import index_kq_fashion
"""
国证指数
"""
from PPshare.index.index_cni import (
    index_hist_cni,
    index_all_cni,
    index_detail_cni,
    index_detail_hist_cni,
    index_detail_hist_adjust_cni,
)
"""
中证指数
"""
from PPshare.index.zh_stock_index_csindex import (
    stock_zh_index_hist_csindex,
    stock_zh_index_value_csindex,
)
"""
义乌小商品指数（网站设有反爬机制，需要修改代码，否则会报错）
"""
from PPshare.index.index_yw import index_yw

"""
股票指数-股票指数-成份股
"""
from PPshare.index.index_cons import (
    index_stock_info,
    index_stock_cons,
    index_stock_hist,
    index_stock_cons_sina,
    index_stock_cons_csindex,
    index_stock_cons_weight_csindex,
    stock_a_code_to_symbol,
)
"""
大宗商品-现货价格指数
"""
from PPshare.index.index_spot import spot_goods
"""
申万行业一级
"""
from PPshare.index.index_sw import (
    sw_index_representation_spot,
    sw_index_spot,
    sw_index_second_spot,
    sw_index_cons,
    sw_index_daily,
    sw_index_daily_indicator,
    sw_index_third_cons,
    sw_index_third_info,
)

"""
谷歌指数（网站有反爬或者网站需要翻墙访问，总之代码会报错）
"""
from PPshare.index.index_google import google_index

"""
百度指数（可以考虑优化，cookies应该可以用session方法获取）
"""
from PPshare.index.index_baidu import (
    baidu_search_index,
    baidu_info_index,
    baidu_media_index,
)

"""
微博指数
"""
from PPshare.index.index_weibo import weibo_index
"""
新浪-指数实时行情和历史行情
"""
from PPshare.index.zh_stock_index_sina import (
    stock_zh_index_daily,
    stock_zh_index_spot,
    stock_zh_index_daily_tx,
    stock_zh_index_daily_em,
)
"""
英为财情-指数（网站有加入反爬机制或数据有变动，代码需要修改，否则会报错）
"""
from PPshare.index.index_investing import (
    index_investing_global,
    index_investing_global_country_name_url,
    index_investing_global_from_url,
)