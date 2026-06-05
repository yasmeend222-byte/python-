"""
Custom exceptions for AI Safe Guardian System
"""


class SafeGuardianException(Exception):
    """Base exception for AI Safe Guardian System"""
    pass


class ConfigurationError(SafeGuardianException):
    """Raised when configuration is invalid"""
    pass


class ValidationError(SafeGuardianException):
    """Raised when input validation fails"""
    pass


class InputBlockedError(SafeGuardianException):
    """Raised when input is blocked for safety reasons"""
    pass


class OutputBlockedError(SafeGuardianException):
    """Raised when output is blocked for safety reasons"""
    pass


class RateLimitExceededError(SafeGuardianException):
    """Raised when rate limit is exceeded"""
    pass


class ModerationError(SafeGuardianException):
    """Raised when content moderation fails"""
    pass


class EncryptionError(SafeGuardianException):
    """Raised when encryption/decryption fails"""
    pass


class PrivacyError(SafeGuardianException):
    """Raised when privacy protection fails"""
    pass


class AuditLoggingError(SafeGuardianException):
    """Raised when audit logging fails"""
    pass


class IntegrationError(SafeGuardianException):
    """Raised when integration with external service fails"""
    pass


class PluginError(SafeGuardianException):
    """Raised when plugin loading/execution fails"""
    pass
