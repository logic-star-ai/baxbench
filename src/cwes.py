from enum import Enum


class CWE(Enum):
    """
    CWE nums and official MITRE descriptions.
    """

    XSS = {
        "num": 79,
        "desc": "The product does not neutralize or incorrectly neutralizes user-controllable input before it is placed in output that is used as a web page that is served to other users.",
    }
    PATH_TRAVERSAL = {
        "num": 22,
        "desc": "The product uses external input to construct a pathname that is intended to identify a file or directory that is located underneath a restricted parent directory, but the product does not properly neutralize special elements within the pathname that can cause the pathname to resolve to a location that is outside of the restricted directory.",
    }
    CODE_INJECTION = {
        "num": 94,
        "desc": "The product constructs all or part of a code segment using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the syntax or behavior of the intended code segment.",
    }
    SQL_INJECTION = {
        "num": 89,
        "desc": "The product constructs all or part of an SQL command using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the intended SQL command when it is sent to a downstream component. Without sufficient removal or quoting of SQL syntax in user-controllable inputs, the generated SQL query can cause those inputs to be interpreted as SQL instead of ordinary user data.",
    }
    IMPROPER_ACCESS_CONTROL = {
        "num": 284,
        "desc": "The product does not restrict or incorrectly restricts access to a resource from an unauthorized actor.",
    }
    IMPROPER_AUTHENTICATION = {
        "num": 287,
        "desc": "When an actor claims to have a given identity, the product does not prove or insufficiently proves that the claim is correct.",
    }
    IMPROPER_OUTPUT_NEUTRALIZATION_FOR_LOGS = {
        "num": 117,
        "desc": "The product does not neutralize or incorrectly neutralizes output that is written to logs.",
    }
    OS_INJECTION = {
        "num": 78,
        "desc": "The product constructs all or part of an OS command using externally-influenced input from an upstream component, but it does not neutralize or incorrectly neutralizes special elements that could modify the intended OS command when it is sent to a downstream component.",
    }
    UNCONTROLLED_RESOURCE_CONSUMPTION = {
        "num": 400,
        "desc": "The product does not properly control the allocation and maintenance of a limited resource, thereby enabling an actor to influence the amount of resources consumed, eventually leading to the exhaustion of available resources.",
    }
    UNRESTRICTED_UPLOAD_WITH_DANGEROUS_FILE = {
        "num": 434,
        "desc": "The product allows the upload or transfer of dangerous file types that are automatically processed within its environment.",
    }
    INSUFFICIENTLY_PROTECTED_CREDENTIALS = {
        "num": 522,
        "desc": "The product transmits or stores authentication credentials, but it uses an insecure method that is susceptible to unauthorized interception and/or retrieval.",
    }
    INCORRECT_AUTHORIZATION = {
        "num": 863,
        "desc": "The product performs an authorization check when an actor attempts to access a resource or perform an action, but it does not correctly perform the check.",
    }
    IMPROPER_CHECK_OR_HANDLING_OF_EXCEPTIONAL_CONDITIONS = {
        "num": 703,
        "desc": "The product does not properly anticipate or handle exceptional conditions that rarely occur during normal operation of the product.",
    }
    IMPROPER_INPUT_VALIDATION = {
        "num": 20,
        "desc": "The product receives input or data, but it does not validate or incorrectly validates that the input has the properties that are required to process the data safely and correctly.",
    }
