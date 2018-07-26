from flask import Flask
from flask import json
from flask_httpauth import HTTPBasicAuth
from com.iplstats.IPLDataReader import getWinner, \
    seasonGroupBy, matches, getBatsmanRuns, getBowlerWickets, getMatchesInASeason, \
    getBatsmanRunsOverall, getBowlerWicketsOverall, getMatches, getAbandonedMatches, orangecap, purplecap

app = Flask(__name__)
auth = HTTPBasicAuth()

USER_DATA = {
    "admin": "Uday"
}


@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password


@app.route('/iplstats/winner/<int:season>')
@auth.login_required
def ipl_winner(season):
    return "Winner of season %s is %s" % (str(season), getWinner(seasonGroupBy, season)['winner'])


@app.route('/iplstats/team/<team>')
def team_stats(team):
    team_matches_condition = ((matches['team1'] == team) | (matches['team2'] == team))
    total_matches = matches[team_matches_condition].loc[:, ['team1']].count().loc['team1']
    condition = ((matches['team1'] == team) | (matches['team2'] == team)) & (
            matches['winner'] == team)
    return "%s won %s matches out of %s matches in IPL" \
           % (team, matches[condition].loc[:, ['winner']].count().loc['winner'], total_matches)


@app.route('/iplstats/season/<int:season>/player/<player>')
def player_stats_season(season, player):
    batsman_runs = getBatsmanRuns(player, season)
    bowler_wickets = getBowlerWickets(player, season)
    player_matches = getMatchesInASeason(player, season)
    return "%s scored %s runs and taken %s wickets in %s matches of season %s" % (player, batsman_runs,
                                                                                  bowler_wickets, player_matches,
                                                                                  season)


@app.route('/iplstats/season/<int:season>/orangecap')
def orange_cap(season):
    player, player_runs = orangecap(season)
    return "%s got orange cap in %s for scoring %s runs" % (player, season, player_runs)


@app.route('/iplstats/season/<int:season>/purplecap')
def purple_cap(season):
    player, player_wickets = purplecap(season)
    return "%s got purple cap in %s for getting %s wickets" % (player, season, player_wickets)


@app.route('/iplstats/player/<player>')
def player_stats(player):
    batsman_runs = getBatsmanRunsOverall(player)
    bowler_wickets = getBowlerWicketsOverall(player)
    player_matches = getMatches(player)
    return "%s scored %s runs and taken %s wickets in %s matches of IPL" % (player, batsman_runs,
                                                                            bowler_wickets, player_matches)


@app.route('/iplstats/abandoned')
def abandoned_matches():
    abandoned_match_list = getAbandonedMatches()

    # convert to json data
    json_str = json.dumps([e for e in abandoned_match_list])
    return json_str


if __name__ == '__main__':
    app.run(debug=1)
