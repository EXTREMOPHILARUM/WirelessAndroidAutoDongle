#!/bin/bash

# Function to display usage
show_usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  base    - Build only the base system image without Python package"
    echo "  python  - Build only the Python package"
    echo "  full    - Build complete image including Python package"
    echo "  all     - Build both base and Python package in parallel"
    echo ""
    echo "Example:"
    echo "  $0 python    # Build only Python package"
    echo "  $0 all       # Build everything in parallel"
}

# Function to build base image
build_base() {
    echo "Building base system image..."
    docker-compose run rpi02w_base
}

# Function to build Python package
build_python() {
    echo "Building Python package..."
    docker-compose run rpi02w_python
}

# Function to build full image
build_full() {
    echo "Building full image..."
    docker-compose run rpi02w_full
}

# Function to build everything in parallel
build_all() {
    echo "Building base image and Python package in parallel..."
    docker-compose run rpi02w_base & 
    docker-compose run rpi02w_python &
    wait
    echo "Parallel builds completed"
}

# Main script logic
case "$1" in
    "base")
        build_base
        ;;
    "python")
        build_python
        ;;
    "full")
        build_full
        ;;
    "all")
        build_all
        ;;
    *)
        show_usage
        exit 1
        ;;
esac
