# The container this repo ships. Replace with whatever your service needs.
FROM busybox:1.36
CMD ["sh", "-c", "while true; do echo \"$GREETING\"; sleep 60; done"]
