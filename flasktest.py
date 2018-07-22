from flask import Flask
from com.iplstats.IPLDataReader import getWinner, getWinnerCount, \
    seasonGroupBy, matches, getBatsmanRuns, getBowlerWickets, getMatchesInASeason, \
    getBatsmanRunsOverall, getBowlerWicketsOverall,getMatches


app = Flask(__name__)


@app.route('/iplstats/winner/<int:season>')
def iplwinner(season):
    return "Winner of season %s is %s" %(str(season), getWinner(seasonGroupBy, season))


@app.route('/iplstats/team/<team>')
def teamstats(team):
    teamMatchesCond = ((matches['team1'] == team) | (matches['team2'] == team))
    totalMatches = matches[teamMatchesCond].loc[:, ['team1']].count().loc['team1']
    condition = ((matches['team1'] == team) | (matches['team2'] == team)) & (
            matches['winner'] == team)
    return "%s won %s matches out of %s matches in IPL" % (team, matches[condition].loc[:, ['winner']].count().loc['winner'], totalMatches)


@app.route('/iplstats/season/<int:season>/player/<player>')
def playerStatsSeason(season,player):
    batsmanRuns = getBatsmanRuns(player,season)
    bowlerWickets = getBowlerWickets(player,season)
    matches = getMatchesInASeason(player,season)
    return "%s scored %s runs and taken %s wickets in %s matches of season %s" %(player, batsmanRuns,
                                                                                 bowlerWickets, matches, season)


@app.route('/iplstats/player/<player>')
def playerStats(player):
    batsmanRuns = getBatsmanRunsOverall(player)
    bowlerWickets = getBowlerWicketsOverall(player)
    matches = getMatches(player)
    return "%s scored %s runs and taken %s wickets in %s matches of IPL" %(player, batsmanRuns,
                                                                                 bowlerWickets, matches)


if __name__ == '__main__':
   app.run(debug=1)
