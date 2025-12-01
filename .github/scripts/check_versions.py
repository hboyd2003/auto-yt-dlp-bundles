#!/usr/bin/env python3
"""
Check for new versions of yt-dlp, FFmpeg, and Deno.
Compares with versions from the latest release.
"""

import json
import urllib.request
import urllib.error
import re
import os
import sys


def get_latest_yt_dlp_version():
    """Get the latest yt-dlp release version"""
    try:
        response = urllib.request.urlopen('https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest')
        data = json.loads(response.read().decode())
        return data['tag_name']
    except Exception as e:
        print(f"Error fetching yt-dlp version: {e}")
        return None


def get_latest_ffmpeg_v8_version():
    """Get the latest FFmpeg version 8 release tag"""
    try:
        response = urllib.request.urlopen('https://api.github.com/repos/BtbN/FFmpeg-Builds/releases/latest')
        latest_release = json.loads(response.read().decode())
        actual_release_tag = re.sub(r'[\(\)]', '', latest_release['name'].replace('Latest Auto-Build', 'autobuild'))
        actual_release_tag = re.sub(r'[: ]', '-', actual_release_tag)

        response = urllib.request.urlopen(f'https://api.github.com/repos/BtbN/FFmpeg-Builds/releases/tags/{actual_release_tag}')
        latest_release = json.loads(response.read().decode())

        for asset in latest_release['assets']:
            if asset['name'].endswith('linux64-gpl-8.0.tar.xz'):
                version = re.search(r"n(\d+\.?)*-\d+-g[A-z\d]+", asset['name'])
                if version is None:
                    print("Could not parse FFmpeg version from asset name")
                    return None
                print(f"Latest FFmpeg version found: {version.group(0)}")
                return version.group(0)
        else:
            print("No tags.json found in latest FFmpeg release")
            return None
    except Exception as e:
        print(f"Error fetching FFmpeg version: {e}")
        return None


def get_latest_deno_version():
    """Get the latest Deno release version"""
    try:
        response = urllib.request.urlopen('https://api.github.com/repos/denoland/deno/releases/latest')
        data = json.loads(response.read().decode())
        return data['tag_name']
    except Exception as e:
        print(f"Error fetching Deno version: {e}")
        return None


def read_last_versions():
    """Read the last known versions from the latest release"""
    try:
        # Get the latest release from this repository
        owner_repo = os.environ.get('GITHUB_REPOSITORY', '')
        if not owner_repo:
            print("Could not determine repository")
            return None
        
        url = f'https://api.github.com/repos/{owner_repo}/releases/latest'
        response = urllib.request.urlopen(url)
        release_data = json.loads(response.read().decode())
        
        # Look for versions.json asset in the release
        for asset in release_data.get('assets', []):
            if asset['name'] == 'release.json':
                # Download and parse the versions file
                download_url = asset['browser_download_url']
                asset_response = urllib.request.urlopen(download_url)
                versions = json.loads(asset_response.read().decode())
                print(f"Retrieved last released versions from release {release_data['name']}")
                return versions
        
        print("No release.json found in latest release")
        return None
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("No releases found yet")
        else:
            print(f"Error fetching latest release: {e}")
    except Exception as e:
        print(f"Error reading last versions: {e}")
    return None


def main():
    """Main entry point"""
    print("Checking for new versions...")
    
    # Get current versions
    current_versions = {
        'yt_dlp': get_latest_yt_dlp_version(),
        'ffmpeg': get_latest_ffmpeg_v8_version(),
        'deno': get_latest_deno_version()
    }

    if not all(current_versions.values()):
        print("ERROR: Failed to fetch one or more versions")
        sys.exit(1)
    
    # Read last known versions from latest release
    last_versions = read_last_versions()

    detected_update = 'none'
    if last_versions is not None:
        versions_changed = (last_versions['bundled']['ffmpeg']['version'] != current_versions['ffmpeg']
            or last_versions['bundled']['yt_dlp']['version'] != current_versions['yt_dlp']
            or last_versions['bundled']['deno']['version'] != current_versions['deno'])
        for key in current_versions:
            if last_versions.get(key) != current_versions[key]:
                detected_update = f"{key}: {last_versions.get(key, 'unknown')} → {current_versions[key]}"
    else:  
        versions_changed = False

    # Package if versions changed or this is the first run (no last versions)
    should_package = versions_changed or not last_versions

    # Set outputs for GitHub Actions
    github_output = os.environ.get('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            f.write(f"should_package={'true' if should_package else 'false'}\n")
            f.write(f"versions={json.dumps(current_versions)}\n")
            f.write(f"detected_update={detected_update}\n")
    
    # Print results
    print(f"Current versions: {json.dumps(last_versions, indent=2)}")
    print(f"New versions: {json.dumps(current_versions, indent=2)}")
    if should_package:
        print(f"Detected update: {detected_update}")
    else:
        print("No updates detected")
    
    # Exit with appropriate code
    sys.exit(0 if should_package or not versions_changed else 0)


if __name__ == "__main__":
    main()
