import pandas as pd
import os as os
import numpy as np
from com.iplstats.data.IPLData import Match
# colNames = ['id', 'season', 'city', 'date', 'team1', 'team2', 'toss_winner', 'toss_decision', 'result', 'dl_applied',
#             'winner',
#             'win_by_runs', 'win_by_wickets', 'player_of_match', 'venue', 'umpire1', 'umpire2', 'umpire3']
matchesCSVPath = os.path.abspath('./resources/matches.csv')
print(matchesCSVPath)
matches = pd.read_csv(matchesCSVPath, sep=',', encoding='UTF-8')

deliveries = pd.read_csv('./resources/deliveries_season.csv', sep=',', encoding='UTF-8')

print("Loading matches")

def getWinner(seasonGroupBy, season):
    return seasonGroupBy.get_group(season).tail(1).iloc[0, 1:15]


def getWinnerCount(seasongGroupBy, team):
    return seasongGroupBy.tail(1).loc[:, ['season', 'winner']].groupby('winner').count().loc[team, 'season']


def getBatsmanRunsOverall(batsman):
    return deliveries.groupby(['batsman']).get_group(batsman)['batsman_runs'].sum()


def getBatsmanRuns(batsman, season):
    return deliveriesSeasonGroup.get_group(season).groupby('batsman').get_group(batsman)['batsman_runs'].sum()


def getBowlerWickets(bowler, season):
    try:
        bowlerWickets = deliveriesSeasonGroup.get_group(season).groupby('bowler').get_group(bowler)['dismissal_kind'].count()
        return bowlerWickets
    except:
        return 0



def getBowlerWicketsOverall(bowler):
    return deliveries.groupby(['bowler']).get_group(bowler)['dismissal_kind'].count()


def getMatchesInASeason(batsman, season):
    return deliveriesSeasonGroup.get_group(season).groupby('batsman').get_group(batsman)['match_id'].unique().size


def getMatches(batsman):
    return deliveries.groupby('batsman').get_group(batsman)['match_id'].unique().size

def getAbandonedMatches():
    AbandonedMatches = matches[matches.loc[:, 'winner'].isnull()].loc[:,['id','team1','team2','venue','date']]
    matchList = []
    for index, row in AbandonedMatches.iterrows():
        match = Match(row['id'],row['date'],row['venue'],row['team1'],row['team2'])
        matchList.append(match.toJSON())

    return matchList


def orangecap(season):
    player = deliveriesSeasonGroup.get_group(season).groupby('batsman').\
        agg(np.sum).sort_values(by='batsman_runs').tail(1)['batsman_runs'].index[0]
    playerRuns = deliveriesSeasonGroup.get_group(season).groupby('batsman').\
        agg(np.sum).sort_values(by='batsman_runs').tail(1)['batsman_runs'].iloc[0]
    return  player, playerRuns


def purplecap(season):
    player = deliveriesSeasonGroup.get_group(season).groupby('bowler')['dismissal_kind']\
        .count().sort_values().tail(1).index[0]
    player_wickets = deliveriesSeasonGroup.get_group(season).groupby('bowler')['dismissal_kind']\
        .count().sort_values().tail(1).iloc[0]
    return  player, player_wickets


# Group the matches by season
seasonGroupBy = matches.groupby('season')

deliveriesSeasonGroup = deliveries.groupby(['season'])
# batsman2017 = deliveries.groupby(['season']).get_group(2017).groupby('batsman')
# bowler2017 = deliveries.groupby(['season']).get_group(2017).groupby('bowler')
#
# batsmanRuns = batsman2017.get_group('V Kohli')['batsman_runs'].sum()
# overallRuns = deliveries.groupby('batsman').get_group('V Kohli')['batsman_runs'].sum()
# batsmanMatches = batsman2017.get_group('V Kohli')['match_id'].unique().size
# bowlerWickets = bowler2017.get_group('YS Chahal')['dismissal_kind'].count()
# overallwickets = deliveries.groupby('bowler').get_group('YS  Chahal')['dismissal_kind'].count()
# totalMatches = deliveries.groupby('batsman').get_group('V Kohli')['match_id'].unique().size

# # Winner of each season
# for season, seasonDF in seasonGroupBy:
#     print("Winner of season %s is %s" %(season, getWinner(seasonGroupBy, season)))
#
# # How many times each team won IPL
# team = 'Chennai Super Kings'
# print("%s won IPL %s times" %(team, getWinnerCount(seasonGroupBy, team)))
#
#
# # Result of 2 teams across all seasons
# teams = matches['team1'].unique()
#
# for team in teams:
#     # print(team)
#     teamMatchesCond = ((matches['team1'] == team) | (matches['team2'] == team))
#     totalMatches = matches[teamMatchesCond].loc[:, ['team1']].count().loc['team1']
#     condition = ((matches['team1'] == team) | (matches['team2'] == team)) & (
#                 matches['winner'] == team)
#     print()
#     print("%s won %s matches out of %s matches in IPL" %(team, matches[condition].loc[:, ['winner']].count().loc['winner'], totalMatches))

# seasonList = []
# deliveriesId = deliveries['match_id']
# matchesId = matches[['id','season']]
# counter = 0
# for matchId in deliveriesId:
#     counter +=1
#     seasonList.append(matchesId.loc[matchesId['id'] == matchId, 'season'].iloc[0])
#     if counter % 10000 == 0:
#         print(counter)
#
# print(seasonList)
# deliveries['season'] = seasonList
# deliveries.to_csv('deliveries_season.csv')





