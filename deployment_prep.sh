#!/bin/bash

# Define your package directory
PACKAGE_DIR="package"

# Check if the package directory exists
if [ -d "$PACKAGE_DIR" ]; then
    # The directory exists, so clear it
    echo "Directory exists. Cleaning up..."
    rm -rf $PACKAGE_DIR/*
else
    # The directory does not exist, so create it
    echo "Creating directory..."
    mkdir $PACKAGE_DIR
fi

# Install dependencies into the package directory
echo "Installing dependencies..."
pip install -r requirements.txt -t $PACKAGE_DIR/

# Copy all Python files (and other necessary files) to the package directory
echo "Copying application files..."
cp *.py $PACKAGE_DIR/

# Optionally, add any configuration files or other necessary resources
# echo "Copying additional resources..."
# cp -r config/ $PACKAGE_DIR/config/

# Navigate to the package directory and zip all contents
echo "Creating ZIP file..."
cd $PACKAGE_DIR
zip -r ../deployment_package.zip .
cd ..

# Optionally, remove the package directory after zipping if you want to clean up
# echo "Cleaning up..."
# rm -rf $PACKAGE_DIR

echo "Deployment package created successfully."
