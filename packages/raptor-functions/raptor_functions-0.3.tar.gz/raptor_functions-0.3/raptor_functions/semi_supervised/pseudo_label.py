
from raptor_functions.supervised.prediction import get_production_model, make_prediction_with_pm






loaded_model, relevant_features, offset, gradient, production_model_uri = get_production_model('Covid Classifier')

# def get_labels():