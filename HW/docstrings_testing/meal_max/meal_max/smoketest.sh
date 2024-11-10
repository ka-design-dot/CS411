#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done


###############################################
#
# Healthchecks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to check the database connection
check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"database_status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}


##########################################################
#
# Meals
#
##########################################################

# clear_catalog() {
#   echo "Clearing the playlist..."
#   curl -s -X DELETE "$BASE_URL/clear-catalog" | grep -q '"status": "success"'
# }

create_meal() {
  meal = $1
  cuisine = $2
  price = $3
  difficulty = $4

  echo "Adding meal ($meal - $cuisine, $price) to the battle..."
  curl -s -X POST "$BASE_URL/create-meal" -H "Content-Type: application/json" \
    -d "{\"meal\":\"$meal\", \"cuisine\":\"$cuisine\", \"price\":$price, \"difficulty\":\"$difficulty\"}" | grep -q '"status": "combatant added"'

  if [ $? -eq 0 ]; then
    echo "Meal added successfully."
  else
    echo "Failed to add meal."
    exit 1
  fi
}

#***SHOULD WE ADD DELETE/ CLEAR ALL???****
clear_meals() {
  echo "Clearing meals..."
  response=$(curl -s -X POST "$BASE_URL/clear-playlist")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meals cleared successfully."
  else
    echo "Failed to clear meals."
    exit 1
  fi
}

delete_meal_by_id() {
  meal_id=$1

  echo "Deleting meal by ID ($meal_id)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-meal/$meal_id")
  if echo "$response" | grep -q '"status": "meal deleted"'; then
    echo "Meal deleted successfully by ID ($meal_id)."
  else
    echo "Failed to delete meal by ID ($meal_id)."
    exit 1
  fi
}
#***NOT SURE WE NEED THIS ONE BASED ON THE APP!***

# get_all_songs() {
#   echo "Getting all songs in the playlist..."
#   response=$(curl -s -X GET "$BASE_URL/get-all-songs-from-catalog")
#   if echo "$response" | grep -q '"status": "success"'; then
#     echo "All songs retrieved successfully."
#     if [ "$ECHO_JSON" = true ]; then
#       echo "Songs JSON:"
#       echo "$response" | jq .
#     fi
#   else
#     echo "Failed to get songs."
#     exit 1
#   fi
# }

get_meal_by_id() {
  meal_id=$1

  echo "Getting meal by ID ($meal_id)..."
  response=$(curl -s -X GET "$BASE_URL/get-meal-by-id/$meal_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal retrieved successfully by ID ($meal_id)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal JSON (ID $meal_id):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meal by ID ($meal_id)."
    exit 1
  fi
}

get_meal_by_name() {
  meal_name=$1

  echo "Getting meal by name ($meal_name)..."
  response=$(curl -s -X GET "$BASE_URL/get-meal-by-name/$meal_name")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal retrieved successfully by name ($meal_name)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal JSON (Name $meal_name):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meal by name ($meal_name)."
    exit 1
  fi
}

# get_song_by_compound_key() {
#   artist=$1
#   title=$2
#   year=$3

#   echo "Getting song by compound key (Artist: '$artist', Title: '$title', Year: $year)..."
#   response=$(curl -s -X GET "$BASE_URL/get-song-from-catalog-by-compound-key?artist=$(echo $artist | sed 's/ /%20/g')&title=$(echo $title | sed 's/ /%20/g')&year=$year")
#   if echo "$response" | grep -q '"status": "success"'; then
#     echo "Song retrieved successfully by compound key."
#     if [ "$ECHO_JSON" = true ]; then
#       echo "Song JSON (by compound key):"
#       echo "$response" | jq .
#     fi
#   else
#     echo "Failed to get song by compound key."
#     exit 1
#   fi
# }

# get_random_song() {
#   echo "Getting a random song from the catalog..."
#   response=$(curl -s -X GET "$BASE_URL/get-random-song")
#   if echo "$response" | grep -q '"status": "success"'; then
#     echo "Random song retrieved successfully."
#     if [ "$ECHO_JSON" = true ]; then
#       echo "Random Song JSON:"
#       echo "$response" | jq .
#     fi
#   else
#     echo "Failed to get a random song."
#     exit 1
#   fi
# }


############################################################
#
# Battle
#
############################################################

#*** Not sure if this is correct for battle. ***
battle() {
  
  echo "Two meals enter, one meal leaves!"
  response=$(curl -s -X POST "$BASE_URL/battle") 

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Battle initiated successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Battle JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Battle Error."
    exit 1
  fi
}

clear_combatants() {
  echo "Clearing all combatants..."
  response=$(curl -s -X POST "$BASE_URL/clear-combatants")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Combatants cleared."
  else
    echo "Failed to clear combatants."
    exit 1
  fi
}

get_combatant() {
  echo "Getting combatants..."
  response=$(curl -s -X GET "$BASE_URL/get-combatants")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Combatants retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Combatants JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get combatants."
    exit 1
  fi
}

prep_combatants() {
  meal_name = $1
  echo "Preparing combatants..."
  response=$(curl -s -X POST "$BASE_URL/prep-combatant")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Combatants prepped successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Combatants JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to prepare combatant."
    exit 1
  fi

}


######################################################
#
# Leaderboard
#
######################################################

# Function to get the song leaderboard sorted by play count
get_leaderboard() {
  echo "Getting meal leaderboard sorted by wins, battles, or win percentages"
  response=$(curl -s -X GET "$BASE_URL/leaderboard?sort=win")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Leaderboard retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Leaderboard JSON (sorted by wins):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get leaderboard."
    exit 1
  fi
}
