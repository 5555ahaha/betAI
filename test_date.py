import pickle
outfile = open('bundesliga/data/last_date.pkl','wb')
pickle.dump({'date': '27/01/2019'}, outfile)
outfile.close()
