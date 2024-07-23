from aiogram.fsm.state import StatesGroup, State


class Simulation(StatesGroup):
    metrics = State()
    current_metric = State()
    token_name = State()
    message_to_delete_id = State()
