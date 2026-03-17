import sys


def main():
    """Main entry point for the package."""
    if "--auth" in sys.argv:
        from .server import run_auth
        run_auth()
    else:
        from .server import mcp
        mcp.run()


__all__ = ["main"]
