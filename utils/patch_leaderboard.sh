#!/bin/bash
# If file doesn't exist, create it
if [ ! -f ${LEADERBOARD_ROOT}/leaderboard/leaderboard_evaluator.py.old ]; then
    cp ${LEADERBOARD_ROOT}/leaderboard/leaderboard_evaluator.py ${LEADERBOARD_ROOT}/leaderboard/leaderboard_evaluator.py.old
fi
cp -f ${LEADERBOARD_ROOT}/leaderboard/leaderboard_evaluator.py.old ${LEADERBOARD_ROOT}/leaderboard/leaderboard_evaluator.py
patch -f ${LEADERBOARD_ROOT}/leaderboard/leaderboard_evaluator.py /workspace/team_code/utils/leaderboard_evaluator.py.patch