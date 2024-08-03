# @ Context context

# ------------------------------------------------------------------
# Tagging data items.
# ------------------------------------------------------------------
# License: BSD 2-Clause
# Copyright (C) 2014 - 2024:
#     Tobias Pietzsch, Jean-Yves Tinevez, Ko Sugawara, Matthias Arzt,
#     Vladimír Ulman, Stefan Hahmann
# ------------------------------------------------------------------

from org.mastodon.mamut import Mamut
from org.mastodon.mamut.views.trackscheme import MamutViewTrackScheme
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
logger.info("\n  Tagging data items")
logger.info("\n-------------------------------------\n")

mamut.infoTags()

# We create a 'Fruits' tag-set, with 'Apple', 'Banana', 'Kiwi' as tags.
mamut.createTag("Fruits", "Apple", "Banana", "Kiwi")
# The same with a 'Persons' tag-set.
mamut.createTag("Persons", "User1", "User2")

mamut.setTagColor("Fruits", "Apple", 200, 0, 0)
mamut.setTagColor("Fruits", "Banana", 200, 200, 0)
mamut.setTagColor("Fruits", "Kiwi", 0, 200, 0)

mamut.infoTags()

mamut.select("vertexFeature('Spot position' ,'X' ) > 100.")
mamut.tagSelectionWith("Fruits", "Kiwi")

mamut.select("vertexFeature('Spot frame' ) == 25")
mamut.tagSelectionWith("Fruits", "Banana")

mamut.select("vertexFeature('Spot N links' ) == 1")
mamut.tagSelectionWith("Fruits", "Apple")

# Clear selection.
mamut.resetSelection()

# Showing and configuring views.
displaySettings = {"TagSet": "Fruits"}
mamut.getWindowManager().createTrackScheme(displaySettings)
