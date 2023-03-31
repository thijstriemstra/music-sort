# music-sort

Organize audio files and generate trackslists for Arduino serial audio players like the YX5300 and JQ6500-28P.

## Supported players

| Device | SD-card filesystem | Song prefix | Folder structure | Maximum folders | Maximum songs per folder | Reference |
| --- | --- | --- | --- | --- | --- | --- |
| YX5300, YX6300 | FAT16, FAT32 | 3 digit index, e.g. `001xxx.mp3` | `01`, `02`, etc | 99 | 255 | [MD_YX5300 library](https://majicdesigns.github.io/MD_YX5300/) |
| JQ6500-28P, JQ6500-16P | FAT16, FAT32 | 3 digit index, e.g. `001.mp3` | `01`, `02`, etc | 100 | 1000 | [Module docs](https://sparks.gogo.co.nz/jq6500/index.html), [JQ6500_Serial library](https://github.com/sleemanj/JQ6500_Serial) |

## Installation

Clone the repository and install using `pip`:

```console
pip install -e .
```

You can now use the `music-sort` command, e.g:

```console
music-sort --help
```

## Usage

Let's say you have 3 folders with a couple of tracks you want to place on the SD-card. For example:

```
+-+- 1. The Lord Of The Rings- The Fellowship Of The Ring (OST)
  |   + 01 The Lord Of The Rings (Howard Shore) - The Prophecy.mp3
  |   + 02 The Lord Of The Rings (Howard Shore) - Concerning Hobbits.mp3
  |
  +- 2. The Lord Of The Rings- The Two Towers (OST)
  |   + 01 The Lord Of The Rings (Howard Shore) - Foundations of Stone.mp3
  |   + 02 The Lord Of The Rings (Howard Shore) - The Taming of Smeagol.mp3
  |   + 03 The Lord Of The Rings (Howard Shore) - The Riders of Rohan.mp3
  |
  +- 3. The Lord Of The Rings- The Return Of The King (OST)
      + 01 The Lord Of The Rings (Howard Shore) - A Storm Is Coming.mp3
      + 02 The Lord Of The Rings (Howard Shore) - Hope and Memory.mp3
```

Copy these 3 folders to a new directory, let's say `/tmp/music/`.

Now run `music-sort` and specify the `--src` and `--dry-run` option (allows you
to preview and verify the changes):

```console
music-sort --src=/tmp/music --dry-run
```

This should output something like:

```
2021-08-18 20:28:55,096 INFO - Found 3 directories in /tmp/music
2021-08-18 20:28:55,096 INFO -
2021-08-18 20:28:55,096 DEBUG - Directory: 1. The Lord Of The Rings- The Fellowship Of The Ring (OST)
2021-08-18 20:28:55,096 DEBUG - Processed: 001.mp3
2021-08-18 20:28:55,097 DEBUG - Processed: 002.mp3
2021-08-18 20:28:55,097 DEBUG - Renamed directory: 01
2021-08-18 20:28:55,097 DEBUG -
2021-08-18 20:28:55,097 DEBUG - Directory: 2. The Lord Of The Rings- The Two Towers (OST)
2021-08-18 20:28:55,097 DEBUG - Processed: 003.mp3
2021-08-18 20:28:55,097 DEBUG - Processed: 004.mp3
2021-08-18 20:28:55,097 DEBUG - Processed: 005.mp3
2021-08-18 20:28:55,097 DEBUG - Renamed directory: 02
2021-08-18 20:28:55,097 DEBUG -
2021-08-18 20:28:55,097 DEBUG - Directory: 3. The Lord Of The Rings- The Return Of The King (OST)
2021-08-18 20:28:55,097 DEBUG - Processed: 006.mp3
2021-08-18 20:28:55,097 DEBUG - Processed: 007.mp3
2021-08-18 20:28:55,097 DEBUG - Renamed directory: 03
2021-08-18 20:28:55,097 DEBUG -
2021-08-18 20:28:55,097 DEBUG - Updated include/TrackList.h:
2021-08-18 20:28:55,097 DEBUG -
#ifndef TrackList_h
#define TrackList_h

#include <vector>

// THIS FILE IS AUTO-GENERATED

struct TrackList {
  std::vector<String> folders = {
    "1. The Lord Of The Rings- The Fellowship Of The Ring (OST)",
    "2. The Lord Of The Rings- The Two Towers (OST)",
    "3. The Lord Of The Rings- The Return Of The King (OST)"
  };
  std::vector<String> tracks = {
    "01 The Lord Of The Rings (Howard Shore) - The Prophecy",
    "02 The Lord Of The Rings (Howard Shore) - Concerning Hobbits",
    "01 The Lord Of The Rings (Howard Shore) - Foundations of Stone",
    "02 The Lord Of The Rings (Howard Shore) - The Taming of Smeagol",
    "03 The Lord Of The Rings (Howard Shore) - The Riders of Rohan",
    "01 The Lord Of The Rings (Howard Shore) - A Storm Is Coming",
    "02 The Lord Of The Rings (Howard Shore) - Hope and Memory"
  };
};

#endif
```

The resulting `TrackList.h` contains unnecessary text that we don't want, like
the first part of the:

- folder name: `1. The Lord Of The Rings- `
- filename: `01 The Lord Of The Rings (Howard Shore) - `

Use the `--prefix-length-dir` and `--prefix-length-file` options for this.
The length of the prefix in the folder name (`1. The Lord Of The Rings- `) is 26
and the length of the file name prefix (`01 The Lord Of The Rings (Howard Shore) - `)
is 42.

Run `music-sort` again with these new options:

```
music-sort --src=/tmp/music --dry-run --prefix-length-dir=26 --prefix-length-file=42
```

And the resulting tracklist:

```cpp
#ifndef TrackList_h
#define TrackList_h

#include <vector>

// THIS FILE IS AUTO-GENERATED

struct TrackList {
  std::vector<String> folders = {
    "The Fellowship Of The Ring (OST)",
    "The Two Towers (OST)",
    "The Return Of The King (OST)"
  };
  std::vector<String> tracks = {
    "The Prophecy",
    "Concerning Hobbits",
    "Foundations of Stone",
    "The Taming of Smeagol",
    "The Riders of Rohan",
    "A Storm Is Coming",
    "Hope and Memory"
  };
};

#endif
```

When everything looks right, run `music-sort` without the `--dry-run` option to rename
the files and folders and write the tracklist header file:

```
music-sort --src=/tmp/music --prefix-length-dir=26 --prefix-length-file=42
```

The resulting file tree:

```
+-+- 01
  |   + 001.mp3
  |   + 002.mp3
  |
  +- 02
  |   + 003.mp3
  |   + 004.mp3
  |   + 005.mp3
  |
  +- 03
      + 006.mp3
      + 007.mp3
```

This can be copied onto the SD-card and `TrackList.h` can be compiled into your project
if you want to display track and album information.
