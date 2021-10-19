# Tests that should PASS, before a change in TodaysParkRun.py is pushed to main Git Repo
cd ~/src/running-data-experiments
python ./TodaysParkRun.py 
python ./TodaysParkRun.py -p A1618581 -d 3.16 -t 00:21:07 -C False
python ./TodaysParkRun.py -p A1618582 -d 3.16 -t 00:31:07
python ./TodaysParkRun.py -p A1618583 -d 3.16 -t 00:26:07 -C True
pylint ./TodaysParkRun.py
