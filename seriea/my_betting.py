import sys
import json

def test_betting_stategy(home, away, predictions, match, bet_difference=0.05):
    result = {
        'spend': 0,
        'return': 0,
    }
    def case(argument):
                switcher = {
                    '1': 0,
                    'X': 1,
                    '2': 2,           
                }
                return switcher.get(argument, "Errore")
    def switch(argument):
            switcher = {
                'H': home,
                'A': away,
                'D': "Pareggio",
            }
            return switcher.get(argument, "Errore")
    sys.stdout = open('../pronostici.txt', 'a')
    raw_json = {}

    odds={}
    odds['winner']=switch(predictions[0]['classes'][0])
    tips={}
    print("-------------------------------------------------------------------------------------------------")
    print("\t"+home+" - "+away+":\t 1: %.1f %%\t X: %.1f %%\t 2: %.1f %% \n\tProbabile esito:\t %s \n" % (predictions[0]['probabilities'][0]*100, predictions[0]['probabilities'][1]*100, predictions[0]['probabilities'][2]*100, odds['winner'])) 
    for esito, quota in match.items():   
        for i in range(0, len(predictions)):
            probabilities = predictions[i]['probabilities']
            if probabilities[case(esito)] > (1 / float(quota)) + bet_difference:
                #result['spend'] = result['spend'] + 1
                tips[esito]=quota
                print("=> Esito %s sottostimato a quota %s su Bet365\n\tQuota calcolata: %.2f\n" %(esito, quota, 1.0/probabilities[case(esito)]))
                #if test_labels[i] == 'D':
                    #result['return'] = result['return'] + test_features['odds-draw'][i]
                #result['performance'] = result['return'] / result['spend']
        #return result
    odds['tips']=tips
    raw_json['home']=home
    raw_json['away']=away
    raw_json['result']=odds
    return raw_json
     
        

        