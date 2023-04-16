import asyncio
import os
from typing import Dict, List, Any, Text, Set, Iterable
from rasa.core.agent import Agent
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.core.events import UserUttered
from rasa.shared.core.slots import Slot
from rasa.shared.core.domain import Domain

# Load Rasa NLU model
# Adjust the path if necessary
model_directory = os.path.join(os.getcwd(), "rasa_nlu/models")
nlu_model_path = os.path.join(
    model_directory, "nlu")

# Create Rasa Agent
agent = Agent.load(nlu_model_path)
sender_id = "default"
# set your slot values here
slots = {Slot("my_slot", {"type": "any"}): "my_value"}
max_event_history = 1000  # set a valid integer value
sender_source = None
is_rule_tracker = False


async def get_intent(text):
    sender_id = "default"
    domain = Domain.empty()
    dialogue_state_tracker = DialogueStateTracker(
        sender_id,
        slots,
        max_event_history,
        sender_source,
        is_rule_tracker
    )

    user_uttered_event = UserUttered(text)
    await dialogue_state_tracker.update(user_uttered_event, domain)

    parse_data = await agent.parse_message_using_nlu_interpreter(text, dialogue_state_tracker=dialogue_state_tracker)

    if parse_data and "intent" in parse_data and "name" in parse_data["intent"]:
        return parse_data["intent"]["name"]
    return None
