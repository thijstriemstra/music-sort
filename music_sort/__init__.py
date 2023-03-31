# Copyright (c) 2021-2023 Thijs Triemstra

import logging
import argparse
from pathlib import Path
from string import Template

__version__ = '1.0.0'

TRACKLIST_HEADER = """
#ifndef TrackList_h
#define TrackList_h

#include <vector>

// THIS FILE IS AUTO-GENERATED

struct TrackList {
  std::vector<String> folders = {
    $folders
  };
  std::vector<String> tracks = {
    $tracks
  };
};

#endif
"""

logger = logging.getLogger(__name__)


def run():
    fmt = '%(asctime)-15s %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=fmt)

    parser = argparse.ArgumentParser(
        description='Organize audio files for Arduino serial audio players like the YX5300 and JQ6500',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--src', dest='src', required=True,
                        help='Path to directory containing audio folders')
    parser.add_argument('--outfile', dest='outfile', default='include/TrackList.h',
                        help='Path to output .h file')
    parser.add_argument('--file-type', dest='ftype', default='mp3',
                        help='Filetype to process')
    parser.add_argument('--prefix-length-dir', dest='dlength', type=int, default=0,
                        help='The length of the directory name prefix to strip off')
    parser.add_argument('--prefix-length-file', dest='flength', type=int, default=0,
                        help='The length of the filename prefix to strip off')
    parser.add_argument('--index', dest='index', type=int, default=1,
                        help='Track index to start with')
    parser.add_argument('--dry-run', action='store_true', help='Do not write anything')

    args = parser.parse_args()
    base = Path(args.src)
    track_index = args.index
    dry_run = args.dry_run
    prefix_length_file = args.flength
    prefix_length_dir = args.dlength
    folders = []
    tracks = []

    dirs = [x for x in sorted(base.iterdir()) if x.is_dir()]
    total_dirs = len(dirs)
    logger.info(f"Found {total_dirs} directories in {str(base)}")
    logger.info("")

    for dir_index, dpath in enumerate(dirs, start=1):
        dir_name = str(dpath.relative_to(base))[prefix_length_dir:]
        folders.append(f'"{dir_name}"')
        logger.debug(f"Directory: {dir_name}")

        # rename files
        for filename in sorted(dpath.glob("*." + args.ftype)):
            fname = Path(filename)

            clean_fname = fname.name[prefix_length_file:]
            target = Path(fname.parent).joinpath("{:03}.{}".format(
                track_index, args.ftype
            ))

            # rename file
            if not dry_run:
                fname.replace(target)

            tracks.append(f'"{Path(clean_fname).stem}"')
            logger.debug(f"Processed: {target.name}")

            track_index += 1

        # rename dir
        target = Path(dpath.parent).joinpath("{:02}".format(dir_index))
        if not dry_run:
            dpath.replace(target)
        logger.debug(f"Renamed directory: {target.name}")
        logger.debug("")

    total_tracks = len(tracks)

    # generate tracklist
    pl = Template(TRACKLIST_HEADER)
    tracklist = pl.substitute(
        folders=",\n    ".join(folders),
        tracks=",\n    ".join(tracks)
    )
    if not dry_run:
        # save tracklist
        template = Path(args.outfile)
        template.write_text(tracklist)

    logger.debug(f"Updated {args.outfile}:")
    logger.debug(tracklist)
