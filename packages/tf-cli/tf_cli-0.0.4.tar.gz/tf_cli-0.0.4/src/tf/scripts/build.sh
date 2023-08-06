#!/bin/bash

echo "Initializing the directory..."
terraform init

echo "Formating the configuration..."
terraform fmt

echo "Validating the configuration..."
terraform validate
