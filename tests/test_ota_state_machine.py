class OTAStateMachine:
    VALID_TRANSITIONS = {
        "IDLE": ["DOWNLOADING"],
        "DOWNLOADING": ["VALIDATING", "FAILED"],
        "VALIDATING": ["INSTALLING", "FAILED"],
        "INSTALLING": ["REBOOTING", "ROLLBACK"],
        "REBOOTING": ["SUCCESS", "FAILED"],
        "FAILED": ["ROLLBACK"],
        "ROLLBACK": ["IDLE"],
        "SUCCESS": ["IDLE"]
    }

    def __init__(self):
        self.state = "IDLE"

    def transition_to(self, new_state):
        if new_state not in self.VALID_TRANSITIONS[self.state]:
            raise ValueError(f"Invalid transition from {self.state} to {new_state}")
        self.state = new_state
        return self.state
