# @ Context context

# ------------------------------------------------------------------
# Compute features using the tracking results.
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
logger.info("\n  Compute features")
logger.info("\n-------------------------------------\n")

mamut.infoFeatures()
mamut.computeFeatures("Spot intensity", "Spot center intensity")

# To display 2 tables with the first 10 spots and links:
mamut.echo(10)
