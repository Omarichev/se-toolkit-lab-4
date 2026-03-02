"""Unit tests for edge cases and boundary values."""

from app.models.interaction import InteractionLog
from app.models.item import ItemCreate, ItemUpdate
from app.models.learner import LearnerCreate
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_with_item_id_zero_returns_only_matching() -> None:
    """Test that filtering with item_id=0 (not None) correctly filters items."""
    interactions = [
        _make_log(1, 1, 0),
        _make_log(2, 2, 1),
        _make_log(3, 3, 0),
    ]
    result = _filter_by_item_id(interactions, 0)
    assert len(result) == 2
    assert all(i.item_id == 0 for i in result)


def test_filter_with_large_item_id() -> None:
    """Test filtering with a very large item_id value (boundary test)."""
    large_id = 2**31 - 1  # Max 32-bit signed integer
    interactions = [
        _make_log(1, 1, large_id),
        _make_log(2, 2, 1),
    ]
    result = _filter_by_item_id(interactions, large_id)
    assert len(result) == 1
    assert result[0].id == 1


def test_item_create_with_empty_title() -> None:
    """Test that ItemCreate accepts empty string title (boundary value)."""
    item = ItemCreate(type="step", parent_id=None, title="", description="desc")
    assert item.title == ""
    assert item.type == "step"


def test_learner_create_with_empty_name() -> None:
    """Test that LearnerCreate accepts empty string name (boundary value)."""
    learner = LearnerCreate(name="", email="test@example.com")
    assert learner.name == ""
    assert learner.email == "test@example.com"


def test_interaction_log_with_zero_ids() -> None:
    """Test InteractionLog with zero values for IDs (boundary case)."""
    log = InteractionLog(id=0, learner_id=0, item_id=0, kind="view")
    assert log.id == 0
    assert log.learner_id == 0
    assert log.item_id == 0
