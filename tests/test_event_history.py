from datetime import date, datetime, timezone

from src.history import EventHistoryIndex
from src.models import ContentItem, SourceType


def _item(item_id, *, update=False):
    return ContentItem(
        id=item_id,
        source_type=SourceType.RSS,
        title="Kimi launches a new reasoning model",
        url=f"https://example.com/{item_id}",
        published_at=datetime(2026, 7, 23, tzinfo=timezone.utc),
        ai_summary="Kimi 发布推理模型。",
        metadata={
            "event_key": "kimi-reasoning-model-launch",
            "has_substantive_update": update,
        },
    )


def test_history_dedup_excludes_same_event_within_seven_days(tmp_path):
    history = EventHistoryIndex(tmp_path / "event_index.json")
    history.update([_item("first")], today=date(2026, 7, 20))
    history.save()

    loaded = EventHistoryIndex(history.path).load()
    result = loaded.filter_recent([_item("repeat")], today=date(2026, 7, 23), days=7)

    assert result.items == []
    assert result.excluded == 1


def test_history_dedup_allows_substantive_new_progress(tmp_path):
    history = EventHistoryIndex(tmp_path / "event_index.json")
    history.update([_item("first")], today=date(2026, 7, 20))

    result = history.filter_recent([_item("updated", update=True)], today=date(2026, 7, 23), days=7)

    assert [item.id for item in result.items] == ["updated"]
    assert result.allowed_updates == 1
