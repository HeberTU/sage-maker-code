"""Domain library."""
from fraud.domain.data_simulator import (
    add_frauds,
    generate_customer_profiles_list,
    generate_terminal_profiles_list,
    generate_transaction,
    generate_transaction_table,
    get_available_terminals_for_customer,
    simulate_credit_card_transactions_data,
)
from fraud.domain.kpis import card_precision_top_k
from fraud.domain.models import (
    CustomerProfile,
    TerminalProfiles,
    Transaction,
)

__all__ = [
    "add_frauds",
    "CustomerProfile",
    "generate_customer_profiles_list",
    "generate_terminal_profiles_list",
    "generate_transaction",
    "generate_transaction_table",
    "get_available_terminals_for_customer",
    "simulate_credit_card_transactions_data",
    "TerminalProfiles",
    "Transaction",
    "card_precision_top_k",
]
