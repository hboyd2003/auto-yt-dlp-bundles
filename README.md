# Media Tools Bundle
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/hboyd2003/auto-yt-dlp-bundles/package-tools.yml)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/hboyd2003/auto-yt-dlp-bundles)

This repository automatically packages the latest versions of [yt-dlp](https://github.com/yt-dlp/yt-dlp), [FFmpeg](https://ffmpeg.org), and [Deno](https://github.com/denoland/deno) into single `tar.xz`
New versions of each are checked for nightly.

## Available Platforms
| Platform | Architecture    |
|----------|-----------------|
| Linux    | x64 (AMD64)     |
| Linux    | ARM64 (AArch64) |
| Windows  | x64             |

## Excluded Platforms
The following platforms are currently not included because at least one tool is missing a build for it:

| Platform | Architecture | Missing Tool         |
|----------|--------------|----------------------|
| Windows  | ARM64        | Deno                 |
| macOS    | x64          | FFmpeg (BtbN builds) |
| macOS    | ARM64        | FFmpeg (BtbN builds) |

## License

This packaging project is provided as-is. Each included tool maintains its own license:
- yt-dlp: [Unlicense](https://github.com/yt-dlp/yt-dlp/blob/master/LICENSE)
- FFmpeg: [LGPL](https://ffmpeg.org/legal.html)
- Deno: [MIT](https://github.com/denoland/deno/blob/main/LICENSE.md)

---

*This is an automated packaging repository. For issues with the individual tools, please report to their respective repositories.*
