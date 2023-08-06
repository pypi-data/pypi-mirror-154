"""Cli tunnel."""
import os
import time
import re
import pathlib

from .util.simple_supervision import Supervision
from .util.exception import (
    CmdNotFound, NgrokInstallError, NgrokAuthError,
    NgrokError, FetchUrlError, NgrokNotRunning,
    NgrokCannotStopped
)
from .util.context import (
    get_executable_file_extension, get_cache_dir,
    get_current_platform, which, linux
)


class Tunnel(object):
    """Tunnel interface."""

    # mapping for supported operating systems for where to download ngrok from.
    DOWNLOAD_URLS = {
        "mac": "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-darwin-amd64.zip",
        "mac_m1": "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-darwin-arm64.zip",
        "linux": "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip",
        "windows": "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip",
    }

    PORT = 8081  # port that ngrok will bind to

    @classmethod
    def fetch_url(cls, log_path):
        """Fetch account and url."""
        log = LogParser(log_path)
        account, url = log.do()
        return account, url

    @classmethod
    def install(cls):
        """Download and install ngrok to cache dir."""
        # check if ngrok had been downlodaed.
        if pathlib.Path(cls.ngrok_path()).exists():
            return

        # if not intalled, download.
        # check if curl, unzip, or tar is installed.
        platform = get_current_platform()
        cls.check_prereq_command("curl")
        cls.check_prereq_command("unzip" if linux(platform) else "tar")

        # using curl to download ngrok
        cache_dir = get_cache_dir()
        zip_dest = os.path.join(cache_dir, "ngrok.zip")
        if not pathlib.Path(zip_dest).exists():
            src_url = Tunnel.DOWNLOAD_URLS[platform]
            cmd = f"curl -o {zip_dest} {src_url}"
            os.system(cmd)

        # unzip ngrok.zip
        if linux(platform):
            cmd = f"unzip -s -d {cache_dir} {zip_dest}"
        else:
            cmd = f"tar -xf {zip_dest} -C {cache_dir}"
        os.system(cmd)

        # rm zip
        cmd = f"rm {zip_dest}"
        os.system(cmd)

        if not pathlib.Path(cls.ngrok_path()).exists():
            raise NgrokInstallError("download and install ngrok failed.")
        print("ngrok successfully installed")

    @classmethod
    def auth(cls, token):
        """Install ngrok and config token."""
        cls.install()
        cmd = " ".join([cls.ngrok_path(), "authtoken", token])
        os.system(cmd)

    @classmethod
    def authenticated(cls):
        """Check if ngrok is authenticated."""
        home = pathlib.Path.home()
        ngrok_config_path = os.path.join(home, ".ngrok2/ngrok.yml")
        ng_path = pathlib.Path(ngrok_config_path)
        if not ng_path.exists():
            return False
        with ng_path.open() as fd:
            content = fd.read()
            if "authtoken" in content:
                return True
        return False

    @classmethod
    def start(cls, port):
        """Start ngrok.

        Args:
            port: port to use to open the ngrok tunnel
        Returns:
            url: url that the tunnel is bound to and available to the public
        """
        cls.install()
        if not cls.authenticated():
            raise NgrokAuthError("ngrok account authtoken error.")
        url, account = cls.start_ngrok(port or Tunnel.PORT)
        return url, account

    @classmethod
    def stop(cls):
        """Strop ngrok."""
        identifier = cls.ngrok_identifier()
        if Supervision.is_running(identifier):
            if Supervision.stop(identifier):
                return
            else:
                raise NgrokCannotStopped("ngrok tunnel can not stop")
        else:
            raise NgrokNotRunning("ngrok tunnel not running")

    @classmethod
    def ngrok_identifier(cls):
        """Return identifier."""
        return f"ngrok{get_executable_file_extension()}"

    @classmethod
    def ngrok_path(cls):
        """Get ngrok full path."""
        cache_dir = get_cache_dir()
        ngrok_path = os.path.join(cache_dir, cls.ngrok_identifier())
        return ngrok_path

    @classmethod
    def ngrok_command(cls, port):
        """Format ngrok command."""
        ngrok_path = cls.ngrok_path()
        ngrok_cmd = [
            ngrok_path, "http", "--inspect=false",
            "--log=stdout", "--log-level=debug", port
        ]
        return ngrok_cmd

    @classmethod
    def start_ngrok(cls, port):
        """Start ngrok."""
        ngrok_cmd = cls.ngrok_command(port)
        process = Supervision.start(cls.ngrok_identifier(), *ngrok_cmd)
        account, url = cls.fetch_url(process.log_path)
        return account, url

    def stats(self):
        pass

    def urls(self):
        pass

    @classmethod
    def check_prereq_command(cls, cmd):
        """Check if cmd is installed."""
        cmd_path = which(cmd)
        if cmd_path:
            print(f"{cmd} @ {cmd_path}")
        if not cmd:
            raise CmdNotFound(f"{cmd} is not installed.")


class LogParser(object):
    """Log parser."""

    TIMEOUT = 10

    def __init__(self, log_path):
        """Init."""
        self.log_path = log_path

    def do(self):
        """Begin analize ngrok log."""
        counter = 0
        while counter < self.TIMEOUT:
            account, url = self.parse()
            if url:
                return account, url
            counter += 1
            time.sleep(1)
        raise FetchUrlError("fetch url timeout.")

    def parse(self):
        """Get account and url from ngrok log."""
        p_log = pathlib.Path(self.log_path)
        content = ""
        with p_log.open() as fd:
            content = fd.read()
        self.parse_error(content)
        account = self.parse_account(content)
        url = self.parse_url(content)
        return account, url

    def parse_error(self, log):
        """Extract error from log."""
        match = re.search(
            r"msg=\"command failed\" err=\"([^\"]+)\"",
            log
        )
        if match:
            raise NgrokError(match.group(1))

    def parse_account(self, log):
        """Extract account from log."""
        match = re.search(
            r"AccountName:(.*)\s+SessionDuration",
            log
        )
        if match:
            return match.group(1)
        return None

    def parse_url(self, log):
        """Extract url from log."""
        match = re.search(
            r"msg=\"started tunnel\".*url=(https:\/\/.+)",
            log
        )
        if match:
            return match.group(1)
        return None
