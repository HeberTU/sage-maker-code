"""This is the file that implements a flask server to do inferences."""
from __future__ import print_function

import flask
import pandas as pd
from numpy.typing import NDArray

from fraud import utils
from fraud.config import settings
from fraud.entrypoints.assets import Assets

logger = utils.get_logger()


class ScoringService(object):
    """This class implements a flask server to do inferences."""

    model = None

    @classmethod
    def get_model(cls):
        """Get the model object for this instance."""
        if cls.model is None:
            cls.model = Assets(settings.ENV)()
        return cls.model

    @classmethod
    def predict(cls, input: pd.DataFrame) -> NDArray:
        """For the input, do the predictions and return them.

        Args:
            input: The data on which to do the predictions.

        Returns:
            NDArray: predictions.
        """
        clf = cls.get_model()
        results = clf.predict(data=input)
        return results.predictions


# The flask app for serving predictions
app = flask.Flask(__name__)


@app.route("/ping", methods=["GET"])
def ping():
    """Determine if the container is working and healthy.

    In this sample container, we declare it healthy if we can load the model
    successfully.
    """
    health = ScoringService.get_model() is not None
    status = 200 if health else 404
    return flask.Response(
        response="\n", status=status, mimetype="application/json"
    )


@app.route("/invocations", methods=["POST"])
def transformation():
    """Do an inference on a single batch of data."""
    logger.info(f"Request content type {flask.request.content_type}")
    prediction_request = flask.request.get_json()
    data = pd.DataFrame(data=[prediction_request], index=[0])
    data.tx_datetime = pd.to_datetime(data.tx_datetime, unit="ms")
    # Do the prediction
    predictions = ScoringService.predict(data)
    predictions_list = predictions.tolist()
    # Create a JSON response and set the status code
    response = flask.jsonify(predictions_list)
    response.status_code = 200
    return response
