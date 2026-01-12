# --- Stage 1: Builder ---
FROM ghcr.io/eclipse-velocitas/devcontainer-base-images/cpp:latest AS builder

WORKDIR /workspace

# FIX 1: Copy files and simultaneously transfer ownership to the 'vscode' user
# If you don't do this, 'vscode' cannot read/execute the scripts owned by root.
COPY --chown=vscode:vscode . .

RUN ls -R /workspace

# FIX 2: Explicitly switch to the 'vscode' user before running the build
USER vscode

# Now this command runs as 'vscode' and should succeed
RUN cd vehicle-app-cpp-sdk && ./install_dependencies.sh && ./build.sh

# --- Stage 2: Runner (Keep this as is, or similar to your previous Ubuntu attempt) ---
FROM ubuntu:22.04

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y libstdc++6 && \
    rm -rf /var/lib/apt/lists/*

# Copy the binary from the builder stage
# Note: Adjust the path '/workspace/build/bin' if your build.sh outputs somewhere else
COPY --from=builder /workspace/vehicle-app-cpp-sdk/build/bin/ /app/bin/

# Expose ports
EXPOSE 55555

# Run the app
CMD ["/app/bin/example-seatadjusterapp"]