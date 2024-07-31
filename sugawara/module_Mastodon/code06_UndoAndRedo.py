# @ Context context

# ------------------------------------------------------------------
# Undo and redo.
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
logger.info("\n  Undo and redo")
logger.info("\n-------------------------------------\n")

# Print some info on the model before we remove spots.
logger.info("Before:\n")
mamut.info()

# Let's delete 500 spots.
it = mamut.getModel().getGraph().vertices().iterator()
for i in range(500):
    if it.hasNext():
        spot = it.next()
        mamut.getModel().getGraph().remove(spot)

# We mark this point as an undo point. Calling undo() / redo()
# navigates in the stack of these undo points.
mamut.getModel().setUndoPoint()

# Print some info on the model after we remove spots.
logger.info("After deleting some spots:\n")
mamut.info()

# Undo the deletion of spots.
mamut.undo()
logger.info("After undo:\n")
mamut.info()

# Redo the deletion of spots.
mamut.redo()
logger.info("After redo:\n")
mamut.info()
