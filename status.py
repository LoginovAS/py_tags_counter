from enum import Enum

class JobStatus(Enum):
    QUEUED = 'queued',
    RUNNING = 'running',
    ERROR = 'error',
    DONE = 'done'
