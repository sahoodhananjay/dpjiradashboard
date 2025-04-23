from apscheduler.schedulers.background import BackgroundScheduler
from qualityboard import views
import sys, socket

def start():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 47200))
    except socket.error:
        print("!!!scheduler already started, DO NOTHING")
    else:
        scheduler = BackgroundScheduler()
        #jira = views()
        #scheduler.add_job(views.save_jira_data,"interval",minutes=60,id="jira_001",replace_existing=True)
        scheduler.add_job(views.get_product_health_metrics, "interval", minutes=30, id="jira_001", replace_existing=True)
        scheduler.start()