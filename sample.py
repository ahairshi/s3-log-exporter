while True:
    now = dt.datetime.now()
    schedule.exec_jobs()
    job_timer = JobTimer(JobType.DAILY, timing, start=dt.datetime.now())
    sleep_seconds = int(job_timer.timedelta(now).total_seconds())

    if sleep_seconds > 3600:
        # Sleep 1 hour at a time and log every hour
        while sleep_seconds > 3600:
            logger.info(f"{sleep_seconds} seconds (~{sleep_seconds // 3600} hrs) until next job...")
            time.sleep(3600)
            sleep_seconds -= 3600
    if 600 < sleep_seconds <= 3600:
        # Sleep 10 minutes at a time and log every 10 min
        while sleep_seconds > 600:
            logger.info(f"{sleep_seconds} seconds (~{sleep_seconds // 60} min) until next job...")
            time.sleep(600)
            sleep_seconds -= 600
    if 10 < sleep_seconds <= 600:
        # Sleep the remaining seconds if it's above 10 but within 10 minutes
        logger.info(f"{sleep_seconds} seconds left until next job.")
        time.sleep(sleep_seconds)
    elif sleep_seconds <= 10:
        # Countdown logging from 5 to 0
        for sec in range(sleep_seconds, 0, -1):
            if sec <= 5:
                logger.info(f"{sec} seconds until next job...")
            time.sleep(1)