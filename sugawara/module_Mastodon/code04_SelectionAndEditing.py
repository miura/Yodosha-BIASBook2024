# @ Context context

# ------------------------------------------------------------------
# Selecting and editing the tracking model.
# ------------------------------------------------------------------
# License: BSD 2-Clause
# Copyright (C) 2014 - 2024:
#     Tobias Pietzsch, Jean-Yves Tinevez, Ko Sugawara, Matthias Arzt,
#     Vladimír Ulman, Stefan Hahmann
# ------------------------------------------------------------------

from org.mastodon.mamut import Mamut
import os

mastodonFile = os.path.join(
    os.path.expanduser("~"),
    "Desktop",
    "MastodonTutorialDataset1",
    "test_scripting.mastodon",
)
mamut = Mamut.open(mastodonFile, context)

logger = mamut.getLogger()
logger.info("File opened: %s\n" % mastodonFile)
logger.info("Mamut instance: %s\n" % mamut)

logger.info("\n\n-------------------------------------")
logger.info("\n  Selection and editing")
logger.info("\n-------------------------------------\n")

mamut.computeFeatures("Track N spots")
mamut.select("vertexFeature( 'Track N spots' ) < 10")

mamut.deleteSelection()
