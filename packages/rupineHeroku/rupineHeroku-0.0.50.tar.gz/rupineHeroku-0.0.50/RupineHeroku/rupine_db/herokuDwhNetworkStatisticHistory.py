from psycopg2 import sql
from ..DataStructures.ObjEvmToken import ObjEvmToken
from ..rupine_db import herokuDbAccess

class ObjDmhNetworkStatisticHistory:
    gecko_id = ''
    gecko_market_cap_rank = 0
    gecko_market_cap = 0
    gecko_current_price = 0
    gecko_total_volume = 0
    twitter_follower = 0
    twitter_hashtag_count = 0
    github_total_commits = 0
    github_contributer_gte_100 = 0
    github_contributer_lt_100_gte_10 = 0
    github_contributer_lt_10 = 0
    github_contributer_monthly_gte_100 = 0
    github_contributer_monthly_lt_100 = 0
    defilama_tvl = 0
    created_at = 0 
    modified_at= 0

def ParseDataIntoObj(data):
    retObj = ObjDmhNetworkStatisticHistory()
    retObj.gecko_id = data[0]
    retObj.gecko_market_cap_rank = data[1]
    retObj.gecko_market_cap = data[2]
    retObj.gecko_current_price = data[3]
    retObj.gecko_total_volume = data[4]
    retObj.twitter_follower = data[5]
    retObj.twitter_hashtag_count = data[6]
    retObj.github_total_commits = data[7]
    retObj.github_contributer_gte_100 = data[8]
    retObj.github_contributer_lt_100_gte_10 = data[9]
    retObj.github_contributer_lt_10 = data[10]
    retObj.github_contributer_monthly_gte_100 = data[10]
    retObj.github_contributer_monthly_lt_100 = data[11]
    retObj.defilama_tvl = data[12]
    retObj.created_at = data[13]
    retObj.modified_at= data[14]
    return retObj

def postHistoryEntry(connection, schema:str, entry:ObjDmhNetworkStatisticHistory):

    query = sql.SQL("INSERT INTO {}.dwh_network_statistics_history (gecko_id, gecko_market_cap_rank, gecko_market_cap, gecko_current_price, gecko_total_volume, twitter_follower, twitter_hashtag_count, github_total_commits, github_contributer_gte_100, github_contributer_lt_100_gte_10, github_contributer_lt_10, github_contributer_monthly_gte_100, github_contributer_monthly_lt_100, defilama_tvl) \
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)").format(sql.Identifier(schema))
    params = (
        entry.gecko_id,
        entry.gecko_market_cap_rank,
        entry.gecko_market_cap,
        entry.gecko_current_price,
        entry.gecko_total_volume,
        entry.twitter_follower,
        entry.twitter_hashtag_count,
        entry.github_total_commits,
        entry.github_contributer_gte_100,
        entry.github_contributer_lt_100_gte_10,
        entry.github_contributer_lt_10,
        entry.github_contributer_monthly_gte_100,
        entry.github_contributer_monthly_lt_100,
        entry.defilama_tvl)
    result = herokuDbAccess.insertDataIntoDatabase(query, params, connection)    
    return result

def getNetworkHistory(connection, schema, gecko_id):
    
    # query database    
    query = sql.SQL("SELECT gecko_id, gecko_market_cap_rank, gecko_market_cap, gecko_current_price, gecko_total_volume, twitter_follower, twitter_hashtag_count, github_total_commits, github_contributer_gte_100, github_contributer_lt_100_gte_10, github_contributer_lt_10, github_contributer_monthly_gte_100, github_contributer_monthly_lt_100, defilama_tvl, created_at, modified_at \
        FROM {}.dwh_network_statistics WHERE gecko_id=%s").format(sql.Identifier(schema))
    result = herokuDbAccess.fetchDataInDatabase(query, [gecko_id], connection)    
    
    # parse into objects
    rows = []
    for tok in result:
        addRow = ParseDataIntoObj(tok)
        rows.append(addRow)

    # return objects
    return rows