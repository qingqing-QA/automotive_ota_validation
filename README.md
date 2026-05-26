# Automotive OTA System Validation & API Testing Framework

This project simulates an automotive OTA (Over-the-Air) software update workflow and validates the system through automated API and system-level tests.

## Project Overview

The goal of this project is to validate a simulated vehicle software update process, including:

- Checking current vehicle software version
- Checking latest OTA package version
- Downloading OTA update package
- Validating checksum, battery level, and network condition
- Installing software update
- Simulating ECU reboot
- Verifying final update status
- Handling failure scenarios
- Validating rollback behavior

## OTA Validation Workflow

```text
ECU Simulator
    ↓
Request OTA Update
    ↓
Download Package
    ↓
Validate Checksum / Battery / Network Condition
    ↓
Install Update
    ↓
Reboot ECU
    ↓
Verify Final Status
    ↓
Success or Rollback
```

## Tech Stack

- Python
- Flask
- PyTest
- Requests
- pytest-html
- GitHub Actions

## Project Structure

```text
automotive_ota_validation/
│
├── app/
│   ├── __init__.py
│   ├── server.py
│   ├── ota_state_machine.py
│   └── ota_validator.py
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_ota_state_machine.py
│   └── test_ota_failure_scenarios.py
│
├── reports/
│   └── ota_test_report.html
│
├── .github/
│   └── workflows/
│       └── python-tests.yml
│
├── pytest.ini
├── requirements.txt
└── README.md
```

## Test Coverage

This project includes automated tests for:

- Vehicle version API validation
- Latest OTA version API validation
- Successful OTA update workflow
- OTA state transition validation
- Invalid OTA state transition rejection
- Checksum mismatch failure scenario
- Network interruption failure scenario
- Low battery failure scenario
- Download failure scenario
- Installation failure scenario
- Install without download
- Invalid vehicle ID
- Rollback validation
- System status validation

## Failure Scenarios Covered

- Checksum mismatch
- Network interruption
- Low battery level
- Invalid OTA state transition
- Failed download
- Failed installation
- Rollback after failure

## What This Project Demonstrates

This project demonstrates system-level validation for an automotive OTA update workflow.  
It focuses not only on happy-path API testing, but also on failure handling, rollback behavior, and reliability validation.

The OTA workflow is modeled using a state-machine approach, which helps validate whether each software update step follows the correct sequence.  
PyTest is used to automate validation scenarios, and GitHub Actions is used to run tests automatically in a CI/CD pipeline.

## How to Run the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Flask API server:

```bash
python app/server.py
```

In another terminal, run tests:

```bash
python -m pytest
```

Run tests with HTML report:

```bash
python -m pytest --html=reports/ota_test_report.html --self-contained-html
```

## CI/CD

This project uses GitHub Actions to automatically run PyTest test cases whenever code is pushed to the repository.

The CI pipeline validates:

- Python environment setup
- Dependency installation
- API and system-level test execution
- Automated test report generation

## Interview Talking Point

I built this project to simulate an automotive OTA software update validation workflow.  
The system validates each step of the OTA process, including version checking, package download, checksum validation, installation, reboot, final status verification, and rollback handling.

I also added failure scenarios such as checksum mismatch, network interruption, low battery level, and invalid state transitions.  
This helped me practice system-level validation, negative testing, and reliability-focused testing, which are important in automotive software testing.
