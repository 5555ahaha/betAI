import dataset
import my_betting
import tensorflow as tf
import numpy as np
import csv
import datetime
import sys
import bet365
import os
import json


TRAINING_SET_FRACTION = 0.95

def main(argv):
    print("Caricamento delle prossime 10 partite Liga Spagnola...")
    os.system("rm quote.json")
    os.system("scrapy runspider bet365.py -o quote.json > /dev/null 2>&1")
    data = dataset.Dataset('data/liga.csv')
    #os.system("clear")
    with open('quote.json') as f:
        for match in json.load(f):
            train_results_len = int(TRAINING_SET_FRACTION * len(data.processed_results))
            def refresh_key(place, stat):
                result ={}
                for key, value in stat.items():
                    result[place+'-'+key]= np.array([value]);
                return result
            try:   
                test_features = dict(refresh_key("home",data.get_statistics(match["home"], datetime.datetime.now())).items() + refresh_key("away",data.get_statistics(match["away"], datetime.datetime.now())).items())
            except AttributeError:
                print("Statistiche non disponibili "+match["home"]+" "+ match["away"])
                continue
            def map_results(results):
                features = {}

                for result in results:
                    for key in result.keys():
                        if key not in features:
                            features[key] = []

                        features[key].append(result[key])

                for key in features.keys():
                    features[key] = np.array(features[key])

                return features, features['result']
           
            test_input_fn = tf.estimator.inputs.numpy_input_fn(
                x=test_features,
                num_epochs=1,
                shuffle=False
            )

            feature_columns = []

            for mode in ['home', 'away']:
                feature_columns = feature_columns + [
                    tf.feature_column.numeric_column(key='{}-wins'.format(mode)),
                    tf.feature_column.numeric_column(key='{}-draws'.format(mode)),
                    tf.feature_column.numeric_column(key='{}-losses'.format(mode)),
                    tf.feature_column.numeric_column(key='{}-goals'.format(mode)),
                    tf.feature_column.numeric_column(key='{}-opposition-goals'.format(mode)),
                    tf.feature_column.numeric_column(key='{}-shots'.format(mode)),
                    tf.feature_column.numeric_column(key='{}-shots-on-target'.format(mode)),
                    tf.feature_column.numeric_column(key='{}-opposition-shots'.format(mode)),
                    tf.feature_column.numeric_column(key='{}-opposition-shots-on-target'.format(mode)),
                ]
            model = tf.estimator.DNNClassifier(
                model_dir='model/',
                hidden_units=[10],
                feature_columns=feature_columns,
                n_classes=3,
                label_vocabulary=['H', 'D', 'A'],
                optimizer=tf.train.ProximalAdagradOptimizer(
                    learning_rate=0.1,
                    l1_regularization_strength=0.001
                ))
           
            predictions = list(model.predict(input_fn=test_input_fn))

            home= match['home']
            del match['home']
            away = match['away']
            del match['away']
            with open('liga_bet.json', 'a') as outfile:
                json.dump(my_betting.test_betting_stategy(home, away, predictions, match), outfile)

if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    tf.logging.set_verbosity(tf.logging.ERROR)
    tf.app.run(main=main)
