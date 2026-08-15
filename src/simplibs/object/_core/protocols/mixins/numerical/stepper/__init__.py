from .StepperProtocol import StepperProtocol

_DESIGN_NOTES = """
# Stepper Protocol Sub-Package

## Purpose
Defines the protocol for encapsulated numerical stepping, limit checking, and threshold actions.

## Internal Components Registry

| Component         | Type     | Description                                                                  |
| :---------------- | :------- | :--------------------------------------------------------------------------- |
| `StepperProtocol` | Protocol | Interface for stepping controller managing bounds and increment/decrement.   |
"""