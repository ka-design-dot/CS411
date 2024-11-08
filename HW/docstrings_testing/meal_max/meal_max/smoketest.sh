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

clear_catalog() {
  echo "Clearing the playlist..."
  curl -s -X DELETE "$BASE_URL/clear-catalog" | grep -q '"status": "success"'
}

create_song() {
  artist=$1
  title=$2
  year=$3
  genre=$4
  duration=$5

  echo "Adding song ($artist - $title, $year) to the playlist..."
  curl -s -X POST "$BASE_URL/create-song" -H "Content-Type: application/json" \
    -d "{\"artist\":\"$artist\", \"title\":\"$title\", \"year\":$year, \"genre\":\"$genre\", \"duration\":$duration}" | grep -q '"status": "success"'

  if [ $? -eq 0 ]; then
    echo "Song added successfully."
  else
    echo "Failed to add song."
    exit 1
  fi
}

delete_song_by_id() {
  song_id=$1

  echo "Deleting song by ID ($song_id)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-song/$song_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Song deleted successfully by ID ($song_id)."
  else
    echo "Failed to delete song by ID ($song_id)."
    exit 1
  fi
}

get_all_songs() {
  echo "Getting all songs in the playlist..."
  response=$(curl -s -X GET "$BASE_URL/get-all-songs-from-catalog")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "All songs retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Songs JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get songs."
    exit 1
  fi
}

get_song_by_id() {
  song_id=$1

  echo "Getting song by ID ($song_id)..."
  response=$(curl -s -X GET "$BASE_URL/get-song-from-catalog-by-id/$song_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Song retrieved successfully by ID ($song_id)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Song JSON (ID $song_id):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get song by ID ($song_id)."
    exit 1
  fi
}

get_song_by_compound_key() {
  artist=$1
  title=$2
  year=$3

  echo "Getting song by compound key (Artist: '$artist', Title: '$title', Year: $year)..."
  response=$(curl -s -X GET "$BASE_URL/get-song-from-catalog-by-compound-key?artist=$(echo $artist | sed 's/ /%20/g')&title=$(echo $title | sed 's/ /%20/g')&year=$year")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Song retrieved successfully by compound key."
    if [ "$ECHO_JSON" = true ]; then
      echo "Song JSON (by compound key):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get song by compound key."
    exit 1
  fi
}

get_random_song() {
  echo "Getting a random song from the catalog..."
  response=$(curl -s -X GET "$BASE_URL/get-random-song")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Random song retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Random Song JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get a random song."
    exit 1
  fi
}


############################################################
#
# Battle
#
############################################################

add_song_to_playlist() {
  artist=$1
  title=$2
  year=$3

  echo "Adding song to playlist: $artist - $title ($year)..."
  response=$(curl -s -X POST "$BASE_URL/add-song-to-playlist" \
    -H "Content-Type: application/json" \
    -d "{\"artist\":\"$artist\", \"title\":\"$title\", \"year\":$year}")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Song added to playlist successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Song JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to add song to playlist."
    exit 1
  fi
}

remove_song_from_playlist() {
  artist=$1
  title=$2
  year=$3

  echo "Removing song from playlist: $artist - $title ($year)..."
  response=$(curl -s -X DELETE "$BASE_URL/remove-song-from-playlist" \
    -H "Content-Type: application/json" \
    -d "{\"artist\":\"$artist\", \"title\":\"$title\", \"year\":$year}")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Song removed from playlist successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Song JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to remove song from playlist."
    exit 1
  fi
}

remove_song_by_track_number() {
  track_number=$1

  echo "Removing song by track number: $track_number..."
  response=$(curl -s -X DELETE "$BASE_URL/remove-song-from-playlist-by-track-number/$track_number")

  if echo "$response" | grep -q '"status":'; then
    echo "Song removed from playlist by track number ($track_number) successfully."
  else
    echo "Failed to remove song from playlist by track number."
    exit 1
  fi
}

clear_playlist() {
  echo "Clearing playlist..."
  response=$(curl -s -X POST "$BASE_URL/clear-playlist")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Playlist cleared successfully."
  else
    echo "Failed to clear playlist."
    exit 1
  fi
}

######################################################
#
# Leaderboard
#
######################################################

# Function to get the song leaderboard sorted by play count
get_song_leaderboard() {
  echo "Getting song leaderboard sorted by play count..."
  response=$(curl -s -X GET "$BASE_URL/song-leaderboard?sort=play_count")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Song leaderboard retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Leaderboard JSON (sorted by play count):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get song leaderboard."
    exit 1
  fi
}
