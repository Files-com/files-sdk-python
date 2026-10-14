"""Getting started with the Files.com Python SDK.

Install the SDK into Python 3.11 or newer, then run this with an API key:

    pip install Files.com
    FILES_API_KEY=... python getting_started.py

Set FILES_BASE_URL too if your site needs its own URL, such as
https://SUBDOMAIN.files.com. The script lists your users, creates, renames
and deletes a group, uploads a file and downloads it again, and shows how the
SDK reports an error. It needs a site administrator's API key.

Every call goes through one files_sdk.Client, which keeps its own settings
and connections and closes them at the end.
"""

import contextlib
import os
import sys
import tempfile
import uuid
from pathlib import Path

import files_sdk
from files_sdk.error import Error, NotFoundError


def print_users(client: files_sdk.Client) -> None:
    # auto_paging_iter() fetches each page of users only when the loop needs
    # it, so stopping early sends no further requests.
    for user in client.user.list({"per_page": 100}).auto_paging_iter():
        print(f"User {user.id}: {user.username}")


def rename_a_group(client: files_sdk.Client) -> None:
    group = client.group.create({"name": "SDK example"})
    try:
        group.name = "SDK example (renamed)"
        group.save()  # group now holds the server's copy of the record.
        print(f"Group {group.id} is named {group.name!r}")
    finally:
        group.delete()


def upload_and_download(client: files_sdk.Client) -> None:
    # A name no other file has, so the cleanup removes only this upload.
    remote_path = f"sdk-example/report-{uuid.uuid4().hex}.csv"
    with tempfile.TemporaryDirectory() as scratch:
        report = Path(scratch, "report.csv")
        report.write_bytes(b"id,total\n1,10.50\n")
        uploaded = client.file.upload_file(report, remote_path)
        print(f"Uploaded {uploaded.size} bytes to {uploaded.path}")
        try:
            # The local copy replaces copy.csv only once all of it arrived.
            copy = Path(scratch, "copy.csv")
            client.file.download_file(remote_path, copy)
            print(f"Downloaded {copy.stat().st_size} bytes from {remote_path}")
            # A remote file can also be read like a local one, line by line.
            with client.file.open(remote_path) as remote:
                for line in remote:
                    print(f"  {line.rstrip()}")
        except BaseException:
            # delete_upload reports its own failure, and the download failure
            # stays the error this raises.
            with contextlib.suppress(Error):
                delete_upload(client, remote_path)
            raise
        delete_upload(client, remote_path)


def delete_upload(client: files_sdk.Client, remote_path: str) -> None:
    try:
        client.file.delete(remote_path)
    except NotFoundError:
        pass  # Already gone, which is all the cleanup needs.
    except Error as error:
        # Name the file, so it can be deleted by hand.
        print(f"Could not delete {remote_path}: {error}", file=sys.stderr)
        raise


def show_an_error(client: files_sdk.Client) -> None:
    try:
        client.file.find("sdk-example/missing.csv")
    except NotFoundError as error:
        print(f"Expected error: {error}")


def main():
    api_key = os.environ.get("FILES_API_KEY")
    if not api_key:
        sys.exit("Set FILES_API_KEY to a Files.com API key.")
    # The module's default base URL, unless FILES_BASE_URL names another.
    base_url = os.environ.get("FILES_BASE_URL") or files_sdk.base_url

    try:
        with files_sdk.Client(api_key=api_key, base_url=base_url) as client:
            print_users(client)
            rename_a_group(client)
            upload_and_download(client)
            show_an_error(client)
    except Error as error:
        # files_sdk.error.Error is the base of every API and connection
        # error. Local file problems still raise OSError.
        sys.exit(f"Files.com request failed: {error}")


if __name__ == "__main__":
    main()
