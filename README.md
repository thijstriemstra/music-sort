# music-sort

Organize audio files for Arduino serial audio players like the YX5300 and JQ6500-28P.

## Supported players

| Device | SD-card filesystem | Song prefix | Folder structure | Maximum folders | Maximum songs per folder | Reference |
| --- | --- | --- | --- | --- | --- | --- |
| YX5300, YX6300 | FAT16, FAT32 | 3 digit index, e.g. `001xxx.mp3` | `01`, `02`, etc | 99 | 255 | [MD_YX5300 library](https://majicdesigns.github.io/MD_YX5300/) |
| JQ6500-28P, JQ6500-16P | FAT16, FAT32 | 3 digit index, e.g. `001.mp3` | `01`, `02`, etc | 100 | 1000 | [Module docs](https://sparks.gogo.co.nz/jq6500/index.html), [JQ6500_Serial library](https://github.com/sleemanj/JQ6500_Serial) |
