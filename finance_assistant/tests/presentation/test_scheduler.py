import pytest
from datetime import timedelta, datetime
from src.presentation.scheduler import AssetScheduler

def test_schedule_jobs_registers_all():
    sched = AssetScheduler()
    sched.schedule_jobs()
    jobs = sched.scheduler.get_jobs()
    # идентификаторы совпадают с ключами jobs_config
    assert set(job.id for job in jobs) == set(sched.jobs_config.keys())

def test_schedule_jobs_intervals():
    sched = AssetScheduler()
    sched.schedule_jobs()
    for job in sched.scheduler.get_jobs():
        minutes = sched.jobs_config[job.id][1]
        # проверяем, что интервал секунд равен minutes*60
        assert job.trigger.interval.total_seconds() == minutes * 60

def test_start_and_exit(monkeypatch, capsys):
    # эмулируем мгновенный ввод «выход»
    monkeypatch.setattr("builtins.input", lambda prompt="": "выход")
    sched = AssetScheduler()
    sched.start()
    out = capsys.readouterr().out
    assert "Периодические задачи запущены" in out
    assert "Завершение по команде пользователя" in out or "Завершение по команде" in out
