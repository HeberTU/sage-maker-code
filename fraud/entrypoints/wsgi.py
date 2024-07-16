"""Wrapper for gunicorn to find your app."""
import fraud.services.sm_prediction_service as myapp

app = myapp.app
