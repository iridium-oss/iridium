"""
IRIDIUM federated learning subsystem.

Scope: congestion forecasting model family. FedAvg baseline; optional FedProx and
secure aggregation. Simulation and institution-lab modes only; production federation
is future work.

Do not import heavy FL runtime here; keep API and status checks lightweight.
"""

__version__ = "0.1.0"

FL_SCOPE_MODEL_FAMILIES = ["congestion_forecasting"]
FL_DEPLOYMENT_MODES = ["simulation", "institution_lab", "staging", "production_future"]
