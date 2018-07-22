from com.iplstats.IPLDataReader import getWinner, getWinnerCount, seasonGroupBy, matches

# colNames = ['id', 'season', 'city', 'date', 'team1', 'team2', 'toss_winner', 'toss_decision', 'result', 'dl_applied',
#             'winner',
#             'win_by_runs', 'win_by_wickets', 'player_of_match', 'venue', 'umpire1', 'umpire2', 'umpire3']

# matches = pd.read_csv('/Users/udaykiranss/Learning/Data/ipl/matches.csv', sep=',', encoding='UTF-8')
#
# # Group the matches by season
# seasonGroupBy = matches.groupby('season')

# Winner of each season
for season, seasonDF in seasonGroupBy:
    print("Winner of season %s is %s" %(season, getWinner(seasonGroupBy, season)))

# How many times each team won IPL
team = 'Chennai Super Kings'
print("%s won IPL %s times" %(team, getWinnerCount(seasonGroupBy, team)))


# Result of 2 teams across all seasons
teams = matches['team1'].unique()

for team in teams:
    # print(team)
    teamMatchesCond = ((matches['team1'] == team) | (matches['team2'] == team))
    totalMatches = matches[teamMatchesCond].loc[:, ['team1']].count().loc['team1']
    condition = ((matches['team1'] == team) | (matches['team2'] == team)) & (
                matches['winner'] == team)
    print()
    print("%s won %s matches out of %s matches in IPL" %(team, matches[condition].loc[:, ['winner']].count().loc['winner'], totalMatches))



