from apscheduler.schedulers.background import BackgroundScheduler

from app.collectors.gold_price_collector import GoldPriceCollector
from app.services.gold_alert_checker import GoldAlertChecker


scheduler = BackgroundScheduler()

collector = GoldPriceCollector()
alert_checker = GoldAlertChecker()


def collect_gold_price():

    try:

        result = collector.collect()

        print(
            "Gold price collected:",
            result
        )

    except Exception as error:

        print(
            "Gold price collection failed:",
            error
        )


def check_gold_alerts():

    try:

        result = alert_checker.check_alerts()

        print(
            "Gold alerts checked:",
            result
        )

    except Exception as error:

        print(
            "Gold alert checking failed:",
            error
        )


def start_scheduler():

    scheduler.add_job(
        collect_gold_price,
        "interval",
        minutes=15,
        id="gold_price_collection",
        replace_existing=True
    )

    scheduler.add_job(
        check_gold_alerts,
        "interval",
        minutes=15,
        id="gold_alert_checking",
        replace_existing=True
    )

    scheduler.start()

    print(
        "Gold price scheduler started."
    )

    print(
        "Gold alert checker started."
    )
