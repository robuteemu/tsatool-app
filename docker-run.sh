docker run --rm --name tsatool -p 8080:8080 \
  -v /Users/teemusalminen/Developer/tmfg/tsatool-app/analysis:/app/analysis \
  -v /Users/teemusalminen/Developer/tmfg/tsatool-app/results:/app/results \
  -v /Users/teemusalminen/Developer/tmfg/tsatool-app/tsa:/app/tsa \
  --network="tsatool-network" \
  --entrypoint '/bin/sh' \
  tsatool:latest -c 'python3 tsabatch.py -i analysis/porvootest.xlsx -n porvootest --dryvalidate && \
  python3 tsabatch.py -i analysis/porvootest.xlsx -n porvootest'
  