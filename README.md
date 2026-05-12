# Automotive OTA System Validation & API Testing Framework

This project simulates an automotive OTA (Over-the-Air) software update workflow and validates the system through automated API and system-level tests.

## Project Overview

The goal of this project is to validate a simulated vehicle software update process, including:

- Checking current vehicle software version
- Checking latest OTA package version
- Downloading OTA update package
- Installing software update
- Verifying version consistency
- Handling failure scenarios
- Validating rollback behavior

## Tech Stack

- Python
- Flask
- PyTest
- Requests
- pytest-html
- GitHub Actions

## Test Coverage

This project includes automated tests for:

- Vehicle version API validation
- Latest OTA version API validation
- Successful OTA update workflow
- Download failure scenario
- Installation failure scenario
- Install without download
- Invalid vehicle ID
- Rollback after successful update
- System status validation

## How to Run the Project

Install dependencies:

```bash
pip install -r requirements.txt