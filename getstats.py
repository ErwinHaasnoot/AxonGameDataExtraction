import csv
from datetime import date
from itertools import izip
argmin = lambda array: min(izip(array, xrange(len(array))))
players = {}
maxPlays = 0
maxPlaysId = ''
someguyStartDate = 20120718
someguyEndDate = 0
someguyMaxScore = 0
lines = 0
games = 0
maxScores = [0]*10
with open('analytics/game_data_21_06_2014.csv','rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        lines += 1
        if lines == 1:
            print ', '.join(row)
            continue
        if row[0] in ['attempt','host','complete','score','link','results link']:
            continue
        if row[0] == 'C6B25A70-C4B6-16F0-4192-E18CE42CCC84':
            if row[2] < someguyStartDate:
                someguyStartDate = row[2]
            if row[2] > someguyEndDate:
                someguyEndDate = row[2]
            if int(row[4]) > someguyMaxScore:
                someguyMaxScore = int(row[4])      

        games += 1    
        if lines % 100000 == 0:
            print 'Lines read so far: {}'.format(lines)
        pid = row[0]
        if pid in players:
            players[pid] += 1
        else:
            players[pid] = 1
            
        if players[pid] > maxPlays:
            maxPlays = players[pid]
            maxPlaysId = pid
        
        minv, argminv = argmin(maxScores)
        if int(row[4]) > minv:
            maxScores[argminv] = int(row[4])

playerAmount = len(players)

print 'DONE!!!'
print 'Amount of players: {}'.format(playerAmount)
print 'Amount of Games: {}'.format(games)
print 'Highest scoring games: {}'.format(sorted(maxScores))
print 'Highest amount of plays for one player: {} - {}'.format(maxPlaysId,maxPlays)
print 'He played from {} to {} with max score: {}'.format(someguyStartDate,someguyEndDate,someguyMaxScore)

            