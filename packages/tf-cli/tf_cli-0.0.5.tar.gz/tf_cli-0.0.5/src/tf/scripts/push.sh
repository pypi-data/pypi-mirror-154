#!/bin/bash

echo "Creating infrastructure..."
terraform apply

echo "Inspecting state..."
terraform show
