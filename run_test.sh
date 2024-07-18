#!/bin/bash
#qdtrack_ training.xml
mkdir -p results

# export ROUTES=${LEADERBOARD_ROOT}/data/routes_controlling.xml
export ROUTES=/workspace/team_code/routes/route_1_avddiem.xml
export REPETITIONS=1
export DEBUG_CHALLENGE=1
export TEAM_AGENT=/workspace/team_code/agent/basic_autonomous_agent.py
export TEAM_CONFIG=/workspace/team_code/agent/config_agent_basic.json
export CHECKPOINT_ENDPOINT=${LEADERBOARD_ROOT}/results.json
export CHALLENGE_TRACK_CODENAME=SENSORS
export CARLA_PORT=6015
export CARLA_TRAFFIC_MANAGER_PORT=8815

# Extract the filename from the ROUTES variable
filename=$(basename "${ROUTES}")
# Remove the .xml extension
dirname=${filename%.xml}
# Create the directory if it doesn't exist
mkdir -p "/workspace/team_code/results/${dirname}"

CURRENT_TIME=$(date +"%Y-%m-%d_%H-%M-%S")
mkdir -p "/workspace/team_code/results/${dirname}/${CURRENT_TIME}"
export RESULT_PATH="/workspace/team_code/results/${dirname}/${CURRENT_TIME}"

export CHECKPOINT_ENDPOINT=/${RESULT_PATH}/result.json
export DEBUG_CHECKPOINT_ENDPOINT=/${RESULTS_PATH}/result.txt
export RESUME=0
export TIMEOUT=60
# 193.205.163.183
# 193.205.163.17

python3 ${LEADERBOARD_ROOT}/leaderboard/leaderboard_evaluator.py \
--routes=${ROUTES} \
--routes-subset=${ROUTES_SUBSET} \
--repetitions=${REPETITIONS} \
--track=${CHALLENGE_TRACK_CODENAME} \
--checkpoint=${CHECKPOINT_ENDPOINT} \
--debug-checkpoint=${DEBUG_CHECKPOINT_ENDPOINT} \
--agent=${TEAM_AGENT} \
--agent-config=${TEAM_CONFIG} \
--debug=${DEBUG_CHALLENGE} \
--record=${RECORD_PATH} \
--resume=${RESUME} \
--host=${CARLA_HOST} \
--port=${CARLA_PORT} \
--timeout=${TIMEOUT} \
--traffic-manager-port=${CARLA_TRAFFIC_MANAGER_PORT} 
