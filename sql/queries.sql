-- Routes with the most scheduled trips
SELECT route_id, COUNT(*) AS trip_count
FROM trips
GROUP BY route_id
ORDER BY trip_count DESC;

-- Stops with the most scheduled stop-time records
SELECT stop_id, COUNT(*) AS stop_time_count
FROM stop_times
GROUP BY stop_id
ORDER BY stop_time_count DESC;
