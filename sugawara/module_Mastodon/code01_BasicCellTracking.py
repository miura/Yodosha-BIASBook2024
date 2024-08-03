# @ Context context

# ------------------------------------------------------------------
# Basic detection and linking.
# ------------------------------------------------------------------
# License: BSD 2-Clause
# Copyright (C) 2014 - 2024:
#     Tobias Pietzsch, Jean-Yves Tinevez, Ko Sugawara, Matthias Arzt,
#     Vladimír Ulman, Stefan Hahmann
# ------------------------------------------------------------------

from org.mastodon.mamut import Mamut
from org.mastodon.mamut.views.bdv import MamutViewBdv
import os

bdvFile = os.path.join(
    os.path.expanduser("~"),
    "Desktop",
    "MastodonTutorialDataset1",
    "datasethdf5.xml",
)
mamut = Mamut.newProject(bdvFile, context)

logger = mamut.getLogger()
logger.info("File opened: %s\n" % bdvFile)
logger.info("Mamut instance: %s\n" % mamut)

logger.info("\n\n-------------------------------------")
logger.info("\n  Basic detection and linking")
logger.info("\n-------------------------------------\n")

# Detect with the DoG detector, a radius of 6 and a threshold on quality of 200.
radius = 6.0
threshold = 200.0
mamut.detect(radius, threshold)
# Link spots with the simple LAP tracker, with a max linking distance of 10, and forbidding gap-closing
max_linking_distance = 10.0
gap_closing_n_frames = 0
mamut.link(max_linking_distance, gap_closing_n_frames)

# A new BDV window.
mamut.getWindowManager().createBigDataViewer()
