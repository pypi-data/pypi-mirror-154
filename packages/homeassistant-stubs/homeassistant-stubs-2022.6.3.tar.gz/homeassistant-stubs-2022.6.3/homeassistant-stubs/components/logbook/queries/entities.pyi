import sqlalchemy
from .common import apply_events_context_hints as apply_events_context_hints, apply_states_context_hints as apply_states_context_hints, apply_states_filters as apply_states_filters, select_events_context_id_subquery as select_events_context_id_subquery, select_events_context_only as select_events_context_only, select_events_without_states as select_events_without_states, select_states as select_states, select_states_context_only as select_states_context_only
from collections.abc import Iterable
from datetime import datetime as dt
from homeassistant.components.recorder.models import ENTITY_ID_IN_EVENT as ENTITY_ID_IN_EVENT, ENTITY_ID_LAST_UPDATED_INDEX as ENTITY_ID_LAST_UPDATED_INDEX, EventData as EventData, Events as Events, OLD_ENTITY_ID_IN_EVENT as OLD_ENTITY_ID_IN_EVENT, States as States
from sqlalchemy.orm import Query as Query
from sqlalchemy.sql.lambdas import StatementLambdaElement as StatementLambdaElement
from sqlalchemy.sql.selectable import CTE as CTE, CompoundSelect as CompoundSelect

def _select_entities_context_ids_sub_query(start_day: dt, end_day: dt, event_types: tuple[str, ...], entity_ids: list[str], json_quotable_entity_ids: list[str]) -> CompoundSelect: ...
def _apply_entities_context_union(query: Query, start_day: dt, end_day: dt, event_types: tuple[str, ...], entity_ids: list[str], json_quotable_entity_ids: list[str]) -> CompoundSelect: ...
def entities_stmt(start_day: dt, end_day: dt, event_types: tuple[str, ...], entity_ids: list[str], json_quotable_entity_ids: list[str]) -> StatementLambdaElement: ...
def states_query_for_entity_ids(start_day: dt, end_day: dt, entity_ids: list[str]) -> Query: ...
def apply_event_entity_id_matchers(json_quotable_entity_ids: Iterable[str]) -> sqlalchemy.or_: ...
def apply_entities_hints(query: Query) -> Query: ...
