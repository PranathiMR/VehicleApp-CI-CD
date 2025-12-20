FROM ubuntu:22.04

# Minimal runtime dependencies (generic)
RUN apt-get update && apt-get install -y \
    ca-certificates \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy prebuilt binaries (generic pattern)
COPY vehicle-app-cpp-sdk/build-seat/bin/ /app/bin/

# Expose commonly used ports (optional, generic)
EXPOSE 1883
EXPOSE 55555

# Default entrypoint (can be overridden in CI)
CMD ["bash"]
