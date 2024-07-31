# @ Context context

# ------------------------------------------------------------------
# Configure detection and linking algorithms.
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
logger.info("\n  Configure tracking")
logger.info("\n-------------------------------------\n")

# Create a TrackMate instance
trackmate = mamut.createTrackMate()

# Print info on available detectors and linkers.
trackmate.infoDetectors()
trackmate.infoLinkers()

# Configure detection.
trackmate.useDetector("Advanced DoG detector")
trackmate.setDetectorSetting("RADIUS", 8.0)
trackmate.setDetectorSetting("THRESHOLD", 200.0)
trackmate.setDetectorSetting("ADD_BEHAVIOR", "DONTADD")

# Show info on the config we have.
trackmate.info()

# Run the full tracking process.
trackmate.run()
# Show results.
mamut.getWindowManager().createBigDataViewer()

# Save Mastodon project.
newMastodonFile = os.path.join(
    os.path.expanduser("~"),
    "Desktop",
    "MastodonTutorialDataset1",
    "test_scripting.mastodon",
)
mamut.saveAs(newMastodonFile)
